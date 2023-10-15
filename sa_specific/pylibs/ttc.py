# This utility allows the user to encrypt, decrypt, and generate arbitrary
# twist tokens.  It uses the "twist-key.pem" to seed a SHA1PRNG in order to
# determine a 128 bit key for AES EBC encryption/decryption.
#
# It contains a convenience feature that allows for easy generation of the
# XML content of a typical twist token.  (So that the user doesn't have to
# do this from scratch if they don't want to.)
#

# ../py_build sha1prng.py aes.py ttc.py

import os,sys,time,string,types,cStringIO,re,base64,sha

import sha1prng, aes

TWIST_KEY_FILE = "/var/opt/opsware/crypto/twist/twist-key.pem"

def usage():
  sys.stdout.write("""Twist Token Crypto (ttc)

A utility for encrypting, decrypting, and generating twist tokens.

Usage:

  %s [-h] [-k <twist_key_file>] (-e <cleartext_token>|-d <encrypted_token>|
     -g [-<element_path> <element_value>] ...)

  -e <cleartext_token>
    Encrypt <cleartext_token> using aes-128-ecb(sha1prng(twist-key.pem)).

  -d <enc_b64_token>
    Decrypt <enc_b64_token> using aes-128-ecb(sha1prng(twist-key.pem)).

  -g [-<element_path> <element_value>] ...
    Generate an encrypted token using one or more XML element path and values
    specified on the command line.  One of either "-uid" or "-un" are required.
    If certain expected XML element paths are not specified, then the following
    defaults will be used:

      -v 1.0
      -t ident
      -vf <now>
      -vu <now_plus_1_year>

  -ge [-<element_path> <element_value>] ...
    Same as -g, exception encrypts the resulting token.

  [-h]
    Display help info.

  [-k <twist_key_file>]
    Loads the encryption key from the specified twist key file.  The default
    file path is "/var/opt/opsware/crypto/twist/twist-key.pem".

Examples:

  # ./ttc -g -un dwest

  # ./ttc -g -un dwest -o/realm TRANSITIONAL -o/ip_addr 127.0.0.1

  An example oaque token demonstraiting the expected XML elements:

-------------------------------------------------------------------------------
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<tok>
    <v>1.0</v>
    <t>svc</t>
    <uid>810001</uid>
    <un>dwest</un>
    <o>
        <realm>TRANSITIONAL</realm>
        <ip_addr>127.0.0.1</ip_addr>
    </o>
    <vf>1318391124000</vf>
    <vu>1318477379006</vu>
</tok>
-------------------------------------------------------------------------------
""" % os.path.basename(sys.argv[0]))

class TTCException(Exception):
  def __init__(*args, **kwargs):
    return apply(Exception.__init__, args, kwargs)

AES_BLOCK_SIZE = 16

# split a string by length.
def split(s, l):
  return map(lambda i,l=l,s=s:s[i:i+l], range(0, len(s), l))

def load_key(twist_key_file=TWIST_KEY_FILE):
  if ( not os.path.exists(twist_key_file) ):
    raise TTCException("%s: twist key file not found." % twist_key_file)
  tk = open(twist_key_file).read()
  tk = map(ord, re.compile("-----BEGIN.+?(\r|\n|\r\n)(.+?)-----END.+?(\r|\n|\r\n)", re.DOTALL).match(tk).groups()[1])
  key = [0] * 16
  sha1prng.sha1prng(tk).next_bytes(key)
  return key

def encrypt(s_tok, key):
  """args: s_tok, key
returns: base64 encoded encrypted string
"""
  if ( s_tok == "-" ):
    s_tok = sys.stdin.read()

  s_tok = s_tok + sha.sha(s_tok).digest()
  s_tok = aes.append_PKCS7_padding(s_tok)

  chunks = split(s_tok, AES_BLOCK_SIZE)
  if ( len(chunks) == 0 ): chunks = [""]

  cipher = aes.AES()

  s_enc_tok = ""
  for chunk in chunks:
    s_enc_tok = s_enc_tok + string.join(map(chr, cipher.encrypt(map(ord, chunk), key, len(key))), "")

  s_enc_b64_tok = base64.encodestring(s_enc_tok)
  s_enc_b64_tok = string.replace(s_enc_b64_tok, "\n", "")
  return s_enc_b64_tok

def decrypt(s_enc_b64_tok, key):
  """args: s_enc_b64, key
returns: cleartext string
"""
  if ( s_enc_b64_tok == "-" ):
    s_enc_b64_tok = sys.stdin.read()

  s_enc_tok = base64.decodestring(s_enc_b64_tok)

  cipher = aes.AES()

  s_tok = ""
  for chunk in split(s_enc_tok, AES_BLOCK_SIZE):
    s_tok = s_tok + string.join(map(chr, cipher.decrypt(map(ord, chunk), key, len(key))), "")

  s_tok = aes.strip_PKCS7_padding(s_tok)

  if ( len(s_tok) < 20 ):
    raise TTCException("%s: Decrypted token appears to be too short to have a trailing sha1 hash." % repr(s_tok))

  s_hash = s_tok[-20:]
  s_tok = s_tok[:-20]
  s_calc_hash = sha.sha(s_tok).digest()
  if ( s_hash != s_calc_hash ):
    raise TTCException("%s: Decrypted token's hash does not match what was expected:  (%s)" % (repr(s_tok+s_hash), repr(s_calc_hash)))

  return s_tok

def shift(l):
  r = l[0]
  del l[0]
  return r

def _dict_to_xml(fo, dict, indent=4, indent_inc=4):
  for key in dict.keys():
    s_indent = " "*indent
    val = dict[key]
    if ( type(val) == types.DictType ):
      fo.write("%s<%s>\n" % (s_indent,key))
      _dict_to_xml(fo, val, indent+indent_inc)
      fo.write("%s</%s>\n" % (s_indent,key))
    else:
      fo.write("%s<%s>%s</%s>\n" % (s_indent, key, val, key))

def gen_token_xml(argv):
  """  argv: ["-<element_path>", "<value>" ...]
  raises: TTCException - If an expected failure occured.

Constructs a cleartext token based on <argv>.  Populates with certain default 
values if not present.
"""
  now = (time.time()*1000)
  dict_tok = {"v":"1.0", "t":"ident", "vf":("%d" % now), "vu":("%d" % (now+1000*60*60*24*365))}

  while argv:
    cur_arg = shift(argv)
    if ( cur_arg[0] == "-" ):
      if ( len(argv) < 1 ):
        raise TTCException("%s: Missing value argument." % cur_arg)
      val = shift(argv)
      cur_arg = cur_arg[1:]
      els = string.split(cur_arg, "/")
      cur_dict = dict_tok
      for el in els:
        if ( not cur_dict.has_key(el) ):
          cur_dict[el] = {}
        last_dict = cur_dict
        cur_dict = cur_dict[el]
      last_dict[el] = val
    else:
      raise TTCException("%s: Unexpected argument." % cur_arg)

  if ( (not dict_tok.has_key("uid")) and (not dict_tok.has_key("un")) ):
    raise TTCException("one of either \"uid\" or \"un\" elements must be specified.")

  if ( not dict_tok.has_key("uid") ):
    from coglib import spinwrapper
    uids = map(lambda r:r[0], spinwrapper.SpinWrapper()._AAAAaaUser.getList(restrict={"username":dict_tok["un"], "user_status":"ACTIVE"}))
    if ( len(uids) < 1 ):
      raise TTCException("%s: Unable to locate an ACTIVE user by this name." % dict_tok["un"])
    dict_tok["uid"] = uids[0]

  if ( not dict_tok.has_key("un") ):
    from coglib import spinwrapper
    uid = dict_tok["uid"]
    try:
      uid = int(uid)
    except:
      raise TTCException("%s: Is not a valid uid." % uid)
    uns = map(lambda r:r[1], spinwrapper.SpinWrapper()._AAAAaaUser.getList(restrict={"user_id":uid, "user_status":"ACTIVE"}, fields=["username"]))
    if ( len(uns) < 1 ):
      raise TTCException("%s: Unable to locate an ACTIVE user by this uid.\n" % dict_tok["uid"])
    dict_tok["un"] = uns[0]

  f_tok = cStringIO.StringIO()
  f_tok.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<tok>\n')
  std_keys = ["v", "t", "uid", "un", "o", "vf", "vu"]
  nstd_keys = filter(lambda k,sks=std_keys:k not in sks, dict_tok.keys())
  for el in std_keys + nstd_keys:
    if ( dict_tok.has_key(el) ):
      val = dict_tok[el]
      if ( type(val) == types.DictType ):
        _dict_to_xml(f_tok, {el:val}, 4, 4)
      else:
        f_tok.write("    <%s>%s</%s>\n" % (el, val, el))
  f_tok.write("</tok>\n")

  return f_tok.getvalue()

def main(argv):
  twist_key_file = TWIST_KEY_FILE

  if ( len(argv) == 0 ):
    usage()
    sys.exit(1)

  while argv:
    cur_arg = shift(argv)
    if ( cur_arg in ("-h", "--help") ):
      usage()
    elif ( cur_arg == "-k" ):
      twist_key_file = shift(argv)
    elif ( cur_arg == "-e" ):
      if ( len(argv) < 1 ):
        usage()
        sys.exit(1)
      s_cleartext = shift(argv)
      if ( s_cleartext == "-" ): s_cleartext = sys.stdin.read()
      try:
        sys.stdout.write(encrypt(s_cleartext, load_key(twist_key_file)))
      except TTCException, e:
        sys.stderr.write("ERROR: %s\n" % str(e))
    elif ( cur_arg == "-d" ):
      if ( len(argv) < 1 ):
        usage()
        sys.exit(1)
      s_enc_b64 = shift(argv)
      if ( s_enc_b64 == "-" ): s_enc_b64 = sys.stdin.read()
      try:
        sys.stdout.write(decrypt(s_enc_b64, load_key(twist_key_file)))
      except TTCException, e:
        sys.stderr.write("ERROR: %s\n" % str(e))
    elif ( cur_arg == "-g" ):
      try:
        sys.stdout.write(gen_token_xml(argv[:]))
        del argv[:]
      except TTCException, e:
        sys.stderr.write("ERROR: %s\n" % str(e))
    elif ( cur_arg == "-ge" ):
      try:
        sys.stdout.write(encrypt(gen_token_xml(argv[:]), load_key(twist_key_file)))
        del argv[:]
      except TTCException, e:
        sys.stderr.write("ERROR: %s\n" % str(e))

if ( __name__ == "__main__" ):
  sys.exit(main(sys.argv[1:]))

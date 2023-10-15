import os, md5, sys, string, signal
from coglib import certmaster
from M2Crypto import RSA

def msg(s, args=None):
  if (args is not None):
    s = s % args
  sys.stdout.write(s)
  sys.stdout.flush()

def md5file(fn):
  checksum = md5.new()
  f = open(fn, "rb")
  try:
    while 1:
      buf = f.read(8192)
      if (not buf):
        break
      checksum.update(buf)
  finally:
    f.close()
  return checksum.digest()

def main():
  signal.signal(signal.SIGPIPE, signal.SIG_DFL)

  if ( len(sys.argv) == 1 ):
    msg("""Usage: %s <file1> [<file2> ...]

Will verify the signature of the given software repository files.

""", (sys.argv[0],))
    sys.exit()

  old_cert_path  = certmaster.getCryptoPath( "wordbot", "wordbot~0.pub" )
  cert_path  = certmaster.getCryptoPath( "wordbot", "wordbot.srv" )

  rsa = RSA.load_key(cert_path)
  old_cert = None
  if ( os.path.exists(old_cert_path) ):
    try:
      old_cert = RSA.load_pub_key(old_cert_path)
    except:
      msg("WARNING: %s: Failed to load.\n", (old_cert_path,))

  for cur_file_path in sys.argv[1:]:
    if (cur_file_path[-4:] == ".sig"):
      msg("WARNING: %s (appears to be a .sig file, skipping)\n", (cur_file_path,))
      continue

    b_valid = 0

    md5_checksum = md5file(cur_file_path)

    sig_file = cur_file_path + ".sig"
    if ( os.path.exists(sig_file) ):
      s_reason = ".sig file invalid"
      sig = open(sig_file, "rb").read()

      b_valid = rsa.verify(md5_checksum, sig, 4)
      if ( (not b_valid) and (old_cert is not None) ):
        b_valid = old_cert.verify(md5_checksum, sig, 4)
      if ( b_valid ):
        msg("VALID:   %s\n", (cur_file_path,))
      else:
        msg("INVALID: %s (bad .sig file)\n", (cur_file_path,))
    else:
      msg("INVALID: %s (.sig file not present)\n", (cur_file_path,))

if __name__ == "__main__":
  try:
   main()
  except KeyboardInterrupt, e:
    pass

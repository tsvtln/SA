# ./py_build pylibs/des.py pylibs/dblib.py da_sapassword.py

import sys, des, getpass, os, md5, base64, string, dblib

pbe_password = "DA_password"

def msg(s):
  sys.stdout.write(s)
  sys.stdout.flush()

new_sapassword = getpass.getpass("new password: ")
new_sapassword_conf = getpass.getpass("confirm new password: ")

if ( new_sapassword != new_sapassword_conf ):
  msg("ERROR: mismatch, password not changed.\n")
  sys.exit(1)

if ( hasattr(os, "urandom") ):
  salt = os.urandom(8)
else:
  msg("WARNING: native source of random not available, using python psuedo rng.\n")
  import time, random
  random.seed(time.time())
  salt = string.join(map(lambda i:chr(random.randrange(0,256)), range(8)),"")

#salt = 'v\207d\320\276\261\031]'

def pbe_with_md5_and_des(password, msg, salt, iterations):
  # Calculate the des key and iv from the supplied password and salt:
  key_iv = password + salt
  cnt = 0
  while cnt < 1000:
    key_iv = md5.md5(key_iv).digest()
    cnt = cnt + 1
  s_key = key_iv[:8]
  s_iv = key_iv[8:]

#  print "s_key:", map(ord, s_key), "s_iv:", map(ord, s_iv)

  ec = des.des(key=s_key, mode=des.CBC, IV=s_iv, padmode=des.PAD_PKCS5)
  return ec.encrypt(new_sapassword)

cur = dblib.get_cursor()

cur.execute("select id from truth.da_global_configuration")
dgc_ids = map(lambda i:i[0], cur.fetchall())
dgc_ids.sort()

if ( len(dgc_ids) != 1 ):
  msg("WARNING: %d TRUTH.DA_GLOBAL_CONFIGURATION found.  Expecting 1.\n")
  if ( len(dgc_ids) == 0 ):
    msg("Nothing to do.\n")
    sys.exit(1)
  else:
    msg("Updating the record with the lowest id, %d\n" % dgc_ids[0])

dgc_id = dgc_ids[0]

new_sapassword_enc = string.strip(base64.encodestring(salt + pbe_with_md5_and_des(pbe_password, new_sapassword, salt, 1000)))

#print repr(new_sapassword_enc)

cur.callproc("LCREPPKG.BEGIN_TRANSACTION")
cur.execute("update truth.da_global_configuration set sapassword=:1 where id=:2", (new_sapassword_enc, dgc_id))
cur.callproc("LCREPPKG.END_TRANSACTION")
cur.execute("commit")

msg("DA's sapassword successfully updated.\n")


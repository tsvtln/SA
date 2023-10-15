
# verify_user_sigs Program Overview:
#
#   Itterates through AAA.AAA_USER records and verifies that the <SIGNATURE>
# field is correct.  If not, the user is asked if they would like to correct
# it.
#

import string, datetime, time, types, base64, sha, sys, hmac, cStringIO
import dblib, ttc, io, util

# ./py_build pylibs/io.py pylibs/util.py pylibs/loglib.py pylibs/dblib.py pylibs/sha1prng.py pylibs/aes.py pylibs/ttc.py verify_user_sigs.py

map_user_keys = {"user_id":"userId",
  "username":"username",
  "password_verified":"passwordVerified",
  "password_hash":"passwordHash",
  "password_modified_date":"passwordModifiedDate",
  "password_modified_by":"passwordModifiedBy",
  "created":"created",
  "most_recent_login":"mostRecentLogin",
  "most_recent_verification":"mostRecentVerification",
  "most_recent_lockout":"mostRecentLockout",
  "most_recent_invalid_login":"mostRecentInvalidLogin",
  "grace_login_count":"graceLoginCount",
  "invalid_login_attempts_count":"invalidLoginAttemptsCount",
  "password_reset_needed":"passwordResetNeeded",
  "account_status":"accountStatus",
  "auth_profile_id":"authProfileId",
  "user_status":"userStatus",
  "credential_store":"credentialStore",
  "external_auth_id":"externalAuthId",
  "hub_uid":"hubUid",
  "hub_gid":"hubGid",
  "auth_source_id":"authSourceId"}

lst_user_db_keys = map_user_keys.keys()
lst_user_db_keys.sort()

g_s_prog_name = os.path.basename(sys.argv[0])
def usage():
  io.out("""%s - Verifies <SIGNATURE> field of "AAA.AAA_USER" records.  If
an invalid signature is found, the user is asked if they would like to
correct it.

Usage: %s [-y] [-n] [<username_glob>|<user_id>]

  [-n]
    Will not attempt to fix any invalid signatures.

  [-y]
    Fix invalid signatures without asking for permission.

  [<username_glob>|<user_id>]
    Optional user id or username glob.

""" % ((g_s_prog_name,)*2))

def _str_to_hex(s):
  return string.join(map(lambda c:"%02X" % ord(c), s),'')

def shift(l):
  r = l[0]
  del l[0]
  return r

g_mmc_dvc = None
def _get_mmc_dvc():
  global g_mmc_dvc
  if ( g_mmc_dvc is None ):
    cur = dblib.get_cursor()
    mmc_dvc_id = dblib.get_mm_central_dvc_id()
    cur.execute("select * from devices where dvc_id=:1", (mmc_dvc_id,))
    g_mmc_dvc = dict(map(lambda k,v:(k,v), map(lambda d:string.lower(d[0]) ,cur.description), cur.fetchone()))
  return g_mmc_dvc

def _fix_user_sig(user, new_sig):
  try:
    my_dc_id = dblib.get_local_dc_id()
    if ( user["conflicting"] == "Y" ):
      if ( my_dc_id == dblib.get_mm_central_dc_id() ):
        dcs = dblib.get_all_dcs().values()
        for dc in dcs:
          _fix_user_sig_at_dc(dc, user, new_sig)
      else:
        mmc_dvc = _get_mmc_dvc()
        # It would be nice if the "update_all" flag worked, then we wouldn't have to require mm-central to fix this sort of problem. -dw
        io.out("ERROR: User %s(%d) is currently locked due to conflict.  In order to resign, unlock, and synchronize this user record, %s must be executed on the mm-central infra box: %s(%d/%s)\n\n" % 
               (user["username"], user["user_id"], g_s_prog_name, repr(mmc_dvc["system_name"]), mmc_dvc["dvc_id"], mmc_dvc["management_ip"]))
    else:
      _fix_user_sig_at_dc(dblib.get_all_dcs()[my_dc_id], user, new_sig)
  except:
    io.out("ERROR: Unexpceted error while attempting to fix signature for user %s(%d):\n%s\n" % (repr(user["username"]), user["user_id"], util.last_ex()))

def _fix_user_sig_at_dc(dc, user, new_sig):
  try:
    ucur = _get_update_cursor(dc["dc_id"])
    ucur.callproc("LCREPPKG.BEGIN_TRANSACTION")

    # Grab the transaction id.
    ucur.execute("select LCREPPKG.currentTransactionId from dual")
    tran_id = ucur.fetchone()[0]

    # If the record is conflicted.
    if ( user["conflicting"] == "Y" ):
      # Set this transaction to be forceful and non replicating.
      ucur.callproc("LCREPPKG.SET_FORCE")
      ucur.callproc("LCREPPKG.REPLICATE", ("N",))
      user_up = user.copy()
      user_up["conflicting"] = "N"
      del user_up["tran_id"]
      tran_desc = "forced non-replicating transction %d at %s(%d/%s)" % (tran_id, repr(dc["data_center_name"]), dc["dc_id"], dc["display_name"])
    else:
      user_up = {"user_id":user["user_id"]}
      tran_desc = "transaction %d" % tran_id

    # Set the username field of the transaction so folks know where it came from.
    # (We must do this _after_ calling lcreppkg.replicate other tran will replicate! -dw)
    ucur.callproc("LCREPPKG.SET_USERNAME", (g_s_prog_name,))

    new_sig_b64 = base64.encodestring(new_sig)
    # Remove all newline chars from the b64 signature.  (Twist does not like these.)
    new_sig_b64 = string.replace(new_sig_b64, "\n", "")
    user_up["signature"] = new_sig_b64

    # Construct SQL update string based on the user update dictionary.
    sql_up = "update aaa.aaa_user set %s where user_id=:user_id" % string.join(map(lambda k:"%s=:%s" % (k,k), filter(lambda k:k not in ("user_id",), user_up.keys())), ", ")
#    io.out("DEBUG: sql_up: %s, user_up: %s\n" % (repr(sql_up), repr(user_up)))

    # Execute the update.
    ucur.execute(sql_up, user_up)

    # Close out the HPSA LCREP transaction and commit it.
    ucur.callproc("LCREPPKG.END_TRANSACTION")
    ucur.execute("commit")

    # Let user know what we just did.
    io.out("FIXED signature for user %s(%d) via %s.\n" % (repr(user["username"]), user["user_id"], tran_desc))
  except:
    ucur.execute("rollback")
    io.out("ERROR: Unexpected error occured while attempting to fix signature for user %s(%d) at DC %s:\n%s\n" % (repr(user["username"]), user["user_id"], repr(dc), util.last_ex()))

g_map_dc_ucur = {}
def _get_update_cursor(dc_id):
  ucur = g_map_dc_ucur.get(dc_id, None)
  if ( ucur is None ):
    ucur = dblib.get_cursor(dc_id)
    g_map_dc_ucur[dc_id] = ucur
  return ucur

def main(args):
  s_def_answer = "x"
  s_where_clause = ""

  while ( args ):
    cur_arg = shift(args)
    if ( len(cur_arg) == 2 and cur_arg[0] == "-" and cur_arg[1] in "yYnN" ):
      s_def_answer = cur_arg[1]
    elif ( cur_arg in ("-h", "--help", "-?") ):
      usage()
      sys.exit()
    else:
      s_user_spec = cur_arg
      try:
        s_where_clause = "where user_id=%d" % long(s_user_spec)
      except ValueError, e:
        s_user_spec = string.replace(s_user_spec, "%", "\\%")
        s_user_spec = string.replace(s_user_spec, "*", "%")
        s_where_clause = "where username like '%s'" % s_user_spec

  # Query for a set of users to scan.
  qcur = dblib.get_cursor()
  s_sql = "select * from aaa.aaa_user %s" % s_where_clause
#  sys.stdout.write("DEBUG: s_sql: %s\n" % repr(s_sql))
  qcur.execute(s_sql)

  # Go ahead and load the twist key.
  twist_key = string.join(map(chr, ttc.load_key()), "")

  # Itterate over every record.
  while 1:
    # Fetch the next user record to analyze.
    user_rec = qcur.fetchone()
    if ( user_rec is None ): break

    # collapse this record into a dictionary.
    user = dict(map(lambda k,v:(k,v), map(lambda d:string.lower(d[0]) ,qcur.description), user_rec))

    # Decode the signature field.
    cur_sig = None
    try:
      cur_sig = base64.decodestring(user["signature"])
    except:
      io.out("WARNING: %s: Not a base64 encoded user signature.\n" % user["signature"])
      cur_sig = ""

    # Itterate through the sorted list of keys and compile a java.util.TreeMap
    # commpatible string representation of the user fields.
    lst_user_flds = []
    for key in lst_user_db_keys:
      if ( not user.has_key(key) ):
        continue
      val = user[key]
      if ( val is None ):
        continue
      elif ( type(val) == datetime.datetime ):
        val = "%d000" % time.mktime(val.timetuple())
      elif ( key in ("password_reset_needed", "password_verified") ):
        val = val and "true" or "false"
      lst_user_flds.append("%s=%s" % (map_user_keys[key], val))
    s_user_flds = "{%s}" % string.join(lst_user_flds, ", ")
#    sys.stdout.write("DEBUG: s_user_flds: %s\n" % repr(s_user_flds))

    # Calculate the signature of this user record.
    mac = hmac.new(twist_key, "", sha)
    mac.update(s_user_flds)
    exp_sig = mac.digest()

    # If the signatures differ:
    if ( cur_sig != exp_sig ):
      io.out("INVALID: %s(%d) - %s: (cur_sig=\"%s\", exp_sig=\"%s\").\n" % (repr(user["username"]), user["user_id"], user["user_status"], _str_to_hex(cur_sig), _str_to_hex(exp_sig)))
      a = s_def_answer
      b_fix = 0
      while ( a not in "yYaAnNoO" ):
        io.out("Resign? [y]es, [n]o, [a]ll, n[o]ne: ")
        try:
          a = sys.stdin.readline()[0]
        except KeyboardInterrupt, e:
          io.out("Interrupted.\n")
          sys.exit(1)
      if ( a in "yYaF" ):
        b_fix = 1
      if ( a in "aA"):
        s_def_answer = "y"
      if ( a in "oO" ):
        s_def_answer = "n"
      if ( b_fix ):
        _fix_user_sig(user, exp_sig)
    else:
      io.out("VALID: %s(%d) - %s\n" %  (repr(user["username"]), user["user_id"], user["user_status"]))

  if ( qcur.rowcount == 0 ):
    io.out("No matching user records found.\n")
  else:
    io.out("Done.\n")

if ( __name__ == "__main__" ):
  main(sys.argv[1:])
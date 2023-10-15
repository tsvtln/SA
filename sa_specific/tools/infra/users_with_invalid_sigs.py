import sys
from coglib import spinwrapper
import pytwist

b_all = 0
for arg in sys.argv[1:]:
  if ( arg == '-h' ):
    sys.stdout.write("""Usage: %s [-h] [-a]

  -h print this help text.

  -a scan all user records, otherwise only scans ACTIVE ones.

""" % sys.argv[0])
    sys.exit(0)
  elif ( arg == '-a' ):
    b_all = 1

spin = spinwrapper.SpinWrapper()
if ( b_all):
  sys.stdout.write("Scanning all user records.\n")
  restrict = {}
else:
  sys.stdout.write("Scanning ACTIVE user records.\n")
  restrict={'user_status':'ACTIVE'}
user_ids = spin._AAAAaaUser.getIDList(restrict=restrict)
num_users = spin._AAAAaaUser.getCount(restrict=restrict)

ts=pytwist.twistserver.TwistServer()

n = 1
for user_id in user_ids:
  sys.stderr.write("\r%d of %d" % (n,num_users))
  sys.stderr.flush()
  try:
    ts._makeCall("fido/ejb/session/UserFacade","getUserVOForUser",(user_id,))
  except pytwist.com.opsware.exception.TwistNonExistentException, e:
    user = spin._AAAAaaUser.get(user_id)
    sys.stdout.write("\n%s user %s(%d) appears to have an invalid signature.\n" % (user['user_status'], user['username'], user_id))
  n = n + 1
sys.stdout.write("\n")

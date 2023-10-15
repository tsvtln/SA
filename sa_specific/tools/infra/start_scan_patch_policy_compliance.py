import sys,getpass,pytwist

def usage():
  sys.stdout.write("%s [-u hpsa_username] <dvc_id1> [<dvc_id2> ...]\n\n")

args = sys.argv[1:]

def shift(l):
  r = l[0]
  del l[0]
  return r

username = None
password = None
dvc_ids = []

while ( len(args) > 0 ):
  cur_arg = shift(args)
  if ( cur_arg == "-u" ):
    username = shift(args)
    password = getpass.getpass("%s's password: ")
  else:
    dvc_ids.append(cur_arg)

if ( len(dvc_ids) == 0 ):
  usage()
  sys.exit(1)

ts = pytwist.twistserver.TwistServer()
if ( username is not None ):
  ts.authenticate(username, password)

from pytwist.com.opsware.server import ServerRef

dvc_refs = map(lambda id:ServerRef(id), dvc_ids)

job_ref = ts._makeCall("com/opsware/server/ServerService", "startScanPatchPolicyCompliance", [dvc_refs])

sys.stdout.write("%s\n" % str(job_ref))

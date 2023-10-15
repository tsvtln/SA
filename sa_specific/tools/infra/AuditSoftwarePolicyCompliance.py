import sys,time
sys.path.append("/opt/opsware/pylibs")
sys.path.append("/opt/opsware")
if ( len(sys.argv) != 3 ):
  print "Usage: %s <dvc_id> <user_token>" % sys.argv[0]
  sys.exit(1)
from waybot.base import twistaccess
ta = twistaccess.getTwistServiceForIp("127.0.0.1")
print ta.auditSoftwarePolicyCompliance(token=sys.argv[2], device=sys.argv[1], updateCompliance=1, fail=0)

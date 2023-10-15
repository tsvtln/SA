#!/opt/opsware/bin/python -u

import sys
sys.path.append('/opt/opsware/pylibs')
import pytwist

if ( len(sys.argv) < 3 ):
  print "Usage: %s <username> <newpassword>" % sys.argv[0]
  sys.exit(1)

sUsername = sys.argv[1]
sNewPassword = sys.argv[2]

ts = pytwist.twistserver.TwistServer()

lAdminUserId = ts._makeCall('fido/ejb/session/UserFacade','getUserVOForUser', [sUsername,'ACTIVE']).userId

ts._makeCall('fido/ejb/session/UserFacade','changePasswordForUser',[int(lAdminUserId),sNewPassword])
print "Successfully change password for user %s to %s." % (sUsername, sNewPassword)

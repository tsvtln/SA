import sys
import thread
import string

sys.path.append("/opt/opsware/pylibs")
sys.path.append("/lc/blackshadow")

from coglib import spinwrapper

from coglib import timegm

spin = spinwrapper.SpinWrapper()

key_map = {'id': 'userId', 'username': 'username', 'password_verified': 'passwordVerified', 
	'password_hash': 'passwordHash', 'password_modified_date': 'passwordModifiedDate', 
	'password_modified_by': 'passwordModifiedBy', 
	'created': 'created', 'most_recent_login': 'mostRecentLogin', 
	'most_recent_verification': 'mostRecentVerification', 
	'most_recent_lockout': 'mostRecentLockout', 
	'most_recent_invalid_login': 'mostRecentInvalidLogin', 
	'grace_login_count': 'graceLoginCount', 
	'invalid_login_attempts_count': 'invalidLoginAttemptsCount',
	'password_reset_needed': 'passwordResetNeeded', 'account_status': 'accountStatus',
	'auth_profile_id': 'authProfileId', 'user_status': 'userStatus',
	'credential_store': 'credentialStore', 'external_auth_id': 'externalAuthId'}

# | 3
# : 2
# % 1
# <None> 4
def Encode( val ):
	if (val is None):
		return "%4"

	if ( str(type(val)) == "<type 'xmlrpcdateTime'>" ):
		return str(timegm.timegm(val.date())) + '000'

	val = string.replace( str(val), "%", "%1" )
	val = string.replace( val, ":", "%2" )
	return string.replace( val, "|", "%3" )

if ( len(sys.argv) != 2 ):
	sys.stderr.write( "Usage: %s <AAA_USER_ID>\n\n" % sys.argv[0] )
	sys.exit(1)

user = spin._AAAAaaUser.get( id=sys.argv[1] )

for key in key_map.keys():
	val = Encode(user[key])
	sys.stdout.write( "|%s:%s" % (key_map[key],val) )

sys.stdout.write( '||' )

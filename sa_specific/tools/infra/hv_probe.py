import sys,pytwist,pprint,string,getpass
from coglib import spinwrapper

if ( len(sys.argv) != 5 ):
  sys.stdout.write("Usage: %s <sa_username> <hv_username> <hv_IP> <realm_name>\n" % sys.argv[0])
  sys.exit(1)

sa_username=sys.argv[1]
hv_username=sys.argv[2]
hv_ip=sys.argv[3]
hv_realm_name=sys.argv[4]

# Check the realm name.
spin = spinwrapper.SpinWrapper()
realm_names=filter(lambda i:i[-3:]!="-mm", map(lambda i:i[1],spin.Realm.getList(fields=['realm_name'],restrict={'realm_type':['SATELLITE','BASE']})))
if ( not (hv_realm_name in realm_names) ):
  sys.stdout.write("%s: %s: Realm not found, valid realms:\n%s\n" % (sys.argv[0],hv_realm_name,string.join(realm_names,"\n")))
  sys.exit(1)

ts = pytwist.twistserver.TwistServer()

so=sys.stdout;getpass.sys.stdout=sys.stderr
ts.authenticate(sys.argv[1],getpass.getpass("%s's password for HPSA:" % sa_username))
getpass.sys.stdout=so

from pytwist.com.opsware.virtualization import ESXServerConnectionInfoVO
from pytwist.com.opsware.locality import RealmRef
ci = ESXServerConnectionInfoVO()
ci.username=hv_username

getpass.sys.stdout=sys.stderr
ci.password=getpass.getpass("%s's password for hypervisor %s:" % (hv_username,hv_ip))
getpass.sys.stdout=so

ci.connectionIP=hv_ip
ci.realm=RealmRef(0)
ci.realm.name=hv_realm_name
pprint.pprint(ts._makeCall("com.opsware.virtualization.HypervisorService","probeDevice",(ci,)).__dict__)


import sys,os,copy,getpass,pytwist

help = 0
username = None

def shift(l):
  r = l[0]
  del l[0]
  return r

argv = copy.copy(sys.argv[1:])
while (argv):
  arg = shift(argv)
  if ( arg == '-h' ):
    help = 1
  elif ( arg == '-u' ):
    username = shift(argv)

if ( help ):
  sys.stdout.write("""Usage: %s [-u <username>]

""" % sys.argv[0])
  sys.exit(1)

ts = pytwist.twistserver.TwistServer()
if ( username ):
  password = getpass.getpass("password: ")
  ts.authenticate(username, password)

dg_service = ts.device.DeviceGroupService

from pytwist.com.opsware.search import Filter

dgs = dg_service.findDeviceGroupRefs(Filter())

do_all = 0
for dg in dgs:
  os.write(2,'\x1B[2K\r%s' % str(dg))
  dgvo = dg_service.getDeviceGroupVO(dg)
  if ( dgvo.dynamic ):
    dyn_rule = dgvo.dynamicRule.expression
    if ( dyn_rule ):
      if ( not sys.stdout.isatty() ):
        sys.stdout.write("%s" % str(dg))
      sys.stdout.write("\n  %s\n\n" % dyn_rule)

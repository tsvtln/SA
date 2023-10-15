# update_dyn_group_filter <orig_re> [<replacement>]

import sys,os,re,copy,getpass,pytwist

orig_re = None
replacement = None
username = None

def shift(l):
  r = l[0]
  del l[0]
  return r

argv = copy.copy(sys.argv[1:])
while (argv):
  arg = shift(argv)
  if ( arg == '-o' ):
    orig_re = re.compile(shift(argv))
  elif ( arg == '-r' ):
    replacement = shift(argv)
  elif ( arg == '-u' ):
    username = shift(argv)

if ( orig_re == None ):
  sys.stdout.write("""Usage: %s [-u <username>] -o <orig_re> [-r <replacement>]

Examples:

  (1) To list all dynamic group rules:

      # ./mod_dyn_group_filter -o .

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
  dyn_rule = dgvo.dynamicRule.expression
  if ( dgvo.dynamic and orig_re.search(dyn_rule)):
    if ( not sys.stdout.isatty() ):
      sys.stdout.write("%s" % str(dg))
    sys.stdout.write("\n  %s\n\n" % dyn_rule)
    if ( replacement != None ):
      new_dyn_rule = orig_re.sub(replacement, dyn_rule)

      if ( not do_all ):
        sys.stdout.write("Would be changed to:\n  %s\n" % new_dyn_rule)
        sys.stdout.write("replace? y/n/a\n")

        resp = os.read(0,1024)[0]
        if ( resp in "aA" ):
          do_all = 1

      if ( do_all or resp in "yY" ):
        dgvo.dynamicRule.expression = new_dyn_rule
        sys.stdout.write("dynamic rule changed to:\n  %s\n" % dgvo.dynamicRule.expression)
        dg_service.setDynamicRule(dg,dgvo.dynamicRule)



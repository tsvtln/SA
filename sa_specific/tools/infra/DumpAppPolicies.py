#!/opt/opsware/bin/python

import sys

sys.path.append("/opt/opsware/pylibs")

from coglib import spinwrapper

spin = spinwrapper.SpinWrapper()
#url="http://localhost:1007", userName="JkO9VOIB", userPassword="c3xrofNMgl")

dvc = spin.Device.get(sys.argv[1])

aps = dvc.getChildren( child_class="AppPolicy" )

units = {}

print "Application Policies for Device '%s' (%d):" % (dvc['system_name'], dvc['id'])

nAppPolicyCount = 1

for ap in aps:
  print "  %d. Application Policy '%s' (%d):" % ( nAppPolicyCount, ap['app_policy_name'], ap['id'] )
  nAppPolicyCount = nAppPolicyCount + 1
  apuis = ap.getChildren( child_class="AppPolicyUnitItem" )
  for apui in apuis:
    if (not units.has_key(apui['unit_id'])):
      units[apui['unit_id']] = spin.Unit.get(apui['unit_id'])
    print "    %s. %s | %s | %s" % (str(apui['install_order']), units[apui['unit_id']]['unit_file_name'], apui['unit_id'], units[apui['unit_id']]['install_flags'])


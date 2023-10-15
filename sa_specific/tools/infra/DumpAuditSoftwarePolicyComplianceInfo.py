import sys, pprint, time

if ( len(sys.argv) != 2 ):
  print "Usage: %s <dvc_id>" % sys.argv[0]
  sys.exit(1)
from coglib import spinwrapper

def getUnitCustomers(u):
  if ( u['acct_id'] != 25 ):
    return str(u['acct_id'])
  else:
    r = {}
    fs = u.getChildren(child_class="Folder")
    for f in fs:
      accts = map(lambda x:x['id'], f.getChildren(child_class="Account"))
      r[f['id']] = accts
    return str(r)

def replDates(o):
  for k in o.keys():
    if (str(type(o[k])) == "<type 'xmlrpcdateTime'>"):
      o[k] = time.asctime(o[k].date() + (0,0,0))
  return o

spin = spinwrapper.SpinWrapper()
dvc_id=sys.argv[1]
d = spin.Device.get(dvc_id)
print "Device %s(%s)%s(acct: %s)(plat: %s)" % (d['system_name'], dvc_id, str(replDates(d)), d.getAccount()['id'], d.getPlatform()['id'])
print "Application Policies:"
aps = d.getChildren(child_class="AppPolicy")
for ap in aps:
  print "  App Policy: %s(%s):" % (ap['app_policy_name'], ap['app_policy_id'])
  apuis = ap.getChildren(child_class="AppPolicyUnitItem")
  for apui in apuis:
    uid = apui['unit_id']
    u = spin.Unit.get(uid)
    print "    Unit: %s(accts: %s)" % (str(replDates(u)), getUnitCustomers(u))
print "InstalledUnits:"
ius = d.getChildren(child_class="InstalledUnit")
for iu in ius:
  print "  iu: %s" % (str(replDates(iu)))
print "Virtual Columns Values:"
pprint.pprint(replDates(d.getVirtualColumnValues()))
print "SwComplianceResults:"
pprint.pprint(spin.SwComplianceResult.getAll(restrict={'dvc_id':dvc_id}))
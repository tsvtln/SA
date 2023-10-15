import sys,traceback,string,types,cPickle
from coglib import spinwrapper
from opsware_common import errors
spin = spinwrapper.SpinWrapper()

def str_dates(obj):
  if ( type(obj) != types.DictType ): return
  for key in obj.keys():
    val = obj[key]
    if type(val).__name__ == 'xmlrpcdateTime':
      obj[key] = str(val)

def obj_key(klass, id):
  if (type(id) == types.LongType): id = "%d" % id
  return "%s:%s" % (klass, id)

g_objs = {}
def getObj(klass, id):
  key = obj_key(klass, id)
  if g_objs.has_key(key): return g_objs[key]
  try:
    obj = getattr(spin, klass).get(id).data
  except errors.OpswareError, e:
    if (hasattr(e,'params') and type(e.params)==types.DictType and e.params.has_key('msg') and type(e.params['msg'])==types.StringType and string.find(e.params['msg'], 'Record not found in table') > -1):
      obj = None
    else:
      raise e
  str_dates(obj)
  g_objs[key] = obj
  return obj

def getChildObjs(pklass, pid, cklass):
# The code below performs slow, and a cache hit is very unlickly, so commenting it out.
#  obj_ids = getattr(spin, pklass).getChildIDList(id=pid,child_class=cklass)
#  return map(lambda id,k=cklass:getObj(k,id), obj_ids)
  cobjs = map(lambda o:o.data, getattr(spin, pklass).getChildren(id=pid,child_class=cklass))
  for cobj in cobjs:
    key = obj_key(cklass, cobj['id'])
    if (not g_objs.has_key(key)):
      str_dates(cobj)
      g_objs[key] = cobj
  return cobjs

def dump_del_unit_rels(u):
  try:
    rius = getChildObjs(u['obj_class'],u['id'],"ReconcileInstalledUnit")
    sys.stdout.write("  rius: %d\n" % len(rius))
    rius.sort(lambda a,b:cmp(a['install_order'],b['install_order']))
    for riu in rius:
      dvc_id = riu['dvc_id']
      d = getObj("Device",dvc_id)
      rc_id = riu['role_class_id']
      rc = getObj("RoleClass", rc_id)
      rcfn = "**Not Found**"
      if ( rc ): rcfn = rc['role_class_full_name']
      sys.stdout.write("    %d: dvc:%s(%d), rc:%s(%d), create_dt:%s\n" % (riu['install_order'],d['system_name'],dvc_id,rcfn,rc_id,riu['create_dt']))

    aprius = getChildObjs(u['obj_class'], u['id'], "AppPolicyRIU")
    sys.stdout.write("  aprius: %d\n" % len(aprius))
    aprius.sort(lambda a,b:cmp(a['install_order'],b['install_order']))
    for apriu in aprius:
      dvc_id = apriu['dvc_id']
      d = getObj("Device",dvc_id)
      ap_id = apriu['app_policy_id']
      ap = getObj("AppPolicy", ap_id)
      sys.stdout.write("    %d: dvc:%s(%d), ap:%s(%d), create_dt:%s\n" % (apriu['install_order'],d['system_name'],dvc_id,ap['app_policy_name'],ap_id,apriu['create_dt']))

    rus = getChildObjs(u['obj_class'], u['id'], "RealmUnit")
    sys.stdout.write("  rus: %d\n" % len(rus))
    for ru in rus:
      realm_id = ru['realm_id']
      realm = getObj("Realm",realm_id)
      sys.stdout.write("    %s/%s(%d): should_exist:%s, does_exist:%s\n" % (realm['display_name'],realm['realm_name'],realm_id,ru['should_exist'],ru['does_exist']))
  except KeyboardInterrupt, e:
    raise e
  except:
    sys.stdout.write("Trapped Exception while process unit_id %s:\n" % repr(unit_id))
    sys.stdout.write(string.join(apply(traceback.format_exception, sys.exc_info())))

unit_ids = []
if ( len(sys.argv) > 1 ):
  unit_ids = sys.argv[1:]
  sys.stderr.write("Dumping GC related information for %d specified unit ids...\n" % len(unit_ids))
else:
  unit_ids = spin.Unit.getIDList(restrict={'status':'DELETED'})
  sys.stderr.write("Dumping GC related information for %d units...\n" % len(unit_ids))
sys.stderr.flush()

n = 1
for unit_id in unit_ids:
  u = getObj("Unit",unit_id)
  unit_desc = "[%d/%d] %s: %s(%s)\n" % (n,len(unit_ids),unit_id, u['unit_name'], u['unit_loc'])
  sys.stdout.write(unit_desc)
  sys.stderr.write(unit_desc)
  sys.stderr.flush()
  dump_del_unit_rels(u)
  n = n + 1

sys.stdout.write("g_objs:\n")
sys.stderr.write("Emitting object dictionary...\n")
sys.stderr.flush()

cPickle.dump(g_objs, sys.stdout)

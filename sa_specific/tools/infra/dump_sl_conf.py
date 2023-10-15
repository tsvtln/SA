import sys,types,string,cPickle
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

def dump_rc_conf(rc, depth=0):
  indent = '  ' * depth
  rc_id = rc['id']
  sl_desc = "%s%s(%d)\n" % (indent, rc['role_class_full_name'], rc_id)
  sys.stdout.write(sl_desc)
  sys.stderr.write(sl_desc)
  sys.stderr.flush()

  dvcs_count = spin.RoleClass.getChildCount(id=rc_id, child_class="Device")
  sys.stdout.write("%s  Attached Devices(%d):\n" % (indent, dvcs_count))
  if ( dvcs_count > 100 ):
    sys.stdout.write("%s    (Too many devices to list)\n" % indent)
  else:
    dvcs = getChildObjs("RoleClass", rc_id, "Device")
    for dvc in dvcs:
      sys.stdout.write("%s    %s/%s(%d)\n" % (indent, dvc['system_name'], dvc['management_ip'], dvc['id']))

  acws = getattr(spin, "RoleClass").getChildren(id=rc_id,child_class="AppConfigWad")
  if ( acws ):
    items = acws[0].getLocalDictItems()
    sys.stdout.write("%s  Configuration Items(%d):\n" % (indent, len(items)))
    for item in items:
      sys.stdout.write("%s    %s: %s\n" % (indent, item[0], repr(item[1])))

  # Recurse for child service levels.
  crcs = getChildObjs("RoleClass", rc_id, "RoleClass")
  for crc in crcs:
    dump_rc_conf(crc, depth=depth+1)

sl_rc_root = getObj("RoleClass", 4)
dump_rc_conf(sl_rc_root)

sys.stdout.write("g_objs:\n")
sys.stderr.write("Emitting object dictionary...\n")
sys.stderr.flush()
cPickle.dump(g_objs, sys.stdout)


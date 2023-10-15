import sys, pytwist, opsware_common, string
from coglib import spinwrapper

spin = spinwrapper.SpinWrapper()

mapORTtoSO = {
  'FACILITY':('DataCenter', ('data_center_name', 'display_name', 'data_center_id'), '"%s" (%s/%d)'),
  'DEVICE_GROUP':('RoleClass', ('role_class_short_name', 'role_class_id'), '"%s" (%d)'),
  'STACK':('RoleClassStack', ('stack_name', 'id'), '"%s" (%d)'),
  'STACK_LOCKING':('RoleClassStack', ('stack_name', 'id'), '"%s" (%d)'),
  'CUSTOMER':('Account', ('display_name', 'acct_name', 'acct_id'), '"%s" (%s/%d)')}

user_groups = []
if ('is_private' in map(lambda f:f['name'], spin._AAAOccGroup.getFields())):
  user_groups = spin._AAAOccGroup.getAll(restrict={'is_private':0})
else:
  user_groups = spin._AAAOccGroup.getAll()

obj_name_cache = {}

progress_chars = '\-/-'
cur_progress_char = 0
def progress_char():
  global cur_progress_char
  cur_progress_char = cur_progress_char + 1
  if ( cur_progress_char == len(progress_chars) ):
    cur_progress_char = 0
  return progress_chars[cur_progress_char]

for user_group in user_groups:
  sys.stdout.write('"%s" (%s):\n' % (user_group['group_name'], user_group['occ_group_id']))
  rss = spin._AAAOccGroupResourceSetting.getAll(restrict={'occ_group_id':user_group['id']})
  rss.sort(lambda a,b:cmp(a['occ_resource_type'],b['occ_resource_type']))

  sys.stdout.write("  OCC Resource Permissions:\n")
  for rs in rss:
    obj_res_type = rs['occ_resource_type']
    obj_class_spec = mapORTtoSO[obj_res_type]
    obj_class = obj_class_spec[0]
    obj_id = rs['value']
    obj_key = "%s:%s" % (obj_class, obj_id)
    obj_name = ''
    if ( obj_name_cache.has_key(obj_key) ):
      obj_name = obj_name_cache[obj_key]
    else:
      try:
        obj = getattr(spin, obj_class).get(obj_id)
        obj_name = obj_class_spec[2] % tuple(map(lambda fn,o=obj.data:o[fn], obj_class_spec[1]))
      except opsware_common.errors.OpswareError, e:
        obj_name = "**%s**" % e.faultString
      obj_name_cache[obj_key] = obj_name
    sys.stdout.write("    o %s:%s [%s] %s\n" % (obj_res_type, obj_id, rs['occ_access_level'], obj_name))

  sys.stdout.write("  User Members: ")
  if ( len(sys.argv) > 1 and sys.argv[1] == '-u' ):
    aaa_role = user_group.getChildren(child_class='_AAARole', restrict={'namespace':'ACCESS_CONTROL'})[0]
    arus = aaa_role.getChildren(child_class='_AAARoleUser')
    users = []
    for aru in arus:
      au = aru.getParent(parent_class='_AAAAaaUser')
      users.append("%s(%s)" % (au['username'], au['user_id']))
      sys.stderr.write("%s\r" % progress_char())
      sys.stderr.flush()
    sys.stdout.write("[%s]\n" % string.join(users, ', '))
  else:
    sys.stdout.write("(add '-u' to see users)\n")

  sys.stdout.write("\n")
  sys.stdout.flush()

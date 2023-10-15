import sys, opsware_common, string, new
from coglib import spinwrapper

# (18:19:29) baaz1505: 1) dump a specified user's priveleges such as: 1) Customers 2) Facilities 3) Device Groups 4) Folders (this needs to tell you also what you can do with a folder and it's contents)
# (18:20:21) baaz1505: 4) Feature permissions 5) OGSH permissions
# (18:20:59) baaz1505: 5) Optionally write out to an Excel sheet ... I know I know but cust.'s love Excel, I am OK with plain text :)
# (18:22:12) baaz1505: 6) Given a customer/facility/dvc group/folder/feature/OGSH perm, dump out who has that perm
# (18:22:24) baaz1505: #6 would be a powerful feature to have

# util name: occ_perms
#
# Todo:
#
# [X] List all users.
# [X] List permissions of given users.  (wildcards)
# [X] List all user groups.
# [ ] List permissions of given user groups. (wildcards)
# [ ] List all possible permissions.
# [ ] List groups -> users who have given permissions.
#

# Major hack to get around python2 protocol=1 pickle issue with the use of
# legacy classes.
sys.path.append((filter(lambda p:p[:19]=='/opt/opsware/pylibs',sys.path) or ['/opt/opsware/pylibs'])[0] + '/pytwist')
import twistserver
g_ts = twistserver.TwistServer()

g_spin = spinwrapper.SpinWrapper()

def usage():
  sys.stdout.write("""Tool to query for and dump OCC permission details.

Usage:
  %s [-li [<user>[:<password>]][@<server>[:<port>]]] [-lu | -u <user_glob>] |
     -lg | -g <group_glob> | -lp | -p <perm_spec>]

  -li [<user>[:<password>]][@<server>[:<port>]]
    Login using the specified credentials.

  -lu
    List all OCC users in the system.

  -u <user_glob>
    List OCC  permissions for  the users given  by <user_glob>.  (To  specify a
    user by ID, use "id:<user_id>".

  -lg
    List all OCC user groups in the system.

  -g <group_glob>
    List OCC permissions  for the groups given by  <group_glob>.  (To specify a
    group by ID, use "id:<group_id>".

  -lp
    List all permissions.

  -p <perm_spec>
    List  all  users who  have  the  permissions  given by  <perm_spec>.   Also
    indicates which group the user inherretted the permission from.

  -h
    Print usage.
""" % sys.argv[0])

def fmt_rows(rows, col_sep='  ', indent=0):
  if ( not rows ): return ''
  num_cols = len(rows[0])
  col_maxes = range(num_cols)
  for cur_col in col_maxes:
    col_maxes[cur_col] = max(map(lambda r,cc=cur_col:len(str(r[cc])), rows))
  fmt = string.join(["%%-%ds"] * num_cols, col_sep) % tuple(col_maxes)
  return string.join(map(lambda r,f=fmt,i=indent:' '*i + (f % r), rows), '\n') + '\n'

def safe_int_to_str(val):
  try:
    return '%d' % val
  except:
    return '%s' % val

def progress_char(progress_chars='\-/-', pcur_progress_char=[0]):
  cur_progress_char = pcur_progress_char[0]
  cur_progress_char = cur_progress_char + 1
  if ( cur_progress_char == len(progress_chars) ):
    cur_progress_char = 0
  pcur_progress_char[0] = cur_progress_char
  return progress_chars[cur_progress_char]

def login(login_spec):
  sys.stdout.write("TODO: '-li' option not implemented.\n")

def tweak_legacy_obj(obj, args):
  obj.__getinitargs__ = new.instancemethod(lambda self,a=args:a, obj, obj.__class__)
  obj.__getstate__ = new.instancemethod(lambda self:{},obj,obj.__class__)

def get_user_filter(uns=None):
  user_filter = twistserver._findVOs("com.opsware.fido.list.filter.impl", "UserFilter")()
  user_filter.userNames = uns
  return user_filter

def get_group_filter(uid=None, gn=None):
  group_filter = twistserver._findVOs("com.opsware.fido.list.filter.impl", "OccGroupFilter")()
  group_filter.occGroupName = gn
  group_filter.userId = uid
  return group_filter

def get_occ_groups_by_uid(uid):
  group_filter = get_group_filter(uid=uid)
  ogvos = g_ts._makeCall("fido/ejb/session/OccAdminFacade", "getOccGroupVOList", [group_filter])
  # We need to filter out dups. (why is the twist returning dups?)
  ogvos_map = {}
  for ogvo in ogvos:
    ogvos_map[ogvo.occGroupId] = ogvo
  return ogvos_map.values()

def ogrs_vo_to_spec(ogrsvo):
  return "%s:%d:%s" % (ogrsvo.occResourceType, ogrsvo.value, ogrsvo.occAccessLevel)

g_ogvo_cache = {} # {ogid:ogvo}
def get_ogvo_by_ogid(ogid):
  ogvo = None
  if ( g_ogvo_cache.has_key(ogid) ):
    ogvo = g_ogvo_cache[ogid]
  else:
    ogvo = g_ts._makeCall("fido/ejb/session/OccAdminFacade", "getOccGroupVO", [ogid])
    g_ogvo_cache[ogid] = ogvo
  return ogvo

def get_ogvo_rep(ogvo):
  if ( ogvo ):
    return '"%s" (%s)' % (ogvo.groupName, ogvo.occGroupId)
  else:
    return "**ogid:%s not found**" % str(ogid)

g_mapORTtoSO = {
  'FACILITY':('DataCenter', ('data_center_name', 'display_name'), '"%s" (%s)'),
  'DEVICE_GROUP':('RoleClass', ('role_class_short_name',), '"%s"'),
  'STACK':('RoleClassStack', ('stack_name',), '"%s"'),
  'STACK_LOCKING':('RoleClassStack', ('stack_name',), '"%s"'),
  'CUSTOMER':('Account', ('display_name', 'acct_name'), '"%s" (%s)')}

g_spin_obj_rep_cache = {} # {"<obj_class>:<obj_id>":"<obj_rep>"}
def get_spin_obj_rep(res_type, obj_id):
  obj_class_spec = g_mapORTtoSO[res_type]
  obj_class = obj_class_spec[0]
  obj_key = "%s:%s" % (obj_class, obj_id)
  obj_rep = ''
  if ( g_spin_obj_rep_cache.has_key(obj_key) ):
    obj_rep = g_spin_obj_rep_cache[obj_key]
  else:
    try:
      obj = getattr(g_spin, obj_class).get(obj_id)
      obj_rep = obj_class_spec[2] % tuple(map(lambda fn,o=obj.data:o[fn], obj_class_spec[1]))
    except opsware_common.errors.OpswareError, e:
      obj_rep = "**%s**" % e.faultString
    g_spin_obj_rep_cache[obj_key] = obj_rep
  return obj_rep

def get_ogfs_perms(ogvo):
  pass

def list_user_perms(uvo):
  sys.stdout.write('  Group Membership: ')
  ogvos = get_occ_groups_by_uid(uid=uvo.userId)
  ogvos.sort(lambda a,b:cmp(a.occGroupId,b.occGroupId))
  ogids = map(lambda ogvo:ogvo.occGroupId, ogvos)
  rows = [('ID', 'Name')]
  sys.stdout.write('(%d)\n' % len(ogvos))
  for ogvo in ogvos:
    rows.append((ogvo.occGroupId, ogvo.groupName))
  sys.stdout.write('%s\n' % fmt_rows(rows, indent=4))

  sys.stdout.write('  OCC Resource Permissions: ')
  sys.stdout.flush()
  ogrs_map = {} # {<ogrs_spec>:(<ogrsvo>, [<ogid>, ...])}
  for ogid in ogids:
    ogrsvos = g_ts._makeCall("fido/ejb/session/OccAdminFacade", "getOccGroupResourceSettingVOsByGroup", [ogid])
    for ogrsvo in ogrsvos:
      sys.stderr.write('%s\x1B[1D' % progress_char())
      sys.stderr.flush()
      ogrs_spec = '%s:%s:%s' % (ogrsvo.occResourceType, ogrsvo.occAccessLevel, safe_int_to_str(ogrsvo.value))
      if ( ogrs_map.has_key(ogrs_spec) ):
        ogrs_map[ogrs_spec][1].append(ogid)
      else:
        ogrs_map[ogrs_spec] = (ogrsvo,[ogid])
  sys.stdout.write('(%d)\n' % len(ogrs_map))
  ogrsvo_recs = list(ogrs_map.values())
  ogrsvo_recs.sort(lambda a,b:cmp(a[0].occResourceType, b[0].occResourceType))
  rows = [('Type', 'Access', 'Obj_Name', 'Obj_ID', 'Via_Groups')]
  for ogrsvo_rec in ogrsvo_recs:
    ogrsvo = ogrsvo_rec[0]
    via_ogids = ogrsvo_rec[1]
    ogs_rep = string.join(map(lambda i:'%d' % i, via_ogids), ', ')
    obj_name = get_spin_obj_rep(ogrsvo.occResourceType, ogrsvo.value)
    rows.append((ogrsvo.occResourceType, ogrsvo.occAccessLevel, obj_name, safe_int_to_str(ogrsvo.value), ogs_rep))
  sys.stdout.write('%s\n' % fmt_rows(rows, indent=4))

  sys.stdout.write('  OCC Features: ')
  sys.stdout.flush()
  ofr_map = {} # {<ofid>:(<ofvo>, [<ogid>, ...])}
  for ogid in ogids:
    ofvos = g_ts._makeCall("fido/ejb/session/OccAdminFacade", "getOccFeatureVOsByGroup", [ogid])
    for ofvo in ofvos:
      sys.stderr.write('%s\x1B[1D' % progress_char())
      sys.stderr.flush()
      ofid = ofvo.occFeatureId
      if ( ofr_map.has_key(ofid) ):
        ofr_map[ofid][1].append(ogid)
      else:
        ofr_map[ofid] = (ofvo,[ogid])
  sys.stdout.write('(%d)\n' % len(ofr_map))
  ofvo_recs = list(ofr_map.values())
  ofvo_recs.sort(lambda a,b:cmp(a[0].occFeatureCategory, b[0].occFeatureCategory))
  rows = [('Category', 'Name', 'Key', 'Via_Groups')]
  for ofvo_rec in ofvo_recs:
    ofvo = ofvo_rec[0]
    via_ogids = ofvo_rec[1]
    ogs_rep = string.join(map(lambda i:'%d' % i, via_ogids), ', ')
    rows.append((ofvo.occFeatureCategory, ofvo.displayName, ofvo.resourceKey, ogs_rep))
  sys.stdout.write('%s\n' % fmt_rows(rows,indent=4))

  # use UserRoleService to map a group into a role. (usually by name)

  # Dump OGFS perms.
  # (see OGFSPermissionsBean.java::getPermissions())
#  for ogvo in ogvos:
#    ogfs_perms = get_ogfs_perms(ogvo)
#    for ogfs_perm in ogfs:
#    # TODO
#  list_ogfs_perms(uvo, indent=4)

  # Dump folder perms.
  # (see FolderSearchBean.java::getFolderPathPermissions())
#  list_folder_perms(uvo, indent=4)
# example: ./sql "select f.folder_name, ar.role_name, ar.role_type, arfs.occ_access_level from aaa.aaa_user aau, aaa.role_user aru, aaa.role ar, aaa.role_folder_setting arfs, folder f where aau.user_id=aru.user_id and aru.role_id=ar.role_id and ar.role_id=arfs.role_id and arfs.folder_id=f.folder_id and aau.username='dwest'"
# Should also join with aaa.occ_group.
# And resolve folder into an absolute path.

def list_users(uns=None, list_perms=0):
  user_filter = get_user_filter(uns)
  uvos = g_ts._makeCall("fido/ejb/session/UserFacade", "getUserVOs", [user_filter])
  uvos = list(uvos)
  uvos.sort(lambda a,b:cmp(a.username, b.username))
  for uvo in uvos:
    status = ''
    if (uvo.accountStatus != 'ACTIVE'):
      status = "(%s)" % uvo.accountStatus
    sys.stdout.write('%s%s (%s)\n' % (status, uvo.username, uvo.userId))
    if (list_perms):
      list_user_perms(uvo)

def list_groups():
  group_filter = get_group_filter()
  ogvos = g_ts._makeCall("fido/ejb/session/OccAdminFacade", "getOccGroupVOList", [group_filter])
  ogvos = list(ogvos)
  ogvos.sort(lambda a,b:cmp(a.groupName, b.groupName))
  for ogvo in ogvos:
    sys.stdout.write('%s\n' % get_ogvo_rep(ogvo))

def shift(lst):
  if lst:
    ret = lst[0]
    del lst[0]
    return ret
  else:
    return None

def main(argv):
  if ( not argv ):
    usage()
    sys.exit(1)
  while argv:
    arg = shift(argv)
    if ( arg == '-li' ):
      login(shift(argv))
    elif ( arg == '-lu' ):
      list_users()
    elif ( arg == '-u' ):
      user_glob = shift(argv)
      if ( not user_glob ):
        sys.stdout.write('%s: "-u" option requires a <user_glob>\n' % sys.argv[0])
        usage()
        sys.exit(1)
      list_users(uns=string.split(user_glob, ','), list_perms=1)
    elif ( arg == '-lg' ):
      list_groups()
    elif ( arg == '-h' ):
      usage()
      sys.exit(0)
    else:
      sys.stderr.write("%s: WARNING: '%s' is an unrecognized argument.  skipping\n" % (sys.argv[0], arg))

if __name__ == "__main__":
  main(sys.argv[1:])

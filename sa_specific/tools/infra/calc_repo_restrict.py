import sys

def out(msg, args=None):
  if ( args ): msg = (msg % args)
  sys.stdout.write(msg)
  sys.stdout.flush()

def info(msg, args=None):
  msg = msg + "\n"
  out(msg, args)

def usage():
  info( """Usage: %s <app_policy_id>

Calculates the unique list of HPSA Library folder paths from which all the
RPMs, directly attached to the software policy given by <app_policy_id>
originate.
""" % sys.argv[0])

if ( len(sys.argv) != 2 ):
  usage()
  sys.exit(1)

app_policy_id = sys.argv[1]

def _calc_folder_path(spin, f_id):
  folder_path = ""
  cur_f_id = f_id
  while cur_f_id:
    cur_f_name = spin.Folder.getList(restrict={'folder_id':cur_f_id}, fields=['folder_name'])[0][1]
    folder_path = "/" + cur_f_name + folder_path
    cur_f_id = spin._FolderFolderLink.getList(restrict={'folder_id':cur_f_id}, fields=['parent_folder_id'])[0][1]
  return folder_path

_folder_paths = {}
def get_folder_path(spin, f_id):
  folder_path = _folder_paths.get(f_id,None)
  if ( not folder_path ):
    folder_path = _calc_folder_path(spin,f_id)
    _folder_paths[f_id] = folder_path
  return folder_path

from coglib import spinwrapper
spin = spinwrapper.SpinWrapper()

ap = spin.AppPolicy.get(app_policy_id)
info("Processing %s(%s):\n", (repr(ap['app_policy_name']), ap['id']))

# get a list of unit ids that are directly associated with the given app policy.
apui_rs = ap.getChildList(child_class='AppPolicyUnitItem', fields=['unit_id'])
u_ids = map(lambda r:r[1], apui_rs)
info("%d units found", (len(u_ids),))
if (not u_ids): sys.exit(0)

# Filter out any non RPM units.
u_rs = spin.RPMUnit.getList(restrict={'unit_id':u_ids}, fields=['unit_id'])
u_ids = map(lambda r:r[1], u_rs)
info("%d RPM units found", (len(u_ids),))
if ( not u_ids): sys.exit(0)

# Get a list of folders for all these units.
fu_rs = spin._FolderUnit.getList(restrict={'unit_id':u_ids}, fields=['folder_id'])
f_ids = map(lambda r:r[1], fu_rs)
info("%d folders found (not uniq)", (len(f_ids),))

fps = {}
for f_id in f_ids:
  fp = get_folder_path(spin, f_id)
  fpc = fps.get(fp, 0)
  fpc = fpc + 1
  fps[fp] = fpc

info("\nThe repo.restrict.* CA for Software Policy %s(%s) should be set to the following:\n", (repr(ap['app_policy_name']), ap['id']))
for k in fps.keys():
  info(k)

out("\n")

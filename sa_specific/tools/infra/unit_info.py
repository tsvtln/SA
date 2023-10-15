import sys,pprint

from coglib import spinwrapper
spin=spinwrapper.SpinWrapper()

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

g_verbose = 0
for uid in sys.argv[1:]:
  if ( uid == '-v' ):
    g_verbose = 1
  else:
    u = spin.Unit.get(uid)
    if ( g_verbose ):
      sys.stdout.write("Software Package (Unit):\n")
      sys.stdout.write("%s\n" % pprint.pformat(u.data))
      sys.stdout.write("Folder(s) that contain this package:\n")
    else:
      sys.stdout.write("%s (%s)\n" % ( u['unit_desc'], u['unit_display_name']))
    fids = u.getChildIDList(child_class='Folder')
    for fid in fids:
      sys.stdout.write("  %d: %s\n\n" % (long(fid), get_folder_path(spin,fid)))

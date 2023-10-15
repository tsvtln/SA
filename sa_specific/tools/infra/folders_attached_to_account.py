import sys, string, types
from coglib import spinwrapper

spin = spinwrapper.SpinWrapper()

if ( len(sys.argv) != 2 ):
  sys.stdout.write("Usage: %s (<acct_name>|<acct_id>)\n")
  sys.exit(1)

an = sys.argv[1]

try:
  an = long(an)
except:
  pass

if ( type(an) == types.LongType ):
  aids = spin.Account.getIDList(restrict={"acct_id":an})
else:
  aids = spin.Account.getIDList(restrict={"acct_name":an}, ignore_case=1)
  if ( len(aids) == 0 ):
    aids = spin.Account.getIDList(restrict={"display_name":an}, ignore_case=1)

if ( len(aids) == 0 ):
  sys.stdout.write("%s: No such account found.\n" % an)
  sys.exit(1)

g_folder_node_info = {} # {<fid>: (folder_name, parent_folder_id)}
def _get_folder_node_info(spin, fid):
  if ( not g_folder_node_info.has_key(fid) ):
    fns = map(lambda i:i[1], spin.Folder.getList(restrict={"folder_id":fid}, fields=["folder_name"]))
    if ( len(fns) == 0 ):
      return None
    fn = fns[0]
    pfids = map(lambda i:i[1], spin._FolderFolderLink.getList(restrict={"folder_id":fid, "link_type_name":"HARD LINK"}, fields=["parent_folder_id"]))
    if ( len(pfids) > 0 ):
      pfid = pfids[0]
    else:
      pfid = None
    g_folder_node_info[fid] = (fn, pfid)
  return g_folder_node_info.get(fid, None)

def get_folder_path(spin, fid):
  cfid = fid
  path = []
  while cfid is not None:
    cnode = _get_folder_node_info(spin, cfid)
    cfid = cnode[1]
    path.insert(0, cnode[0])
  return "/" + string.join(path[1:], "/")

try:
  for aid in aids:
    acct = spin.Account.get(aid)

    fids = map(lambda i:i[1], spin._FolderAccount.getList(restrict={"acct_id":aid}, fields=["folder_id"]))

    sys.stdout.write("Folders associated with account \"%(display_name)s\" (%(acct_name)s/%(acct_id)d):\n" % acct.data)
    sys.stdout.flush()
    for fid in fids:
      sys.stdout.write("  %s\n" % get_folder_path(spin, fid))
      sys.stdout.flush()
    sys.stdout.write("\n")
except KeyboardInterrupt, e:
  sys.stdout.write("Interrupted\n")


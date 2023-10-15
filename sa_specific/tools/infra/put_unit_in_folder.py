import sys
from coglib import spinwrapper
from opsware_common import errors

spin = spinwrapper.SpinWrapper(url="http://127.0.0.1:1007")

if ( len(sys.argv) != 3 ):
  sys.stdout.write("Usage: %s <unit_id> <folder_id>\n" % sys.argv[0])
  sys.exit(1)

unit_id = long(sys.argv[1])
folder_id = long(sys.argv[2])

# Verify unit exists.
if ( len(spin.Unit.getIDList(restrict={'unit_id':unit_id})) == 0 ):
  sys.stdout.write("Unit %s not found.\n" % repr(unit_id))
  sys.exit(1)

# Verify folder exists.
if ( len(spin.Folder.getIDList(restrict={'folder_id':folder_id})) == 0 ):
  sys.stdout.write("Folder %s not found.\n" % repr(folder_id))
  sys.exit(1)

fus = spin._FolderUnit.getAll(restrict={'unit_id':unit_id})
if ( len(fus) == 0 ):
  # Create a new _FolderUnit record:
  sys.stdout.write("Moving folderless unit %d into folder %d.\n" % (unit_id, folder_id))
  spin._FolderUnit.new(folder_id=folder_id, unit_id=unit_id, link_type_name="HARD LINK")
else:
  fu = fus[0]
  old_folder_id = fu["folder_id"]
  if ( old_folder_id != folder_id ):
    sys.stdout.write("Moving unit %d from folder %d to folder %d.\n" % (unit_id, old_folder_id, folder_id))
    fu.delete()
    spin._FolderUnit.new(folder_id=folder_id, unit_id=unit_id, link_type_name="HARD LINK")
  else:
    sys.stdout.write("Unit %d already exists in folder %d.\n" % (unit_id, folder_id))


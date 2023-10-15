
import sys,traceback,string,os
from coglib import spinwrapper
spin = spinwrapper.SpinWrapper(url="http://127.0.0.1:1007")

def msg(s, args=None):
  if (args is not None):
    s = s % args
  sys.stdout.write(s)
  sys.stdout.flush()

if ( len(sys.argv) < 3 ):
  msg("Usage %s <dvc_id> <new_realm_id>\n", (sys.argv[0],))
  sys.exit(1)

dvc_id = sys.argv[1]
new_realm_id = long(sys.argv[2])

dvc = spin.Device.get(dvc_id)
new_realm = spin.Realm.get(new_realm_id)
new_realm_rc = new_realm.getRoleClass()
old_realm = dvc.getRealm()

msg("Attempting to move device %s(%d) from realm %s(%d) to realm %s(%d).\n", (repr(dvc['system_name']), dvc['dvc_id'], repr(old_realm['realm_name']), old_realm['realm_id'], repr(new_realm['realm_name']), new_realm['realm_id']))

msg("(1) Updating <realm_id> of devices record from %d to %d.\n", (old_realm['realm_id'], new_realm_id))
spin.Device.update(dvc_id, realm_id=new_realm_id)

old_realm_rc_recs = dvc.getChildList(child_class="RoleClass", restrict={'stack_id':16}, fields=['role_class_short_name'])
msg("(2) Moving device from realm role class %s to %s.\n", (string.join(map(lambda i:"%s(%d)" % (i[1],i[0]),old_realm_rc_recs),","), new_realm_rc['role_class_short_name']))
old_realm_rc_ids = map(lambda i:i[0], old_realm_rc_recs)
dvc.removeRoleClasses(child_ids=old_realm_rc_ids)
dvc.addRoleClasses(child_ids=[new_realm_rc['role_class_id']])

old_dc_rc_recs = dvc.getChildList(child_class='RoleClass', restrict={'stack_id':2}, fields=['role_class_short_name'])
old_dc_rc_ids = map(lambda i:i[0], old_dc_rc_recs)
new_dc = new_realm.getDataCenter()
new_dc_rc = new_dc.getRoleClass()
if ( new_dc_rc['role_class_id'] not in old_dc_rc_ids ):
  msg("(3) Moving device from datacenter role class %s to %s.\n", (string.join(map(lambda i:"%s(%d)" % (i[1],i[0]),old_dc_rc_recs),","), new_dc_rc['role_class_short_name']))
  dvc.removeRoleClasses(child_ids=old_dc_rc_ids)
  dvc.addRoleClasses(child_ids=[new_dc_rc['role_class_id']])

  dvc_role = dvc.getChildren(child_class='DeviceRole')[0]
  dvc_cust = dvc.getCustomer()
  new_cust_cloud_id = new_dc.getChildren(child_class="CustomerCloud",restrict={'acct_id':dvc_cust['acct_id']})[0]['cust_cld_id']
  msg("(4) Moving device from customer cloud %d to %d.\n", (dvc_role['cust_cld_id'], new_cust_cloud_id))
  dvc_role.update(cust_cld_id=new_cust_cloud_id)


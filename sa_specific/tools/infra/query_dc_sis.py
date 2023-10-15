import sys
from coglib import spinwrapper
from opsware_common.errors import OpswareError
spin = spinwrapper.SpinWrapper(url="http://localhost:1007")

dc_ids = []
try:
  dc_ids = map(lambda i:int(i), sys.argv[1:])
except:
  sys.stdout.write("Non integer argument\n")

if ( not dc_ids ):
  dc_ids = [spin.sys.getDCFromDB()['id']]

sys.stdout.write("dc_ids: %s\n" % dc_ids)

def expand_dcs(spin, dc_ids):
  all_dcs = spin.DataCenter.getAll()
  ret = []
  for dc in all_dcs:
    try:
      dc_core_dc_id = dc.getCoreDC()['id']
      if dc_core_dc_id in dc_ids:
        ret.append(dc['id'])
    except OpswareError, e:
      if e.error_name == "spin.notFoundInDatabase":
        # Asking for core DC of an unreachable DC -> DBNotFound
        # ignore these
        pass
      else:
        raise
  return ret

dc_ids = expand_dcs(spin, dc_ids)

sys.stdout.write("dc_ids (expanded): %s\n" % dc_ids)

dvc_ids = []
for dc_id in dc_ids:
  dvc_ids.extend(spin.DataCenter.getChildIDList(child_class='Device',id=dc_id))

sys.stdout.write("len(dvc_ids): %d\n" % len(dvc_ids))

si_ids = spin.ServiceInstance.getIDList(restrict={'dvc_id':dvc_ids, 'srvc_type':'COGBOT', 'status':'UP'})
sys.stdout.write("len(si_ids): %d\n" % len(si_ids))

if ( (len(sys.argv) > 1) and (sys.argv[1] == '-d') ):
  sys.stdout.write("%s\n" % repr(si_ids))

si_dvc_ids = spin.ServiceInstance.getList(restrict={'srvc_inst_id':si_ids}, fields=['dvc_id'])
sys.stdout.write("len(si_ids): %d\n" % len(si_ids))


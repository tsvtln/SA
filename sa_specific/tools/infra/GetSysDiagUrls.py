import sys
sys.path.append("/opt/opsware/pylibs")
sys.path.append("/lc/blackshadow")
from coglib import spinwrapper
spin = spinwrapper.SpinWrapper()
#dc = spin.DataCenter.get(id=1)
dcs = spin.DataCenter.getAll()
for dc in dcs:
  print("-" * 79)
  print("Datacenter: '%s' sys diag URLs:" % dc["display_name"])
  rc = dc.getRoleClass()
  acw = rc.getChildren(child_class="AppConfigWad")[0]
  print(acw.getDictValue(key="sysdiag_core"))
  print("-" * 79)

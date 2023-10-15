import sys, os
os.chdir("/opt/opsware/spin")
sys.path.append("/opt/opsware/pylibs")
sys.path.append("/opt/opsware/spin")
import spinconf, truthdb, spinobj
from tunnel import tunnelconf

spinconf.initLocal()
spinconf.loadConfFromTruth()

db=truthdb.DB()
truthdb.setDC(spinobj.DataCenter(db, db.getDCID()))
dc = spinobj.DataCenter(db, db.getDCID())

tunnelconf.updateLocalSpinConf()

from coglib import platform
mid = platform.Platform().getMid()
print mid

dvc=spinobj.Device(db,mid=mid)
rcs = dvc.getAttachedOpswareRCs( "spin" )
print rcs
for rc in rcs:
	print rc
	remote_conf = dvc.getConfigItems( rc )
	print remote_conf

#!/opt/opsware/bin/python2

import sys

sys.path.append("/opt/opsware/pylibs2")

from coglib import certmaster
from coglib import spinwrapper
from opsware_common.errors import OpswareError


ctx = certmaster.getContextByName("spin", "spin.srv", "opsware-ca.crt")
s = spinwrapper.SpinWrapper("https://spin:1004", ctx=ctx)

platform_list = [180075L, 190075L, 180076L, 190076L, 180077L, 190077L]

for plat in platform_list:
	p = s.Platform.get(id=plat)
	print "Platorm: '%s'" % p['platform_name']
	r = p.getRoleClass()
	id = r.getChildren(child_class="RoleClassSpindictorWad")[0]['id']
	print s.RoleClassSpindictorWad.getDictItems(id=id)
	print "="*50 + "\n"

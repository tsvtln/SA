import sys
sys.path.append("/lc/blackshadow")
from coglib import certmaster
ctx = certmaster.getContextByName('spin','spin.srv','opsware-ca.crt')
from coglib import spinwrapper
s=spinwrapper.SpinWrapper('https://spin:1004',ctx=ctx)
for id in [256150100,256040100,256050100,256070100,256130100,256180100,256080100]:
	try:
		vcv = s._VirtualColumnValue.get(id=id)
		vcv.delete()
	except: 
		pass

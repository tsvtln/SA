import sys

if "/lc/blackshadow" not in sys.path: sys.path.append("/lc/blackshadow")
sys.path.append("/cust/usr/blackshadow")

from coglib import spinwrapper

spin = spinwrapper.SpinWrapper()

for sWS_ID in sys.argv[1:]:
	ws = spin.WayScript.get(id=sWS_ID)

	from waybot.base import signor

	if ( signor.verify(ws) ):
		sys.stdout.write( "Way Script '%s' has a valid signature.\n" % ws['script_name'] )
	else:
		sys.stdout.write( "Way Script '%s' DOES NOT HAVE a valid signature.\n" % ws['script_name'] )
	        sys.stdout.write( "Expected signature is:\n\n%s" % signor.make_sig_by_type(ws.data,ws["obj_class"]) )


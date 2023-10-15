import sys

if "/lc/blackshadow" not in sys.path: sys.path.append("/lc/blackshadow")
sys.path.append("/cust/usr/blackshadow")

from coglib import spinwrapper
from coglib import certmaster

spin = spinwrapper.SpinWrapper(
	ctx = certmaster.getContextByName("spin", "spin.srv", ""),
)

for sWS_ID in sys.argv[1:]:
	ws = spin.WayScript.get(id=sWS_ID)

	from waybot.base import signor

	if ( signor.verify(ws) ):
		sys.stdout.write( "Way Script '%s' alright has a valid.\n" % ws['script_name'] )
	else:
		sys.stdout.write( "Way Script '%s' DOES NOT HAVE a valid signature.\n\n" % ws['script_name'] )
		sys.stdout.write( "Current signature is:\n\n%s\n\n" % ws['signature'] )
		sNewSig = signor.make_sig_by_type(ws.data,ws["obj_class"])
	        sys.stdout.write( "Expected signature is:\n\n%s\n\n" % sNewSig )

		sAnswer = "x"
		while ( not( sAnswer[0] in "ynYN" ) ):
			sys.stdout.write( "Would you like to resign this Way Script? [yn]" )
			sAnswer = sys.stdin.read(1)

		sys.stdout.write( "\n" )
		if ( len(sAnswer) > 0 and sAnswer[0] in "yY" ):
			ws.update( signature=sNewSig )
			sys.stdout.write( "Way Script '%s' resigned.\n" % ws['script_name'] )
		else:
			sys.stdout.write( "Way Script '%s' not modified.\n" % ws['script_name'] )

			


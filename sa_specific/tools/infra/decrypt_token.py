import sys

if ( len(sys.argv) == 1 ):
  sys.stdout.write( """Usage: %s [tok1 [tok2 [...]]]
""" % sys.argv[0] )
  sys.exit(1)

import pytwist

ts = pytwist.twistserver.TwistServer()

for tok in sys.argv[1:]:
  ptok = ts._makeCall("fido/ejb/session/UserFacade", "decryptToken", [tok])
  sys.stdout.write("\n%s\n" % ptok)

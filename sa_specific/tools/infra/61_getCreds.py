#!/opt/opsware/bin/python

import sys
sys.path.append("/opt/opsware/pylibs")
name="spin"
if ( len(sys.argv) > 1 ): name=sys.argv[1]
from shadowbot.LocalhostBasicAuthorizer import *
getCredentials(name)

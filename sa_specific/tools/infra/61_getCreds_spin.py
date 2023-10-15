#!/opt/opsware/bin/python

import sys
sys.path.append("/opt/opsware/pylibs")
from shadowbot.LocalhostBasicAuthorizer import *
getCredentials("spin")

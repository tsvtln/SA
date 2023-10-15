import sys
import os
import string
import getopt
import types
import time
import traceback

sys.path.append( "/lc/blackshadow" )
sys.path.append( "/cust/usr/blackshadow" )
sys.path.append( "/cust/usr/blackshadow/spin" )
sys.path.append( "/cust/ldapmodule" )
sys.path.append( "/opt/opsware/corelibs" )
sys.path.append( "/opt/opsware" )
sys.path.append( "/opt/opsware/spin" )
sys.path.append( "/opt/opsware/pylibs" )
sys.path.append( "/soft/blackshadow/spin" )# For development
if not os.environ.has_key( "SPIN_DIR" ):
    os.environ["SPIN_DIR"] = "/cust/usr/blackshadow/spin"
try:
    import truthdb
    import spinobj
    import truthtable
    import multimaster
    import spinconf
    from spinerror import *
except ImportError:
    sys.stderr.write( "Unable to import Data Access Engine libraries: %s, %s.  Is the Data Access Engine installed on this host?\n" % sys.exc_info()[0:2] )
    sys.exit( 1 )

debug = 0

db = truthdb.DB( "truth" )

# Some good stuff to initialize for generic mini-spin usage:
from init import findDC
findDC()

print( db )

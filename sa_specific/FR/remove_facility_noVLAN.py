# USE THIS SCRIPT WITH CAUTION!!!
# Removes a facility from Opsware SAS.
# Be sure to verify that the facility is no longer associated with any user groups or
# device groups and that there are no managed servers that reference the facility.
# ALSO: ensure that you replace the <dc_id> with the opsware ID for the facility
# to be removed before running this script.

# usage:  /opt/opsware/bin/python remove_facility.py

import sys
sys.append.path=("/opt/opsware/pylibs")
from coglib import spinwrapper
from external_spinmethods import *
spin = spinwrapper.SpinWrapper("http://localhost:1007")
datacenter_deleteEntire(spin,<dc_id>)

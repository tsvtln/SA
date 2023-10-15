#!/opt/opsware/bin/python

# fix up the PYTHONPATH, so no need to set that in environment first
import sys
import string
sys.path.append("/lc/blackshadow")
sys.path.append("/opt/opsware/pylibs")

# make sure we get just one argument, else complain and die
if len(sys.argv) == 2:
  oc = sys.argv[1]
else:
  print "Usage: %s <ObjectClass>" % sys.argv[0]
  sys.exit(1)

from coglib import spinwrapper
s = spinwrapper.SpinWrapper()
count=getattr(s,oc).getCount()
print count

#!/opt/opsware/bin/python

import sys
import string
sys.path.append("/lc/blackshadow")
sys.path.append("/opt/opsware/pylibs")
from coglib import spinwrapper
s = spinwrapper.SpinWrapper()
cc=s.sys.getClasses()
for c in cc:
  if c["canonical"] and c["replicated"] and not c["is_view"]:
    print c["name"]

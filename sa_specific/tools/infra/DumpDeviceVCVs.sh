#!/bin/sh

cat <<PYTHON_CODE | /opt/opsware/bin/python -c 'import sys,string;eval(compile(string.join(sys.stdin.readlines(),""),"DumpDeviceVCVs","exec"))' "$@"
import sys, pprint, time

if (len(sys.argv) == 1):
  sys.stdout.write("Usage: %s dvc_id1 [dvc_id2 [dvc_id3] ...]\n" % sys.argv[0] )
  sys.exit(1)

sys.path.append("/opt/opsware/pylibs")
from coglib import spinwrapper
spin = spinwrapper.SpinWrapper()

def replDates(o):
  for k in o.keys():
    if (str(type(o[k])) == "<type 'xmlrpcdateTime'>"):
      o[k] = time.asctime(o[k].date() + (0,0,0))
  return o

for dvc_id in sys.argv[1:]:
  sys.stdout.write( "Virtual Column Values for device %s:\n" % dvc_id )
  pprint.pprint(replDates(spin.Device.get(dvc_id).getVirtualColumnValues()))
  sys.stdout.write("\n")
PYTHON_CODE
#!/bin/sh

if ( [ \! "$1" ]; ) then {
  echo Usage: $0 "<way_script_version_id>"
  exit 1
} fi

cat << PYTHON_CODE | /opt/opsware/bin/python -c 'import sys,string;eval(compile(string.join(sys.stdin.readlines(),""),"touch_way_script_version","exec"));' "$@"
import sys
sys.path.append("/opt/opsware/pylibs")
from coglib import spinwrapper
spin = spinwrapper.SpinWrapper(url="http://localhost:1007")
wsv_id = sys.argv[1]
wsv = spin.WayScriptVersion.get(wsv_id)
print 'Touching way script version: %s of way script "%s"' % (str(wsv_id), spin.WayScript.get(wsv['way_script_id'])['script_name'])
sys.stdout.write( "%s " % wsv.update(signature=wsv['signature'] + ' ') )
sys.stdout.write( "%s\n" % wsv.update(signature=wsv['signature']) )
PYTHON_CODE

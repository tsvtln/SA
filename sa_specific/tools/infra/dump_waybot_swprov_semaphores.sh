#!/bin/sh

# Extract the basename of this script.
sName="`basename $0`"
sWayOpletFileName="${sName}_oplet.py"
sWayOpletFilePath="/opt/opsware/waybot/base/way/bidniss/${sWayOpletFileName}"

# lay down the clear container caches oplet into the waybot:
cat <<WAY_OPLET_CODE > "$sWayOpletFilePath"
self.send_response(200)
self.send_header("Content-type", "text/plain")
self.end_headers()

import sys,string
from waybot.base import script

doer_mod_keys = filter(lambda k:string.find(k,"opsware:swprov:doer") > -1, sys.modules.keys())

for doer_mod_key in doer_mod_keys:
  doer_mod = sys.modules[doer_mod_key]
  self.wfile.write("%s\n" % str(doer_mod_key))
  for sem_name in ("app_config_controller", "app_compliance_controller", "action_controller", "controller"):
    self.wfile.write("  %s: %s\n" % (sem_name, getattr(getattr(doer_mod, sem_name, None), "_Semaphore__value", None)))

WAY_OPLET_CODE

# if there was an error while writting out the waybot oplet, then bail out.
if ( [ $? -ne 0 ]; ) then {
  echo "$0: Failed to write out '$sWayOpletFilePath'."
  echo $0: Is this a 6.x+ waybot box?
  exit $?
} fi

# Invoke the python code to execute this oplet:
cat <<WAY_OPLET_INVOKER_BLOB | /opt/opsware/bin/python -c 'import sys,string; eval(compile(string.join(sys.stdin.readlines(),""),"way_oplet_invoker_blob","exec"));'
import sys;
sys.path.append("/opt/opsware/pylibs");
from coglib import certmaster,urlopen;
(url_obj,headers)=urlopen.httpReply(urlopen.httpUrlRequest("https://localhost:1018/way/bidniss/${sWayOpletFileName}",ctx=certmaster.getContextByName("spin","spin.srv","opsware-ca.crt"),connect_timeout=
60,read_timeout=60,write_timeout=60));
info_str=""
add_str = url_obj.read()
while add_str:
  info_str = info_str + add_str
  add_str = url_obj.read()
print info_str
WAY_OPLET_INVOKER_BLOB

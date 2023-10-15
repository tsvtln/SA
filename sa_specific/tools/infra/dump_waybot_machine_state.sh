#!/bin/sh


sShadowBotName="way"

# Extract the basename of this script.
sName="`basename $0`"
sSBOpletFileName="way/bidniss/${sName}_oplet.py"
sSBOpletFilePath="/opt/opsware/waybot/base/${sSBOpletFileName}"

# lay down the clear container caches oplet into the shadowbot:
cat <<SB_OPLET_CODE > "$sSBOpletFilePath"
self.send_response(200)
self.send_header("Content-type", "text/plain")
self.end_headers()

import string,time
from waybot.base import deliverance
from waybot.base import dc_cache

page = self.page

page.write( "Waybot machine state at %r:\n\n" % time.ctime(time.time()) )

def str_next(n):
  return "%r~%s" % (time.ctime(n[1]), n[0])

for (id, (next, history_list)) in deliverance.dumpMachineState().items():
  page.write("| %s | %s | %s|\n\n" % (id, str_next(next), string.join(map(str_next,history_list),", ")))

SB_OPLET_CODE

# if there was an error while writting out the shadowbot oplet, then bail out.
if ( [ $? -ne 0 ]; ) then {
  echo "$0: Failed to write out '$sSBOpletFilePath'."
  echo $0: Is this a 6.x+ $sShadowBotName box?
  exit $?
} fi

# Invoke the python code to execute this oplet:
cat <<SB_OPLET_INVOKER_BLOB | /opt/opsware/bin/python -c 'import sys,string; eval(compile(string.join(sys.stdin.readlines(),""),"SB_oplet_invoker_blob","exec"));'
import sys;
sys.path.append("/opt/opsware/pylibs");
from coglib import certmaster,urlopen;
(url_obj,headers)=urlopen.httpReply(urlopen.httpUrlRequest("https://localhost:1018/${sSBOpletFileName}",ctx=certmaster.getContextByName("spin","spin.srv","opsware-ca.crt"),connect_timeout=
60,read_timeout=60,write_timeout=60));
info_str=""
add_str = url_obj.read()
while add_str:
  info_str = info_str + add_str
  add_str = url_obj.read()
try:
  sys.stdout.write(info_str)
except IOError, e:
  pass
SB_OPLET_INVOKER_BLOB

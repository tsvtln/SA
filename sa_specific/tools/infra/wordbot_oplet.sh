#!/bin/sh

sShadowBotName="word"

# Extract the basename of this script.
sName="`basename $0`"
sSBOpletFileName="${sName}_oplet.py"
sSBOpletFilePath="/opt/opsware/mm_wordbot/${sSBOpletFileName}"

# lay down the clear container caches oplet into the shadowbot:
cat <<SB_OPLET_CODE > "$sSBOpletFilePath"
self.send_response(200)
self.send_header("Content-type", "text/plain")
self.end_headers()

import wordbot_common

import pprint

self.wfile.write("wordbot_common.getWordDirs():\n%s\n\n" % str(wordbot_common.getWordDirs()))

import wordfilehandlers
path='/packages/opsware/nt/5.2/opsware-agent-34c.0.0.93-win32-5.2.exe'
#path='/packages/opsware/nt/6.0-X64/opsware-agent-34c.0.0.115-win32-6.0-X64.exe'
filehandler_obj = wordfilehandlers.getFileHandler(wordbot_common.hive, path, None)
self.wfile.write('filehandler_obj.locateFile(\'%s\', 0):\n%s' % (path, str(filehandler_obj.locateFile(path, 0))))

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
(url_obj,headers)=urlopen.httpReply(urlopen.httpUrlRequest("https://localhost:1003/${sSBOpletFileName}",ctx=certmaster.getContextByName("spin","spin.srv","opsware-ca.crt"),connect_timeout=
60,read_timeout=60,write_timeout=60));
info_str=""
add_str = url_obj.read()
while add_str:
  info_str = info_str + add_str
  add_str = url_obj.read()
print info_str
SB_OPLET_INVOKER_BLOB

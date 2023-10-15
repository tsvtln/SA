#!/bin/sh

sShadowBotName="spin"

# Extract the basename of this script.
sName="`basename $0`"
sSBOpletFileName="${sName}_oplet.py"
sSBOpletFilePath="/opt/opsware/spin/sys/${sSBOpletFileName}"

# lay down the clear container caches oplet into the shadowbot:
cat <<SB_OPLET_CODE > "$sSBOpletFilePath"
self.send_response(200)
self.send_header("Content-type", "text/plain")
self.end_headers()

import string, time
from coglib import platform

page = self.page

page.write( "current thread stack frames:\n" )
page.write( "%s\n"  % time.ctime(time.time()) )
page.write( "(note: some threads may have been skipped)\n" )

def format_rows(rows, col_sep=' ', header=0):
  if ( not rows ): return ''
  num_cols = len(rows[0])
  col_maxes = range(num_cols)
  for cur_col in col_maxes:
    col_maxes[cur_col] = max(map(lambda r,cc=cur_col:len(str(r[cc])), rows))
  fmt = string.join(["%%-%ds"] * num_cols, col_sep) % tuple(col_maxes)
  res = string.join(map(lambda r,f=fmt:f % r, rows), '\n') + '\n'
  if ( header ):
    hline = '\n' + ('-' * (len(col_sep)*(num_cols-1) + reduce(lambda a,b:a+b,col_maxes))) + '\n'
    res = string.replace(res, '\n', hline, 1)
  return res

tframes = platform.Platform().getAllThreadStackFrames()

for frame_list in tframes:
  page.write( "\n" )
  rows = [("frame", "file", "line", "function")]
  for i in range(len(frame_list)):
    filename, lineno, name = frame_list[i]
    rows.append((str(len(frame_list)-i),filename,str(lineno),name))
  page.write(format_rows(rows, col_sep=' | ', header=1))

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
(url_obj,headers)=urlopen.httpReply(urlopen.httpUrlRequest("https://localhost:1004/sys/${sSBOpletFileName}",ctx=certmaster.getContextByName("spin","spin.srv","opsware-ca.crt"),connect_timeout=
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

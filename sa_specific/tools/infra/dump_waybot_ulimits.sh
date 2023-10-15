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


import resource,string

# poor man's table formatting:
def format_rows(rows, col_sep=' '):
  if ( not rows ): return ''
  num_cols = len(rows[0])
  col_maxes = range(num_cols)
  for cur_col in col_maxes:
    col_maxes[cur_col] = max(map(lambda r,cc=cur_col:len(str(r[cc])), rows))
  fmt = string.join(["%%-%ds"] * num_cols, col_sep) % tuple(col_maxes)
  return string.join(map(lambda r,f=fmt:f % r, rows), '\n') + '\n'

rl_keys = filter(lambda i:i[:7]=="RLIMIT_", resource.__dict__.keys())
rl_keys.sort()
rows = [("  _Name_", "_soft_", "_hard_")]
for rl_key in rl_keys:
  (rl_cur, rl_max) = resource.getrlimit(getattr(resource,rl_key))
  if ( rl_cur == -1 ): rl_cur = "unlimited"
  if ( rl_max == -1 ): rl_max = "unlimited"
  rows.append(("  " + rl_key, str(rl_cur), str(rl_max)))

self.wfile.write("$sShadowBotName internal rlimits (aka ulimits):\n\n")
self.wfile.write(format_rows(rows))

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

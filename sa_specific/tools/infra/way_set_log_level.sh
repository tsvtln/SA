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

import urllib,traceback,sys,string
from waybot.base import logger

def get_tb():
  return string.join(apply(traceback.format_exception, sys.exc_info()),'')

argv = map(urllib.unquote, args['args'])
#self.wfile.write("argv: %s\n" % (argv))

if ( len(argv) == 1 ):
  from opsware_common import logging
  log_names = logging.LogManager.getLoggerNames()
  self.wfile.write("%d active loggers:\n" % len(log_names))
  for log_name in log_names:
    log = logger.get(log_name)
    self.wfile.write("  %s: %s: %s\n" % (log_name, log.getLevel().getName(), map(lambda h:h.level.getName(),log.getHandlers())))
else:
  for log_cmd in argv[1:]:
    if ( '=' in log_cmd ):
      try:
        log_name, log_val = string.split(log_cmd,'=')
        log = logger.get(log_name)
        old_level_name = log.getLevel().getName()
        new_level = getattr(logger,log_val)
        log.setLevel(new_level)
        for handler in log.getHandlers():
          handler.setLevel(new_level)
        self.wfile.write("%s: %s changed: %s -> %s\n" % (log_cmd, log_name, old_level_name, new_level.getName()))
      except:
        self.wfile.write("Error parsing arg %s:\n%s\n" % (repr(log_cmd),get_tb()))
    else:
      self.wfile.write("%s: %s\n" % (log_cmd,logger.get(log_cmd).getLevel().getName()))

WAY_OPLET_CODE

# if there was an error while writting out the waybot oplet, then bail out.
if ( [ $? -ne 0 ]; ) then {
  echo "$0: Failed to write out '$sWayOpletFilePath'."
  echo $0: Is this a 6.x+ waybot box?
  exit $?
} fi

# Invoke the python code to execute this oplet:
cat <<WAY_OPLET_INVOKER_BLOB | /opt/opsware/bin/python -c 'import sys,string; eval(compile(string.join(sys.stdin.readlines(),""),"way_oplet_invoker_blob","exec"));' "$@"
import sys,urllib,string;
sys.path.append("/opt/opsware/pylibs");
from coglib import certmaster,urlopen;
sys.argv[0]="$0"
args=string.join(map(lambda a:"args=%s" % urllib.quote(a),sys.argv),'&')
if ( args != '' ): args = "?%s" % args
(url_obj,headers)=urlopen.httpReply(urlopen.httpUrlRequest("https://localhost:1018/way/bidniss/${sWayOpletFileName}%s" % args,ctx=certmaster.getContextByName("spin","spin.srv","opsware-ca.crt"),connect_timeout=
60,read_timeout=60,write_timeout=60));
info_str=""
add_str = url_obj.read()
while add_str:
  info_str = info_str + add_str
  add_str = url_obj.read()
print info_str
WAY_OPLET_INVOKER_BLOB

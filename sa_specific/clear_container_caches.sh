#!/bin/sh

# lay down the clear container caches oplet into the waybot:
cat <<CLEAR_CONTAINER_CACHES_OPLET > /opt/opsware/waybot/base/way/bidniss/clear_container_caches_oplet.py
self.send_response(200)
self.send_header("Content-type", "text/plain")
self.end_headers()

import libHomeDepot;

# Container objects whose cache we want cleared:
acs = ['Company', 'Division', 'BuyingOffice', 'Market', 'Store']

self.wfile.write("Size of Content Caches:\n")

for c in acs:
  self.wfile.write("  len(libHomeDepot.%s._DICT: %s\n" % (c, len(getattr(libHomeDepot, c)._DICT)))

self.wfile.write("\nClearing all caches...\n\nSize of Content Caches:\n")

for c in acs:
  getattr(libHomeDepot, c)._DICT = {}

for c in acs:
  self.wfile.write("  len(libHomeDepot.%s._DICT: %s\n" % (c, len(getattr(libHomeDepot, c)._DICT)))
CLEAR_CONTAINER_CACHES_OPLET

# if there was an error while writting out the waybot oplet, then bail out.
if ( [ $? -ne 0 ]; ) then {
  echo $0: Failed to write out '/opt/opsware/waybot/base/way/bidniss/clear_container_caches_oplet.py'.
  echo $0: Is this a 6.x+ waybot box?
  exit $?
} fi

# Invoke the python code to execute this oplet:
cat <<CLEAR_CONTAINER_CACHES_BLOB | /opt/opsware/bin/python -c 'import sys,string; eval(compile(string.join(sys.stdin.readlines(),""),"clear_container_caches_blob","exec"));'
import sys;
sys.path.append("/opt/opsware/pylibs");
from coglib import certmaster,urlopen;
(url_obj,headers)=urlopen.httpReply(urlopen.httpUrlRequest("https://localhost:1018/way/bidniss/clear_container_caches_oplet.py",ctx=certmaster.getContextByName("spin","spin.srv","opsware-ca.crt"),connect_timeout=
60,read_timeout=60,write_timeout=60));
info_str=""
add_str = url_obj.read()
while add_str:
  info_str = info_str + add_str
  add_str = url_obj.read()
print info_str
CLEAR_CONTAINER_CACHES_BLOB

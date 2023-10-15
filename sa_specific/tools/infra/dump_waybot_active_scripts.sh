#!/bin/sh

# Extract the basename of this script.
sName="`basename $0`"
sWayOpletFileName="${sName}_oplet.py"
sWayOpletFilePath="/opt/opsware/waybot/base/way/bidniss/${sWayOpletFileName}"

# lay down the clear container caches oplet into the waybot:
cat <<WAY_OPLET_CODE > "$sWayOpletFilePath"
def dictify(o,seen_oids=None):
  if (type(o) == types.DictType):
    m = {}
    for key in o.keys():
      m[key] = dictify(o[key], seen_oids)
    return m
  elif ( (type(o) == types.TupleType) or (type(o) == types.ListType) ):
    l = []
    for i in o:
      l.append(dictify(i, seen_oids))
    if ( type(o) == types.TupleType ):
      return tuple(l)
    else:
      return l
  elif ( (type(o) == types.InstanceType) and hasattr(o,"__dict__") ):
    oid = id(o)
    if (seen_oids == None): seen_oids = []
    if ( oid in seen_oids ): return "Already Seen %s %s(%s)" % (getattr(o,"__class__","N/A"),type(o),oid)
    seen_oids.append(oid)
    m = o.__dict__.copy()
    m['__id'] = oid
    return dictify(m, seen_oids)
  elif ( type(o) in (types.IntType, types.LongType, types.StringType) ):
    return o
  else: return str(o)

def dictify2(o,max_depth=5):
  max_depth = max_depth - 1
  if (type(o) == types.DictType):
    m = {}
    for key in o.keys():
      m[key] = dictify(o[key],max_depth)
    return m
  elif (hasattr(o,"__dict__")):
    m = o.__dict__.copy()
    if ( max_depth <= 0 ):
      return m
    else:
      return dictify(m, max_depth)
  else: return o

self.send_response(200)
self.send_header("Content-type", "text/plain")
self.end_headers()

import types,cPickle,base64,zlib
from waybot.base import script

self.wfile.write("Active Scripts:\n")

active_scripts = script.active_dict.copy()
for key in active_scripts.keys():
  self.wfile.write("%s\n%s\n\n" % (key, base64.encodestring(zlib.compress(cPickle.dumps(dictify(active_scripts[key]), 1), 9))))
#  self.wfile.write("%s\n%s\n\n" % (key, dictify(active_scripts[key])))

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

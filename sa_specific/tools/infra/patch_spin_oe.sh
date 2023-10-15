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

from pyiconv import iconv

new_toUTF8_src = """
def toUTF8(legacy_obj,from_encoding_str):
  '''convert all strings in a python object from legacy encoding into a UTF-8 strings in place.'''
  from opsware_common import logging
  logging.Logger.log(logging.Logger.level.INFO, "DEBUG: iconv.toUTF8: from_encoding_str: %s, legacy_obj: %s%s" % (repr(from_encoding_str), repr(legacy_obj), chr(10)))
#  import sys
#  if ( legacy_obj == [] ): sys.exit()
  iconv_obj=_iconv.open(from_encoding_str,'UTF-8')

  return iconv_obj.convert(legacy_obj)
"""
if ( not hasattr(iconv,"orig_toUTF8") ):
  iconv.orig_toUTF8 = iconv.toUTF8
exec compile(new_toUTF8_src, '', 'exec') in iconv.__dict__
self.wfile.write("patched: %s, %s\n" % (iconv.toUTF8, iconv.orig_toUTF8))

new_fromUTF8_src = """
def fromUTF8(utf8_obj,to_encoding_str):
  '''convert all UTF-8 strings in a python object to strings in a legacy encoded in place.'''
  from opsware_common import logging
  logging.Logger.log(logging.Logger.level.INFO, "DEBUG: iconv.fromUTF8: to_encoding_str: %s, utf8_obj: %s%s" % (repr(to_encoding_str), repr(utf8_obj), chr(10)))
  iconv_obj=_iconv.open('UTF-8',to_encoding_str)

  return iconv_obj.convert(utf8_obj)
"""
if ( not hasattr(iconv,"orig_fromUTF8") ):
  iconv.orig_fromUTF8 = iconv.fromUTF8
exec compile(new_fromUTF8_src, '', 'exec') in iconv.__dict__
self.wfile.write("patched: %s, %s\n" % (iconv.fromUTF8, iconv.orig_fromUTF8))

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
print info_str
SB_OPLET_INVOKER_BLOB

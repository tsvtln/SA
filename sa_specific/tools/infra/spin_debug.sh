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

import urllib,sys,string,traceback

def format_rows(rows, col_sep=' '):
  if ( not rows ): return ''
  num_cols = len(rows[0])
  col_maxes = range(num_cols)
  for cur_col in col_maxes:
    col_maxes[cur_col] = max(map(lambda r,cc=cur_col:len(str(r[cc])), rows))
  fmt = string.join(["%%-%ds"] * num_cols, col_sep) % tuple(col_maxes)
  return string.join(map(lambda r,f=fmt:f % r, rows), '\n') + '\n'

def append_uniq(lst,item):
  if ( item not in lst ): lst.append(item)

def usage():
  self.wfile.write("""
Utility for listing and setting debug and profile flags for the spin.

Usage: %s [<mod_name>[.(debug|profile)=(1|0)] ...]

  If no arguments are given, then it will list the debug and profile flag for 
  all internal modules

  If a module name is supplied, then only the settings for that module will be
  printed.

  The debug or profile flag can be set by appending ".(debug|profile)=(1|0)" to
  the name of the module.

Examples:

  List all module debug and profile flags:

    # %s

  List debug and profile flags for only the truthcon module:

    # %s truthcon

  Setting the truthcon.debug flag:

    # %s truthcon.debug=1

  Resetting the truthcon.debug flag:

    # %s truthcon.debug=0
""" % ((argv[0],) * 5))

def main(argv):
  mods_to_list = []

  for mod_spec in argv[1:]:
    try:
      if ( mod_spec in ("-h", "--help", "/?") ):
        usage()
        return
      else:
        if ( string.find(mod_spec, "=") == -1 ):
          append_uniq(mods_to_list, mod_spec)
          continue
        s_path, val = string.split(mod_spec,"=")

        last_period_idx = string.rfind(s_path, ".")
        if ( last_period_idx == -1 ):
          self.wfile.write("WARN: %s: missing \".\" character.\n" % mod_spec)
          continue
        mod_name = s_path[:last_period_idx]
        fld_name = s_path[last_period_idx+1:]
        if ( fld_name not in ("debug","profile") ):
          self.wfile.write("WARN: %s: field must be either \"debug\" or \"profile\"\n" % mod_spec)
          continue

        val = int(val)

        if ( not sys.modules.has_key(mod_name) ):
          self.wfile.write("WARN: %s: module does not exist\n" % mod_spec)
          continue
        mod = sys.modules[mod_name]

        if ( (not hasattr(mod,fld_name)) or (getattr(mod,fld_name) not in (0,1)) ):
          self.wfile.write("WARN: %s: %s module does not support the %s setting.\n" % (mod_spec, repr(mod_name), repr(fld_name)))
          continue
        if ( val not in (0,1) ):
          self.wfile.write("WARN: %s: value must be \"0\" or \"1\"\n" % mod_spec)
          continue
        setattr(mod, fld_name, val)
        if ( mod_name == "spinrpc" ):
          setattr(hive, "rpc_%s" % fld_name, val)
        append_uniq(mods_to_list, mod_name)
    except:
      self.wfile.write("%s: Unexpected exception:\n%s" % (mod_spec, string.join(apply(traceback.format_exception, sys.exc_info()), "")))

  def get_row(mod):
    row = [mod_name, "n/a", "n/a"]
    if ( hasattr(mod, "debug") and (mod.debug in (0,1)) ):
      row[1] = mod.debug
    if ( hasattr(mod, "profile") and (mod.debug in (0,1)) ):
      row[2] = mod.profile
    if ( (row[1] in (0,1)) or (row[2] in (0,1)) ):
      return tuple(row)

  rows = [("Module", "Debug", "Profile"),("","","")]
  if ( len(mods_to_list) > 0 ):
    for mod_name in mods_to_list:
      if ( sys.modules.has_key(mod_name) ):
        mod = sys.modules[mod_name]
        row = get_row(mod)
        if ( row is not None ):
          rows.append(row)
        else:
          self.wfile.write("WARN: %s module does not support debug or profile setting.\n" % repr(mod_name))
      else:
        self.wfile.write("WARN: %s: module not found.\n" % mod_name)
  elif ( len(argv) == 1 ):
    for (mod_name,mod) in sys.modules.items():
      row = get_row(mod)
      if ( row is not None ):
        rows.append(row)
  if ( len(rows) > 2 ):
#    self.wfile.write(repr(rows))
    self.wfile.write("\n" + format_rows(rows, " | "))

argv = map(urllib.unquote, args['args'])
#self.wfile.write("argv: %s\n" % (argv))
main(argv)

SB_OPLET_CODE

# if there was an error while writting out the shadowbot oplet, then bail out.
if ( [ $? -ne 0 ]; ) then {
  echo "$0: Failed to write out '$sSBOpletFilePath'."
  echo $0: Is this a 6.x+ $sShadowBotName box?
  exit $?
} fi

# Invoke the python code to execute this oplet:
cat <<SB_OPLET_INVOKER_BLOB | /opt/opsware/bin/python -c 'import sys,string; eval(compile(string.join(sys.stdin.readlines(),""),"SB_oplet_invoker_blob","exec"));' $@
import sys,urllib;
sys.path.append("/opt/opsware/pylibs");
from coglib import certmaster,urlopen;
sys.argv[0]="$0"
args=string.join(map(lambda a:"args=%s" % urllib.quote(a),sys.argv),'&')
if ( args != '' ): args = "?%s" % args
(url_obj,headers)=urlopen.httpReply(urlopen.httpUrlRequest("https://localhost:1004/sys/${sSBOpletFileName}%s" % args,ctx=certmaster.getContextByName("spin","spin.srv","opsware-ca.crt"),connect_timeout=60,read_timeout=60,write_timeout=60));
info_str=""
add_str = url_obj.read()
while add_str:
  info_str = info_str + add_str
  add_str = url_obj.read()
print info_str
SB_OPLET_INVOKER_BLOB

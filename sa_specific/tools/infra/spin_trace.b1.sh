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

import urllib,string,traceback,types,sys,imp,time,threading

# Dynamically create our trace module.
_trace = sys.modules.get("_trace", None)
if ( _trace == None ):
  _trace = imp.new_module("_trace")
  sys.modules["_trace"] = _trace
  _trace = sys.modules["_trace"]
  _trace.out_lock = threading.Lock()
  _trace.out_file = None
  _trace.time = time
  _trace.sys = sys
  _trace.string = string,
  _trace.traceback = traceback
  exec """def out(s):
  while ( (s != "") and (s[-1] == "\\\\n") ): s = s[:-1]
  s = "%s: %s\\\\n" % (time.ctime(time.time()), s)
  if ( out_file != None ):
    out_lock.acquire()
    try:
      out_file.write(s)
      out_file.flush()
    except:
      try:
        sys.stderr.write("TRACE: EXCEPTION:\\\\n%s\\\\nOrigonal Message: %s" % (string.join(apply(traceback.format_exception, sys.exc_info()), ""),s))
        sys.stderr.flush()
      except:
        pass
    out_lock.release()
  else:
    try:
      sys.stderr.write("TRACE: %s" % s)
      sys.stderr.flush()
    except:
      pass
""" in _trace.__dict__

argv = map(urllib.unquote, args['args'])

def get_exc_bt():
  return string.join(apply(traceback.format_exception, sys.exc_info()), "")

def get_exc():
  return sys.exc_info()[1]

def usage():
  self.wfile.write("""Usage: %s [-d] [-o <outfile>] <function|method>

  -d
    Enable debug message

  -o <outfile>
    Send trace message to the file specified by <outfile>.  Default is 
    "/tmp/%s.txt"
-------------------------------------------------------------------------------

""" % (argv[0], argv[0]))

args = argv[1:]

b_debug = 0
while len(args) > 0:
  if ( args[0] == "-d" ):
    b_debug = 1
    del args[0]
  elif ( args[0] == "-o" ):
    try:
      if ( args[1] == "<stderr>" ):
        _trace.out_lock.acquire()
        try:
          _trace.out_file = None
        except:
          pass
        _trace.out_lock.release()
      else:
        if ( args[1][0] != "/" ):
          self.wfile.write("%s: Relative file names not allowed.\n")
        else:
          _trace.out_file = open(args[1], "a")
    except:
      self.wfile.write("%s: Error while opening file for append:\n%s" % (args[1], get_exc_bt()))
    del args[0]
    del args[0]
  else:
    break

s_out_filename = "<stderr>"
try:
  s_out_filename = repr(_trace.out_file.name)
except:
  pass
self.wfile.write("Tracing to %s\n" % s_out_filename)

if ( len(argv) < 2 ):
  usage()

s_orig_prefix = "__orig_trace_"

s_trace_src = """def %s*args, **kwargs):
  import sys,string,traceback,threading
  tk = "__trace_%%s" %% threading._get_ident()
  _trace = sys.modules["_trace"]
  if ( not hasattr(_trace, tk) ):
    setattr(_trace, tk, 1)
    try:
      bt = "['sys._getframe()' not available on this python interpreter]"
      if ( sys._getframe ): bt = string.join(traceback.format_stack(sys._getframe()))
      _trace.out("%s:\\\\n  args: %%s\\\\n  kwargs: %%s\\\\n  stack:%%s\\\\n" %% (repr(args), repr(kwargs), bt))
    except:
      try:
        sys.stderr.write("TRACE: EXCEPTION:\\\\n %%s\\\\n" %% string.join(apply(traceback.format_exception, sys.exc_info()), ""))
        sys.stderr.flush()
      except:
        # well we tried.
        pass
    delattr(sys.modules["_trace"], tk)
  return apply(%s, args, kwargs)
"""

for s_fq_thing in args:
  parts = string.split(s_fq_thing,".")
  if ( len(parts) < 2 ):
    self.wfile.write("ERROR: %s: is not a fully qualified function or method.\n" % s_fq_thing)
    continue
  s_mod = parts[0]
  mod = sys.modules.get(s_mod, None)
  if ( mod == None ):
    self.wfile.write("ERROR: %s: Module not found\n" % s_mod)
    continue
  owner = mod
  for s_sub_owner in parts[1:-1]:
    owner = getattr(owner, s_sub_owner)
    if ( owner == None ):
      self.wfile.write("ERROR: %s: Attribute not found\n" % s_sub_owner)
      break
  if ( owner == None ):
    continue
  if ( type(owner.__dict__) != types.DictType ):
    self.wfile.write("ERROR: %s: owner is immutable, metthod can't be traced.\n" % s_fq_thing)
    continue

  s_thing = parts[-1]
  thing = getattr(owner,s_thing,None);

  if (thing == None):
    self.wfile.write("ERROR: %s: Attribute not found\n" % s_thing)
    continue

  s_orig_thing = "%s%s" % (s_orig_prefix, s_thing)
  orig_thing = getattr(owner, s_orig_thing, None)
  if (orig_thing != None):
    setattr(owner, s_thing, orig_thing)
    delattr(owner, s_orig_thing)
    self.wfile.write("%s: untraced\n" % s_fq_thing)
  else:
    if (type(thing) == types.FunctionType):
      setattr(owner, s_orig_thing, thing)
      s_trace_func = s_trace_src % ("%s(" % s_thing, s_fq_thing, s_orig_thing)
      exec s_trace_func in owner.__dict__
      self.wfile.write("%s: traced\n" % s_fq_thing)
    elif (type(thing) == types.MethodType):
      setattr(owner, s_orig_thing, thing)
      s_trace_meth = s_trace_src % ("%s(self, " % s_thing, s_fq_thing, "self.%s" % s_orig_thing)
#      self.wfile.write("DEBUG: owner: %s, type(owner.__dict__): %s, s_trace_meth: |%s|\n" % (str(owner), type(owner.__dict__), repr(s_trace_meth)))
      exec s_trace_meth in owner.__dict__
      self.wfile.write("%s: traced\n" % s_fq_thing)
    else:
      self.wfile.write("ERROR: %s: is not a function or method, it is a: %s\n", (s_thing, str(type(thing))))
      continue

SB_OPLET_CODE

# if there was an error while writting out the shadowbot oplet, then bail out.
if ( [ $? -ne 0 ]; ) then {
  echo "$0: Failed to write out '$sSBOpletFilePath'."
  echo $0: Is this a 6.x+ $sShadowBotName box?
  exit $?
} fi

# Invoke the python code to execute this oplet:
cat <<SB_OPLET_INVOKER_BLOB | /opt/opsware/bin/python -c 'import sys,string; eval(compile(string.join(sys.stdin.readlines(),""),"SB_oplet_invoker_blob","exec"));' "$@"
import sys,string,urllib;
sys.path.append("/opt/opsware/pylibs");
from coglib import certmaster,urlopen;
sys.argv[0] = "$0"
args=string.join(map(lambda a:"args=%s" % urllib.quote(a),sys.argv),'&')
if ( args != '' ): args = "?%s" % args
(url_obj,headers)=urlopen.httpReply(urlopen.httpUrlRequest("https://localhost:1004/sys/${sSBOpletFileName}%s" % args,ctx=certmaster.getContextByName("spin","spin.srv","opsware-ca.crt"),connect_timeout=
60,read_timeout=60,write_timeout=60));
info_str=""
add_str = url_obj.read()
while add_str:
  info_str = info_str + add_str
  add_str = url_obj.read()
print info_str
SB_OPLET_INVOKER_BLOB

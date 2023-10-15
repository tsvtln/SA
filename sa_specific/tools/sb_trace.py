
import urllib,string,traceback,sys,os

from coglib import urlopen,certmaster

# <sb_name>: (<base_url>, <base_doc>
g_map_known_shadowbots = {
    "spin":  ("https://127.0.0.1:1004/sys/",         "/opt/opsware/spin/sys/"),
    "way":   ("https://127.0.0.1:1018/way/bidniss/", "/opt/opsware/waybot/base/way/bidniss/"),
    "word":  ("https://127.0.0.1:1003/",             "/opt/opsware/mm_wordbot/"),
    "agent": ("https://127.0.0.1:1002/",             "/opt/opsware/agent/pylibs/cogbot/base/")
  }

g_s_oplet_src = """self.send_response(200)
self.send_header("Content-type", "text/plain")
self.end_headers()

import urllib,string,traceback,types,sys,imp,time,threading

# Dynamically create our trace module.
_sb_trace = sys.modules.get("_sb_trace", None)
if ( _sb_trace == None ):
  _sb_trace = imp.new_module("_sb_trace")
  # There is a chance for a race around adding this module to sys.modules.
  # But I don't see an elegant way to avoid that. -dw
  sys.modules["_sb_trace"] = _sb_trace
  _sb_trace = sys.modules["_sb_trace"]
  _sb_trace.out_lock = threading.Lock()
  _sb_trace.out_file = None
  _sb_trace.lock = threading.Lock()
#  _sb_trace.traces = {}  # {<s_fq_thing>: {"owner":<owner>, "thing":<thing>, "s_thing":<s_thing>, "co_after":<co_after>, "co_before":<co_before>)}
  _sb_trace.traces = {}  # {id(<Trace>}: <Trace>]
  _sb_trace.time = time
  _sb_trace.sys = sys
  _sb_trace.string = string,
  _sb_trace.traceback = traceback
  exec \"""def out(s):
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
\""" in _sb_trace.__dict__

argv = map(urllib.unquote, args['args'])

def get_exc_bt():
  return string.join(apply(traceback.format_exception, sys.exc_info()), "")

def get_exc():
  return sys.exc_info()[1]

def usage():
  self.wfile.write(\"""
Shadowbot Trace

Utility allows for tracing arbitrary functions and methods inside of a live 
running shadowbot without having to restart it.

Usages: %s [-sb <name>] [-o file] [-B <code>] [-A <code>] [-e <owner> <thing>]
           <function|method|id> ...

        %s -u <function|method|id>

        %s -ls

  [-sb <name>]
    The shadowbot to trace.  Currently supported shadowbots are:

      spin, way, word, agent

  [-o <outfile>]
    Send trace message to the file specified by <outfile>.  Default is 
    "/tmp/<name>.txt"

  [-B <code>]
    Code to execute before the origonal method or function is called.

  [-A <code>]
    Code to execute after the origonal method or function is called.

  [-e <owner> <attr>]
    This form allows for articulating functions or methods using
    python's internal eval() function, by specifying an <owner> expression
    and a <attr> attribute experssion.  The <attr> will be looked up based
    upon the type of <owner>.  This form is more complex to specify than the
    dotted notation of the <function|method|id>, but it is much more flexible.

  <function|method|id>
    The fully qualified function or method to be traced.  Or the object id of
    a method or function already being traced.  If an <id> is given then the
    before or after code of the trace can me modified.

  -u
    Untrace the given function or method.

  <id>
    The object ID of a method or function already being traced.

  -ls
    List any currently traced functions or methods.

Known Limitations:

  o If a traced function or method gets copied or moved, the right thing does 
    not happen.  :)  (Live by the mutability, die by the mutibility.)

\""" % ((argv[0],)*3))

def list_sb_traces(_sb_trace):
  _sb_trace.lock.acquire()
  try:
    if ( len(_sb_trace.traces) > 0 ):
      self.wfile.write("Current traces:\\n")
      trace_items = _sb_trace.traces.items()
      trace_items.sort(lambda a,b:cmp(a[0],b[0]))
      for trace_item in trace_items:
        self.wfile.write("  %d: %s\\n" % (trace_item[0], trace_item[1].s_fq_thing))
    else:
      self.wfile.write("No current traces.\\n")
  except:
    _sb_trace.lock.release()
    raise
  else:
    _sb_trace.lock.release()

args = argv[1:]

b_debug = 0
b_untrace = 0
s_sb_name = None
co_after = None

# Default before code.
co_before = compile(\"""import sys,string,traceback
bt = "***'sys._getframe()' not available on this python interpreter***"
if ( hasattr(sys,"_getframe") ): bt = string.join(traceback.format_stack(sys._getframe()))
_sb_trace.out("%s:\\\\n  args: %s\\\\n  kwargs: %s\\\\n  stack: %s\\\\n" % (trace.s_fq_thing, repr(args), repr(kwargs), bt))
\""", "<_sb_trace_co-B>", "exec")

while len(args) > 0:
  if ( args[0] in ("-h", "--help", "/?") ):
    del args[0]
    usage()
  elif ( args[0] == "-d" ):
    b_debug = 1
    del args[0]
  elif ( args[0] == "-u" ):
    b_untrace = 1
    del args[0]
  elif ( args[0] in ("-A", "-B") ):
    ct = args[0]
    del args[0]
    if ( len(args) > 0 ):
      try:
        co = compile(args[0], "<_sb_trace_co%s>" % ct, "exec")
      except:
        self.wfile.write("%s: Error while compiling code:\\n%s" % (ct, get_exc_bt()))
      else:
        del args[0]
        if ( ct == "-A" ):
          co_after = co
        else:
          co_before = co
    else:
      self.wfile.write("%s: No code given\\n" % ct)
  elif ( args[0] == "-sb" ):
    del args[0]
    if ( len(args) > 0 ):
      s_sb_name = args[0]
      del args[0]
    else:
      self.wfile.write("%s: No shadowbot name given.\\n" % "-sb")
  elif ( args[0] == "-o" ):
    try:
      if ( args[1] == "<stderr>" ):
        _sb_trace.out_lock.acquire()
        try:
          _sb_trace.out_file = None
          self.wfile.write("Tracing to <stderr>\\n")
        except:
          pass
        _sb_trace.out_lock.release()
      else:
        if ( args[1][0] != "/" ):
          self.wfile.write("%s: Relative file names not allowed.\\n")
        else:
          _sb_trace.out_file = open(args[1], "a")
          self.wfile.write("Tracing to %s\\n" % repr(args[1]))
    except:
      self.wfile.write("%s: Error while opening file for append:\\n%s" % (args[1], get_exc_bt()))
    del args[0]
    del args[0]
  elif ( args[0] == "-ls" ):
    del args[0]
    list_sb_traces(_sb_trace)
  else:
    break

if ( len(argv) < 2 ):
  usage()

s_orig_prefix = "__orig_sb_trace_"

s_sb_trace_src = \"""def %s(*args, **kwargs):
  try:
    import sys,string,traceback
    _sb_trace = sys.modules["_sb_trace"]
    trace = _sb_trace.traces[%s]
    if trace.co_before: eval(trace.co_before)
  except:
    try:
      s_err_msg = "TRACE(before): EXCEPTION:\\\\n %%s\\\\n"
      s_err_msg = s_err_msg %% string.join(apply(traceback.format_exception, sys.exc_info()), "")
      _sb_trace.out(s_err_msg)
    except:
      try:
        sys.stderr.write(s_err_msg)
        sys.stderr.flush()
      except:
        # well we tried.
        pass
  ret = apply(trace.thing, args, kwargs)
  try:
    if trace.co_after: eval(trace.co_after)
  except:
    try:
      s_err_msg = "TRACE(after): EXCEPTION:\\\\n %%s\\\\n"
      s_err_msg = s_err_msg %% string.join(apply(traceback.format_exception, sys.exc_info()), "")
      _sb_trace.out(s_err_msg)
    except:
      try:
        sys.stderr.write(s_err_msg)
        sys.stderr.flush()
      except:
        # well we tried.
        pass
  return ret
\"""

class Trace:
  def __init__(self, owner, thing, thing_name, s_fq_thing, co_after = None, co_before = None):
    (self.owner, self.thing, self.thing_name, self.s_fq_thing, self.co_after, self.co_before) = (
      owner, thing, thing_name, s_fq_thing, co_after, co_before)

    # trace id.  This is the id() of the function or method created for this
    # trace when it is activated.  This can be used to help identify this
    # trace record in the future.
    self.id = None

  def __str__(self):
    return "%d: %s" % (id(self), self.s_fq_thing)

def lookup_trace(owner, thing_name):
  trace = None
  traces = filter(lambda t,o=owner,tn=thing_name:(t.owner is o) and (t.thing_name == tn), _sb_trace.traces.values())
  if ( len(traces) > 0 ): trace = traces[0]
  if ( len(traces) > 1 ):
    self.wfile.write("WARNING: There appear to be multiple traces for the same thing:\\n%s\\n" % string.join(map(lambda i:str(i), traces), "\\n"))
  return trace

def resolve_dotted(s_fq_thing):
  \"""Resolves a Trace instance based on the fully qualified thing description,
<s_fq_thing>, given in dotted notation.  If a trace already exists for this
thing, then it will be returned.  If no callable is found based on the given
name, then <None> is returned.
\"""
  trace = None
  try:
    trace = _sb_trace.traces[int(s_fq_thing)]
  except:
    pass
  if ( trace is not None ): return trace
  parts = string.split(s_fq_thing, ".")
  if ( len(parts) < 2 ):
    self.wfile.write("ERROR: %s: is not a fully qualified function or method.\\n" % s_fq_thing)
    return None
  s_mod = parts[0]
  mod = sys.modules.get(s_mod, None)
  if ( mod == None ):
    self.wfile.write("ERROR: %s: Module not found\\n" % repr(s_mod))
    return None
  owner = mod
  for s_sub_owner in parts[1:-1]:
    owner = getattr(owner, s_sub_owner, None)
    if ( owner is None ):
      self.wfile.write("ERROR: %s: Attribute not found\\n" % s_sub_owner)
      break
  if ( owner is None ):
    return None
  if ( type(owner.__dict__) != types.DictType ):
    self.wfile.write("ERROR: %s: owner is immutable, method can't be traced.\\n" % s_fq_thing)
    return None
  thing_name = parts[-1]
  thing = getattr(owner, thing_name, None)
  if (thing == None):
    self.wfile.write("ERROR: %s: Attribute not found\\n" % thing_name)
    return None

  # See if this thing _is_ a trace.
  trace = lookup_trace(owner, thing_name)

  # If no existing trace found,
  if (trace is None):
    # Create a new trace record.
    trace = Trace(owner, thing, thing_name, s_fq_thing)

  return trace

def resolve_exp_pair(s_owner_expr, s_attr_expr):
  \"""returns: Trace instance if resolution successful, otherwise, None
\"""
  # Construct a fq thing string.
  s_fq_thing = repr((s_owner_expr, s_attr_expr))

  # Try to eval the owner expression.
  try:
    owner = eval(s_owner_expr)
  except:
    self.wfile.write("ERROR: %s: Failed to eval owner expression due to:\\n%s\\n" % (repr(s_owner_expr), get_exc_bt()))
    return None

  # Try to eval the attribute expression.
  try:
    thing_name = eval(s_attr_expr)
  except:
    self.wfile.write("ERROR: %s: Failed to eval attribute expression due to:\\n%s\\n" % (repr(s_attr_expr), get_exc_bt()))
    return None

  # Try to obtain the thing from the owner using the thing name.
  try:
    if ( type(owner) in (types.ModuleType, types.ClassType, types.InstanceType) ):
      thing = getattr(owner, thing_name, None)
    elif ( type(owner) in (types.ListType, types.DictType) ):
      thing = owner[thing_name]
    else:
      self.wfile.write("ERROR: %s: owner's type of %s is not supported.\\n" % (repr(s_owner_expr), repr(type(owner).__name__)))
      return None
  except:
    self.wfile.write("ERROR: %s: Unable to obtain thing from owner due to:\\n%s\\n" % (repr((s_owner_expr, s_attr_expr)), get_exc_bt()))
    return None

  # Make sure the obtained thing is of a tracable type.
  if ( not ( type(thing) in (types.FunctionType, types.MethodType) ) ):
    self.wfile.write("ERROR: %s: thing is of the wrong type to be traced.\\n" % type(thing).__name__)
    return None

  # See if this thing _is_ a trace.
  trace = lookup_trace(owner, thing_name)

  # If no existing trace found,
  if (trace is None):
    # Create a new trace record.
    trace = Trace(owner, thing, thing_name, s_fq_thing)

  return trace

_sb_trace.lock.acquire()
try:
  while args:
    if (args[0] == "-e"):
      del args[0]
      if ( len(args) > 1 ):
        trace = apply(resolve_exp_pair,args[:2])
        del args[:2]
      else:
        del args[:]
        self.wfile.write("ERROR: -e: Requires both an owner and attribute expression.\\n")
    else:
      trace = resolve_dotted(args[0])
      del args[0]

    # if we failed to obtain or create a trace instance, then continue.
    # (We assume that a more specific error message was already emitted.)
    if ( trace is None ): continue

    if ( b_untrace ):
      # If this trace was not already registered, let user know we can't untrace it.
      if ( not _sb_trace.traces.has_key(id(trace)) ):
        self.wfile.write("ERROR: %s: Is not currently being traced.\\n" % trace.s_fq_thing)
        continue

      # deactivate the trace.
      self.wfile.write("%d: %s: Untracing\\n" % (id(trace), trace.s_fq_thing))
      try:
        if ( type(trace.owner) in (types.ModuleType, types.ClassType, types.InstanceType) ):
          setattr(trace.owner, trace.thing_name, trace.thing)
        elif ( type(trace.owner) in (types.DictType, types.ListType) ):
          trace.owner[trace.thing_name] = trace.thing
        else:
          # This should really never happen, but if it does we will know about it.
          self.wfile.write("UNEXPECTED ERROR: %s: is not a support type of owner.\\n" % owner_type.__name__)
      except:
        self.wfile.write("UNEXPECTED ERROR: %s: Unable to deactivate trace due to:\\n%s\\n" % (trace.s_fq_thing, get_exc_bt()))

      # Remove the trace record.
      try:
        del _sb_trace.traces[id(trace)]
      except:
        self.wfile.write("UNEXPECTED ERROR: %s: Failed to unregister trace record due to:\\n%s\\n" % (trace.s_fq_thing, get_exc_bt()))
    else:
      # Set the before and after code objects.
      trace.co_before = co_before
      trace.co_after = co_after

      # activate the trace, if it is a new one.
      if ( not _sb_trace.traces.has_key(id(trace)) ):
        self.wfile.write("%d: %s: Tracing.\\n" % (id(trace), trace.s_fq_thing))
        fn_name = "_sb_trace_anon_fn_%s" % trace.thing.__name__
        if ( type(trace.owner) in (types.ModuleType, types.ClassType, types.InstanceType) ):
          exec compile(s_sb_trace_src % (fn_name, repr(id(trace))), "s_sb_trace_src", "exec") in trace.owner.__dict__
          setattr(trace.owner, trace.thing_name, getattr(trace.owner, fn_name))
#          self.wfile.write("D1: %s\\n" % dir(trace))
#          self.wfile.write("D1b: %s, %s\\n" % (trace.owner, fn_name))
          delattr(trace.owner, fn_name)
#          self.wfile.write("D2: %s\\n" % dir(trace))
        elif ( type(trace.owner) in (types.DictType, types.ListType) ):
          exec compile(s_sb_trace_src % (fn_name, repr(id(trace))), "s_sb_trace_src", "exec") in trace.thing.func_globals
          try:
#            trace.owner.set(trace.thing_name, trace.thing.func_globals[fn_name])
            trace.owner[trace.thing_name] = trace.thing.func_globals[fn_name]
            del trace.thing.func_globals[fn_name]
          except:
            # This should never happen, but if it does...
            self.wfile.write("UNEXPECTED ERROR: %s: failed to assign trace function to owner due to:\\n%s\\n" % (trace.s_fq_thing, get_exc_bt()))
        else:
          # This should never happen, but if it does...
          self.wfile.write("UNEXPECTED ERROR: %s: is not a support type of owner.\\n" % type(trace.owner).__name__)

        # Register the trace record.
        _sb_trace.traces[id(trace)] = trace
      else:
        self.wfile.write("%d: %s: Updating existing trace.\\n" % (id(trace), trace.s_fq_thing))
except:
  _sb_trace.lock.release()
  self.wfile.write("UNEXPECTED ERROR: %s" % get_exc_bt())
else:
  _sb_trace.lock.release()
"""

def main(argv):
  # Identify the shadowbot we will be working on.
  sb_name = None
  if ( (len(argv) > 1) and (argv[1] == "-sb") ):
    del argv[1]
    if ( len(argv) > 1 ):
      sb_name = argv[1]
      del argv[1]
  if ( sb_name == None ):
    sb_name = string.replace(os.path.basename(argv[0]), "_trace", "")
  if ( not (sb_name in g_map_known_shadowbots.keys()) ):
    sys.stderr.write("%s: %s: Unkown shadowbot.  Specify \"-sb\" with one of the following: %s\n" % (sys.argv[0], sb_name, g_map_known_shadowbots.keys()))
    sys.exit(1)
  (sb_url, sb_dir) = g_map_known_shadowbots[sb_name]

  sb_oplet_name = "sb_oplet.py"

  # Emit the oplet.
  open(os.path.join(sb_dir, sb_oplet_name), "w").write(g_s_oplet_src)

  # Serialize the arguments for the oplet.
  s_args=string.join(map(lambda a:"args=%s" % urllib.quote(a),argv),'&')
  if ( s_args != '' ): s_args = "?%s" % s_args

  # Invoke the oplet.
  url_req = urlopen.httpUrlRequest("%s%s%s" % (sb_url,sb_oplet_name,s_args),ctx=certmaster.getContext("/var/opt/opsware/crypto/spin/spin.srv"),connect_timeout=60,read_timeout=60,write_timeout=60);

  try:
    (url_obj,headers)=urlopen.httpReply(url_req)
  except urlopen.ReplyError, e:
    sys.stdout.write("ReplyError: %s\n\n" %e)
    url_obj = url_req
    sys.stdout.write("Response and Headers:\n%s\n\n" % url_req.buffer[:string.find(url_req.buffer,'\r\n\r\n')])
    sys.stdout.write("Response Body:\n")

  info_str=""
  add_str = url_obj.read()
  while add_str:
    info_str = info_str + add_str
    add_str = url_obj.read()
  sys.stdout.write(info_str)

if ( __name__ == "__main__" ):
  main(sys.argv[:])

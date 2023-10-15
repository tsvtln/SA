
# TODO: 
#
# [X] Allow this tool to package up multiple modules into a single self executable.
#     (see comments in: http://technogeek.org/2007/05/29/dynamic-module-loading-in-python-2/  http://technogeek.org/python-module.html)
#

# Arch notes:
#
# Generated self executable file has the following format:
#
# <shell_loader>
# <zlib_pkl_dict> {"src_list": [(<mod_name>, <mod_src>), ...]
#                  "py_loader1": <py_loader1_src>
#                  "main_mod": <main_mod_name>}
# <4-byte_len> of of previous <pkl_dict> record.
#

import sys,os,string,time,struct,zlib,socket,cPickle,base64

if ( not hasattr(os.path,'sep') ): os.path.sep = os.path.join('.','.')[1]

def out(s, args=None):
  if ( args is not None ): s = s % args
  sys.stdout.write(s)

def err(s, args=None):
  if ( args is not None ): s = s % args
  sys.stderr.write(s)

def info(s, args=None):
  out("%s\n" % s, args)

def error(s, args=None):
  err("ERROR: %s: %s\n" % (time.ctime(time.time()), s), args)

def warn(s, args=None):
  err("WARNING: %s: %s\n" % (time.ctime(time.time()), s), args)

def usage():
  err("""Usage: %s [-r] <py1> [<pyn> ...]

  -r Converts all instances of crnl ("\\r\\n") to nl ("\\n").  The reason for
     this is that python's internal compiler expects source files to be nl
     terminated.  Alternatively you could run all source files through dos2unix
     before running py_build.

Will generate a self executable shell script with the basename of the last
python module listed on the command line.  This shell script will have the
source code of listed modules compressed and embedded

  env PYTHONPATH=/opt/opsware/pylibs2:/opt/opsware/spin /opt/opsware/bin/python2
  env PYTHONPATH=/opt/opsware/pylibs:/opt/opsware/sbin /opt/opsware/bin/python
  env PYTHONPATH=/lc/blackshadow/pylibs(?):/lc/blackshadow/spin(?) /lc/bin/python
    (deprecated)
  env python

At runtime, the self executable shell script will determine which version of
python to use to execute the embedded source code.  It will look for the
following python interpreters and use the corresponding environment by 
preference of the order of the following list:

  (1) /opt/opsware/bin/python2
        PYTHONPATH=/opt/opsware/pylibs2:/opt/opsware/spin
        LD_LIBRARY_PATH=/opt/opsware/lib

  (2) /opt/opsware/bin/python
        PYTHONPATH=/opt/opsware/pylibs:/opt/opsware/spin
        LD_LIBRARY_PATH=/opt/opsware/lib

  (3) /opt/opsware/agent/bin/python
        PYTHONPATH=/opt/opsware/agent/pylibs:/opt/opsware/spin

If neither of these python executables are found, it will default to looking
for "python" in the current path, and will use no environment settings.

At runtime, before the main program is loaded and invoked, if either of the
first two python interpreters are chosen, then a further check is performed to
make sure that the chosen version matches the /opt/opsware/spin/truthdb.pyc
file.  If a mismatch is detected, then the other python interpreter is used.
""", (sys.argv[0],))

g_py_profiles = ( \
  ("/opt/opsware/bin/python2", "LD_LIBRARY_PATH=/opt/opsware/lib PYTHONPATH=/opt/opsware/pylibs2:/opt/opsware/spin"),
  ("/opt/opsware/bin/python", "LD_LIBRARY_PATH=/opt/opsware/lib PYTHONPATH=/opt/opsware/pylibs:/opt/opsware/spin"),
  ("/opt/opsware/agent/bin/python", "PYTHONPATH=/opt/opsware/agent/pylibs"),
  ("python", ""),
)

# Model the profiles into shell source varibales.
g_py_profiles_sh_src = ""
idx = 0
for py_prof in g_py_profiles:
  g_py_profiles_sh_src = g_py_profiles_sh_src + ("PY_BIN%d=\"%s\"\nPY_ENV%d=\"%s\"\n" % (idx, py_prof[0], idx, py_prof[1]))
  idx = idx + 1

g_shell_loader_src = """#!/bin/sh

# Dynamically generated code
# Build date: %s
# Build machine: %s
# Build dir: %s
# Build invocation: %s

%s

NUM_PY_PROFS=%d

IDX=0

while ( [ $IDX -lt $NUM_PY_PROFS ] ) do
  eval CUR_PY_BIN=\$PY_BIN${IDX}
  if ( [ \( -f $CUR_PY_BIN \) -o \( "`expr $IDX + 1`" -eq $NUM_PY_PROFS \) ] ) then
    eval CUR_PY_ENV=\$PY_ENV${IDX}
    exec env ${CUR_PY_ENV} "$CUR_PY_BIN" -c 'import zlib,base64;eval(compile(zlib.decompress(base64.decodestring("%s")),"py_loader0","exec"))' "$0" "$@"
  fi
  IDX="`expr $IDX + 1`"
done

# We should not get here, but if we do, go ahead and exit.
exit 1
"""

# remove this, right? -dw
# g_py_compile_src = "import zlib,marshal,sys;sys.stdout.write(zlib.compress(marshal.dumps(compile(open(sys.argv[1]).read()+\"\\n\",sys.argv[1],\"exec\"))))"

# Responsible for loading and executing python_loader_1.
g_py_loader0_src = """import sys,os,zlib,struct,cPickle
_fn=sys.argv[1]
_fl=os.stat(_fn)[6]
_f=open(_fn)
_f.seek(_fl-4)
_pbs_len=struct.unpack("<I",_f.read(4))[0]
_f.seek(_fl-4-_pbs_len)
_py_dict=cPickle.loads(zlib.decompress(_f.read(_fl)))
eval(compile(_py_dict["py_loader1"],"py_loader1","exec"))
"""
g_py_loader0_src_gz_b64 = string.replace(base64.encodestring(zlib.compress(g_py_loader0_src)),'\n','')

g_py_loader1_src = """import sys,imp,os,cPickle,marshal,zlib,string

g_py_loader0_src_gz_b64 = %s

g_py_loader0_c = 'import zlib,base64;eval(compile(zlib.decompress(base64.decodestring("%%s")),"py_loader0","exec"))' %% g_py_loader0_src_gz_b64

truthdb_pyc_file = "/opt/opsware/spin/truthdb.pyc"

# Check to see if we need to re-exec due to truthdb.pyc magic mismatch.
# (HPSA specific loader code.)
if ( sys.executable[:23] == "/opt/opsware/bin/python" and 
     os.path.exists(truthdb_pyc_file) and
     imp.get_magic() != open(truthdb_pyc_file).read(4) and
     (not os.environ.has_key("PY_BUILD_TRUTHDB_MAGIC_CHECKED")) ):
  os.environ["PY_BUILD_TRUTHDB_MAGIC_CHECKED"] = '1'
  next_py_bin = '/opt/opsware/bin/python'
  if ( sys.executable[-1] != '2' ):
    next_py_bin = next_py_bin + '2'
    os.environ['PYTHONPATH'] = string.replace(os.environ['PYTHONPATH'], 'pylibs', 'pylibs2')
  else:
    os.environ['PYTHONPATH'] = string.replace(os.environ['PYTHONPATH'], 'pylibs2', 'pylibs')
  os.execv(next_py_bin, [next_py_bin, '-c', g_py_loader0_c] + sys.argv[1:])

# Load the src list.
_src_list = _py_dict["src_list"]

def load_mod(mod_name, mod_src, global_ns=0):
  if ( global_ns ):
    exec compile(mod_src, mod_name + ".py", "exec") in globals()
  else:
    mod = imp.new_module(mod_name)
    sys.modules[mod_name] = mod
    exec compile(mod_src, mod_name + ".py", "exec") in mod.__dict__

#print "DEBUG: ", _src_dict.keys()

# extract and each module.
#main_mod_name = _py_dict["main_mod"]
for mod_rec in _src_list[:-1]:
  apply(load_mod, mod_rec)

# Load the main module into the global namespace.
sys.argv = sys.argv[1:]
apply(load_mod, _src_list[-1] + (1,))

""" % repr(g_py_loader0_src_gz_b64)
#g_py_loader1_src_gz = zlib.compress(g_py_loader1_src)

def mod_name_from_file(mod_file):
  mod_name = os.path.basename(mod_file)
  if ( mod_name[-3:] != '.py' ):
    error("%s: File name does not end in \".py\".", (mod_file,))
    sys.exit(1)
  mod_name = mod_name[:-3]
  if ( string.find(mod_name, '.') > -1 ):
    error("%s: File name contains invalid '.' characters", (mod_file,))
    sys.exit(1)
  return mod_name

def main(args):
  args = args[1:]
  b_crnl_to_nl = 0
  if ( (len(args) > 0) and (args[0] == "-r") ):
    b_crnl_to_nl = 1
    del args[0]

  mod_files = args
  if ( len(mod_files) == 0 ):
    usage()
    sys.exit()

  # python dictionary.
  py_dict = {}

  # Get the output name from the last source file given.
  out_name = mod_name_from_file(mod_files[-1])

  # Open up a temp file to compile to.
  tmp_out_name = ".%s" % out_name
  f_out = open(tmp_out_name, 'w')

  # Emit the shell loader source to the file.
  f_out.write(g_shell_loader_src % (time.ctime(time.time()),
                                    socket.gethostname(),
                                    os.getcwd(),
                                    string.join(sys.argv, ' '),
                                    g_py_profiles_sh_src,
                                    len(g_py_profiles),
                                    g_py_loader0_src_gz_b64))

  # Source list
  src_list = []

  # Itterate over every module.
  for mod_file in mod_files:
    # Extract the module name from the 
    mod_name = mod_name_from_file(mod_file)

    # Load the source for the current module.
    mod_src = open(mod_file).read() + '\n'

    if ( b_crnl_to_nl ):
      # Replace all crnl to nl.
      mod_src = string.replace(mod_src, "\r\n", "\n")
    else:
      # Look to see if there are any CRs in the current file.
      if ( string.find(mod_src, "\r\n") > -1 ):
        # Warn the user what might happen and how to work around it.
        sys.stderr.write("""WARNING: %s: carrage return ('\\r') character detected.
  This can cause the resulting compiled script to fail with a "SyntaxError: invalid syntax" type error.
  To workaround this issue, use "-r" option to replace all "\\r\\n" strings with "\\n".
  The side effect to "-r" is that it will also modify any string literals that contain "\\r\\n".

""" % mod_file)

    # Store the module source.
    src_list.append((mod_name, mod_src))

  # Add the module source to the python dictionary.
  py_dict["src_list"] = src_list

  # Add the py_loader1 source code to the python dictionary
  py_dict["py_loader1"] = g_py_loader1_src

  # Add the last module name as the main module.
  py_dict["main_mod"] = out_name

  # Pickle and emit the python dictionary.
  py_dict_pkl = zlib.compress(cPickle.dumps(py_dict, 1))
  f_out.write(py_dict_pkl)

  # Finally, emit the length of the module index.
  f_out.write(struct.pack("<I", len(py_dict_pkl)))

  # Close and rename the file to the final target.
  f_out.close()
  os.rename(tmp_out_name, out_name)
  os.chmod(out_name, 0755)

  # Let user know what we did.
  info("Compiled to %s", (out_name,))

if ( __name__ == '__main__' ):
  main(sys.argv[:])


# TODO: 
#
# [ ] Allow this tool to package up multiple modules into a single self executable.
#     (see comments in: http://technogeek.org/2007/05/29/dynamic-module-loading-in-python-2/  http://technogeek.org/python-module.html)
#

# Arch notes:
#
# Generated compiled file has the following format:
#
# <shell_loader>
# <pkl_dict> {<mod_name>: <zlib_marshaled_co> ...} for a given version of python.
# . . .
# <pkl_dict> {<python_magic>: <file_offset>, . . .
#             "py_loader1": <zlib_py_loader1_src>}
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
  err("""Usage: %s <py1> [<pyn> ...]

Will generate a self executable shell script with the basename of the last
python module listed on the command line.  This shell script will have appended
to it versions of all modules listed compiled using various python
interpreters present on the build system.  At the moment it is designed to
look for:

  env PYTHONPATH=/opt/opsware/pylibs2:/opt/opsware/spin /opt/opsware/bin/python2
  env PYTHONPATH=/opt/opsware/pylibs:/opt/opsware/sbin /opt/opsware/bin/python
  env PYTHONPATH=/lc/blackshadow/pylibs(?):/lc/blackshadow/spin(?) /lc/bin/python
    (deprecated)
  env python

At runtime, the self executable shell script will determine which version of
python is present, based on the list above, and invoke the matching set of
compiled python code.  It will attempt to invoke a main(args) function in the
module specified last on the py_build command line.

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
  if ( [ \( -f $CUR_PY_BIN \) -o \( $(($IDX+1)) -eq $NUM_PY_PROFS \) ] ) then
    eval CUR_PY_ENV=\$PY_ENV${IDX}
    exec env ${CUR_PY_ENV} "$CUR_PY_BIN" -c 'import zlib,base64;eval(compile(zlib.decompress(base64.decodestring("%s")),"py_loader0","exec"))' "$0" "$@"
  fi
  IDX=$(($IDX+1))
done

# We should not get here, but if we do, go ahead and exit.
exit 1
"""

g_py_compile_src = "import zlib,marshal,sys;sys.stdout.write(zlib.compress(marshal.dumps(compile(open(sys.argv[1]).read()+\"\\n\",sys.argv[1],\"exec\"))))"

# Responsible for loading and executing python_loader_1.
g_py_loader0_src = """import sys,os,zlib,struct,cPickle
_fn=sys.argv[1]
_fl=os.stat(_fn)[6]
_f=open(_fn)
_f.seek(_fl-4)
_pbs_len=struct.unpack("<I",_f.read(4))[0]
_f.seek(_fl-4-_pbs_len)
_mod_idx=cPickle.load(_f)
eval(compile(zlib.decompress(_mod_idx["py_loader1"]),"py_loader1","exec"))
"""
g_py_loader0_src_gz_b64 = string.replace(base64.encodestring(zlib.compress(g_py_loader0_src)),'\n','')

g_py_loader1_src = """import sys,imp,os,cPickle,marshal,zlib,string

py_magic = imp.get_magic()

g_py_loader0_src_gz_b64 = %s

g_py_loader0_c = 'import zlib,base64;eval(compile(zlib.decompress(base64.decodestring("%%s")),"py_loader0","exec"))' %% g_py_loader0_src_gz_b64

truthdb_pyc_file = "/opt/opsware/spin/truthdb.pyc"

# Check to see if we need to re-exec due to truthdb.pyc magic mismatch.
# (HPSA specific loader code.)
if ( sys.executable[:23] == "/opt/opsware/bin/python" and 
     os.path.exists(truthdb_pyc_file)  and
     py_magic != open(truthdb_pyc_file).read(4) and
     (not os.environ.has_key("PY_BUILD_TRUTHDB_MAGIC_CHECKED")) ):
  os.environ["PY_BUILD_TRUTHDB_MAGIC_CHECKED"] = '1'
  next_py_bin = '/opt/opsware/bin/python'
  if ( sys.executable[-1] != '2' ):
    next_py_bin = next_py_bin + '2'
    os.environ['PYTHONPATH'] = string.replace(os.environ['PYTHONPATH'], 'pylibs', 'pylibs2')
  else:
    os.environ['PYTHONPATH'] = string.replace(os.environ['PYTHONPATH'], 'pylibs2', 'pylibs')
  os.execv(next_py_bin, [next_py_bin, '-c', g_py_loader0_c] + sys.argv[1:])

# if there is no index record for the current py magic
if ( not _mod_idx.has_key(py_magic) ):
  # if we haven't tried a re-exec yet.
  if (not os.environ.has_key("PY_BUILD_ENV_RE_EXECED") ):
    # Set the re-exec env key.
    os.environ["PY_BUILD_ENV_RE_EXECED"] = '1'

    # Re exec using "env python".
    # (TODO, could inject the final py profile as a default.)
    os.execvp("env", ["env", "python", '-c', g_py_loader0_c] + sys.argv[1:])
  else:
    sys.stderr.write("WARNING: %%s's magic number does not match any compiled modules\\nattempting to execute default compiled modules anyway.\\n" %% sys.executable)
    py_magic = _mod_idx["def_py_magic"]
#    sys.stdout.write("py_loader1: No compiled python modules found that match the versions of python on this box.\\n")
#    sys.exit(1)

# Load the module dictionary that matches this version of python.
mod_cos_offset = _mod_idx[py_magic]
_f.seek(mod_cos_offset)
mod_cos = cPickle.load(_f)

def load_mod(mod_name, mod_co_str_zlib, global_ns=0):
  mod = imp.new_module(mod_name)
  sys.modules[mod_name] = mod
  if ( global_ns ):
    exec marshal.loads(zlib.decompress(mod_co_str_zlib)) in globals()
  else:
    exec marshal.loads(zlib.decompress(mod_co_str_zlib)) in mod.__dict__

# extract and each module.
main_mod_name = _mod_idx["main_mod"]
for mod_key in mod_cos.keys():
  if ( mod_key != main_mod_name ):
    load_mod(mod_key, mod_cos[mod_key])

# Load the main module into the global namespace.
sys.argv = sys.argv[1:]
load_mod(main_mod_name, mod_cos[main_mod_name], 1)

""" % repr(g_py_loader0_src_gz_b64)
g_py_loader1_src_gz = zlib.compress(g_py_loader1_src)

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
  mod_files = args[1:]
  if ( len(mod_files) == 0 ):
    usage()
    sys.exit()

  # Modules index.
  mod_idx = {}

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

  # Itterate through all profiles.
  for py_profile in g_py_profiles:
    py_bin = py_profile[0]
    py_env = py_profile[1]

    # module dictionary for the current python profile.
    mod_cos = {}

    # Obtain the magic number for the current python.
    py_magic = os.popen("%s -c 'import imp,sys;sys.stdout.write(imp.get_magic())' 2>/dev/null" % py_bin).read()

    # If we have already compiled using a version of python with the current magic.
    if ( mod_idx.has_key(py_magic) ):
      # Let user know and skip.
#      info("Already compiled with py_magic=%s, skipping %s" % (repr(py_magic), py_bin))
      continue

    # If no magic was found or of the wrong size.
    if ( len(py_magic) != 4 ):
      # Let user know this profile will be skipped.
      warn("%s, py_magic==%s: failed to obtain valid magic for this python profile. skipping...", (repr(py_bin), repr(py_magic)))
      continue

    # Itterate over every module.
    for mod_file in mod_files:
      # Extract the module name from the 
      mod_name = mod_name_from_file(mod_file)

      # Let user know what is going on.
#      info("Compiling %s for %s (py_magic=%s)" % (mod_name, py_bin, repr(py_magic)))

      # Obtain zlib/marshaled/co for current module using current py profile.
      mod_cos[mod_name] = os.popen("%s -c '%s' %s" % (py_bin, g_py_compile_src, mod_file)).read()

    # Record the current file offset in the index.
    mod_idx[py_magic] = f_out.tell()
   
    # Emit the dictionary of compiled modules to the output file.
    cPickle.dump(mod_cos, f_out, 1)

  # Add the py_loader1 source code to the module index.
  mod_idx["py_loader1"] = g_py_loader1_src_gz

  # Add the last module name as the main module.
  mod_idx["main_mod"] = out_name

  # Add the last py_magic as the default.
  mod_idx["def_py_magic"] = py_magic

  # Pickle and emit the index dictionary.
  mod_idx_pkl = cPickle.dumps(mod_idx, 1)
  f_out.write(mod_idx_pkl)

  # Finally, emit the length of the module index.
  f_out.write(struct.pack("<I", len(mod_idx_pkl)))

  # Close and rename the file to the final target.
  f_out.close()
  os.rename(tmp_out_name, out_name)
  os.chmod(out_name, 0755)

  # Let user know what we did.
  info("Compiled to %s", (out_name,))

if ( __name__ == '__main__' ):
  main(sys.argv[:])

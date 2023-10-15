import sys,os

from coglib import certmaster
ctx = certmaster.getContext("/var/opt/opsware/crypto/spin/spin.srv")
from librpc.xmlrpc import lcxmlrpclib
from librpc import SSLTransport

way = lcxmlrpclib.Server('https://127.0.0.1:1018/wayrpc.py', transport=SSLTransport.SSLTransport(ctx=ctx))

def shift(l):
  r = l[0]
  del l[0]
  return r

if ( len(sys.argv) == 1 or (sys.argv[1] in ("-h","--help")) ):
  sys.stdout.write("""Usage:

  %s [-c <concurrency>] [-f <dvc_id_file>] [<dvc_id1> [<dvc_id2> ...]]

  %s [-c <concurrency>] -dc

""" % ((sys.argv[0],)*2))
  sys.exit()

job = {}
args = sys.argv[1:]

concurrency = -1
if ( args[0] == "-c" ):
  shift(args)
  concurrency = int(shift(args))

if ( args[0] == "-dc" ):
  from coglib import spinwrapper
  spin = spinwrapper.SpinWrapper()
  dc_id = spin.sys.getDCFromDB()['id']
  job["script"] = "opsware.agent_reach.check_reachability"
  job["session_desc"] = "(manual) Automated Communications Test for core: %s" % dc_id
  job["username"] = "$spin"
  job["sync"] = 0 # Run asynchronously
  job["acct_id"] = None
  job["params"] = { "dc_ids":[dc_id], "recurse_dcs":1, "incl_unreach_dcs":1 }
else:
  dvc_ids = []
  while len(args) > 0:
    cur_arg = shift(args)
    if ( cur_arg == '-f' ):
      try:
        fn = shift(args)
        f = sys.stdin
        if ( fn != '-' ):
          f = open(fn)
        dvc_ids.extend(map(long, filter(lambda i:i!='',string.split(f.read(), '\n'))))
      except ValueError, e:
        sys.stdout.write("ERR: stdin: %s\n" % e)
    else:
      try:
        dvc_ids.append(long(cur_arg))
      except ValueError, e:
        sys.stdout.write("ERR: %s\n" % e)

  job["script"] = "opsware.agent_reach.check_reachability"
  job["session_desc"] = "(manual) Batch Communications Test for %d devices" % len(dvc_ids)
  job["username"] = "$spin"
  job["sync"] = 0 # Run asynchronously
  job["acct_id"] = None
  job["params"] = { "dvc_ids":dvc_ids }

if ( concurrency > 0 ):
  job["params"]["concurrency"] = concurrency

def read_char():
  import termios,tty
  try:
    import TERMIOS
    termios.TCSAFLUSH = TERMIOS.TCSAFLUSH
  except ImportError:
    pass
  for fd in (0,1,2):
    try:
      orig_mode = termios.tcgetattr(fd)
      tty.setraw(fd)
      try:
        return os.read(fd,1)
      finally:
        termios.tcsetattr(fd,termios.TCSAFLUSH,orig_mode)
    except:
#      import traceback
#      print string.join( apply( traceback.format_exception, sys.exc_info() ), "")
      pass

def read_char2():
  for fd in (0,1,2):
    try:
      return os.read(fd,1)
    except:
      pass

sys.stdout.write("About to execute: %s\nContinue? (y/n)\n" % job["session_desc"])
res = read_char()
if ( (not res) or (not (res in "yY")) ):
  sys.stdout.write("Comm test _NOT_ executed.\n")
  sys.exit(0)

sys.stdout.write("Session ID: %s\n" % way.script.run( job ))

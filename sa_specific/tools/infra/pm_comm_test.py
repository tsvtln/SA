import string,threading,sys,time,thread,traceback,select,socket,Queue
from coglib import spinwrapper,certmaster
from librpc.xmlrpc import lcxmlrpclib;from librpc import SSLTransport

spin = spinwrapper.SpinWrapper(url="http://127.0.0.1:1007")
ctx = certmaster.getContextByName("waybot","waybot.srv","agent-ca.crt")

def log(msg, args=None):
  if ( args != None ): msg = msg % args
  header = "%s: %s(%d): " % (time.ctime(time.time()), threading.currentThread().getName(), thread.get_ident())
  if ( msg[-1] == '\n' ): msg = msg[:-1]
  msg = string.replace(msg,'\n', '\n%s' % header)
  msg = "%s%s\n" % (header, msg)
  sys.stdout.write(msg)

def get_last_tb():
  return string.join( apply( traceback.format_exception, sys.exc_info() ), "")

def usage():
  sys.stdout.write("""Usage: %s [-gw <gw>] [-u] [-q <dvc_id_query>]
""" % sys.argv[0])

NUM_WORKER_THREADS = 10
connect_timeout = 10
read_timeout = 10

# returns (result, comment) result=1 on success, result=0 on failure.
def ping_dvc(dvc_ip, dst_realm):
  log("Attempting to ping dvc_ip=%s, dst_realm=%s", (repr(dvc_ip), repr(dst_realm)))
  result = 0
  comment = "Presumed Failure"
  if ( dst_realm == "TRANSITIONAL" ):
    transport = SSLTransport.SSLTransport(ctx=ctx, connect_timeout=connect_timeout, read_timeout=read_timeout)
  else:
    transport = SSLTransport.SSLTransport(ctx=ctx, connect_timeout=connect_timeout, read_timeout=read_timeout, realm=dst_realm, gw_list=[g_gw])
  aw = lcxmlrpclib.Server("https://%s:1002/rpc.py" % dvc_ip,transport=transport)
  try:
    comment = "aw.cogbot.getUptime(): %s" % str(aw.cogbot.getUptime())
    result = 1
  except:
    comment = get_last_tb()
  return (result, comment)

def ping_dvc2(dvc_ip, dst_realm):
  log("Attempting to ping dvc_ip=%s, dst_realm=%s", (repr(dvc_ip), repr(dst_realm)))
  result = 0
  comment = "Presumed Failure"
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  if ( dst_realm != "TRANSITIONAL" ):
    try:
      sock.connect(g_gw)
    except socket.error, e:
      comment = str(e)
      return
    sock.send("CONNECT %s:1002 HTTP/1.0\r\nX-OPSW-REALM: %s\r\n\r\n" % (dvc_ip, dst_realm))
    rl,wl,xl = select.select([sock],[],[],read_timeout)
    if ( len(rl) > 0 ):
      resp = rl[0].recv(1024)
      if ( string.find(resp, "200 Connection Established") > -1 ):
        result = 1
        comment = resp
      else:
        comment = resp
    else:
      comment = "Timeout"
  else:
    try:
      sock.connect((dvc_ip,1002))
    except socket.err, e:
      comment = str(e)
      return
    result = 1
    comment = "TRANSITIONAL realm connection successful"

  try:
    sock.close()
  except:
    pass

  return (result, comment)

def pm_comm_test_dvcs_thread():
  while 1:
    try:
      dvc_id = g_dvc_ids.pop()
    except IndexError, e:
      dvc_id = None
    if ( dvc_id == None ): break
    try:
      log("Attempting to load and test device %s", dvc_id)
      dvc = spin.Device.get(dvc_id)
      dst_realm = dvc.getRealm()['realm_name']
      dvc_ip = dvc['management_ip']
      (result, comment) = ping_dvc(dvc_ip, dst_realm)
      if ( result ):
        log("PASS: device %s, comment=%s", (dvc_id, repr(comment)))
        if ( g_update ):
          log("Updating device %s to status=OK", (dvc_id,))
          dvc.update(state="OK")
      else:
        log("FAIL: device %s, comment=%s", (dvc_id, repr(comment)))
    except:
      log("Unexpected error occured while attempting to ping device %s:", dvc_id)
      log(get_last_tb())

g_dvc_ids_query = "spin.Device.getIDList(restrict={'state':'UNREACHABLE','opsw_lifecycle':'MANAGED'})"
g_update = 0
g_gw = ("127.0.0.1",3002)

def shift(l):
  r = l[0]
  del l[0]
  return r

args = sys.argv[1:]
while ( len(args) > 0 ):
  cur_arg = shift(args)
  if ( cur_arg == '-q' ):
    g_dvc_ids_query = shift(args)
  elif ( cur_arg == '-u' ):
    g_update = 1
  elif ( cur_arg == '-gw' ):
    gw = list(string.split(shift(args), ':'))
    gw[1] = int(gw[1])
    g_gw = tuple(gw)
  elif ( cur_arg in ("-h", "--help") ):
    usage()
    sys.exit()
  else:
    sys.stdout.write("%s: Unrecognized argument\n" % cur_arg)
    sys.exit(1)

g_dvc_ids = eval(g_dvc_ids_query)

log("Scanning %d devices.", len(g_dvc_ids))

if ( len(g_dvc_ids) > 0 ):
  log("Starting %d worker threads", NUM_WORKER_THREADS)
  threads = []
  while len(threads) < NUM_WORKER_THREADS:
    thread_name = "PingerThread-%d" % (len(threads)+1)
#    log("Starting %s", thread_name)
    cur_thread = threading.Thread(name=thread_name, target=pm_comm_test_dvcs_thread)
    cur_thread.start()
    threads.append(cur_thread)

  log("Waiting on worker threads to complete")
  for cur_thread in threads:
    cur_thread.join()

log("Done.")


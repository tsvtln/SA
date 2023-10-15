import sys,gzip,cPickle,types,time,traceback

def usage():
  sys.stdout.write("""Usage: %s [-h|--help] [-i <infile>] [-o <outfile>]
        [--spin_ip <spin_ip>] [-q <query>] [-s <slice>] [<dvc_id1> ...]

    [-i <infile>]
        Will pretty print the results previously dumped with the "-o" option.

    [-o <outfile>]
        Write the results to a gzipped, pickle file named <outfile>.

    [--pp]
        Force pretty print summary even when "-o" option is used.

    [-q <query>]
        Use <query> to select a set of device ids from the database whose comm
        test results are to be dumped.  This query is only used if no device
        ids are specified on the command line.  As an example, if no query is 
        given then the following query is used by default:

'spin.Device.getIDList(restrict={"state":"UNREACHABLE", "opsw_lifecycle":"MANAGED"})'

    [-v]
        Verbose summary report.

# Test Error codes
SUCCESS               = 0
NOT_TESTED            = 1
UNEXPECTED            = 2
CONN_REFUSED          = 3
CONN_TIMEOUT          = 4
NOT_RESOLVE           = 12
AGENT_REQ_TIMEOUT     = 5
AGENT_NO_SERVICE_INST = 6
CRYPTO_CERT_MISMATCH  = 7
CRYPTO_NEG_FAILURE    = 8
OLD_AGENT_VERSION     = 9
WORD_CANT_IDENT       = 10
MID_MISMATCH          = 11
WAY_NO_GETCOMMAND     = 21
REALM_UNREACHABLE     = 13
NO_GATEWAY_DEFINED    = 14
TUNNEL_SETUP_ERROR    = 15
GW_ACCESS_DENIED      = 16
GW_RESOLUTION_FAILED  = 17
GW_INTERNAL_ERROR     = 18
GW_COULDNT_CONNECT    = 19
GW_TIMEOUT            = 20

""" % sys.argv[0])

def write(f, msg, args=None):
  if ( args != None ):
    msg = msg % args
  f.write(msg)
  f.flush()

def out(msg, args=None):
  write(sys.stdout, msg, args)

def err(msg, args=None):
  write(sys.stderr, msg, args)

def str_id(id):
  if ( type(id) == types.LongType ): return repr(id)[:-1]
  else: return str(id)

CHUNK_SIZE=1000
g_b_verbose = 0

def get_device_recs(dvc_ids):
  dvc_ids = dvc_ids[:]
  dvc_recs = []
  while (len(dvc_ids) > 0):
    dvc_ids_chunk = shift_chunk(dvc_ids, CHUNK_SIZE)
    drs = spin.Device.getList(restrict={'dvc_id':dvc_ids_chunk},fields=["management_ip",'realm_id','state','opsw_lifecycle','system_name'])
    for dr in drs:
      dvc_rec = {"dvc_id":str_id(dr[0]),
                 "management_ip":str(dr[1]),
                 'realm_id':str_id(dr[2]),
                 'state':dr[3],
                 'opsw_lifecycle':dr[4],
                 'system_name':dr[5]}
      dvc_rec["realm_name"] = cached_spin_call("Realm.get", dvc_rec["realm_id"]).get("realm_name", "**NOT FOUND**")
      dvc_recs.append(dvc_rec)
    err(".")
  return dvc_recs

def get_device_role_ids(dvc_recs):
  dvc_ids = map(lambda dr:dr["dvc_id"], dvc_recs)
  map_dvc_dr = {}
  while ( len(dvc_ids) > 0 ):
    dvc_ids_chunk = shift_chunk(dvc_ids ,CHUNK_SIZE)
    dr_recs_chunk = spin.DeviceRole.getList(restrict={'dvc_id':dvc_ids_chunk},fields=["dvc_id","cust_cld_id"])
    for dr_rec in dr_recs_chunk:
      map_dvc_dr[str_id(dr_rec[1])] = dr_rec
    err(".")
  rm_dvc_recs = []
  for dvc_rec in dvc_recs:
    dr_rec = map_dvc_dr.get(dvc_rec["dvc_id"], None)
    if ( dr_rec != None ):
      dvc_rec["dvc_role_id"] = dr_rec[0]
      dvc_rec["acct_cld_id"] = dr_rec[2]
    else:
      err("\nERR: %(system_name)s(%(dvc_id)s): does not have a corresponding DeviceRole.  Skipping.\n", dvc_rec)
      rm_dvc_recs.append(dvc_rec)
  for rm_dvc_rec in rm_dvc_recs:
    dvc_recs.remove(rm_dvc_rec)

def get_dc_and_accts(dvc_recs):
  acct_cld_ids = map(lambda dr:dr["acct_cld_id"], dvc_recs)
  map_cld = {}
  while ( len(acct_cld_ids) > 0 ):
    acct_cld_ids_chunk = shift_chunk(acct_cld_ids, CHUNK_SIZE)
    acct_recs = spin.AccountCloud.getList(restrict={'cust_cld_id':acct_cld_ids_chunk},fields=["acct_id", "data_center_id"])
    for acct_rec in acct_recs:
      map_cld[acct_rec[0]] = acct_rec
    err(".")
  for dvc_rec in dvc_recs:
    cld_rec = map_cld[dvc_rec["acct_cld_id"]]
    dvc_rec["acct_id"] = cld_rec[1]
    dvc_rec["acct_name"] = cached_spin_call("Account.get", dvc_rec["acct_id"]).get("acct_name", "**NOT FOUND**")
    dvc_rec["dc_id"] = cld_rec[2]
    dvc_rec["dc_name"] = cached_spin_call("DataCenter.get", dvc_rec["dc_id"]).get("display_name", "**NOT FOUND**")
    try:
      dc = cached_spin_call("DataCenter.getCoreDC", dvc_rec["dc_id"])
    except:
      dc = {}
    (root_dc_id, dvc_rec["root_dc_name"]) = (dc.get("data_center_id", "-1"), dc.get("display_name","**NOT FOUND**"))
    dvc_rec["root_dc_id"] = root_dc_id

def load_comm_test_results(dvc_rec, dr_id):
  items = spin.DeviceRole.getDictItems(dr_id)
  for item in items:
    if ( string.find(item[0], "__OPSW_reachability_") == 0 ):
      dvc_rec[item[0]] = item[1]

def calc_slice_affinity(dvc_rec):
  if ( dvc_rec["root_dc_id"] == "-1" ):
    dvc_rec["slice_ips"] = ("**NOT FOUND**",)
  else:
    slice_ips = spin.DataCenter.getDictValue(dvc_rec["root_dc_id"], key='__OPSW_slice_ips')
    slice_ips = map(lambda i:string.split(i,':')[1], filter(lambda i:string.find(i,':')>-1,string.split(slice_ips,' ')))
    seed = "%(realm_name)s:%(management_ip)s" % dvc_rec
    indexes = shuffle.random_list(len(slice_ips), seed)
    shuffled_slice_ips = []
    for idx in indexes:
      shuffled_slice_ips.append(slice_ips[idx])
    dvc_rec["slice_ips"] = tuple(shuffled_slice_ips)

g_spin_cache = {}
def cached_spin_call(fn, *args, **kwargs):
  key = "%s(args=%s,kwargs=%s)" % (fn, args, kwargs)
  if ( not g_spin_cache.has_key(key) ):
    ret = apply(getattr(spin, fn), args, kwargs)
    g_spin_cache[key] = ret
  return g_spin_cache[key]

def is_num(s):
  try:
    long(s)
  except:
    return 0
  return 1

def pp_dvc_rec(dvc_rec, verbose=0):
  items = dvc_rec.items()
  m = {}
  for item in items:
    m[item[0]] = item[1]
  keys = map(lambda i:i[0],items)
  ct_keys = filter(lambda k:string.find(k,"__OPSW_reachability_")==0,keys)
  tb_keys = filter(lambda k:string.find(k,"__OPSW_reachability_tb_")==0,ct_keys)
  tb_keys.sort()
  ct_keys = filter(lambda k:string.find(k,"__OPSW_reachability_tb_")==-1,ct_keys)
  ct_keys = filter(lambda k:string.find(k,"__OPSW_reachability_time")==-1,ct_keys)
  ct_keys.sort()
  res = []
  if ( m.has_key("__OPSW_reachability_time") ):
    ts = m["__OPSW_reachability_time"]
    if ( ts != None ):
      try:
        ts = time.ctime(float(ts))
      except:
        pass
    res.append("time:%s" % repr(ts))
  for key in ct_keys:
    val = m[key]
    res.append("%s:%s" % (key[20:],val))
  for key in tb_keys:
    val = m[key]
    res.append("%s:%s" % (key[20:],val))
  if ( g_b_verbose ):
    dvc_id = "%(system_name)s(%(dvc_id)s)" % dvc_rec
    acct = "acct:%(acct_name)s, " % dvc_rec
  else:
    dvc_id = "%(dvc_id)s" % dvc_rec
    acct = ""
  out(("%%s(%(state)s): %%sroot_dc:%(root_dc_name)s, realm:%(realm_name)s, slice:%%s, %%s\n" % dvc_rec) % (dvc_id, acct, dvc_rec["slice_ips"][0], string.join(res,", ")))

def shift_chunk(l,sz):
  r = l[:sz]
  del l[:sz]
  return r

def shift(l):
  r = l[0]
  del l[0]
  return r

spin = None

def main(args):
  spin_ip = "127.0.0.1"
  slice = ":"
  qas = 'spin.Device.getIDList(restrict={"state":"UNREACHABLE", "opsw_lifecycle":"MANAGED"})'
  dvc_ids = []
  inf = None
  of = None
  b_pp = 0
  while len(args) > 0:
    cur_arg = shift(args)
    if ( cur_arg == "--spin_ip" ):
      spin_ip = shift(args)
    elif ( cur_arg == "-q" ):
      qas = shift(args)
    elif ( cur_arg in ("-h", "--help") ):
      usage()
      sys.exit()
    elif ( cur_arg in ("-i", "-r") ):
      fn = shift(args)
      if ( of == None ):
        try:
          inf = gzip.open(fn)
        except:
          err("%s: Unable to open for reading.\n", (fn,))
      else:
        err("%s: Already specified \"-o\", ignoring\n", (fn,))
    elif ( cur_arg in ("-o", "-w") ):
      fn = shift(args)
      if ( inf == None ):
        try:
          if (fn[-7:] != '.pkl.gz'):
            fn = "%s.pkl.gz" % fn
          of = gzip.open(fn,'w')
          err("Records will be written to %s\n", (fn,))
        except:
          err("%s: Unable to open for writing.\n", (fn,))
      else:
        err("%s: Already specified \"-i\", ignoring\n", (fn,))
    elif ( cur_arg == "--pp" ):
      b_pp = 1
    elif ( cur_arg == "-s" ):
      slice = shift(args)
    elif ( cur_arg == "-v" ):
      global g_b_verbose
      g_b_verbose = 1
    else:
      if ( is_num(cur_arg) ):
        dvc_ids.append(cur_arg)
      else:
        err("%s: Unrecognized argument.\n\n", (cur_arg,))
        usage()
        sys.exit(1)
  global spin
  try:
    if ( inf == None ):
      from coglib import spinwrapper
      spin = spinwrapper.SpinWrapper(url="https://%s:1004" % spin_ip)
      sys.path.append("/opt/opsware")
      global shuffle
      from waybot.base.shuffle import shuffle
      if ( len(dvc_ids) == 0 ):
        out("query: %s\n\n", (qas,))
        dvc_ids = eval(qas)
      dvc_ids = map(str_id, dvc_ids)
      dvc_ids.sort(lambda a,b:cmp(long(a),long(b)))
      dvc_ids = eval("dvc_ids[%s]" % slice)

      err("Retreiving %d device records", (len(dvc_ids),))
      dvc_recs = get_device_recs(dvc_ids)
      dvc_recs.sort(lambda a,b:cmp(long(a["dvc_id"]),long(b["dvc_id"])))
      err("\n")

      err("Retreiving device roles for %d devices", (len(dvc_recs),))
      get_device_role_ids(dvc_recs)
      err("\n")

      err("Retreiving accounts for %d devices", (len(dvc_recs),))
      get_dc_and_accts(dvc_recs)
      err("\n")

      err("Loading comm test data for %d devices\n", (len(dvc_recs),))
      c = 0
      for dvc_rec in dvc_recs:
        c = c + 1
        err("\r%d/%d ", (c,len(dvc_recs)))
        load_comm_test_results(dvc_rec, dvc_rec['dvc_role_id'])
        calc_slice_affinity(dvc_rec)
        if ( of != None ):
          cPickle.dump(dvc_rec, of)
        if ( (of == None) or (b_pp) ):
          pp_dvc_rec(dvc_rec)
      if ( of != None ): of.close()
    else:
      try:
        c = 0
        while 1:
          c = c + 1
          dvc_rec = cPickle.load(inf)
          err("\r%d " % c)
          pp_dvc_rec(dvc_rec)
      except:
#        err(string.join( apply( traceback.format_exception, sys.exc_info() ), ""))
        pass
  except KeyboardInterrupt, e:
    err("Interrupted by user.")
  err("\n")

if ( __name__ == "__main__" ):
  main(sys.argv[1:])

# Rewrite of dump_session from the ground up with the following goals in mind:
#
# feature todo:
# [X] multi-pickle indexed gzipped output for scalability.
# [X] Only capture one copy of each object.
# [X] Capture session metadata
# [X] Capture more info on which slice session was executed.
#     ("Ran On" pseudo field in session.)
# [X] Follow sessions linked via session metadata.
# [X] Follow child/parent sessions.
# [X] prevent numbers from being cast to strings.
# [X] dump and html combined into one utility.
# [X] line numbers on wayscript version source code.
# [X] capture referenced device and realm info. (initiator field)
# [X] resolve SessionCommand.module field.
# [X] resolve SessionCommand.step field.
# [X] resolve Session.host_name field.
# [X] Options to list last n sessions per core.
# [X] capture and resolve Session.account_ids pseudo field.
# [X] capture Account.getDictItems pseudo field.
# [ ] capture and resolve MegaServiceinstance.data_center_id pseudo field.
# [ ] capture and resolve Device.data_center_id pseudo field.
# [ ] capture datacenter.getDictItems
# [ ] add realm info to the SessionCommand.srvc_inst_id field.
#
# arch todo:
# [X] Generalize the _mod mechanism to allow for field renaming and ordering.
#     (Now we have a _full and _fmt class based overrides.)
# [X] Impliment Oid class.
# [X] Use isinstance() to determine whether or not to html_escape body objects.
# [ ] change ex_ so that caller creates ex_obj and passes it in.
#

import sys, os, time, string, gzip, zlib, base64, types, cPickle, traceback, struct, pprint

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

g_dbg_level=0
def dbg(s, level, args=None):
  if ( g_dbg_level >= level ):
    err("DEBUG%d: %s: %s\n" % (level, time.ctime(time.time()), s), args)

def link(src_node, dst_node):
  dbg("link(%s, %s)", 1, (repr(src_node), repr(dst_node)))
  if ( os.path.exists(dst_node) ): os.unlink(dst_node)
  os.link(src_node, dst_node)

def shift(l):
  ret = l[0]
  del l[0]
  return ret

def shift_len(l, len):
  ret = l[:len]
  del l[:len]
  return ret

def uniq(l):
  m = {}
  for i in l:
    m[i] = 0
  return m.keys()

def dict_get_with_init(dict, key, init_val):
  ret = dict.get(key, init_val)
  if ( ret == init_val ): dict[key] = ret
  return ret

def tup_join(tup, item):
  return tuple(reduce(lambda a,b:a+b, apply(map, (None,)+(tup, (item,)*len(tup))))[:-1])

def pull(m, k, def_val="---"):
  ret = def_val
  if ( m is not None ):
    if ( m.has_key(k) ):
      ret = m[k]
      del m[k]
    if ( ret is None ): ret = def_val
  return ret

def usage():
  err("""Usage: %s [<session_id> ...] [<session_file> ...] [-h] [-l <num>] [-d<num>]

Utility for extracting and formatting sessions and their commands from the 
database.

  <session_id> ...
     One or more session ids from the database.  These sessions will be dumped 
     to a gzipped multi-pickle file named "<session_id>.pkl.gz" in the current 
     working directory.

  <session_file> ...
     One or more previous dumped "<session_id>.pkl.gz" files.  These files will
     be processed and converted into a static HTML directory structure 
     resembling the waybot's backend web UI.  Like the old "html_session.py".

  -h
     This help screen.

  -l <num>
     Will emit to stdout the last <num> sessions executed on each core in the 
     mesh.  If <num> is omitted, then 10 is assumed.  (<num> can only be 
     omitted when -l is the last argument on the command line.

  -d<num>
     Increase the debug level from 0 by <num>.
""", sys.argv[0])

class DumbPklCache:
  """Open ended dictionary backed cache implimentation."""
  def __init__(self, maxsize):
    self._cache = {}

  def get(self, key):
    skey = str(key)
    if ( not self._cache.has_key(skey) ): return ()
    return (cPickle.loads(self._cache[skey]),)

  def put(self, key, val):
    self._cache[str(key)] = cPickle.dumps(val)

class CacheRecord:
  def __init__(self, key, val):
    self.key = key
    self.val = val
    self.prev = self
    self.next = self

  def rm(self):
    self.prev.next = self.next
    self.next.prev = self.prev
    self.prev = self.next = self

  def move_to_after(self, cr):
    self.next.prev = self.prev
    self.prev.next = self.next
    self.prev = cr
    self.next = cr.next
    cr.next.prev = self
    cr.next = self

class PklCache:
  """Generic cache implementation.  Not designed to be super duper efficient, but
designed to be:  (1) space bounded as opposed to an opened ended dictionary, and
(2) more effecient than talking to the spin via XMLRPC.  As the name of this
implementation suggest, the values are serialized as pickles.
"""
  def __init__(self, maxsize):
    if ( maxsize < 1 ): raise ValueError("<maxsize> must be greater than 0")
    self._tail = None
    self._cache = {}
    self._cursize = 0
    self._maxsize = maxsize

  def get(self, key):
    cr = self._cache.get(str(key), None)
    if ( cr is None ): return ()
    if ( cr is self._tail ):
      self._tail = cr.prev
    else:
      cr.move_to_after(self._tail)
    return (cPickle.loads(cr.val),)

  def put(self, key, val):
    skey = str(key)
    sval = cPickle.dumps(val)

    if ( cr is None ): cr = CacheRecord(skey, sval)
    self._cache[skey] = cr
    if ( self._tail is None ):
      self._tail = cr
    else:
      cr.move_to_after(self._tail)
    self._cursize = self._cursize + len(sval)
    while ( self._cursize > self._maxsize ):
      self._purge_lru()

  def _purge_lru(self):
    if ( len(self._cache) == 1 ):
      self._cache.clear()
      self._cursize = 0
      self._tail = None
    else:
      cr = self._tail
      self._tail = cr.prev
      cr.rm()
      del self._cache[cr.key]
      self._cursize = self._cursize - len(cr.val)

g_spin = None
g_spin_url = "https://127.0.0.1:1004"
MAX_SPIN_CHUNK_SIZE = 900
def get_spin():
  global g_spin
  if ( not g_spin ):
    from coglib import spinwrapper

    # import opsware_common.errors into the global namespace.
    global errors
    oc = __import__('opsware_common', globals(), locals(), ['errors'])
    errors = oc.errors

    # Import lcxmlrpclib into the global namespace.
    global lcxmlrpclib
    xmlrpc = __import__('librpc.xmlrpc', globals(), locals(), ['lcxmlrpclib'])
    lcxmlrpclib = xmlrpc.lcxmlrpclib

    g_spin = spinwrapper.SpinWrapper(g_spin_url)
  return g_spin

def decode_spin_val( val ):
  try:
    # try to decode the object as XML
    val = lcxmlrpclib.decode( val )
  except:
    try:
      # maybe it's an old eval'd object
      val = eval( val )
    except:
      # sometimes a string is just a string
      pass
  return val

def get_child_chunked_dicts(spin, pobj_ids, pobj_id_fld, key_class, key_id_fld, key_name_fld, val_class):
  pobjs_dicts = {}
  key_names = {}
  key_recs = spin_call_raw(spin, "%s.getList" % key_class, kwargs={'restrict':{pobj_id_fld:pobj_ids},'fields':[pobj_id_fld, key_name_fld]})
  for kr in key_recs:
    key_names[kr[0]] = (kr[1], kr[2])
  key_ids = map(lambda kr:str_id(kr[0]), key_recs)
  if ( key_ids ):
    while key_ids:
      key_ids_chunk = shift_len(key_ids, MAX_SPIN_CHUNK_SIZE)
      val_recs = spin_call_raw(spin, "%s.getList" % val_class, kwargs={"restrict":{key_id_fld:key_ids_chunk}, 
                                                                     "fields":[key_id_fld, 'text_order', 'text_data']})
      for vr in val_recs:
        knr = key_names[vr[1]]; pobj_id = str_id(knr[0]); kn = knr[1]
        dict = dict_get_with_init(pobjs_dicts, pobj_id, {})
        v = dict_get_with_init(dict, kn, [])
        v.append((vr[2], vr[3]))
  # Combine and decode the chunked dictionary values.
  for pobj_id in pobjs_dicts.keys():
    dict = pobjs_dicts[pobj_id]
    for key_id in dict.keys():
      v = dict[key_id]
      v.sort(lambda a,b:cmp(a[0],b[0]))
      v = decode_spin_val(string.join(map(lambda vi:vi[1], v), ''))
      dict[key_id] = v
  return pobjs_dicts

g_spin_call_raw_cache = DumbPklCache(0)
def spin_call_raw_cached(spin, xmlrpc_mthd, args=(), kwargs={}):
  key = cPickle.dumps((xmlrpc_mthd, args, kwargs))
  cval = g_spin_call_raw_cache.get(key)
  if ( len(cval) == 1 ):
    return cval[0]
  else:
    val = spin_call_raw(spin, xmlrpc_mthd, args, kwargs)
    val = sanitize_spin_result(val)
    g_spin_call_raw_cache.put(key, val)
    return val

def spin_call_raw(spin, xmlrpc_mthd, args=(), kwargs={}):
  dbg("SC: %s(args=%s, kwargs=%s)", 2, (xmlrpc_mthd, args, kwargs))
  return apply(getattr(spin, xmlrpc_mthd), args, kwargs)

# Cached version of spin_call.
g_spin_call_cache = DumbPklCache(0)
def spin_call_cached(spin, xmlrpc_mthd, args=(), kwargs={}):
  key = cPickle.dumps((xmlrpc_mthd, args, kwargs))
  cval = g_spin_call_cache.get(key)
  if ( len(cval) == 1 ):
    return cval[0]
  else:
    val = spin_call_raw(spin, xmlrpc_mthd, args, kwargs)
    val = sanitize_spin_result(val)
    g_spin_call_raw_cache.put(key, val)
    return val

# Invokes given spin call and if an exception occurs packages it as a string 
# and returns it.
def spin_call(spin, xmlrpc_mthd, args=(), kwargs={}, ret_ex=1):
  try:
    return spin_call_raw(spin, xmlrpc_mthd, args, kwargs)
  except:
    if ( ret_ex ):
      return string.join( apply( traceback.format_exception, sys.exc_info() ), "")
    else:
      dbg(string.join( apply( traceback.format_exception, sys.exc_info() ), ""), 1)
      return None

def format_rows(rows, col_sep=' '):
  if ( not rows ): return ''
  num_cols = len(rows[0])
  col_maxes = range(num_cols)
  for cur_col in col_maxes:
    col_maxes[cur_col] = max(map(lambda r,cc=cur_col:len(str(r[cc])), rows))
  fmt = string.join(["%%-%ds"] * num_cols, col_sep) % tuple(col_maxes)
  return string.join(map(lambda r,f=fmt:f % r, rows), '\n') + '\n'

def list_last_sessions(num):
  spin = get_spin()
  dc_ids = spin.DataCenter.getIDList(restrict={'status':'ACTIVE','ontogeny':'PROD'})
  for dc_id in dc_ids:
    sess_recs = spin.Session.getList(restrict={'session_id':("*%04.d" % dc_id)}, fields=['start_dt','session_desc'])
    sess_recs = filter(lambda sr:not (sr[1]==None), sess_recs)
    sess_recs = map(lambda sr:(sr[0],str(sr[1]),repr(sr[2])), sess_recs)
    sess_recs.sort(lambda a,b:cmp(a[1],b[1]))
    out(format_rows([("Session ID","Start Date","Session Desc")] + sess_recs[-num:], ' | ') + '\n')

g_sanitize_spin_results_builtin_types = map(lambda k:getattr(types,k), filter(lambda k:k[-4:]=='Type', types.__dict__.keys()))
def sanitize_spin_result(obj):
  if ( type(obj) == types.DictType ):
    m = {}
    for k in obj.keys():
      m[k] = sanitize_spin_result(obj[k])
    return m
  elif ( type(obj) in (types.ListType, types.TupleType) ):
    l = []
    for i in obj:
      l.append(sanitize_spin_result(i))
    if ( type(obj) == types.TupleType ): l = tuple(l)
    return l
  elif ( hasattr(obj, "data") ):
    return sanitize_spin_result(obj.data)
  elif ( type(obj) not in g_sanitize_spin_results_builtin_types ):
    return str(obj)
  else:
    return obj

def str_id(id):
  if (type(id) in (types.IntType, types.LongType)):
    return "%d" % id
  else: return str(id)

class OidStack:
  def __init__(self):
    self._moids = {}
    self._seen_soids = []

  def append(self, oid):
    soid = str(oid)
    if ( soid in self._seen_soids ): return
    cls_oids = dict_get_with_init(self._moids, oid.cls, [])
    cls_oids.append(oid)
    self._seen_soids.append(soid)

  def extend(self, oids):
    for oid in oids:
      self.append(oid)

  def pull_oids(self):
    if ( len(self._moids) > 0 ):
      cls = self._moids.keys()[0]
      oids = self._moids[cls]
      del self._moids[cls]
      return oids
    else:
      return None

  def has_more(self):
    return len(self._moids) > 0

class Oid:
  def __init__(*args):
    self = args[0]
    if ( len(args) == 3 ):
      self.cls = args[1]
      self.id = args[2]
      if ( type(self.id) != types.StringType ): self.id = "%d" % self.id
    elif ( len(args) == 2 ):
      self.cls, self.id = string.split(args[1], ':')
    else:
      raise TypeError("Oid%s: Invalid arguments" % str(args[1:]))
  def __str__(self):
#    if ( type(self.id) != types.StringType ): self.id = "%d" % self.id
    return "%s:%s" % (self.cls, self.id)

def oid_of_obj(obj):
  return Oid(obj['obj_class'],obj['id'])

class ObjWritter:
  """Class used for writting out a bundle of spin object dictionaries.  Will create
an internal index random access.  Expected general usage pattern is:

  (1) ObjWritter(<outfile>)
  (2) emit_obj() several times.
  (3) finalize() - signifies we are done emitting objects and the index can be
      packaged and appended to the archive, and the whole archive is gzipped.
"""
  def __init__(self, outfilename):
    self.outfile = gzip.open(outfilename,'w')
    self.count = 0
    self.index = {}
    self.finalized = 0

  def emit_raw(self, obj):
    obj_pkl = cPickle.dumps(obj)
    self.count = self.count + len(obj_pkl)
    self.outfile.write(obj_pkl)

  def emit_obj(self, oid, obj):
    if (self.finalized):
      raise ValueError("ObjWritter @%S finalized." % id(self))

    # Enter this oid into the index.
    soid = str(oid)
    self.index[soid] = self.count

    # Emit the raw object.
    dbg("emit_obj(%s)", 1, soid)
    self.emit_raw(obj)

  def finalize(self):
    """Closes the object writting session and appends the built index to the end of 
the output stream.
"""
    if (self.finalized):
      raise ValueError("ObjWritter @%S already finalized." % id(self))

    idx_pkl = cPickle.dumps(self.index)
    idx_pkl_len = len(idx_pkl)
    self.outfile.write(idx_pkl)
    self.outfile.write(struct.pack("<I", idx_pkl_len))
    self.outfile.close()
    self.finalized = 1

  def seen_before(self,oid):
    """Whether or not this object writter has written an object with the given <oid>."""
    return self.index.has_key(str(oid))

class ObjReader:
  def __init__(self, infilename):
    # Decompress the input file.
    self._init_infile(infilename)

    # Extract the index from the file.
    self._extract_index()

  def _init_infile(self, infilename):
    # Decompression 
    fi = gzip.open(infilename)
    fo_name = infilename
    if ( fo_name[-3:] == '.gz' ): fo_name = fo_name[:-3]
    else: fo_name = fo_name + '.decompressed'
    self.infile = open(fo_name,'w+')
    os.unlink(fo_name)
    BS = 4096
    buf = fi.read(BS)
    while (len(buf) > 0):
      self.infile.write(buf)
      buf = fi.read(BS)
    self.infile.flush()
    fi.close()

  def _extract_index(self):
    # Find out the file length.
    file_len = os.fstat(self.infile.fileno())[6]

    # Seek to the begining of the index length record. (last 4 bytes).
    self.infile.seek(file_len-4)

    # Read in the index length.
    idx_len = struct.unpack("<I", self.infile.read(4))[0]

    # Seek to the begining of the index pkl.
    self.infile.seek(file_len-4-idx_len)

    # Extract the index.
    self.index = cPickle.load(self.infile)

  def get_soids(self):
    return self.index.keys()

  def has_oid(self, oid):
    return self.index.has_key(str(oid))

  def get(self, oid):
    soid = str(oid)
    if ( self.index.has_key(soid) ):
      self.infile.seek(self.index[soid])
      return cPickle.load(self.infile)
    else:
      return None

def ex_obj_class(obj_class):
  return "%s.ex" % obj_class

def new_ex_obj(obj):
  return {'obj_class':ex_obj_class(obj['obj_class']), 'id':str_id(obj['id'])}

def update_with_ex_obj(o_r, obj):
  obj_ex = o_r.get(Oid("%s.ex" % obj['obj_class'], obj['id']))
  pull(obj_ex, 'id')
  pull(obj_ex, 'obj_class')
  if ( obj_ex is not None ):
    obj.update(obj_ex)

# Display an info message if the size is greater than some threshold.
def bulk_info(msg, args, size, threshold=30):
  if ( size >= threshold ):
    info(msg, args)

def ex_Session(spin, objs, oid_stack):
  # List of extension objects.
  ex_objs = []

  # get all the sids.
  sids = map(lambda o:str_id(o['id']), objs)

  # Grab the parameters of every session.
  bulk_info("Gathering parameters for %d sessions...", (len(sids),), len(sids))
  all_params = get_child_chunked_dicts(spin, sids, "session_id", "_SessionParam", "session_param_id", "session_param_name", "_SessionParamValue")

  # Grab the results of every session.
  bulk_info("Gathering results for %d sessions...", (len(sids),), len(sids))
  all_results = get_child_chunked_dicts(spin, sids, "session_id", "_SessionResult", "session_result_id", "session_result_name", "_SessionResultValue")

  # Grab the set of accounts for each session.
  all_acct_ids = {}
  perm_acct_ids = {}
  sessp_recs = spin_call_raw(spin, "SessionPermission.getList", kwargs={"restrict":{"session_id":sids},
                                                                        "fields":["session_id", "permission_id"]})
  # (TODO: it is theoretically possible that len(perm_ids) could be > 1000, which would cause an ORA error.)
  perm_ids = uniq(map(lambda p:p[2], sessp_recs))
  if ( perm_ids ):
    perm_recs = spin_call_raw_cached(spin, "SecurityPermission.getList", 
                                           kwargs={"restrict":{"permission_id":perm_ids},
                                                   "fields":["acct_id"]})
    for pr in perm_recs:
      perm_acct_ids[pr[0]] = pr[1]
      oid_stack.append(Oid("Account",pr[1]))
    for sessp_rec in sessp_recs:
      sid = str_id(sessp_rec[1]); perm_id = sessp_rec[2]
      acct_ids = dict_get_with_init(all_acct_ids, sid, [])
      acct_ids.append(perm_acct_ids[perm_id])

  # Grab the child session ids for every session.
  bulk_info("Gathering child sessions for %d sessions...", (len(sids),), len(sids))
  child_sess_recs = spin_call_raw(spin, "Session.getList", kwargs={"restrict":{"parent_session_id":sids},
                                                                    "fields":["parent_session_id"]})
  all_child_sessions = {}
  for csr in child_sess_recs:
    child_session_ids = dict_get_with_init(all_child_sessions, str_id(csr[1]), [])
    sid = str_id(csr[0])
    child_session_ids.append(sid)
    oid_stack.append(Oid("Session", sid))

  # Grab the list of child SessionCommand ids for all sessions.
  bulk_info("Gathering child commands for %d sessions...", (len(sids),), len(sids))
  child_cmd_recs = spin_call_raw(spin, "SessionCommand.getList", kwargs={"restrict":{"session_id":sids},
                                                                         "fields":["session_id"]})
  all_child_cmds = {}
  for ccr in child_cmd_recs:
    child_cmd_ids = dict_get_with_init(all_child_cmds, str_id(ccr[1]), [])
    cid = str_id(ccr[0])
    child_cmd_ids.append(cid)
    oid_stack.append(Oid("SessionCommand", cid))

  # Grab the metadata.
  bulk_info("Gathering metadata for %d sessions...", (len(sids),), len(sids))
  all_sess_metadata = {}
  sess_md_recs = spin_call_raw(spin, "_SessionMetaData.getList", kwargs={"restrict":{"session_id":sids},
                                                                         "fields":["session_id","key_name","key_value"]})
  for smdr in sess_md_recs:
    sess_md = dict_get_with_init(all_sess_metadata, str_id(smdr[1]), {})
    sess_md[smdr[2]] = smdr[3]

  # Itterate through each object and create an extension object.
  bulk_info("Sorting gathered data for %d sessions...", (len(sids),), len(sids))
  for obj in objs:
    # Create and register a new extension object.
    ex_obj = new_ex_obj(obj)
    ex_objs.append(ex_obj)

    # Get the session id of the current object.
    sid = ex_obj['id']

    # Assign the parameters of this obj.
    params = all_params.get(sid, None)
    if ( params is not None ): ex_obj['getParams'] = params

    # Push any dvc_ids from the params onto the oid stack.
    if ( type(params) == types.DictType ):
      dvc_ids = params.get('dvc_ids', None)
      if ( type(dvc_ids) in (types.ListType, types.TupleType) ):
        oid_stack.extend(map(lambda dvc_id:Oid("Device", dvc_id), dvc_ids))

    # Assign the results of this obj.
    result = all_results.get(sid, None)
    if ( result is not None ): ex_obj['getResults'] = result

    # Grab the parent MegaServiceInstance (i.e. where this session was executed)
    msi_oid = Oid("MegaServiceInstance",obj['srvc_inst_id'])
    oid_stack.append(msi_oid)

    # Assign the list of account ids.
    acct_ids = all_acct_ids.get(sid, None)
    if ( acct_ids is not None ):  ex_obj['account_ids'] = acct_ids

    # If this session has a way script version.
    if ( obj['way_script_version_id'] ):
      oid_stack.append(Oid("WayScriptVersion", obj['way_script_version_id']))

    # Push the parent user oid onto the stack.
    oid_stack.append(Oid("SecurityUser", obj['user_id']))

    # Attempt to locate a dvc_id for the host_name, and append oids for the 
    # device and realm objects respectively.
    if ( '@' in obj['host_name'] ):
      realmful_ip = string.split(obj['host_name'], '@')
      if ( len(realmful_ip) == 2 ):
        realm_ids = spin_call_raw_cached(spin, "Realm.getIDList", kwargs={"restrict":{'realm_name':realmful_ip[1]}})
        if ( len(realm_ids) == 1):
          dvc_ids = spin_call_raw_cached(spin, "Device.getIDList", kwargs={"restrict":{'management_ip':realmful_ip[0], 'realm_id':realm_ids[0]}})
          if ( len(dvc_ids) == 1 ):
            ex_obj['host_name_dvc_id'] = dvc_ids[0]
            oid_stack.append(Oid("Realm", realm_ids[0]))
            oid_stack.append(Oid("Device", dvc_ids[0]))

    # Assign the list of child sessions.
    child_sessions = all_child_sessions.get(sid, None)
    if ( child_sessions is not None ):
      child_sessions.sort(lambda a,b:cmp(int(a[-3:]+a[:-3]), int(b[-3:]+b[:-3])))
      ex_obj['children_Session'] = child_sessions

    # Assign the list of child commands.
    child_cmds = all_child_cmds.get(sid, None)
    if ( child_cmds is not None ):
      child_cmds.sort()
      ex_obj['children_SessionCommand'] = child_cmds

    # Assign the metadata.
    md = all_sess_metadata.get(sid, None)
    if ( md is not None ):
      ex_obj["getMetadata"] = md
      if ( type(md) == types.DictType ):
        if ( md.get('NEXT_SESSION_ID',None) != None ):
          sid = str(md['NEXT_SESSION_ID'])
          info("Found subsession %s via NEXT_SESSION_ID metadata.", sid)
          oid_stack.append(Oid("Session", sid))
        if ( md.get('JOB_ID', None) != None ):
          sid = str(md['JOB_ID'])
          oid_stack.append(Oid("Session", sid))

  # Return the list of extention objects.
  return ex_objs

def ex_SessionCommand(spin, objs, oid_stack):
  # Extension objects.
  ex_objs = []

  # Aggrigate stuff here.

  # get all the command ids:
  cids = map(lambda o:str_id(o['id']), objs)

  # Grab the parameters for all commands.
  bulk_info("Gathering parameters for %d commands...", (len(cids),), len(cids))
  all_cmd_params = get_child_chunked_dicts(spin, cids, "session_cmd_id", "_SessionCommandParam", "session_cmd_param_id", "session_cmd_param_name", "_SessionCommandParamvalue")

  # Grab the results for all commands.
  bulk_info("Gathering results for %d commands...", (len(cids),), len(cids))
  all_cmd_results = get_child_chunked_dicts(spin, cids, "session_cmd_id", "_SessionCommandResult", "session_cmd_result_id", "session_cmd_result_name", "_SessionCommandResultvalue")

  # Itterate through each object individually.
  bulk_info("Sorting gathered data for %d commands...", (len(cids),), len(cids))
  for obj in objs:
    # Create a new extension object and register it for return.
    ex_obj = new_ex_obj(obj)
    ex_objs.append(ex_obj)

    # Get the command id.
    cid = ex_obj['id']

    # Assign parameters
    params = all_cmd_params.get(cid, None)
    if ( params is not None ):
      ex_obj['getParams'] = params

    # Assign cmd results.
    results = all_cmd_results.get(cid, None)
    if ( results is not None ):
      ex_obj['getResults'] = results
      if ( type(results)==types.DictType and results.get('$session_id',None)!=None ):
        sid = results['$session_id']
        oid_stack.append(Oid("Session", sid))

    # Push parent MegaServiceInstance onto oid stack. (i.e. SI this command targeted.)
    msi_oid = Oid("MegaServiceInstance",str(obj['srvc_inst_id']))
    oid_stack.append(msi_oid)

    # If this command has a way script version, push it onto the oid stack.
    if ( obj['way_script_version_id'] ):
      oid_stack.append(Oid("WayScriptVersion", obj['way_script_version_id']))

    # Resolve the oid of the calling wayscript/wayscript version.
    module = string.split(str(obj.get('module', '')), '~')
    if ( len(module) == 2 ):
      wss = spin_call_raw_cached(spin, "WayScript.getIDList", kwargs={"restrict":{'script_name':module[0]}})
      if ( len(wss) == 1 ):
        ex_obj['module_ws_id'] = wss[0]
        oid_stack.append(Oid("WayScript", wss[0]))
        wsvs = spin_call_raw_cached(spin, "WayScriptVersion.getIDList", kwargs={"restrict":{'way_script_id':wss[0], 
                                                                                'version': module[1]}})
        if ( len(wsvs) == 1 ):
          ex_obj['module_wsv_id'] = wsvs[0]
          oid_stack.append(Oid("WayScriptVersion", wsvs[0]))

  # Return the extension objects.
  return ex_objs

def ex_WayScriptVersion(spin, objs, oid_stack):
  # Extension objects to return
  ex_objs = []

  # itterate over every object.
  for obj in objs:
    # Create and register a new extension object.
    ex_obj = new_ex_obj(obj)
    ex_objs.append(ex_obj)

    # Get the way script version id.
    wsv_id = ex_obj['id']

    # Append the way script oid to the stack.
    oid_stack.append(Oid("WayScript", obj['way_script_id']))

    # Grab the source code for the script.
    ex_obj['getSource'] = spin_call_cached(spin, "WayScriptVersion.getSource", (wsv_id,))

  # Return the extension objects.
  return ex_objs

def ex_MegaServiceInstance(spin, objs, oid_stack):
  # Add a device oid to the stack to be pulled down.
  oid_stack.extend(map(lambda o:Oid("Device", o['dvc_id']), objs))

def ex_Device(spin, objs, oid_stack):
  # Add a realm oid to the stack to be pulled down.
  realm_ids = uniq(filter(lambda rid:rid is not None, map(lambda o:o.get('realm_id', None), objs)))
  oid_stack.extend(map(lambda rid:Oid("Realm", rid), realm_ids))

def ex_Account(spin, objs, oid_stack):
  # Extension objects
  ex_objs = []

  # Itterate through all objects.
  for obj in objs:
    # Extension object.
    ex_obj = new_ex_obj(obj)

    # Grab the dictionary items for this account.
    di = spin_call_cached(spin, "Account.getDictItems", (obj['id'],))
    if ( type(di) in (types.ListType, types.TupleType) ):
      m = {}
      for r in di:
        m[r[0]] = r[1]
      di = m
    ex_obj['getDictItems'] = di

  # Return the extension objects.
  return ex_objs

# Map of spin classes to their id field.  We could in theory glean this from 
# the spin dynamically via the spin schema reflection, but I don't trust that
# this API to always be accurate.
g_cls_id_flds = { \
  "Account"             : "acct_id",
  "DataCenter"          : "data_center_id",
  "Device"              : "dvc_id",
  "MegaServiceInstance" : "srvc_inst_id",
  "Realm"               : "realm_id",
  "SecurityUser"        : "user_id",
  "ServiceInstance"     : "srvc_inst_id",
  "Session"             : "session_id",
  "SessionCommand"      : "session_cmd_id",
  "WayScript"           : "way_script_id",
  "WayScriptVersion"    : "way_script_version_id",
}

# Objects are generally dumped generically, then we invoke an extension
# function for certain classes that will emit a seperate record with extra
# information about the object.
def dump_spin_obj(spin, oid):
  """Dumps the object referenced by <oid> from the <spin> to a file named after the
class of the oid.  Cooperates with the various class extension function via an
oid stack in order to effect an itterative crawl of related objects and data.
"""
  # Create an object writter.
  of_name = "%s%s.pkl.gz" % (oid.cls, oid.id)
  info("Dumping session to %s", repr(of_name))
  ow = ObjWritter(of_name)
  dc = spin.sys.getDCFromDB()
  spin_ver = spin.sys.getVersion()
  ow.emit_obj(Oid("__Header.ex", 0),
              {'obj_class':'__Header.ex',
               'id':0, 'soid':str(oid),
               'spin_ver': spin_ver,
               'dc_id':str_id(dc['id']),
               'dc_display_name':dc['display_name']})

  # Create initial oid stack.
  oid_stack = OidStack()
  oid_stack.append(oid)

  # itterate over the oid_stack.
  while oid_stack.has_more():
    # TODO: sort the stack and pull the objects in groups of like class from 
    # the spin.  So that we minimize the number of XMLRPCs to the spin.

    # Pull a set of common class oids off the stack.
    oids = oid_stack.pull_oids()

    # Process the set of oids in chunks.
    ids = map(lambda o:o.id, oids)
    cls = oids[0].cls
    cls_id_fld = g_cls_id_flds[cls]
    while (ids):
      chunk_ids = shift_len(ids, MAX_SPIN_CHUNK_SIZE)
      bulk_info("Gathering %d %s records...", (len(chunk_ids), cls), len(chunk_ids))
      objs = spin_call_raw(spin, "%s.getAll" % cls, kwargs={"restrict":{cls_id_fld:chunk_ids}})

      # flatten spin objects into simple python data structures.
      objs = map(lambda o,ssr=sanitize_spin_result:ssr(o), objs)

      # itterate though each obtained object.
      found_ids = []
      for obj in objs:
        # Get the oid of the currently found object.
        oid = oid_of_obj(obj)
        found_ids.append(oid.id)

        # Let user know what we are currently emitting.
        info("Emitting %s", (oid,))

        # emit it.
        ow.emit_obj(oid, obj)

      # Invoke the corresponding extension function for this object's class.
      if ( len(objs) > 0 ):
        ex_objs = globals().get("ex_%s" % cls, lambda *args:None)(spin, objs, oid_stack)
        if ( ex_objs is not None ):
          for ex_obj in ex_objs:
            ow.emit_obj(oid_of_obj(ex_obj), ex_obj)

      # Calculate the set of oids that where not found and warn user.
      not_found_ids = filter(lambda oid,fi=found_ids:oid not in fi, chunk_ids)
      for id in not_found_ids:
        warn("Failed to locate %s in database" % Oid(cls, id))

  # Finalize the object writter.
  ow.finalize()

CSS = """
<!--
html { background: #e25923 ; color: black }
body { background: #e25923 ; color: black }
th { text-align: left }
h1 { text-align: center }
pre { margin-bottom: 0; margin-top: 0 }
-->
"""

def html_escape(s):
  s = string.replace(s, '&', "&amp;")
  s = string.replace(s, '<', "&lt;")
  s = string.replace(s, '>', "&gt;")
  s = string.replace(s, '"', "&quot;")
  return s

class HtmlElem:
  def __init__(*args, **attrs):
    self = args[0]
    self.body = list(args[1:])
    self.attrs = attrs

  def __str__(self):
    name = string.lower(self.__class__.__name__)
    body_html = ""
    if ( len(self.body) > 0 ):
      for body_item in self.body:
#        if ( type(body_item) == types.StringType ):
        if ( isinstance(body_item, HtmlElem) ):
          body_html = body_html + str(body_item)
        else:
          body_html = body_html + html_escape(str(body_item))
      if ( body_html == "" ): body_html = "&nbsp;"
    if ( name == 'htmlelemlist' ):
      return body_html
    else:
      attrs = ""
      if ( self.attrs ):
        attrs = []
        for k,v in self.attrs.items():
          k = string.replace(k,"_","-")
          if (v is None): attrs.append(str(k))
          else: attrs.append("%s=%s" % (k,repr(v)))
        attrs = ' ' + string.join(attrs, ' ')
      open_tag = "<%s%s>" % (name, attrs)
      if ( len(self.body) > 0 ):
        close_tag = "</%s>" % name
        html = "%s%s%s" % (open_tag, body_html, close_tag)
        if ( name not in ("a",) ): html = html + '\n'
        return html
      else:
        return open_tag

class Table(HtmlElem): pass
class Td(HtmlElem): pass
class Tr(HtmlElem): pass
class Pre(HtmlElem): pass
class Meta(HtmlElem): pass
class Title(HtmlElem): pass
class Style(HtmlElem): pass
class Br(HtmlElem): pass
class Html(HtmlElem): pass
class Head(HtmlElem):pass
class Body(HtmlElem): pass
class Hr(HtmlElem): pass
class H1(HtmlElem): pass
class H2(HtmlElem): pass
class B(HtmlElem): pass
class I(HtmlElem): pass
class Font(HtmlElem): pass
class A(HtmlElem): pass
class Center(HtmlElem): pass
class Img(HtmlElem): pass
class A(HtmlElem): pass
class HtmlElemList(HtmlElem): pass

class HtmlPage:
  def __init__(self, title=None, style=None):
    self.head = []
    self.body = []
    self.head.append(Meta(http_equiv="content-type", content="text/html; charset=UTF-8",))
    if ( title is not None ):
      self.head.append(Title(title))
    if ( style is not None ):
      self.head.append(Style(style, type="text/css"))

  def __str__(self):
    return str(Html(
                 apply(Head, self.head),
                 apply(Body, self.body),
               ))

  def write(self, out_path):
    info(out_path)
    open(out_path,'w').write(str(self))

def _html_cell_value(val, def_val="---"):
  # If the value is a multi-line string, then wrap in a <pre>.
  if ( (type(val) == types.StringType) and (string.find(val,'\n') > -1) ): val = Pre(val)
  return val

def obj_html_file_name(oid):
  return "%s%s.html" % (oid.cls, oid.id)

def obj_html_path(out_dir, oid):
  return "%s/%s" % (out_dir, obj_html_file_name(oid))

g_html_page_header = []
g_html_page_footer = []

def html_generic_(o_r, oid, out_dir):
  # Load the referenced object and parse the oid.
  obj = o_r.get(oid)
  if ( obj is None ): return

  # Create html page and setup header info.
  page = HtmlPage(title=("%s %s Details" % (oid.cls, oid.id)), style=CSS)
  page.body.append(g_html_page_header)
  page.body.append(H2("%s %s Details" % (oid.cls, oid.id)))

  # Combine extension record into main record.
  update_with_ex_obj(o_r, obj)

  # Main object table.
  page.body.append(obj_to_html_tab(o_r, obj))

  # Append the standard footer, calculate the output path, and write.
  page.body.append(g_html_page_footer)
  out_path = obj_html_path(out_dir, oid)
  page.write(out_path)

def _append_dict_to_html_tab_rows(tab_rows, key, dict, def_val="---"):
  if ( len(dict) == 0 ):
    tab_rows.append(Tr(Td(key), Td(def_val,colspan=2)))
  else:
    items = dict.items()
    items.sort(lambda a,b:cmp(a[0],b[0]))
    k,v = items[0]
    del items[0]
    tab_rows.append(Tr(Td(key, rowspan=len(dict)), Td(k), Td(_html_cell_value(v, def_val))))
    for k,v in items:
      tab_rows.append(Tr(Td(k), Td(_html_cell_value(v, def_val))))

def obj_to_html_tab(o_r, obj):
  "<obj> is assumed to be a dictionary.\n"
  top_fields = []
  bot_fields = [("conflicting","conflicting"),
                ("tran_id","tran_id")]
  def_cell_val = "---"

  # New table.
  tab = Table(border=1)

  # Attempt to call out to html_<cls>_fmt() function.
  cls = pull(obj, 'obj_class', None)
  id = pull(obj, 'id')
  if ( cls is not None ):
    globals().get("html_%s_fmt" % cls, lambda *args:None)(o_r, obj, top_fields, bot_fields)

  # Top fields
  for field in top_fields:
    k = field[1]
    v = pull(obj, k, def_cell_val)
    if ( type(v) == types.DictType ):
      _append_dict_to_html_tab_rows(tab.body, field[0], v, def_cell_val)
    else:
      tab.body.append(Tr(Td(field[0]), Td(_html_cell_value(v, def_cell_val), colspan=2)))

  # Bottom fields
  bot_rows = []
  for field in bot_fields:
    k = field[1]
    v = pull(obj, k, def_cell_val)
    if ( type(v) == types.DictType ):
      _append_dict_to_html_tab_rows(bot_rows, field[0], v, def_cell_val)
    else:
      bot_rows.append(Tr(Td(field[0]), Td(_html_cell_value(v, def_cell_val), colspan=2)))

  # Middle fields
  keys = obj.keys()
  keys.sort()
  for k in keys:
    v = obj[k]
    if ( type(v) == types.DictType ):
      _append_dict_to_html_tab_rows(tab.body, k, v, def_cell_val)
    else:
      tab.body.append(Tr(Td(k), Td(_html_cell_value(v, def_cell_val), colspan=2)))

  # Append bottom fields and return result.
  tab.body.extend(bot_rows)
  return tab

def mk_html_obj_link(oid, body):
  return A(body, href=obj_html_file_name(oid))

def html_MegaServiceInstance_fmt(o_r, obj, top_fields, bot_fields):
  dvc_id = obj['dvc_id']
  dvc_oid = Oid("Device", dvc_id)
  dvc = o_r.get(dvc_oid)
  obj['dvc_id'] = mk_html_obj_link(dvc_oid, "%s (%s)" % (dvc['system_name'], dvc_id))

def html_Device_fmt(o_r, obj, top_fields, bot_fields):
  dvc_id = obj['dvc_id']
  dvc_oid = Oid("Device", dvc_id)
  obj['dvc_id'] = mk_html_obj_link(dvc_oid, dvc_id)

  realm_id = obj['realm_id']
  realm_oid = Oid("Realm", realm_id)
  realm = o_r.get(realm_oid)
  obj['realm_id'] = mk_html_obj_link(realm_oid, "%s (%s)" % (realm_id, realm['realm_name']))

def html_Session_fmt(o_r, sess, top_fields, bot_fields):
  top_fields.extend([ \
    ("Session ID"  , "session_id"),
    ("Status"      , "status"),
    ("Script"      , "way_script_version_id"),
    ("Username"    , "user_id"),
    ("Initiator"   , "host_name"),
    ("Ran On"      , "srvc_inst_id"),
    ("Accounts"    , "account_ids"),
    ("Sched time"  , "sched_dt"),
    ("Start time"  , "start_dt"),
    ("End time"    , "end_dt"),
    ("Agent name"  , "agent_name"),
    ("Owner name"  , "owner_name"),
    ("Description" , "session_desc"),
    ("Params"      , "getParams"),
    ("Results"     , "getResults"),
    ("Metadata"    , "getMetadata"),
  ])

  # user_id field.
  su_oid = Oid("SecurityUser", sess['user_id'])
  su = o_r.get(su_oid)
  if ( su ):
    sess['user_id'] = mk_html_obj_link(su_oid, su['username'])

  # way_script_version_id field
  way_script_version_id = sess.get('way_script_version_id', None)
  if ( way_script_version_id is not None ):
    wsv_oid = Oid("WayScriptVersion", way_script_version_id)
    wsv = o_r.get(wsv_oid)
    ws_oid = Oid("WayScript", wsv['way_script_id'])
    ws = o_r.get(ws_oid)
    sess['way_script_version_id'] = HtmlElemList(mk_html_obj_link(ws_oid, ws['script_name']), 
                                                 '~',
                                                 mk_html_obj_link(wsv_oid, wsv['version']))

  # host_name field:
  host_name = sess['host_name']
  if ( string.lower(host_name[:8]) == "session:" ):
    sess['host_name'] = mk_html_obj_link(Oid("Session", host_name[8:]), host_name)
  elif ( '@' in host_name ):
    host_name_dvc_id = pull(sess, 'host_name_dvc_id')
    if ( host_name_dvc_id is not None ):
      sess['host_name'] = mk_html_obj_link(Oid("Device", host_name_dvc_id), host_name)

  # srvc_inst_id field:
  msi_oid = Oid("MegaServiceInstance", pull(sess, 'srvc_inst_id', None))
  msi = o_r.get(msi_oid)
  if ( msi is not None ):
    sess['srvc_inst_id'] = mk_html_obj_link(msi_oid, "%s/%s (%s)" % (msi['system_name'], msi['mid'], msi['ip_address']))

  # account_ids field:
  acct_ids = sess.get('account_ids', None)
  if ( type(acct_ids) == types.ListType ):
    accts = HtmlElemList("[")
    c = 1
    for acct_id in acct_ids:
      aoid = Oid("Account", acct_id)
      acct = o_r.get(aoid)
      if ( acct is not None ): acct_link_body = acct['acct_name']
      else: acct_link_body = acct_id
      accts.body.append(mk_html_obj_link(aoid, acct_link_body))
      if ( c < len(acct_ids) ): accts.body.append(', ')
      c = c + 1
    accts.body.append("]")
    sess['account_ids'] = accts

  # getParams field:
  params = sess.get('getParams', None)
  if ( type(params) == types.DictType ):
    dvc_ids = params.get('dvc_ids', None)
    if ( type(dvc_ids) in (types.ListType, types.TupleType) ):
      params['dvc_ids'] = apply(HtmlElemList, ("[",) + tup_join(map(lambda dvc_id:mk_html_obj_link(Oid("Device", dvc_id), dvc_id), dvc_ids), ', ') + ("]",))

  # getMetadata field:
  md = sess.get('getMetadata', None)
  if ( type(md) == types.DictType ):
    next_session_id = md.get('NEXT_SESSION_ID', None)
    if ( next_session_id is not None ):
      md['NEXT_SESSION_ID'] = mk_html_obj_link(Oid("Session", next_session_id), next_session_id)
    job_id = md.get('JOB_ID', None)
    if ( job_id is not None ):
      md['JOB_ID'] = mk_html_obj_link(Oid("Session", job_id), job_id)
    prev_session_id = md.get('PREV_SESSION_ID', None)
    if ( prev_session_id is not None ):
      md['PREV_SESSION_ID'] = mk_html_obj_link(Oid("Session", prev_session_id), prev_session_id)

def html_Session_full(o_r, oid, out_dir):
  cmd_fields = ( \
    ("ID"      , "session_cmd_id"),
    ("Host"    , "host"),
    ("Port"    , "port"),
    ("Method"  , "method"),
    ("Tag"     , "tag"),
    ("Status"  , "status"),
    ("Timeout?", "timeout_type"),
    ("Created" , "init_dt"),
    ("Finished", "end_dt"),
  )

  child_session_fields = ( \
    ("Session ID"  , "session_id"),
    ("Ran On"      , "srvc_inst_id"),
    ("Status"      , "status"),
    ("Sched time"  , "sched_dt"),
    ("Start time"  , "start_dt"),
    ("End time"    , "end_dt"),
  )
    
  sess = o_r.get(oid)
  if ( sess is None ): return
  page = HtmlPage(title=("Session %s Details" % oid.id), style=CSS)
  page.body.append(g_html_page_header)
  page.body.append(H2("%s %s" % (oid.cls, oid.id)))

  # Pull in data from the corresponding extension object.
  update_with_ex_obj(o_r, sess)

  # Grab the child sessions
  child_sess_ids = pull(sess, 'children_Session', [])

  # Grab the child session commands.
  cmd_ids = pull(sess,'children_SessionCommand', [])

  # Main table
  page.body.append(obj_to_html_tab(o_r, sess))

  # Commands table.
  page.body.append(Hr())
  cmds_tab = Table(border=1)
  cmds_tab.body.append(Tr(Td(Center("%d Command%s" % (len(cmd_ids),{1:'', 0:'s'}[len(cmd_ids)==1])), colspan=len(cmd_fields))))
  cmds_tab.body.append(apply(Tr, map(Td, map(lambda f:f[0], cmd_fields))))
  for cmd_id in cmd_ids:
    cmd = o_r.get(Oid("SessionCommand",cmd_id))
    if ( cmd is None ): continue
    cmd['session_cmd_id'] = mk_html_obj_link(Oid("SessionCommand", cmd_id), cmd_id)
    msi = o_r.get(Oid("MegaServiceInstance", cmd['srvc_inst_id']))
    if ( msi is not None ):
      cmd['host'] = mk_html_obj_link(Oid("MegaServiceInstance", msi['srvc_inst_id']), msi['system_name'])
      cmd['port'] = msi['port']
    else:
      cmd['host'] = Oid("MegaServiceInstance", cmd['srvc_inst_id'])
    cmds_tab.body.append(apply(Tr, map(lambda f,o=cmd,p=pull:Td(p(o,f[1])), cmd_fields)))
  page.body.append(cmds_tab)

  # Child sessions table.
  len_child_sess_ids = len(child_sess_ids)
  if ( len_child_sess_ids > 0 ):
    page.body.append(Hr())
    child_sesss_tab = Table(border=1)
    child_sesss_tab.body.append(Tr(Td(Center("%d Child Session%s" % (len_child_sess_ids,{1:'', 0:'s'}[len_child_sess_ids==1])), colspan=len(child_session_fields))))
    child_sesss_tab.body.append(apply(Tr, map(Td, map(lambda f:f[0], child_session_fields))))
    for child_sess_id in child_sess_ids:
      child_sess = o_r.get(Oid("Session",child_sess_id))
      if ( child_sess is None ): continue
      child_sess['session_id'] = mk_html_obj_link(Oid("Session", child_sess_id), child_sess_id)
      msi = o_r.get(Oid("MegaServiceInstance", child_sess['srvc_inst_id']))
      if ( msi is not None ):
        child_sess['srvc_inst_id'] = mk_html_obj_link(Oid("MegaServiceInstance", child_sess['srvc_inst_id']), msi['system_name'])
      else:
        child_sess['srvc_inst_id'] = Oid("MegaServiceInstance", child_sess['srvc_inst_id'])
      child_sesss_tab.body.append(apply(Tr, map(lambda f,o=child_sess,p=pull:Td(p(o,f[1])), child_session_fields)))
    page.body.append(child_sesss_tab)

  # Write the page out to file.
  page.body.append(g_html_page_footer)
  out_path = obj_html_path(out_dir, oid)
  page.write(out_path)

def html_SessionCommand_fmt(o_r, cmd, top_fields, bot_fields):
  top_fields.extend([ \
    ("Command ID"   , "session_cmd_id"),
    ("Status"       , "status"),
    ("Script"       , "way_script_version_id"),
    ("Timeout type" , "timeout_type"),
    ("Timeout time" , "timeout_dt"),
    ("Notified?"    , "notified"),
    ("Method"       , "method"),
    ("Tag"          , "tag"),
    ("Host"         , "srvc_inst_id"),
    ("Port"         , "port"),
    ("Service"      , "srvc_type"),
    ("Init time"    , "init_dt"),
    ("Poke time"    , "poke_dt"),
    ("Start time"   , "start_dt"),
    ("End time"     , "end_dt"),
    ("File"         , "module"),
    ("Line"         , "step"),
    ("Session"      , "session_id"),
    ("Params"       , "getParams"),
    ("Results"      , "getResults")
  ])

  # way_script_version_id field
  way_script_version_id = cmd.get('way_script_version_id', None)
  if ( way_script_version_id is not None ):
    wsv_oid = Oid("WayScriptVersion", way_script_version_id)
    wsv = o_r.get(wsv_oid)
    ws_oid = Oid("WayScript", wsv['way_script_id'])
    ws = o_r.get(ws_oid)
    cmd['way_script_version_id'] = HtmlElemList(mk_html_obj_link(ws_oid, ws['script_name']),
                                                '~',
                                                mk_html_obj_link(wsv_oid, wsv['version']))

  # srvc_inst_id field
  msi_oid = Oid("MegaServiceInstance", pull(cmd, 'srvc_inst_id'))
  msi = o_r.get(msi_oid)
  if ( msi is not None ):
    cmd['srvc_inst_id'] = mk_html_obj_link(msi_oid, "%s\%s (%s)" % (msi['system_name'], msi['mid'], msi['ip_address']))
    # port field
    cmd['port'] = msi['port']
    # srvc_type field:
    cmd['srvc_type'] = msi['srvc_type']
  else:
    cmd['srvc_inst_id'] = msi_oid

  # module field:
  module = string.split(str(cmd.get('module', '')), '~')
  if ( len(module) == 2 ):
    ws_id = pull(cmd, 'module_ws_id', None)
    if ( ws_id is not None ):
      module[0] = mk_html_obj_link(Oid("WayScript", ws_id), module[0])

    wsv_id = pull(cmd, 'module_wsv_id', None)
    if ( wsv_id is not None ):
      module[1] = mk_html_obj_link(Oid("WayScriptVersion", wsv_id), module[1])
      # step field:
      lno = cmd.get('step', None)
      if ( lno is not None ):
        cmd['step'] = mk_html_obj_link(Oid("WayScriptVersion", wsv_id), lno)
        cmd['step'].attrs['href'] = cmd['step'].attrs['href'] + '#%s' % lno

    cmd['module'] = HtmlElemList(module[0], '~', module[1])


  # session_id field:
  session_id = cmd['session_id']
  cmd['session_id'] = mk_html_obj_link(Oid("Session", session_id), session_id)

  # getParams field:
  params = cmd.get('getParams', None)
  if ( type(params) == types.DictType ):
    parent_id = params.get('$parent_id', None)
    if ( parent_id is not None ):
      params['$parent_id'] = mk_html_obj_link(Oid("Session", parent_id), parent_id)

  # getResults field:
  results = cmd.get('getResults', None)
  if ( type(results) == types.DictType ):
    session_id = results.get('$session_id', None)
    if ( session_id is not None ):
      results['$session_id'] = mk_html_obj_link(Oid("Session", session_id), session_id)

def html_WayScriptVersion_fmt(o_r, wsv, top_fields, bot_fields):
  top_fields.extend([ \
    ("ID"                       , "way_script_version_id"),
    ("Comments for this Version", "comments"),
    ("policy for this Version"  , "policy"),
    ("Version uploaded By"      , "uploaded_by")
  ])

  # way_script field:
  way_script_id = wsv['way_script_id']
  ws_oid = Oid("WayScript", way_script_id)
  wsv['way_script_id'] = mk_html_obj_link(ws_oid, way_script_id)

def html_WayScriptVersion_full(o_r, oid, out_dir):
  wsv = o_r.get(oid)
  if ( wsv is None ): return
  ws = o_r.get(Oid("WayScript", wsv['way_script_id']))
  ws_name = wsv['way_script_id']
  if ( ws is not None ): ws_name = ws['script_name']
  title = "Viewing all info about script %s version %s" % (ws_name, wsv['version'])
  page = HtmlPage(title=title, style=CSS)
  page.body.append(g_html_page_header)
  page.body.append(H2(title))

  # Pull in data from the corresponding extension object.
  update_with_ex_obj(o_r, wsv)

  # Extract the source code.
  src = pull(wsv, 'getSource')

  # Emit the raw source.
  raw_src_name = "%s_%s_%s.txt" % (oid.cls, ws_name, wsv['version'])
  raw_src_out_path = os.path.join(out_dir, raw_src_name)
  info(raw_src_out_path)
  open(raw_src_out_path, 'w').write(src)
  
  # Link to the raw source.
  page.body.append(A("show source", href=raw_src_name))
  page.body.extend([Br(), Br()])

  # Main table.
  page.body.append(obj_to_html_tab(o_r, wsv))

  # Emit line numbered source code
  page.body.append(Hr())
  src = string.strip(src)
  lines = string.split(src, '\n')
  lno_width = len(str(int(len(lines))))
  lno = 1
  lno_fmt = "%%%dd: " % lno_width
  pre_body = []
  for line in lines:
    pre_body.extend([A(lno_fmt % lno, name=lno), "%s\n" % line])
    lno = lno + 1
  page.body.append(Br())
  page.body.append(apply(Pre, pre_body))

  # Write the page out to file.
  page.body.append(g_html_page_footer)
  out_path = obj_html_path(out_dir, oid)
  page.write(out_path)

def html_Account_fmt(o_r, acct, top_fields, bot_fields):
  bot_fields.insert(0,("Dict Items", "getDictItems"))

def html_session(sess_filename):
  """Extract data from gzipped pickle <sess_filename> into a set of html files.
"""
  # Create an object reader.
  o_r = ObjReader(sess_filename)

  # Calculate the directory name, and create it.
  out_dir = sess_filename
  if ( out_dir[-7:] == '.pkl.gz' ): out_dir = out_dir[:-7]
  else: out_dir = out_dir + '.dir'
  try:
    os.mkdir(out_dir)
  except OSError, e:
    if ( e.errno == 17 ): pass
    else: raise e

  # Load the header object from the file.
  hdr = o_r.get("__Header.ex:0")

  # Initialize the html header.
  global g_html_page_header
  g_html_page_header = HtmlElemList(
    Table(Tr(
       Td(Img(src="101.gif", alt="[101]"), width='10%'),
       Td(H1("The Way", Br(), Font("(it should have been)", size=-1)),
          "Dumped from Data Center %s (%s)" %
          (hdr['dc_id'], hdr['dc_display_name']), Br(), 
          "Spin Version %s" % hdr['spin_ver'], Br(), align="center"),
       Td(width="104")), border=0, width="100%"),
     Hr())

  # Initialize the html footer
  global g_html_page_footer
  g_html_page_footer = HtmlElemList(Hr(), I("The Way - Delivering distributed goodness since 2000"))

  # Dump out the 101.gif image.
  open(os.path.join(out_dir, "101.gif"), 'w').write(zlib.decompress(base64.decodestring(g_101_gif_zlib_base64)))

  # Load the index oid from the header object.
#  idx_oid = Oid(hdr['soid'])
  idx_oid = Oid("Session", sys.argv[1][7:-7])

  # Itterate through every oid in the session dump.
  for soid in o_r.get_soids():
    oid = Oid(soid)
    if ( oid.cls[-3:] == '.ex' ): continue

    # Invoke the html emitter for the current non-extension object.
    globals().get("html_%s_full" % oid.cls, html_generic_)(o_r, oid, out_dir)

  # Create an index link.
  try:
    src_node = "%s/%s%s.html" % (out_dir, idx_oid.cls, idx_oid.id)
    dst_node = "%s/index.html" % out_dir
    link(src_node, dst_node)
  except OSError, e:
    if ( e.errno == 2 ):
      warn("os.link: %s not found: %s", (repr(src_node), e))
      # TODO: as a backup, generate an index html listing of the session

def main(argv):
  shift(argv)

  if ( not argv ): usage()

  while argv:
    arg = shift(argv)
    if ( arg == '-h' ):
      usage()
    elif ( arg == '-l' ):
      num = 10
      if ( argv ): num = int(shift(argv))
      list_last_sessions(num)
    elif ( arg[:2] == '-d' ):
      global g_dbg_level
      dbg_inc = 1
      if ( len(arg) > 2 ): dbg_inc = int(arg[2:])
      g_dbg_level = g_dbg_level + dbg_inc
    elif ( arg == '--url' ):
      global g_spin_url
      g_spin_url = shift(argv)
    else:
      if ( os.path.isfile(arg) ):
        html_session(arg)
      else:
        dump_spin_obj(get_spin(), Oid("Session", arg))

g_101_gif_zlib_base64 = """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
mH8PV+gu0J0qsJIttJIVBxb/A7C1XvU=
"""

if ( __name__ == '__main__' ):
  main(sys.argv[:])

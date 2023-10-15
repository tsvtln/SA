# This module provides access to HPSA databases


import sys,os,time,copy,string
sys.path.append("/opt/opsware/spin")

g_initialized = 0

def init():
  global g_initialized
  if ( g_initialized ): return
  global spinconf
  import spinconf
  spinconf.initLocal()
  if not os.environ.has_key("TNS_ADMIN"):
    os.environ["TNS_ADMIN"] = spinconf.get( "spin.db.tns_dir" )
  if not os.environ.has_key("ORA_TZFILE"):
    os.environ["ORA_TZFILE"] = spinconf.get( "spin.db.ora_tzfile" )
  if not os.environ.has_key("ORA_NLS10"):
    os.environ["ORA_NLS10"] = spinconf.get( "spin.db.ora_nls10" )
  if not os.environ.has_key("NLS_LANG"):
    os.environ["NLS_LANG"] = spinconf.get( "spin.db.nls_lang" )
  if not os.environ.has_key("NLS_SORT"):
  #  os.environ["NLS_SORT"] = spinconf.get( "spin.db.nls_sort" )
    os.environ["NLS_SORT"] = "BINARY"
  global cx_Oracle
  from cxOracle import cx_Oracle
  g_initialized = 1

# Global map of connections.
# {<tnsentry>: {<sid>: {"cstr":<cstr>, "create_dt":<create_dt>, "sid":<sid>, "cur":<cur>} ...} ...}
g_map_cons = {}

class _CursorProxy:
  """A proxy wrapper around a cx_Oracle cursor object.  The purpose of this proxy
is to allow us to give the client an object, such that when they are finished
with it, we can unregister a per-cursor data structure that keeps up with all
cursor's ever created.
"""
  def __init__(self, cstr):
    """Create a cx_Oracle connection using the connection string <cstr>."""
    self.cur = None

    # Creation date.
    create_dt = time.time()

    # Attempt to connect.
    con = cx_Oracle.connect(cstr, threaded=1)

    # Attempt to obtain a single cursor.
    self.cur = con.cursor()

    # Obtain this connection's session_id
    cur = con.cursor()
    cur.execute("select sys_context('USERENV','SID')  from dual")
    self.sid = cur.fetchone()[0]

    # If all of the above was successful, then register this connection.
    self.tnsentry = self.cur.connection.tnsentry
    map_tnsentry_cons = g_map_cons.get(self.tnsentry, {})
    if ( not g_map_cons.has_key(self.tnsentry) ):
      g_map_cons[self.tnsentry] = map_tnsentry_cons
    map_tnsentry_cons[self.sid] = {"cstr":cstr, "create_dt":create_dt, "sid":self.sid, "cur":self.cur}

  def __del__(self):
    try:
      # Unregister ourselves.
      del g_map_cons[self.tnsentry][self.sid]

      # not sure if this is neccessary, but lets close the cursor.
      self.cur.close()
    except:
      # We don't care if this fails.
      pass

  def __getattr__(self, name):
    return getattr(self.cur, name)

g_local_con = None
def _get_local_cur():
  global g_local_con
  if ( g_local_con is None ):
    cstr = "%s/%s@%s" % (spinconf.get("spin.db.username"), spinconf.get("spin.db.password"), spinconf.get("truth.tnsname"))
    g_local_con = cx_Oracle.connect(cstr, threaded=1)
  return g_local_con.cursor()

g_map_dcs = None
g_local_dc_id = -1
def _init():
  """Loads the local dc_id and datacenter info from the local database.
"""
  init()
  # Connect to the local database.
  cur = _get_local_cur()

  # Find our local dc_id.
  cur.execute("select global_id from lcrep.global_sid_id")
  local_dc_id = int(cur.fetchone()[0])

  # Load up info for datacenters in the mesh.
  map_dcs = {}
  cur.execute("select data_center_id, data_center_name, display_name from data_centers where ontogeny='PROD' and status='ACTIVE'")
  lst_dc_recs = cur.fetchall()
  for dc_rec in lst_dc_recs:
    map_dcs[int(dc_rec[0])] = {"dc_id":int(dc_rec[0]), "data_center_name":dc_rec[1], "display_name":dc_rec[2]}

  # Load up the cstr's for each of the datacenters.
  for dc_id in map_dcs.keys():
    cur.execute("""select cv.config_value
from data_centers dc, role_classes rc, role_class_wads rcw, config_params cp, config_keys ck, config_values cv
where (lower(dc.data_center_name)=lower(rc.role_class_short_name) and rc.stack_id=2 and rc.role_class_id!=2) and
      rc.role_class_id=rcw.role_class_id and
      rcw.rc_wad_id=ck.rc_wad_id and
      cp.config_param_id=ck.config_param_id and
      cp.key_name='truth.tnsname' and
      ck.config_key_id=cv.config_key_id and
      dc.data_center_id=:0""", (dc_id,))
    tnsname = cur.fetchone()[0]
    map_dcs[dc_id]["cstr"] = "%s/%s@%s" % (spinconf.get("spin.db.username"), spinconf.get("spin.db.password"), tnsname)

  # If we got this far, go ahead and commit the info to the module globals.
  global g_map_dcs
  global g_local_dc_id
  g_map_dcs = map_dcs
  g_local_dc_id = local_dc_id

# Public API:

def get_all_dcs():
  """Returns {<dc_id>: {"data_center_name":<data_center_name>, "display_name":<display_name>, "cstr":<cstr>} ...}
"""
  if ( not g_map_dcs ):
    _init()
  return copy.copy(g_map_dcs)

def get_local_dc_id():
  """Returns the datacenter ID for the local datacenter.
"""
  if ( g_local_dc_id == -1 ):
    _init()
  return g_local_dc_id

def get_cursor(arg=None):
  """If <arg> is <None>, then creates a new cursor to the local datacenter's 
database.  If <arg> is an integer, then it is interpreted as a datacenter ID,
and we attempt to create a cursor to that datacenter's DB.  Otherwise, <arg>
is assumed to be a generic connection string, and we attempt to create a new
cursor using that connection string.
"""
  init()
  dc_id = None
  cstr = None
  if ( arg is None ):
    arg = get_local_dc_id()
  try:
    dc_id = int(arg)
  except:
    cstr = arg
  if ( dc_id is not None ):
    return _CursorProxy(get_all_dcs()[dc_id]["cstr"])
  else:
    return _CursorProxy(cstr)

class NoSingleMMCentralException(Exception):
  pass

g_mm_central_dc_id = None
g_mm_central_dvc_id = None
def _init_mm_central_data():
  init()
  global g_mm_central_dc_id
  global g_mm_central_dvc_id

  # Pick datacenter of device attached to rc where role_class_full_name =="ServiceLevel Opsware Spin Multimaster Central".
  cur = _get_local_cur()
  cur.execute("""select cc.data_center_id, dr.dvc_id
from role_classes rc, device_role_classes drc, device_roles dr, customer_clouds cc
where rc.role_class_id=drc.role_class_id and drc.dvc_id=dr.dvc_id and dr.cust_cld_id=cc.cust_cld_id and
  rc.role_class_full_name='ServiceLevel Opsware Spin Multimaster Central'""")

  recs = cur.fetchall()
  if ( len(recs) == 0 or len(recs) > 1 ):
    raise NoSingleMMCentralException("There is not a single DC in this mesh marked as mm-central.  DCs: %s", repr(recs))
  else:
    (g_mm_central_dc_id, g_mm_central_dvc_id) = recs[0]

def get_mm_central_dc_id():
  """Returns the dc_id that is currently marked as mm-central.  If multiple DCs or
no DCs are marked as mm-central, then raises NoSingleMMCentralException.
"""
  if ( g_mm_central_dc_id is None ):
    _init_mm_central_data()
  return g_mm_central_dc_id

def get_mm_central_dvc_id():
  """Returns the dvc_id that is currently marked as mm-central.  If multiple devices
or no devices are marked as mm-central, then raises NoSingleMMCentralException.
"""
  if ( g_mm_central_dvc_id is None ):
    _init_mm_central_data()
  return g_mm_central_dvc_id

def fetch(cur):
  rec = cur.fetchone()
  return dict(map(lambda a,b: (a,b), map(lambda i:string.lower(i[0]), cur.description), rec))

def fetchmany(cur, count=1):
  return map(fetch, cur.fetchmany(count))



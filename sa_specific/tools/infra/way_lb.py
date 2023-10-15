import copy

from coglib import spinwrapper
from coglib import certmaster
from M2Crypto import SSL
from coglib import urlopen

def usage():
  sys.stdout.write("""Way Load Balance: A tool for exploring way/cog mapping configuration.
(A managed server is also know as a "cog" or "cogbot".)

Usages:

  %s

    Dump the slice ips configured for every datacenter and the way load
    balancing rules for every root gw in the mesh.  Highlights any
    misconfigurations.

  %s [-s <spin>] [-dc <dc_id>] <dvc_id1>[ <dvc_id2> ...]

    Calculate the way mapping list for the given device.

    <dvc_id1>[ <dvc_id2> ...]
      Devices for which to calculate waybot mapping.

    [-s <spin>]
      Specify a foreign spin to use.  Format is:

      [<client_cert>@][http:]<host>[:<port>]

    [-dc <dc_id>]
      Calculate the mapping list using core datacenter <dc_id> instead
      of using devices' registered core datacenter.

  %s -h

    Print this help usage.

""" % ((sys.argv[0],)*3))

def info(str, args=None):
  if ( args ):
    str = str % args
  sys.stderr.write("%s: INFO: %s\n" % (sys.argv[0], str))

def err(str, args=None):
  if ( args ):
    str = str % args
  sys.stdout.write("%s: ERR: %s\n" % (sys.argv[0], str))

def format_rows(rows, col_sep=' ', just_fn=lambda c:'-'):
  if ( not rows ): return ''
  num_cols = len(rows[0])
  col_maxes = range(num_cols)
  for cur_col in col_maxes:
    col_maxes[cur_col] = max(map(lambda r,cc=cur_col:len(str(r[cc])), rows))
#  fmt = string.join(["%%-%ds"] * num_cols, col_sep) % tuple(col_maxes)
  fmt = string.join(map(lambda c,just_fn=just_fn: "%%%%%s%%ds" % just_fn(c), range(num_cols)), col_sep) % tuple(col_maxes)
  return string.join(map(lambda r,f=fmt:f % r, rows), '\n') + '\n'

# Returns the content of a URL, or an empty string
def load_url(url,ctx=None):
  try:
    (url_fo,headers) = urlopen.httpReply(urlopen.httpUrlRequest(url,ctx=ctx))
    content = ''
    buf = url_fo.read()
    while buf:
      content = content + buf
      buf = url_fo.read()
    return content
  except:
    return ''

def load_client_cert(cert_path=None):
  if ( cert_path ):
    ctx = SSL.Context("sslv23")
    ctx.load_cert(cert_path)
    ctx.set_cipher_list("RC4-MD5:RC4-SHA:DES-CBC3-SHA:DES-CBC3-MD5")
  else:
    ctx = certmaster.getContextByName("spin","spin.srv","opsware-ca.crt")
    ctx.set_verify(SSL.verify_none, 3)
  return ctx

def load_spin(spin_spec=None):
  if ( not spin_spec ):
    return spinwrapper.SpinWrapper()

  orig_spin_spec = spin_spec
  cert_path = None
  protocol = "https"
  host = "127.0.0.1"
  port = 1004

  if ( '@' in spin_spec ):
    (cert_path,spin_spec) = string.split(spin_spec,'@')

  spin_spec = string.split(spin_spec,':')

  if ( len(spin_spec) > 3 ):
    sys.stderr.write("Invalid spin specification: %s\n" % orig_spin_spec)
    usage()
    sys.exit(1)

  try:
    port = int(spin_spec[-1])
    del spin_spec[-1]
  except ValueError, e:
    pass

  host = spin_spec[-1]
  del spin_spec[-1]

  if ( spin_spec ):
    cert_path = spin_spec[-1]
    del spin_spec[-1]

  if ( cert_path ):
    ctx = load_client_cert(cert_path)
  else:
    ctx = certmaster.getContextByName("spin","spin.srv","opsware-ca.crt")
  return spinwrapper.SpinWrapper(url="%s://%s:%d" % (protocol,host,port), ctx=ctx)

def dump_way_lbrs():
  # {<root_realm>:{'db_ips':str, 'gw_ips':{<gw_name>:str}}}
  map_ips = {}

  # Populate the lbr map with slice_ip data from the spins.
  spin = load_spin()
  dcs = spin.DataCenter.getAll(restrict={'status':'ACTIVE', 'ontogeny':'PROD'})
  for dc in dcs:
    try:
      slice_ips = dc.getDictValue(key='__OPSW_slice_ips')
    except:
      err('__OPSW_slice_ips not found on datacenter "%s"(%d)', (dc['data_center_name'],dc['data_center_id']))
      continue

    try:
      slice_ips = map(lambda i:string.split(i,':')[1], filter(lambda i:string.find(i,':')>-1,string.split(slice_ips,' ')))
    except:
      err('Unable to parse __OPSW_slice_ips value: "%s"', (slice_ips,))
      continue

    slice_ips.sort()

    realm_name = dc['display_name']
    map_ips[realm_name] = {'db_ips':slice_ips, 'gw_ips':{}}
    map_ips[realm_name]['dc_name'] = '%s (%d)' % (dc['data_center_name'],dc['data_center_id'])

  # Load way:1018 LBR rules from the live gw mesh and emit results as found.

  # Load a client cert.
  ctx = load_client_cert()

  # Grab the link state db from the local cgw instance.
  lsdb_url = "https://127.0.0.1:8085/linkTable"
  s_lsdb = load_url(lsdb_url,ctx)
  if ( not s_lsdb ):
    err('Failed to load link state database via "%s".', (lsdb_url,))
    sys.exit(1)
  try:
    lsdb = eval(s_lsdb)
  except:
    err('Unable to parse the following link state database:\n(obtained from "%s")\n%s', (lsdb_url,s_lsdb))
    sys.exit(1)

  # Filter out all non-root ospwgws.
  lsdb = filter(lambda i:string.lower(i['isroot'])=='true',lsdb)

  # Sort the lsdb by realm name.
  lsdb.sort(lambda a,b:cmp(a['realm'],b['realm']))

  for gw in lsdb:
    node_name = gw['node']
    realm_name = gw['realm']
    info("Processing configuration for %s@%s", (node_name, realm_name))

    gw_conf_url = "https://127.0.0.1:8085/config?Gateway=%s" % node_name
    s_gw_conf = load_url(gw_conf_url,ctx)
    if ( not s_gw_conf ):
      err('Failed to load gw conf via "%s"', (gw_conf_url,))
      continue
    try:
      gw_conf = eval(s_gw_conf)
    except:
      err('Unable to parse the following opswgw config:\n(obtained from "%s")\n%s', (gw_conf_url, s_gw_conf))
      continue

    try:
      way_lbr = filter(lambda i:string.find(i,'way:1018')>-1,string.split(gw_conf['propcache']['opswgw.LoadBalanceRule'],','))[0]
      way_ips = string.split(string.replace(way_lbr,":1018",''),':')[3:]
    except:
      err('Unable to parse the way load balance rule IPs from the following opswgw config:\n(obtained from "%s")\n%s', (gw_conf_url, s_gw_conf))

    if ( map_ips.has_key(realm_name) ):
      gw_ip = gw['gwaddr']
      map_ips[realm_name]['gw_ips']["%s@%s" % (node_name,gw_ip)] = way_ips
    else:
      err('No DataCenter record in the database for opswgw "%s" in realm "%s".', (node_name,realm_name))

  def just_fn(c):
    if ( c == 0 ): return ''
    else: return '-'

  # Itterate through the collected data and emit the results:
  realm_names = map_ips.keys()
  realm_names.sort()
  for realm_name in realm_names:
    rows = []
    cur_realm = map_ips[realm_name]
    sys.stdout.write("%s (%s):\n" % (cur_realm['dc_name'], realm_name))
#    rows.append(("DataCenter", "%s (%s)" % (cur_realm['dc_name'], realm_name)))
#    sys.stdout.write("Ordered Slice IPs: %s\n" % string.join(cur_realm['db_ips'], ' '))
    rows.append(("__OPSW_slice_ips sorted", string.join(cur_realm['db_ips'], ' ')))
    for gw_name in cur_realm['gw_ips'].keys():
#      sys.stdout.write("  %s: %s\n" % (gw_name, string.join(cur_realm['gw_ips'][gw_name],' ')))
      rows.append(("%s" % gw_name, "%s" % string.join(cur_realm['gw_ips'][gw_name],' ')))
    sys.stdout.write(format_rows(rows,': ',just_fn))
    sys.stdout.write('\n')
  sys.stdout.flush()

def dump_dvc_ways(dvc_id,spin=None,dc_id=None):
  if ( not spin ):
    spin = spinwrapper.SpinWrapper()

  dvcs = spin.Device.getAll(restrict={'dvc_id':dvc_id})
  if ( not dvcs ):
    sys.stderr.write("Device %s not found.\n" % dvc_id)
    return
  dvc = dvcs[0]

  if ( dc_id ):
    dcs = spin.DataCenter.getAll(restrict={'data_center_id':dc_id})
    if ( not dcs ):
      sys.stderr.write("DataCenter %s not found.\n" % dc_id)
      return
    dc = dcs[0]
  else:
    dc = dvc.getDataCenter().getCoreDC()

  keys = dc.getDictKeys()
  if ( not ("__OPSW_slice_ips" in keys) ):
    sys.stderr.write('The datacenter dictionary item "__OPSW_slice_ips" is not present on "%s"\n' % str(spin))
    return
  slice_ips = dc.getDictValue(key="__OPSW_slice_ips")

  ips = map(lambda i:string.split(i,':')[1], filter(lambda i:string.find(i,':')>-1,string.split(slice_ips,' ')))
  ips.sort()

  msi = spin.MegaServiceInstance.getAll(restrict={'srvc_type':'COGBOT', 'dvc_id':dvc_id})[0]
  realm_name = dvc.getRealm()['realm_name']
  ip_address = msi['ip_address']
  seed = "%s:%s" % (realm_name, ip_address)
  sys.path.append("/opt/opsware")
  from waybot.base.shuffle import shuffle
  indexes = shuffle.random_list(len(ips),seed)
  ips_res = copy.copy(ips)
  idx = 0
  for i in indexes:
    ips_res[idx] = ips[i]
    idx = idx + 1
  sys.stdout.write("dc%d:%d/%s(%s): %s\n" % (long(dc['data_center_id']),long(dvc['dvc_id']),dvc['system_name'],dvc['management_ip'],str(ips_res)))

argv = copy.copy(sys.argv[1:])

def shift(l):
  r = l[0]
  del l[0]
  return r

if ( not argv ):
  dump_way_lbrs()
else:
  dc_id=None
  local_spin=None
  while argv:
    cur_arg = shift(argv)
    if ( cur_arg == '-h' ):
      usage()
      sys.exit(0)
    elif ( cur_arg == '-s' ):
      local_spin = load_spin(shift(argv))
    elif ( cur_arg == '-dc' ):
      dc_id = shift(argv)
    else:
      dump_dvc_ways(cur_arg,spin=local_spin,dc_id=dc_id)


#    # Create a spinwrapper to this specific datacenter.
#    # (So we get the __OPSW_slice_ips from this datacenter's perspective.)
#    dc_spin = spinwrapper.SpinWrapper()
#    dc_gw_conf = dc.getGatewayConf()
#    gw_list = map(lambda gc:(gc['ip'],gc['proxy_port']), spin.sys.getDCFromDB().getGatewayConf())
#    dc_spin.server = lcxmlrpclib.Server("https://spin:1004/spinrpc.py", transport=SSLTransport.SSLTransport(ctx=ctx, realm=dc['display_name'], gw_list=gw_list))


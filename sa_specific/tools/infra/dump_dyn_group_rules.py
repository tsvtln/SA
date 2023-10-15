import sys,copy,getpass,pprint,zlib,base64,string,traceback
from coglib import spinwrapper
import pytwist

def usage():
  sys.stdout.write("""Usage: %s [-u <user>] [<group_id1> ...]

  If no <group_ids> are provided, then all dynamic groups will be processed.

  If no user is specificed, then "detuser" will be used, which does
  not have access to private dynamic groups by default

""")

username = None
password = None

argv = copy.copy(sys.argv)
del argv[0]

if ( len(argv) > 0 ):
  if ( argv[0] == '-u' ):
    del argv[0]
    username = argv[0]
    del argv[0]
    password = getpass.getpass("password: ")
  elif ( argv[0] == '-h' ):
    usage()
    sys.exit()

ts = pytwist.twistserver.TwistServer()

# If user supplied creds, use them.
if ( username ):
  ts.authenticate(username, password)

spin = spinwrapper.SpinWrapper()

def rec_dict_map(map):
  rmap = {}
  for key in map.keys():
    val = map[key]
    rmap[key] = getattr(val,'__dict__',val)
  return rmap  

# Following code renders selector syntax tree into a human readable tuple.
# (deprecated)
#------------------------------------------------------------------------------
def get_selector_tuple(sel):
  l = []
  for exj in sel.getChildren(child_class='_AAAExpressionJunction'):
    s = get_junction_tuple( exj )
    if (s):
      l.append(s) 
  return tuple(l)

def get_junction_tuple(exj):
  l = []

  if ( exj['junction'] == 'INTERSECT'):
    junc = '- AND -'
  else:
    junc = '- OR -'

  for ex in exj.getChildren(child_class='_AAAExpression'):
    s = get_expression_tuple(ex)
    if (s):
      l.extend([s,junc])

  for child_exj in exj.getChildren(child_class='_AAAExpressionJunction'):
    s = get_junction_tuple(child_exj)
    if (s):
      l.extend([s,junc])

  # Take off the trailing junc:
  if (l): l.pop()

  return tuple(l)

def get_expression_tuple(ex):
  rf = ex.getParent( parent_class="_AAAResourceField" )
  values = tuple( map( lambda x: str(x["value"]), ex.getChildren( child_class="_AAAFieldValue" ) ) )
  if ( len(values) == 1):
    values = values[0]

  return (rf['field_name'], ex['operator'], values)
#------------------------------------------------------------------------------

# Following code renders selector syntax tree into a filter style expression.
#------------------------------------------------------------------------------
def get_selector_exp(sel):
  l = []
  for exj in sel.getChildren(child_class='_AAAExpressionJunction'):
    s = get_junction_exp( exj )
    if (s):
      l.append(s) 
  if ( len(l) == 1 ): return l[0]
  return tuple(l)

def get_junction_exp(exj):
  l = []

  if ( exj['junction'] == 'INTERSECT'):
    junc = '&'
  else:
    junc = '|'

  for ex in exj.getChildren(child_class='_AAAExpression'):
    s = get_expression_exp(ex)
    if (s):
      l.append(s)

  for child_exj in exj.getChildren(child_class='_AAAExpressionJunction'):
    s = get_junction_exp(child_exj)
    if (s):
      l.append(s)

  return "(%s)" % string.join(l,'%s' % junc)

def get_expression_exp(ex):
  rf = ex.getParent( parent_class="_AAAResourceField" )
  values = map( lambda x: repr(x["value"]), ex.getChildren( child_class="_AAAFieldValue" ) )
  if ( len(values) == 1):
    values = values[0]
  else:
    values = '(%s)' % string.join(values, ', ')

  return '(%s %s %s)' % (rf['field_name'], ex['operator'], values)
#------------------------------------------------------------------------------

# Following code collects entire selector syntax tree into a python dictionary.
#------------------------------------------------------------------------------
def get_selector(sel):
  r = sel.data
  r['children'] = {'_AAAExpressionJunction':[]}
  for exj in sel.getChildren(child_class='_AAAExpressionJunction'):
    exj = get_junction( exj )
    if (exj):
      r['children']['_AAAExpressionJunction'].append(exj)
  return r

def get_junction(exj):
  r = exj.data
  r['children'] = {'_AAAExpression':[], '_AAAExpressionJunction':[]}
  for ex in exj.getChildren(child_class='_AAAExpression'):
    ex = get_expression(ex)
    if (ex):
      r['children']['_AAAExpression'].append(ex)
  for child_exj in exj.getChildren(child_class='_AAAExpressionJunction'):
    child_exj = get_junction(child_exj)
    if (child_exj):
      r['children']['_AAAExpressionJunction'].append(child_exj)
  return r

def get_expression(ex):
  r = ex.data
  r['children'] = {'_AAAFieldValue':[]}
  for fv in ex.getChildren( child_class="_AAAFieldValue" ):
    r['children']['_AAAFieldValue'].append(fv)
  return r
#------------------------------------------------------------------------------

def last_ex(out):
  exc_info = sys.exc_info()
  out.write(string.join( apply( traceback.format_exception, exc_info ), ""))
  if ( KeyboardInterrupt == exc_info[0] ): sys.exit(1)

if ( not argv ):
  sys.stderr.write("No device group ids provided, processing them all.\n")
#  dgw_ids = spin.DeliveryMechanismValue.get("DYNAMIC").getChildIDList(child_class='DeviceGroupWad')
  dgw_ids = spin.DeviceGroupWad.getIDList(restrict={"delivery_mechanism":"DYNAMIC"})
  argv = map(lambda i:"%d" % i[1], spin.DeviceGroupWad.getList(restrict={'rc_wad_id':dgw_ids}, fields=['role_class_id']))

for group_id in argv:
  group_name = group_id

  # See if we even have any selectors for this group.  otherwise skip.
  try:
    sels = spin._AAASelector.getAll(restrict={'selector_name':group_id, 
                                              'namespace':'DEVICE_GROUP_SELECTOR',
                                              'rolespace':'OPSWARE'})
  except:
    last_ex(sys.stdout)

  if ( len(sels) == 0 ):
    sys.stdout.write("%s: No _AAASelector (aka dynamicRule expression) for group, skipping.\n\n" % group_name)
    continue
  else:
    if ( len(sels) > 1 ):
      sys.stdout.write("WARNING: group %s has multiple selectors, choosing the first one.\n" % group_name)
    else:
      sel = sels[0]

  # load up the DeviceGroupVO from the twist.
  sys.stdout.write("%s: DeviceGroupVO from twist:\n" % group_id)
  try:
    dg_service = ts.device.DeviceGroupService
    from pytwist.com.opsware.device import DeviceGroupRef
    dgr = DeviceGroupRef(group_id)
    dgvo = dg_service.getDeviceGroupVO(dgr)
    pprint.pprint(rec_dict_map(dgvo.__dict__))
    group_name = '"%s"(%s)' % (dgvo.fullName,group_id)
  except:
    last_ex(sys.stdout)

  # Dump selector syntax tree from spin.
  sys.stdout.write("\nSelector syntax tree from spin:\n")
  try:
#    pprint.pprint(get_selector_tuple(sel))
    sys.stdout.write('%s\n' % get_selector_exp(sel))
    sys.stdout.write("raw:(%s)\n" % string.replace(base64.encodestring(zlib.compress(repr(get_selector(sel)))),'\n',''))
  except:
    last_ex(sys.stdout)

  # Get the SQL from the SelectorFacade via twist:
  sys.stdout.write("\nSelectorFacade.transformSQL result:\n")
  try:
    device_resource_type_id = spin._AAAResourceType.getAll(restrict={'resource_type_name':'device'})[0]['id']
    sql = ts._makeCall('fido/ejb/session/SelectorFacade', 'transformSQL', ("SELECT DISTINCT dvc_id from Devices", sel['id'], device_resource_type_id, 0))
    sys.stdout.write("%s\n" % sql)
  except:
    last_ex(sys.stdout)

  sys.stdout.write('\n')
  sys.stdout.flush()

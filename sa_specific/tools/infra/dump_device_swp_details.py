import sys,getpass,types,string,traceback,gzip,cPickle,time,pytwist

g_stdout = sys.stdout
g_stderr = sys.stderr
def info_raw(msg):
  g_stdout.write(msg)
  g_stdout.flush()

def info(msg, args=None):
  if ( args ): msg = (msg % args)
  info_raw(msg + '\n')

def err(msg, args=None, tb=0):
  if ( args ): msg = (msg % args)
  msg = ("%s: ERR: %s\n" % (sys.argv[0], msg))
  if ( tb ):
    msg = msg + string.join(apply(traceback.format_exception, sys.exc_info()),'')
  g_stderr.write(msg)
  g_stderr.flush()

def usage():
  info("""Usage: %s [-u <username>] <dvc_id>
""" % sys.argv[0])

def shift(l):
  r = l[0]
  del l[0]
  return r

def myrepr(obj):
  if ( hasattr(obj,'__dict__') ):
    obj = obj.__dict__.copy()
  obj_type = type(obj)
  if ( obj_type == types.DictType ):
    for key in obj.keys():
      obj[key] = myrepr(obj[key])
  elif ( obj_type in (types.TupleType,types.ListType) ):
    l = []
    for i in obj:
      l.append(myrepr(i))
    obj = l
    if (obj_type == types.TupleType):
      obj = tuple(obj)
  else: obj = repr(obj)
  return obj

def uniq(l, idfun=lambda i:i):
  seen = []
  for i in l:
    if ( not (i in seen) ):
      seen.append(i)
  return seen

def collect_sp_vos(ts, sp_refs, seen_sp_refs=[]):
  filter(lambda sp_ref,seen_sp_refs=seen_sp_refs:not (sp_ref in seen_sp_refs), sp_refs)
  sp_refs = uniq(sp_refs,lambda i:i.id)
  sp_vos = list(ts._makeCall("com.opsware.swmgmt.SoftwarePolicyService", "getSoftwarePolicyVOs", [sp_refs]))
  seen_sp_refs.extend(sp_refs)
  child_spids = map(lambda sp_vo:sp_vo.installableItemData+sp_vo.uninstallableItemData, sp_vos)
  if ( child_spids ):
    child_spids = reduce(lambda a,b:a+b, child_spids)
    child_sp_refs = filter(lambda pi:str(pi.__class__)=='pytwist.com.opsware.swmgmt.SoftwarePolicyRef',map(lambda spid:spid.policyItem, child_spids))
    sp_vos.extend(collect_sp_vos(ts, child_sp_refs, seen_sp_refs))
  return sp_vos

def dump(title, obj, f):
#  info("\n%s\n\n%s" % (title, pprint.pformat(obj)
  info(title)
  cPickle.dump(obj, f)

def spin_repr(o):
  o = o.data
  for k in o.keys():
    if (str(type(o[k])) == "<type 'xmlrpcdateTime'>"):
#      o[k] = time.asctime(o[k].date() + (0,0,0))
      o[k] = str(o[k])
  return o

def dump_device_swp_details(ts, dvc_id):
  info_raw("%s: " % dvc_id)
  f = gzip.open("Device_%s.pkl.gz" % dvc_id, "w")
  m = {}

  # Recursively dump all associated software policies.
  from pytwist.com.opsware.server import ServerRef
  sr = ServerRef(dvc_id)
  asps = ts._makeCall("com.opsware.server.ServerService", "getSoftwarePolicyAssociations", [sr])
  info_raw("Associated Software Policies, ")
  m['asps'] = myrepr(asps)
  sp_refs = map(lambda asp:asp.policy, asps)
  sp_vos = collect_sp_vos(ts, sp_refs)
  info_raw("Software Policy VOs, ")
  m['spvos'] = myrepr(sp_vos)

  # Dump all AppPolicyRIU records.
  from coglib import spinwrapper
  spin = spinwrapper.SpinWrapper()
  aprius = map(spin_repr, spin.AppPolicyRIU.getAll(restrict={'dvc_id':dvc_id}))
  aprius.sort(lambda a,b:cmp(a['app_policy_id'],b['app_policy_id']))
  info_raw("AppPolicyRIU Records, ")
  m['aprius'] = aprius

  # Dump installed software records.
  isws = ts._makeCall("com.opsware.server.ServerService", "getInstalledSoftware", [sr])
  info_raw("InstalledSoftware Records, ")
  m['isws'] = myrepr(isws)

  info_raw("dumping to file\n")
  cPickle.dump(m, f)
    
  # finalize the archive.
  f.close()

def main():
  argv = sys.argv[1:]

  username = None
  password = None
  dvc_ids = None

  if ( len(argv) == 0 ):
    usage()
    sys.exit(1)

  if ( argv[0] == '-u' ):
    if ( len(argv) > 1 ):
      username = argv[1]
      argv = argv[2:]
    else:
      usage()
      sys.exit(1)

  dvc_ids = uniq(map(string.strip,argv))

  if ( not dvc_ids ):
     usage()
     sys.exit(1)

  ts = pytwist.twistserver.TwistServer()

  if ( username ):
    ostdout = sys.stdout
    sys.stdout = sys.stderr
    password = getpass.getpass("password: ")
    sys.stdout = ostdout
    ts.authenticate(username,password)

  for dvc_id in dvc_ids:
    try:
      dump_device_swp_details(ts, dvc_id)
    except KeyboardInterrupt, e:
      user_req_quit()
    except:
      err("%s: Unable to dump specified device", str(dvc_id), tb=1)

if ( __name__ == "__main__" ): main()

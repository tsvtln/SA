import pytwist,getpass,copy,string,types,os,traceback

def usage():
  sys.stderr.write("""Tool for dumping information about devices.

Usage: %s [-pp] [-u <user>[/<password>]] [-f <file>] [<dvc_id1>[ <dvc_id2> ...]]

If stdout is a tty, emits data in ascii text form.  If stdout is not a
tty, then emits data in a pickle/zlib format.

""" % sys.argv[0])

all_errs = []
def err(msg, args=None, tb=0):
  if ( args ): msg = (msg % args)
  msg = ("%s: ERR: %s\n" % (sys.argv[0],msg))
  if ( tb ):
    msg = msg + string.join(apply(traceback.format_exception, sys.exc_info()),'')
  sys.stderr.write(msg)
  all_errs.append(msg)

username = None
password = None
force_pprint = 0

def shift(l):
  r = l[0]
  del l[0]
  return r

argv = copy.copy(sys.argv[1:])

if ( not argv ):
  usage()
  sys.exit(1)

in_filename = None

# Consume leading options
while (argv and argv[0][0] == '-'):
  cur_arg = shift(argv)
  if ( cur_arg == '-u' ):
    un = shift(argv)
    if ( '/' in un ):
      (username, password) = string.split(un,'/')
    else:
      username = un
  elif ( cur_arg == '-f' ):
    in_filename = shift(argv)
  elif ( cur_arg == '-pp' ):
    force_pprint = 1

# If we got a username only, then ask user for password.
if ( username and (not password) ):
  if ( not sys.stdin.isatty() ):
    err("<stdin> is not a tty, unable to ask user for password.")
    sys.exit(1)
  old_stdout = sys.stdout
  sys.stdout = sys.stderr
  password = getpass.getpass('password: ')
  sys.stdout = old_stdout

ts = pytwist.twistserver.TwistServer()

# If we got a username/password, then authenticate
if ( username ):
  ts.authenticate(username, password)

# emit data strcture pprint'ed.
def emit_ds_pp(ds):
  pprint.pprint(ds)

# emit data strcture pickle/zlib compressed.
def emit_ds_comp(ds):
  cPickle.dump(ds,zout)

def ref_from_vo(vo):
  try:
    return ref_from_ref(vo.ref)
  except:
    return None

def ref_from_ref(ref):
  try:
    ret = "%s:%d" % (ref.__class__.__name__, long(ref.id))
    if ( hasattr(ref,'name') and ref.name ): ret = ret + (' (%s)' % ref.name)
    return ret
  except:
    return None

# emits the abstract object <o> as follws:
def repr_obj(obj):
  if ( type(obj) == types.TupleType ):
    obj = tuple(map(lambda o,ro=repr_obj:ro(o), obj))
  elif ( type(obj) == types.ListType ):
    obj = map(lambda o,ro=repr_obj:ro(o), obj)
  elif ( type(obj) == types.DictType ):
    map_obj = {}
    for key in obj.keys():
      map_obj[repr_obj(key)] = repr_obj(obj[key])
    obj = map_obj
  elif ( type(obj) == types.InstanceType):
    if ( hasattr(obj,'__module__') and (string.find(obj.__module__,'pytwist.')>-1) ):
      if ( string.lower(obj.__class__.__name__[-3:]) == 'ref' ):
        obj = ref_from_ref(obj)
      else:
        map_obj = {}
        map_obj['__class__'] = '%s.%s' % (obj.__module__, obj.__class__.__name__)
        for key in filter(lambda k:k[0] in 'abcdefghijklmnopqrstuvwxy', obj.__dict__.keys()):
          map_obj[repr_obj(key)] = repr_obj(obj.__dict__[key])
        obj = map_obj
    else: obj = str(obj)
  return obj

zout = None
if ( force_pprint or sys.stdout.isatty() ):
  import pprint
  emit_ds = emit_ds_pp
else:
  import cPickle,gzip
  zout = gzip.GzipFile(fileobj=sys.stdout)
  emit_ds = emit_ds_comp

def exit(ec):
  # Insure that the gzip output file gets properly closed.
  if (zout): zout.close()

  sys.exit(ec)

def user_req_quit():
  err("Quiting at user's request.")
  exit(1)

sps = ts.swmgmt.SoftwarePolicyService
ss = ts.server.ServerService
search_service = ts.search.SearchService
from pytwist.com.opsware.server import ServerRef
from pytwist.com.opsware.search import Filter

class SeenRefs:
  def __init__(self):
    self.seen_refs = []

  def _normalize_ref(self, ref):
    return string.split(ref,' ')[0]
 
  def add_ref(self, ref):
    self.seen_refs.append(self._normalize_ref(ref))

  def has_ref(self, ref):
    return self._normalize_ref(ref) in self.seen_refs
    

# Recursively dumps out info for referenced software policy and and sub-
# software policies
def dump_sw_policy(spr, seen_refs=None):
  if ( seen_refs == None ): seen_refs = SeenRefs()
  s_spr = ref_from_ref(spr)
  if ( not seen_refs.has_ref(s_spr) ):
    seen_refs.add_ref(s_spr)
    sys.stderr.write("%s\n" % s_spr)
    sp_vo = sps.getSoftwarePolicyVO(spr)
    emit_ds(repr_obj(sp_vo))
    for iid in sp_vo.installableItemData:
      if ( iid.policyItem.__class__.__name__ == 'SoftwarePolicyRef' ):
        dump_sw_policy(iid.policyItem, seen_refs)

def dump_dvc_info(dvc_id, seen_refs=None):
  if ( seen_refs == None ): seen_refs = SeenRefs()

  # Handle device record.
  sr = ServerRef(dvc_id)
  s_sr = ref_from_ref(sr)
  if ( not seen_refs.has_ref(s_sr) ):
    seen_refs.add_ref(s_sr)
    sys.stderr.write("%s\n" % s_sr)
    svo = ss.getServerVO(sr)
    map_svo = repr_obj(svo)
    f = Filter()
    f.expression = 'software_policy_all_dvc_id = %s' % str(dvc_id)
    f.objectType = 'software_policy'

    # Locate all software policies associated with this device.
    sprs = search_service.findObjRefs(f)
    map_svo['_softwarePolicyAssociations'] = repr_obj(sprs)

    # Software registered as installed on this device.
    map_svo['_installedSoftware'] = repr_obj(ss.getInstalledSoftware(sr))

    # Emit the device record.
    emit_ds(map_svo)

    # Load and emit the software policies associated with this device.
    for spr in sprs:
      dump_sw_policy(spr, seen_refs)

# List of references we have seen, so that we don't dump them multiple times.
seen_refs = SeenRefs()

# device ids to process.
dvc_ids = []

# add the devices listed on the command line.
dvc_ids.extend(argv)

# If the user specified an input file:
if ( in_filename ):
  if ( os.path.exists(in_filename) or in_filename == '-' ):
    if ( in_filename == '-' ):
      in_file = sys.stdin
    else:
      in_file = open(in_filename)
    dvc_ids.extend(map(string.rstrip,in_file.readlines()))
  else:
    sys.stderr.write("%s: %s: file not found\n" % (sys.argv[0], in_filename))

# Process device ids passed on the command line.
dvc_count = 0
for dvc_id in dvc_ids:
  dvc_count = dvc_count + 1
  try:
    sys.stderr.write("[%d/%d]\n" % (dvc_count, len(dvc_ids)))
    dump_dvc_info(dvc_id, seen_refs)
  except KeyboardInterrupt, e:
    user_req_quit()
  except:
    err("%s: Unable to dump specified device", str(dvc_id), tb=1)

# If there where any errors, emit them as well.
if ( all_errs ): emit_ds({'all_errs':all_errs})

# Cleanup and exit
exit(0)

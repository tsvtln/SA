import pytwist,getpass,sys,traceback,string

args = sys.argv[1:]

def shift(l):
  r = l[0]
  del l[0]
  return r

username = None
password = None

def usage():
  sys.stdout.write("""Usage: %s [-u <username>] <unit_id1> [<unit_id2> ...]
""" % sys.argv[0])

if ( len(args) == 0 ):
  usage()
  sys.exit(1)

unit_ids = []

while args:
  cur_arg = shift(args)
  if ( cur_arg == "-u" ):
    username = shift(args)
  elif ( cur_arg == "-h"):
    usage()
    sys.exit(1)
  else:
    unit_ids.append(cur_arg)

if ( username is None ):
  sys.stdout.write("username: ")
  sys.stdout.flush()
  username = sys.stdin.readline()[:-1]

if ( password is None ):
  password = getpass.getpass("password: ")

ts = pytwist.twistserver.TwistServer(secure=0)
ts.authenticate(username, password)

search_svc = ts.search.SearchService
unit_svc = ts.pkg.UnitService

for unit_id in unit_ids:
  ur = None
  urs = search_svc.findObjRefs("(UnitVO.pK = %s)" % unit_id, "software_unit")
  if ( len(urs) > 0 ):
    ur = urs[0]
  else:
    urs = search_svc.findObjRefs("(PatchVO.pK = %s)" % unit_id, "patch_unit")
    if ( len(urs) > 0 ):
      ur = urs[0]

  if ( ur is None ):
    sys.stdout.write("%s: No such unit found.\n" % unit_id)
    continue

  sys.stdout.write("Removing %s...  " % repr(str(ur)))
  sys.stdout.flush()

  try:
    unit_svc.remove(ur)
    sys.stdout.write("SUCCESS\n")
  except:
    s_ex = string.join( apply( traceback.format_exception, sys.exc_info() ), "")
    sys.stdout.write("FAILED\n%s" % s_ex)


  
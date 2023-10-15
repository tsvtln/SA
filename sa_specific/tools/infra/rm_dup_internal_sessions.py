import traceback,sys,string

from coglib import spinwrapper

spin = spinwrapper.SpinWrapper()

# Grab an ID list of all active core datacenters.
active_dc_ids = spin.DataCenter.getIDList(restrict={"ontogeny":"PROD", "status":"ACTIVE"})
active_dc_ids.sort()

# Grab an ID list of all PENDING internal sessions.
sess_recs = spin.Session.getList(restrict={"status":"PENDING", "session_desc":("Automated *",)},
                                     omit={"parent_session_id":None},
                                     fields=["parent_session_id", "session_desc"])

# Calculate and prepend the dc_id from each session record.
sess_recs = map(lambda sr:(long(sr[0]) % 1000,) + tuple(sr), sess_recs)

# filter out any sessions from old datacenters.
sess_recs = filter(lambda sr:sr[0] in active_dc_ids, sess_recs)

def last_ex():
  return string.join( apply( traceback.format_exception, sys.exc_info() ), "")

def get_way(way=[None]):
  if (way[0] is None):
    from coglib import serverproxy, certmaster
    ctx = certmaster.getContext('/var/opt/opsware/crypto/spin/spin.srv')
    way[0] = serverproxy.ServerProxy(url='https://127.0.0.1:1018/wayrpc.py', ctx=ctx, r_to=500, c_to=500, w_to=500)
  return way[0]

def cancel_way_session(sess_rec):
  sys.stdout.write("""  -----------------------------------------------------------------------------
  WARNING: For datacenters with a large number of managed servers, it might 
  take several minutes for this process to complete.  Also, a timeout error
  might be displayed below, but this can be ignored, as the waybot should 
  continue the cancelation process on its own within the waybot.
  -----------------------------------------------------------------------------

""")
  way = get_way()
  try:
    way.schedule.cancel( session_id=sess_rec[2] )
  except:
    sys.stdout.write("Exception occurred:\n%s" % last_ex())
  else:
    sys.stdout.write("Recurring session %d canceled.\n" % sess_rec[2])

def cancel_way_sessions(sess_recs):
  s_answer = "N"
  for sess_rec in sess_recs:
    sys.stdout.write("RECURRING Session %s(%d) in DC %d is redundant.\n" % (repr(sess_rec[3]),sess_rec[2],sess_rec[0]))
    if ( s_answer in "YyNn" ):
      s_answer = "*"
      while ( s_answer not in "YyNnOoAaQq" ):
        if ( s_answer != "*" ):
          sys.stdout.write("Invalid response.\n")
        sys.stdout.write("Delete? [Y]es/[N]o/[A]ll/[Q]uit\n")
        s_answer = sys.stdin.readline()[0]
    if ( s_answer in "Qq" ):
      sys.stdout.write("Quiting...\n")
      sys.exit()
    elif ( s_answer in "YyAa" ):
      cancel_way_session(sess_rec)

# List of session records to be deleted.
to_del_sess_recs = []

# For every active datacenter.
for dc_id in active_dc_ids:
  # For each of the two kinds of internal sessions we care about:
  for s_int_sess_desc in ("Automated Communications Test for core: ", "Automated Hypervisor Scan for core: "):
    # Get the list of RECURRING/PENDING sessions
    ct_sess_recs = filter(lambda sr,dc_id=dc_id,sd=s_int_sess_desc:sr[0]==dc_id and sr[3][:len(sd)]==sd, sess_recs)
    ct_sess_recs.sort(lambda a,b:cmp(a[2],b[2]))
    if ( len(ct_sess_recs) > 1 ):
      to_del_sess_recs.extend(ct_sess_recs[1:])
    elif ( len(ct_sess_recs) == 0 ):
      sys.stdout.write("ERROR: DataCenter %d is missing the internal system session: %s\n" % (dc_id, repr(s_int_sess_desc)))

if ( len(to_del_sess_recs) > 0 ):
  cancel_way_sessions(to_del_sess_recs)
else:
  sys.stdout.write("No duplicate internal RECURRING sessions found.\n")

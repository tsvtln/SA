import sys
sys.path.append("/opt/opsware/spin")

if ( len(sys.argv) != 3 ):
  sys.stderr.write("""Usage: %s <from_dc_id> <to_dc_id>

Calculates the actual not recieved transaction ids from <from_dc_id> to <to_dc_id>.
Prints results to stdout.
""" % sys.argv[0])
  sys.exit(1)

from_dc_id = int(sys.argv[1])
to_dc_id = int(sys.argv[2])

sys.stderr.write("loading...")
sys.stderr.flush()
import spinconf, truthdb, multimaster;
spinconf.initLocal();
spinconf.loadConfFromTruth();

all_dcs = multimaster.getAllDCs( sys.argv[0], "spin" )
from_cur = multimaster.getDB( sys.argv[0], "spin", all_dcs[from_dc_id].getDBName() ).getCursor()
to_cur = multimaster.getDB( sys.argv[0], "spin", all_dcs[to_dc_id].getDBName() ).getCursor()
sys.stderr.write("done\n")

lookback_days = spinconf.get("spin.multimaster.mm_state.max_lookback_days")

from_sql = "select tran_id from lcrep.transactions where publish_dt is not null and replicate_flg='Y' and tran_id in (select tran_id from transaction_dml) and publish_dt > (systimestamp - %d) order by tran_id asc" % (lookback_days,)
from_cur.execute(from_sql)

to_sql= "select tran_id from lcrep.transaction_logs where mod(tran_id, %.0f) = %d and publish_dt > (systimestamp - %d) order by tran_id asc" % (truthdb.globalize_size, from_dc_id, lookback_days)
to_cur.execute(to_sql)

CHUNK_SIZE=1000

g_read_count = 0
def get_more(cur, chunk_size=None):
  global g_read_count
  if ( not chunk_size ):
    r = cur.fetchall()
  else:
    r = cur.fetchmany(chunk_size)
  g_read_count = g_read_count + len(r)
  sys.stderr.write("\r%d" % g_read_count)
  sys.stderr.flush()
  return map(lambda i:i[0], r)

def emit_tran_id(tran_id):
#  sys.stderr.write("DEBUG: %s (%s)\n" % (tran_id, type(tran_id)))
  sys.stdout.write("%0.f\n" % tran_id)

def shift(l):
  i=l[0]
  del l[0]
  return i

from_chunk = []
to_chunk = []

sys.stderr.write("Calculating \"Not Received\" transaction ids\nfrom: \"%s\"\nto: \"%s\"\nover the past: %d days\n" % (str(all_dcs[from_dc_id]), str(all_dcs[to_dc_id]), lookback_days))
while 1:
  if ( not from_chunk ):
    from_chunk = get_more(from_cur, CHUNK_SIZE)
    if ( not from_chunk ):
      to_chunk.extend(get_more(to_cur))
      map(emit_tran_id, to_chunk)
      break
  if ( not to_chunk ):
    to_chunk = get_more(to_cur, CHUNK_SIZE)
    if ( not to_chunk ):
      from_chunk.extend(get_more(from_cur))
      map(emit_tran_id, from_chunk)
      break
  if ( from_chunk[0] == to_chunk[0] ):
#    sys.stderr.write("DEBUG: from: %d, to: %d\n" % ( from_chunk[0], to_chunk[0]))
    shift(from_chunk)
    shift(to_chunk)
  elif ( from_chunk[0] < to_chunk[0] ):
    emit_tran_id(shift(from_chunk))
  elif ( from_chunk[0] > to_chunk[0] ):
    # These are tran_ids that are in the dest transaction_logs but _not_ in the
    # source transactions table.  Silently ignoring.  (Maybe emit to stderr?)
    shift(to_chunk)
  else:
    raise "Should never have gotten here!\n"

sys.stderr.write("\n")

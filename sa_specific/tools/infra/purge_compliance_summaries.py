
import sys,dblib,time,string,thread,threading,os,util

# ./py_build ./pylibs/dblib.py ./pylibs/util.py purge_compliance_summaries.py

# compliance_summary FK tree as of HPSA 9.11:
# COMPLIANCE_SUMMARY
#   COMPLIANCE_APP_INST
#   COMPLIANCE_APP_POLICY
#   COMPLIANCE_DETAIL
#     COMPLIANCE_DETAIL_EXCLUSION
#   COMPLIANCE_ROLE_CLASSES
#   COMPLIANCE_SCO_TEST

g_s_prog_name = os.path.basename(sys.argv[0])

g_log_lock = threading.Lock()
def log(s, args=None):
  if ( args is not None ):
    s = s % args
  s = "%s: %s: %s" % (time.ctime(time.time()), threading.currentThread().getName(), s)
  while s[-1] == "\n":
    s = s[:-1]
  s = s + "\n"
  g_log_lock.acquire()
  try:
    sys.stdout.write(s)
    sys.stdout.flush()
  except:
    g_log_lock.release()
    raise
  else:
    g_log_lock.release()

def msg(s, args=None):
  if ( args is not None ):
    s = s % args
  sys.stdout.write(s)
  sys.stdout.flush()

def _delete_table(cur, s_table, chunk_size):
  while 1:
    cur.execute("delete %s where rownum<=:1" % s_table, (chunk_size,))
    log("%d records deleted from table %s", (cur.rowcount, s_table))
    if ( cur.rowcount == 0 ): break

g_max_retry_count = 10
def purge_compliance_summaries_thread(cur, chunk_size):
  for s_table in ("COMPLIANCE_DETAIL_EXCLUSION", "COMPLIANCE_DETAIL", "COMPLIANCE_APP_INST", "COMPLIANCE_APP_POLICY", "COMPLIANCE_ROLE_CLASSES", "COMPLIANCE_SCO_TEST", "COMPLIANCE_SUMMARY"):
    retry_count=0
    while 1:
      try:
        cur.callproc("LCREPPKG.BEGIN_TRANSACTION")
        cur.callproc("LCREPPKG.REPLICATE", ("N",))
        # lets don't set the username so that no transaction record gets created at all. -dw
        #cur.callproc("LCREPPKG.SET_USERNAME", (g_s_prog_name,))
        cur.execute("delete %s where rownum<=:1" % s_table, (chunk_size,))
        rowcount = cur.rowcount
        log("%d records deleted from table %s", (rowcount, s_table))
        cur.callproc("LCREPPKG.END_TRANSACTION")
        cur.execute("commit")
        #cur.execute("rollback")
        if (rowcount < chunk_size): break
        retry_count = 0
      except:
        log("Unexpected exception while attempting to purge compliance summary results:")
        log(util.last_ex())
        if (retry_count >= g_max_retry_count):
          log("Maximum number of retries reached, giving up for this datacenter.")
          return
        try:
          cur.execute("rollback")
        except:
          log("Unexpected exceptio nwhile attempting to rollback a previously failed transaction:")
          log(util.last_ex())
          log("Giving up on this datacenter.")
          return
        retry_count = retry_count + 1

def main():
  map_all_dcs = dblib.get_all_dcs()
  mm_central_dc_id = dblib.get_mm_central_dc_id()
  local_dc_id = dblib.get_local_dc_id()
  if ( mm_central_dc_id != local_dc_id ):
    msg("This utility must be run on the mm-central infra box in datacenter %s (%d).  Not %s (%d)\n", (repr(map_all_dcs[mm_central_dc_id]["display_name"]), mm_central_dc_id, repr(map_all_dcs[local_dc_id]["display_name"]), local_dc_id))
    sys.exit(1)
  msg("This utility will purge all compliance summary results in the mesh using non-replicating transcations to the following datacenters:\n")
  for dc_id, dc_rec in map_all_dcs.items():
    msg("  %d: %s\n", (dc_id, dc_rec["display_name"]))
  msg("\nContinue? (y/n)\n")
  try:
    a = sys.stdin.readline()[0]
  except:
    a = "n"
  if ( a not in "yY" ):
    msg("Canceled.\n")
    sys.exit(0)

  chunk_size = 1000
  if ( len(sys.argv) > 1 ):
    try:
      chunk_size = int(sys.argv[1])
    except:
      pass
  msg("Using chuk size of %d.\n", (chunk_size,))
  
  # Spin up a thread for each datacenter.
  thrds = []
  for dc_id in map_all_dcs.keys():
    thrd = threading.Thread(target=purge_compliance_summaries_thread, name=("DC%d (%s)" % (dc_id,map_all_dcs[dc_id]["display_name"])), args=(dblib.get_cursor(dc_id),chunk_size))
    thrd.start()
    thrds.append(thrd)

  # Wait for all threads to complete.
  for thrd in thrds:
    thrd.join()

  msg("Done.\n")

if ( __name__ == "__main__" ):
  main()

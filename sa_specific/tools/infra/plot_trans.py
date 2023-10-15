##
# This script will emit an xplot.org compatible graph of transaction timing
# overlayed with DML count data for transaction data captured with the following
# sql query:
#
#   # ./sql -a -o /tmp/c1.pkl.gz "select t.tran_id, t.username, t.create_dt, t.publish_dt, count(td.tran_dml_id) from transactions t, transaction_dml td where t.tran_id=td.tran_id and t.replicate_flg='Y' group by t.tran_id, t.username, t.create_dt, t.publish_dt" "select tran_id, publish_dt, receive_dt from transaction_logs"
#
# ------------------------------------------------------------------------------
#

import sys,gzip,cPickle,time,os,string,traceback

TRAN_LOGS_SQL_PAT = "tran_id, publish_dt, receive_dt"
DML_CNT_SQL_PAT = "t.tran_id, t.username, t.create_dt, t.publish_dt, count(td.tran_dml_id)"

def last_ex():
  return string.join( apply( traceback.format_exception, sys.exc_info() ), "")

def msg(s, args=None):
  if ( args is not None ):
    s = s % args
  sys.stdout.write(s)
  sys.stdout.flush()

def to_epoch(dt):
  return float(time.mktime(dt.timetuple()))

def emit_bounds_box(fo, yzero, xmin, xmax, ymin, ymax, yunits, color):
  xpad = (xmax-xmin)/20
  fo.write("invisible %f %f\n" % (xmin,yzero-5))
  fo.write("invisible %f %f\n" % (xmax,yzero+105))
  fo.write("line %f %f %f %f %d\n" % (xmin,yzero,xmax,yzero,color))
  fo.write("line %f %f %f %f %d\n" % (xmin,yzero+100,xmax,yzero+100,color))
  fo.write("btext %f %f\n" % (xmin+xpad,yzero+100))
  fo.write("%f %s\n" % (ymax,yunits))

def emit_key(fo, xmin, xmax, dc_ids):
  y = 200
  xpad = (xmax-xmin)/20
  xdelta = xpad/5
  for dc_id in dc_ids:
    y = y - 5
    fo.write("line %f %f %f %f %d\n" % (xmin+xpad, y, xmin+xpad+xdelta, y, dc_id))
    fo.write("rtext %f %f\n" % (xmin+xpad+xdelta, y))
    fo.write("DC %d\n" % dc_id)

def main():
  if ( len(sys.argv) != 2 ):
    msg("Usage: %s <tran_pkl_gz_file>\n\n" & sys.argv[0])
    sys.exit()

  f_size = None

  fn = sys.argv[1]
  if ( fn == "-" ):
    f = gzip.GzipFile(fileobj=sys.stdin, mode="rb")
    fn = "stdin-%d" % int(time.time())
  else:
    f = gzip.open(fn)
    f_size = os.fstat(f.fileobj.fileno())[6]

  ofn = "%s.xplot" % fn
  ofn2 = "%s.dat" % fn

  msg("%s -> %s\n", (fn, ofn))

  fo = open(ofn, "w")

  fo.write("""double double
title
transaction lag vs recv_dt (top) / dml_count count vs recv_dt (bottom)
xlabel
recv_dt (epoch)
ylabel
lag sec (top) / dml_cnt (bottom)
""")

  cur = 0

  # {<sql_id>:{
  #    <dc_id>:{
  #      'xmin':<xmin>, 'xmax':<xmax>, 'ymin':<ymin>, 'ymax':<ymax>, 
  #      'pts':[(<x1>,<y1>), 
  #             ...]}, 
  #    ...},
  #  ...}
  map_data = {}

  sql_ids = {DML_CNT_SQL_PAT: None, TRAN_LOGS_SQL_PAT: None}

  msg("Importing data from sql dump.\n")
  tran_id_dml_cnt_pts = []
  map_tran_id_recv_dt = {}
  recv_dt_tran_lag_pts = []
  recv_dt_dml_cnt_pts = []
  dc_ids = {}
  sql_bounds = {} # {<sql_id>:[<xmin>,<xmax>,<ymin>,<ymax>], ...}
  while 1:
    try:
      try:
        chunk = cPickle.load(f)
      except:
        break

      if ( chunk['type'] == "SQL_QUERY" ):
        s_sql = chunk['sql']
        sql_id = chunk['sql_id']
        sql_bounds[sql_id] = (None,None,None,None)
        if ( string.find(s_sql, DML_CNT_SQL_PAT) > -1 ):
          sql_ids[DML_CNT_SQL_PAT] = sql_id
        elif ( string.find(s_sql, TRAN_LOGS_SQL_PAT) > -1 ):
          sql_ids[TRAN_LOGS_SQL_PAT] = sql_id
      elif ( chunk['type'] == 'SQL_RESULT_CHUNK' ):
        sql_id = chunk['sql_id']
        if ( sql_id == sql_ids[DML_CNT_SQL_PAT] ):
          # populate tran_id_dml_cnt_pts
          for rec in chunk['data']:
            tran_id_dml_cnt_pts.append((rec[0],rec[4]))
        elif ( sql_id == sql_ids[TRAN_LOGS_SQL_PAT] ):
          # populate recv_dt_tran_lag_pts and map_tran_id_recv_dt
          xmin, xmax, ymin, ymax = sql_bounds[sql_id]
          for rec in chunk['data']:
            tran_id = float(rec[0])
            pub_dt = to_epoch(rec[1])
            recv_dt = to_epoch(rec[2])
            map_tran_id_recv_dt[tran_id] = recv_dt
            x = recv_dt
            y = float(recv_dt-pub_dt)
            dc_id = tran_id % 1000
            if ( dc_id not in dc_ids ): dc_ids[dc_id] = None
            recv_dt_tran_lag_pts.append((x,y,dc_id))
            if ( (xmin is None) or (x < xmin) ): xmin = x
            if ( (xmax is None) or (x > xmax) ): xmax = x
            if ( (ymin is None) or (y < ymin) ): ymin = y
            if ( (ymax is None) or (y > ymax) ): ymax = y
          sql_bounds[sql_id] = (xmin, xmax, ymin, ymax)
        else:
          # maybe emit a warning message here?
          continue

      if ( f_size is not None ):
        new_cur = f.fileobj.tell()
        if ( new_cur > cur ):
          cur = new_cur
          msg("\r%d/%d (%.3f%%)", (cur, f_size, (float(cur)/float(f_size)*100)))
      else:
        cur = cur + 1
        msg("\r%d" % cur)
    except:
      msg("\nBreaking out of sql data import:\n%s", (last_ex(),))
      break


  msg("\nJoining data to buiding graph of dml_cnt vs recv_dt.\n")
  cur = 0
  cur_pct = 0
  sql_id = sql_ids[DML_CNT_SQL_PAT]
  xmin, xmax, ymin, ymax = sql_bounds[sql_id]
  for (tran_id, dml_cnt) in tran_id_dml_cnt_pts:
    try:
      cur = cur + 1
      x = map_tran_id_recv_dt.get(tran_id, None)
      if ( x is None ): continue
      x = float(x)
      y = float(dml_cnt)
      dc_id = tran_id % 1000
      if ( dc_id not in dc_ids ): dc_ids[dc_id] = None
      if ( (xmin is None) or (x < xmin) ): xmin = x
      if ( (xmax is None) or (x > xmax) ): xmax = x
      if ( (ymin is None) or (y < ymin) ): ymin = y
      if ( (ymax is None) or (y > ymax) ): ymax = y
      recv_dt_dml_cnt_pts.append((x,y,dc_id))

      new_cur_pct = float(cur)/float(len(tran_id_dml_cnt_pts))*100
      if ( int(new_cur_pct) > int(cur_pct) ):
        cur_pct = new_cur_pct
        msg("\r%d/%d (%.3f%%)", (cur, len(tran_id_dml_cnt_pts), cur_pct))
    except:
      msg("\nBreaking out of join:\n%s", (last_ex(),))
      break
  sql_bounds[sql_id] = (xmin, xmax, ymin, ymax)

  msg("\nEmitting tran_lag vs recv_dt plot data.\n")
  yzero = 100.0
  xmin, xmax, ymin, ymax = sql_bounds[sql_ids[TRAN_LOGS_SQL_PAT]]
  emit_key(fo, xmin, xmax, dc_ids.keys())
  emit_bounds_box(fo, yzero, xmin, xmax, ymin, ymax, "sec lag", 0)
  for (x, y, dc_id) in recv_dt_tran_lag_pts:
    y = y/ymax*100.0
    fo.write(". %f %f %d\n" % (x,yzero+y,dc_id))

  msg("Emitting dml_cnt vs recv_dt plot data.\n")
  yzero = 0.0
  xmin, xmax, ymin, ymax = sql_bounds[sql_ids[DML_CNT_SQL_PAT]]
  emit_bounds_box(fo, yzero, xmin, xmax, ymin, ymax, "DMLs", 0)
  for (x, y, dc_id) in recv_dt_dml_cnt_pts:
    y = y/ymax*100.0
    fo.write("line %f %f %f %f %d\n" % (x, yzero, x, yzero+y, dc_id))

  fo.close()

if ( __name__=="__main__" ):
  main()


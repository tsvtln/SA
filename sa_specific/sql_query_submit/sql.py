#   This program is a convenient way to submit arbitrary SQL queries to HPSA
# databases from the command line.  When executed from the mm-central infra 
# server, These queries can be targetted towards any subset of HPSA databases
# in the entire mesh.  This tool also contains some hard coded convenience 
# queries that allow for reflecting various parts of the database schema.  It
# also allows for exporting of large batches of data into a gzipped compressed
# python pickle structure.
#
# Architecture description:
#
#   Each invocation represents a multi-database transaction (MDT).  That is an
# internal transaction object keeps up with a series of SQL queries targeted
# at particular databases.  These seperate database specific transactions (DSTs) are
# executed in seperate threads.  If an error occurs while executing one of
# these DSTs, then none of the DSTs in the MDT will be committed.  (Granted, 
# there is nothing to stop the user from inserting their own "commit" commands
# the sql query stream.)
#------------------------------------------------------------------------------

#

# TODO:
#
# [ ] Think up some way to express having multiple SQL queries
#     executed in the same transaction.  (Perhaps even automatically do
#     the lcrep stuff.)  (Auto rollback upon any error at any DC.)
#     "_<python_expr>" syntax -> ((<dc_ids>, ((<sql>, [<bind_vars>, [<fmt_flags>]])...))...)
#
#     [ ] Figure out a way to express seperate queries for seperate DCs.
#
#     [ ] Think up a new command line syntax that makes <python_expr> uneccessary.
#
#     [ ] Don't forget a syntax for bind vars.  (possible a python expr.)  This
#         might be a good way to deal with dates.
#
# [ ] Add some sort of display option encoding to the "SQL_QUERY" record to
#     allow for embedding formatting info.  (I suppose we will have to figure
#     out a way to allow for overriding these embedded format flags.)
#
#     [ ] segregate all the "formatting options" into a dictionary.
#

# to build:
# ./py_build pylibs/io.py pylibs/util.py pylibs/loglib.py pylibs/dblib.py pylibs/tabfmt.py sql.py

import sys,cPickle,time,string,types,threading,copy,gzip,signal
import io,util,loglib,dblib,tabfmt

log = loglib.Logger(__name__)

def usage():
  io.out("""
Usage:  %s [(-+)a] [(-+)dc <dc_ids>] [(-+)db [<user>[/<pass>]@]dbname] 
              [-i <in_file>] [-o <out_file>] [-pp] [-fs <chunk_size>] 
              [<fmt_opt> ...] [<query> ...]
-------------------------------------------------------------------------------

       <query> := (-s <schema_owner> | -t [<owner>.]<table> | -c [<owner>.]<table> |
                   -lss | <sql_query>)

       <fmt_opt> := (+w<width> | -w | +f(01) | -f | +q(01) | -q | +e(01) | -e)
        %s -h

  [-a] 
      Submit given query to every datacenter in the mesh.
      (Only works on the multimaster central spin server.)

  [-dc <dc_ids>]
      Submit given query to given datacenter ids in the coma delimited value 
      <dc_ids>.  (Only works for foreign datacenters when executed on the 
      multimaster central spin server.)

  [-r <in_file>]
      Process previously emitted gzipped pickle file <in_file>.

  [-w <out_file>]
      Emit output to file <out_file> in a gzipped pickle format.

  [-pp]
      Emit output to stdout in human readable form.  Default option.

  [-w <width>]
      Render table to width <width>.  Default is to take the width of the tty
      on stderr (fd 2).  If stderr is not a tty, then a width of 80 is assumed.

  [-f]
      Draw a full table with borders around each cell.

  [-q]
      Show SQL instead of executing it.

  [-fs <fetch_size>]
      Number of records to fetch from the database at one time.
      The default is 1000.

  <sql_query>
      A literal SQL query to be submitted.  If the value is "-", then
      the SQL is read from stdin.

  -s <owner>
      List tables that belong to the schema given by <owner>.

  -t [<owner>.]<table>
      List columns of the table given by [<owner>.]<table>.  If optional 
      <owner> isn't specified, then "truth" is assumed.

  -c [<owner>.]<table>
      Dump column level constratints for the table given by [<owner>.]<table>.
      If optional <owner> isn't specified, then "truth" is assumed.

  -lss
      List session summery for all session on the database.

  -h
      Shows this usage info.

Example:

  > ./sql -a "select job, what, last_date, next_date, failures, broken from dba_jobs where schema_user='GCADMIN'"

""" % ((sys.argv[0],)*2))

def get_all_dc_ids():
  return dblib.get_all_dcs.keys()

CHUNK_SIZE = 1000

def _execute_thread(opts):
  try:
    db_rec = {"type": "DB"}
    db_rec.update(opts.db)
    _out_fmt(db_rec, opts)
    cur = dblib.get_cursor(opts.db["cstr"])
    cur.execute(opts.s_sql)
    num = 0
    while 1:
      num = num + 1
      data = cur.fetchmany(CHUNK_SIZE)
      if ( (len(data) == 0) and (num > 1) ):
        break
      # Gather columns
      cols = tuple(map(lambda col:col[0], cur.description))
      cols_rec = {"type":"SQL_COLS", "db_id":opts.db["db_id"], "sql_id":opts.sql_id, "cols":cols}
      _out_fmt(cols_rec, opts)
      chunk = {"type":"SQL_RESULT_CHUNK", "db_id":opts.db["db_id"], "db_title":opts.db["db_title"], "sql_id":opts.sql_id, "num":num,"data":data}
      _out_fmt(chunk, opts)
  except:
    chunk = {"type":"SQL_RESULT_CHUNK", "db_id":opts.db["db_id"], "db_title":opts.db["db_title"], "sql_id":opts.sql_id, "err":util.last_ex()}
    log.err("db_id: %(db_id)d, sql_id: %(sql_id)d, err:\n%(err)s", chunk)
    try:
      _out_fmt(chunk, opts)
    except:
      pass

def _read_thread(opts):
  try:
    while 1:
      _out_fmt(cPickle.load(opts.inf), opts)
  except EOFError, e:
    pass
  except:
    log.err("Unexpected error:\n%s", util.last_ex())

g_bUseVT = sys.stdout.isatty()
def fn_fmt(r,c,pcv):
  if (r/2 == float(r)/2) and g_bUseVT:
    return "\x1b[%sm%s\x1b[m" % (string.join(map(lambda a:str(a),(1,)), ';'), pcv)
  else:
    return pcv

def _get_tty_width(n_width):
  if ( n_width == -1 ):
    fs = [sys.stdin, sys.stdout, sys.stderr]
    fs = filter(lambda f:f.isatty(), fs)
    if ( len(fs) > 0 ):
      n_width = io.ioctl_GWINSZ(fs[0])[1]
    else:
      n_width = 80
  return n_width

def _get_sql_db_id(rec):
  return "%d.%d" % (rec["sql_id"], rec["db_id"])

def _out_fmt_txt(rec, opts, map_cols_cache={}):
  val = ""
  if ( type(rec) == types.DictType ):
    if ( rec["type"] == "SQL_RESULT_CHUNK" ):
      dict_all_dcs = dblib.get_all_dcs()
      val = "\nQuery #%d on %s:\n" % (rec["sql_id"], rec["db_title"])
      if ( rec.has_key("err") ):
        val = "%s%s" % (val, rec["err"])
      else:
        rows = rec["data"]
        sql_db_id = _get_sql_db_id(rec)
        if ( map_cols_cache.has_key(sql_db_id) ):
          rows.insert(0, map_cols_cache[sql_db_id])
        opts.n_width = _get_tty_width(opts.n_width)
        val = "%s%s" % (val, tabfmt.fmtrows(rows, col_sep=" | ", fn_fmt=fn_fmt, b_header=1, n_width=opts.n_width))
    elif ( rec["type"] == "SQL_COLS" ):
      map_cols_cache[_get_sql_db_id(rec)] = rec["cols"]
    elif ( rec["type"] == "SQL_QUERY" ):
      if ( opts.b_show_sql ):
        val = "Query #%d: %s\n\n" % (rec["sql_id"], rec["sql"])
    elif ( rec["type"] in ("DB", "ERR") ):
      pass
    else:
      val = "Unknown rec type: %s\n" % repr(rec)
  else:
    val = str(rec)
  try:
    opts.of.write(val)
    opts.of.flush()
  except:
    pass

def _out_fmt_bin(rec, opts):
  #buf = cPickle.dumps(rec, 1)
  #opts.of.write(buf)
  #opts.of.flush()
  cPickle.dump(rec, opts.of, 1)

_out_fmt_lock = threading.Lock()
def _out_fmt(rec, opts):
  _out_fmt_lock.acquire()
  try:
    try:
      opts.out_fn(rec, opts)
    except:
      log.err("Unexpected error:\n%s", util.last_ex())
  except:
    log.err("Unexpected error:\n%s", util.last_ex())
    _out_fmt_lock.release()
  else:
    _out_fmt_lock.release()

class Options:
  def copy(self):
    opts = Options()
    for (k,v) in self.__dict__.items():
      if (type(v) in (types.ListType, types.TupleType, types.DictType)):
        opts.__dict__[k] = copy.deepcopy(v)
      else:
        opts.__dict__[k] = v
    log.dbg("Options.copy: %s", repr(self.__dict__))
#    opts.__dict__.update(copy.deepcopy(self.__dict__))
    return opts

def parse_cstr(cstr):
  dbname = None
  username = None
  password = None
  if ( "@" in cstr ):
    (cred, dbname) = string.split(cstr, "@")
    if ( "/" in cred ):
      (username, password) = string.split(cred, "/")
    else:
      username = cred
  else:
    dbname = cstr
  if ( username is None ):
    io.err("%s username: " % dbname)
    username = sys.stdin.readline()[:-1]
  if ( password is None ):
    io.err("%s@%s's password: " % (username, dbname))
    password = getpass("")
  return "%s/%s@%s" % (username, password, dbname)

def parse_dc_id_list(s_dc_ids, opts):
  dbs = []
  all_dcs = dblib.get_all_dcs()
  for dc_id in string.split(s_dc_ids,','):
    opts.db_id = opts.db_id + 1
    try:
      dc_id = int(dc_id)
    except:
      # Assume we are dealing with a cstr.
      cstr = parse_cstr(dc_id)
      clean_cstr = re.sub("/.*@", "@", cstr)
      db = {"db_id":opts.db_id, "db_title":clean_cstr, "cstr":cstr}
    else:
      if ( not all_dcs.has_key(dc_id) ):
        log.warn("%d: Not a valid facility id.", (dc_id,))
        continue
      dc = all_dcs[dc_id]
      db = {"db_id":opts.db_id, "dc_id":dc_id, "db_title":"Facility_id %d (%s)" % (dc_id, dc["data_center_name"]), "cstr":dc["cstr"]}
    dbs.append(db)
  return dbs

def get_schema_list_sql(s_schema):
  return """select lower(table_name) as "Table", num_rows as "Rows", last_analyzed as "Last Analyzed", floor(sysdate-last_analyzed) as "Days"
            from dba_all_tables
            where lower(owner)='%s'
            order by num_rows""" % string.lower(s_schema)

def get_table_list_sql(table_name):
  table_name = string.lower(table_name)
  sql = """select lower(column_name) as "Name", nullable as "Null?", lower(data_type) as "Type", char_length as "Len"
           from all_tab_columns"""
  if ( string.find(table_name, ".") > -1 ):
    owner, table_name = string.split(table_name, ".")
    sql = "%s\nwhere lower(owner)='%s' and lower(table_name)='%s'" % (sql, owner, table_name)
  else:
    sql = "%s\nwhere (table_name, owner) in (select table_name, table_owner from all_synonyms where lower(synonym_name)='%s')" % (sql, table_name)
  return "%s\norder by column_name" % sql

def main(args):
  opts = Options()
  opts.of = None
  opts.out_fn = None
  opts.inf = None
  opts.sql_id = 0
  opts.db_id = 0
  opts.b_show_sql = 0
  opts.n_width = -1
  dbs = parse_dc_id_list("%d" % dblib.get_local_dc_id(), opts)
  b_first_sql_query = 1

  thrds = []

  while len(args) > 0:
    cur_arg = util.shift(args)
    if ( cur_arg == "-a" ):
      dbs = parse_dc_id_list(string.join(map(lambda i:"%d" % i,dblib.get_all_dcs().keys()),","), opts)
    elif ( cur_arg == "-dc" ):
      if ( len(args) == 0 ):
        log.err("-dc option requires a list of datacenter ids.")
        continue
      try:
        s_dc_ids = util.shift(args)
        dbs = parse_dc_id_list(s_dc_ids, opts)
      except:
        log.err("%s: Unexpected error while parsing datacenter id list:\n%s", (s_dc_ids, util.last_ex()))
    elif ( cur_arg in ("--help", "-h") ):
      usage()
      sys.exit(1)
    elif ( cur_arg == "-o" ):
      ofn = util.shift(args)
      if ( opts.of is not None ):
        log.warn("%s: Output file already established, can't be changed midstream.", (ofn,))
        continue
      try:
        if ( ofn == "-" ):
          opts.of = gzip.GzipFile(fileobj=sys.stdout, mode="w")
        else:
          opts.of = gzip.open(ofn, "w")
      except:
        log.warn("%s: Unable to open for writing, ignoring.", (ofn,))
        continue
      opts.out_fn = _out_fmt_bin
    elif ( cur_arg == "-i" ):
      if ( opts.of is None ):
        opts.of = sys.stdout
        opts.out_fn = _out_fmt_txt
      ifn = util.shift(args)
      try:
        opts.inf = gzip.open(ifn)
      except:
        log.warn("%s: Unable to open for reading, ignoring.", (ifn,))
        continue
      thrd = threading.Thread(name="sql._read_thread", target=_read_thread, args=(opts.copy(),))
      thrd.start()
      thrds.append(thrd)
    elif ( cur_arg == "-pp" ):
      opts.of = sys.stdout
      opts.out_fn = _out_fmt_txt
    elif ( cur_arg == "-q" ):
      opts.b_show_sql = 1
    elif ( cur_arg == "-w" ):
      s_width = util.shift(args)
      try:
        n_width = int(s_width)
      except:
        log.warn("%s: Failed to parse width", (s_width,))
        log.dbg("%s", util.last_ex())
      else:
        if ( (n_width > 10) or (n_width == -1) ):
          opts.n_width = n_width
        else:
          log.warn("%d: Invalid width (-w) value, ignoring.", (n_width,))
    elif ( cur_arg == "-s" ):
      if ( len(args) == 0 ):
        log.err("-s option requires a schema name")
        usage()
        continue
      args.insert(0, get_schema_list_sql(util.shift(args)))
    elif ( cur_arg == "-t" ):
      if ( len(args) == 0 ):
        log.err("-t option requires a table name")
        usage()
        continue
      args.insert(0, get_table_list_sql(util.shift(args)))
    elif ( cur_arg[0] == "-" ):
      log.warn("%s: Unrecognized option, ignoring.", (cur_arg,))
    else:
      # Assume this arg is an SQL query to be evaluated.
      if ( opts.of is None ):
        opts.of = sys.stdout
        opts.out_fn = _out_fmt_txt
      if ( b_first_sql_query ):
        b_first_sql_query = 0
        if ( opts.of is not sys.stdout ):
          io.err("Press Ctrl-\\ to obtain status info.\n")
          signal.signal(signal.SIGQUIT, sigquit_handler)
      if ( cur_arg == "-" ):
        opts.s_sql = sys.stdin.read()
        if ( s_sql == "" ):
          log.warn("Empty sql submitted via stdin.  Ignoring...")
          continue
      else:
        opts.s_sql = cur_arg
      opts.sql_id = opts.sql_id + 1
      _out_fmt({"type":"SQL_QUERY", "sql_id":opts.sql_id, "sql":opts.s_sql}, opts.copy())
      for db in dbs:
        dc_opts = opts.copy()
        dc_opts.db = db
        thrd = threading.Thread(name="sql._execute_thread", target=_execute_thread, args=(dc_opts,))
        thrd.start()
        thrds.append(thrd)

  try:
    # Wait for all sql threads to finish.
    for thrd in thrds:
      thrd.join()
  except KeyboardInterrupt, e:
    io.err("Interrupted.\n")
    _out_fmt({"type":"ERR", "err":"Interrupted."}, opts)

  if (opts.out_fn is _out_fmt_txt):
    opts.of.write("\n")

  try:
    if ( opts.of is None ):
      log.warn("No SQL query supplied.")
      usage()
    elif ( opts.of is not sys.stdout ):
      opts.of.close()
  except:
    log.err("%s: Failed to close.", (opts.of,))

def _emit_status_thread():
  io.err("TODO - implement _emit_status_thread.\n")

def sigquit_handler(sig, frame):
  try:
    threading.Thread(name="sql._emit_status_thread", target=_emit_status_thread, args=()).start()
  except:
    err.io("Failed to start status emission thread due to:\n%s", (util.last_ex(),))

if ( __name__ == "__main__" ):
  main(sys.argv[1:])
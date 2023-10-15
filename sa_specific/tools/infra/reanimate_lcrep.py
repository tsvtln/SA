# Assumes a lcrep dump taken as follows:
#   ./sql -o lcrep_dump.pkl.gz "select * from transactions" "select * from transaction_dml" "select * from dml_values"
#
# todos:
#
# [ ] tran_dml_id needs to be differentiated with dc_id.
# [ ] code to create aaa/truth tables and indexes.
# [ ] code to itterate through trans and resurrect records.
#
try:
  import sqlite3 as sql
except ImportError, e:
  import sqlite as sql

import gzip, cPickle, sys, string, os, types, datetime, time, re

def msg(s, args=None):
  if ( args is not None ):
    s = s % args
  sys.stdout.write(s)
  sys.stdout.flush()

fns = sys.argv[1:]
if ( fns[0][-3:] == ".db" ):
  sql_fn = fns[0]
  del fns[0]
else:
  sql_fn = fns[0] + ".db"
con = sql.connect(sql_fn)

# to force 8-bit bytestrings.
con.text_factory = str

cur = con.cursor()

# >>> string.join(map(lambda i:"%s %s%s" % (i['name'], {'int':'int','long':'int','dateTime.iso8601':'real','string':'text'}[i['type']], i['is_unique']==1 and ' unique' or ''), spin._Transaction.getFields()),',')
# 'tran_id int unique,username text,force int,conflicting int,conflicted_elsewhere int,create_dt real,publish_dt real,update_all int,is_republish int,replicate_flg int,signature text,publish_order_id int'
map_table_create_sql = {
  "transactions": "create table transactions(tran_id int primary key,username text,force int,conflicting int,conflicted_elsewhere int,create_dt real,publish_dt real,update_all int,is_republish int,replicate_flg int,signature text,publish_order_id int)",
  "transaction_dml": "create table transaction_dml(tran_dml_id int primary key,tran_id int,table_name text,dml_type text,dml_order int)",
  "dml_values": "create table dml_values(tran_dml_id int,column_name text,data_type text,old_value text,new_value text,pk int)",
  "transaction_conflicts": "create table transaction_conflicts(tran_conflict_id int primary key, conflict_dt date, conflict_tran_id number, current_tran_id number, exception_text varchar2, incoming_tran_id number, resolved varchar2, tran_dml_id number)"
  }

def create_table(table_name):
  sql = map_table_create_sql[table_name]
  try:
    cur.execute(sql)
    con.commit()
    msg("Created table %r.\n", (table_name,))
  except:
    msg("Looks like table %r already exists, skipping.\n", (table_name,))

create_table("transactions")
create_table("transaction_dml")
create_table("dml_values")
create_table("transaction_conflicts")

map_sql_re_to_table = {
  re.compile(" from transactions", re.IGNORECASE): "transactions",
  re.compile(" from transaction_dml", re.IGNORECASE): "transaction_dml",
  re.compile(" from dml_values", re.IGNORECASE): "dml_values",
  re.compile(" from transaction_conflicts", re.IGNORECASE): "transaction_conflicts"
  }

for fn in fns:
  msg("%s -> %s\n", (fn, sql_fn))
  f = gzip.open(fn)
  dbs = {}
  map_sql_id_to_table = {}
  cur_progress = -1
  f_size = os.fstat(f.fileobj.fileno())[6]
  while 1:
    try:
      chunk = cPickle.load(f)
    except:
      break
    if ( chunk['type'] == 'DB' ):
      dbs[chunk['db_id']] = chunk
      chunk['cols'] = {}
    elif ( chunk['type'] == 'SQL_QUERY' ):
      for r, table_name in map_sql_re_to_table.items():
        if ( r.search(chunk['sql']) ):
          map_sql_id_to_table[chunk['sql_id']] = table_name
          msg("\rIdentified sql query %r(%d) as table %r.\n", (chunk['sql'], chunk['sql_id'], table_name))
          break
    elif ( chunk['type'] == 'SQL_COLS' ):
      dbs[chunk['db_id']]['cols'][chunk['sql_id']] = chunk['cols']
    elif ( chunk['type'] == 'SQL_RESULT_CHUNK' ):
      db_id = chunk['db_id']
      dc_id = dbs[db_id]['dc_id']
      sql_id = chunk['sql_id']
      col_names = dbs[db_id]['cols'][sql_id]
      cols = string.join(map(lambda i:i, col_names),",")
      val_vars = string.join(("?",) * len(col_names), ", ")
      try:
        sql = "insert into %s (%s) values (%s)" % (map_sql_id_to_table[sql_id], cols, val_vars)
        cur.executemany(sql, chunk['data'])
      except:
        print sql
        raise
      con.commit()

    new_progress = f.fileobj.tell()
    if ( (new_progress != cur_progress) or (new_progress == f_size) or (cur_progress == -1) ):
      cur_progress = new_progress
      msg("\r%d/%d (%.3f%%)" % (cur_progress, f_size, (float(cur_progress)/float(f_size)*100)))

msg("\nDone.\n")


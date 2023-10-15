#!/opt/opsware/bin/python2
#                      -*- Mode: Python ; tab-width: 4 -*- 

import sys,os,pwd,string,getopt,types,time,traceback,threading,re

if ( sys.executable == "/lc/bin/python" ):
  sys.path.extend( ["/lc/blackshadow", "/cust/usr/blackshadow", "/cust/usr/blackshadow/spin"] )
  os.chdir("/cust/usr/blackshadow/spin")
elif ( string.find(sys.executable,"/opt/opsware/bin/python") == 0 ):
  if (sys.version[0] == "2"):
    sys.path.append( "/opt/opsware/pylibs2" )
  else:
    sys.path.append( "/opt/opsware/pylibs" )
  sys.path.append( "/opt/opsware/spin" )
try:
  import truthdb, spinobj, truthtable, multimaster, spinconf
  from spinerror import *
except ImportError, e:
  if (not os.environ.has_key('ENV_PY_VER_RETRY')):
    os.environ['ENV_PY_VER_RETRY'] = "1"
    exec_path = sys.executable
    if ( exec_path[-1] == '2' ):
      exec_path = exec_path[:-1]
    else:
      exec_path = "%s2" % exec_path
    os.execv(exec_path, [exec_path] + sys.argv)
  raise

g_bDebug = 0

def debug(s):
	sys.stderr.write("%s: %s: DEBUG: %s\n" % (sys.argv[0], threading.currentThread()._Thread__name, s))

def warn(s):
	sys.stderr.write("%s: %s: WARN: %s\n" % (sys.argv[0], threading.currentThread()._Thread__name, s))

def println(s):
	sys.stdout.write("%s\n")

method = "table_checker"
user = pwd.getpwuid(os.getuid())[0]
dc_names = {}

def usage():
	sys.stderr.write( 
"""Usage:  table_checker.py [--sql] [--debug] [-c <obj_classes>] 
          [-x <obj_classes>] [--file fname] [--simple] [-d <core_ids>] 
          [--verbose] [--client-hashing] <ids>

  -c <obj_classes>
      A comma delimited list of Spin class names such as 'Device' to check.  If
      no classes are specified, then all classes are checked.

  -x <obj_classes>
      A comma delimited list of Spin class names to exclude from being checked.

  --file <file>
      A file where each line lists a class name and an object id seperated by a
      space.  For example, the output from a previous --simple run.  Only those
      objects will be checked; -c, -x, and any <ids> are ignored.or is

  --simple
      Only output object names and  IDs, allowing easier parsing.  (Now default
      behavior.)

  --core_ids <core_ids>
      A comma-seperated list of all cores to check.  If not supplied, all cores
      in the mesh are checked.

  --verbose
      For any objects detected out of sync, will output specific information as
      to why this object is out of sync.

  --client_hashing
      Forces use  of client-side  hashing.  (Server side  hashing is  much more
      effecient because less  data ends up getting sent to  the client, and the
      processing  time needed to  perform the  hashing gets  distributed across
      multiple oracle server.)

  <ids>
      A space delimited list of object  ids to check for the given classes.  If
      no IDs are specified, all objects in the given classes are checked.

""" )
	sys.exit( 1 )

def dump_id_diffs( cls_name, obj_ids ):
	for obj_id in obj_ids:
		sys.stdout.write("%s %s\n" % (cls_name, obj_id))

# Effects: Parses object specifications from file object <ofi>.  Reads no more
#   than <chunk_size> items.  Returns <true> if items are parsed, returns 
#   <false> if no more data is avialable via <ofi>.
# Modifies: <map_obj_ids> - Items added parsed from <ofi>
def get_cls_obj_ids(ofi, map_obj_ids, chunk_size):
	ids = []
	bDataRead = 0
	while 1:
		sLine = ofi.readline()
		if (sLine):
			bDataRead=1
			# Collect each line as "<cls_name>:<id>" or "<cls_name> <id>"
			(obj_cls, obj_id) = string.split( string.replace(string.strip(sLine),':', ' '), None, 1 )
			if ( map_obj_ids.has_key(obj_cls) ):
				obj_ids = map_obj_ids[obj_cls]
			else:
				obj_ids = []
			obj_ids.append(obj_id)
			map_obj_ids[obj_cls] = obj_ids
			if (len(obj_ids) == chunk_size):
				break

	return bDataRead

# Used to submit small sql queries to a set of cores.
def submit_sql(core_id, all_dcs, method, user, sSql, mapResults):
	# Allocate a db cursor.
	db = multimaster.getDB( method, user, all_dcs[core_id].getDBName() )
	cur = db.getCursor()

	cur.execute(sSql)
	mapResults[core_id] = cur.fetchall()

# Returns (('col1', <data_type>, <col_length>),...)
def get_table_schema( db, table_name ):
	# Calculate the owner of the table.
	sOwner = 'truth'
	if ( string.find(table_name, ".") > -1 ):
		(sOwner, table_name) = string.split(table_name, '.')

	# Grab the column schema info for this table from all cores.
	sSql = "select lower(column_name), lower(data_type), data_length from dba_tab_columns where lower(owner)='%s' and lower(table_name)='%s'" % (sOwner, table_name)
	cur = db.getCursor()
	cur.execute(sSql)

	# Return the schema result.
	return cur.fetchall()

def get_class(db, cls_name):
	cls = getattr(spinobj,cls_name)(db)

	# In case we are running on a pre-7.0 spin without a compound_id_delimiter.
	if (not hasattr( cls, "compound_id_delimiter" ) ):
		cls.compound_id_delimiter = '-'

	return cls

# The goal of this function is to pack table columns using as few server-side
# hash invocations as possible.  The reason for the need to do this is that
# Oracle has an upper limit of 4000 characters for concatinated items.  The
# algorythm below sorts the columns by length and collects them together into
# bundles that are no longer than 4000 characters long.
def gen_hash_col( lstTabSchema, sHashFunc, lstOtherCols ):
	MAX_COL_LEN=4000
	# Sort the table schema by data length.
	lstTabSchema.sort(lambda x,y:x[2]-y[2])

	# Itterate over every column in the table schema
	lstCols = []
	lstCol = []
	lLen = 0
	for lstCurCol in lstTabSchema:
		if (lstCurCol[0] in lstOtherCols):
			lCurColLen = lstCurCol[2]
			sCurCol = lstCurCol[0]
			if ( lstCurCol[1] == "date" ):
				sCurCol = "hextoraw(rawtohex(%s))" % sCurCol
			if ( lstCol and (lCurColLen > (4000 - lLen - 1)) ):
				lstCols.append(lstCol)
				lstCol = []
				lLen = 0
			else:
				lstCol.append(sCurCol)
			lLen = lLen + lstCurCol[2] + 1

	if ( lstCol ): lstCols.append(lstCol)
	lstCols = map(lambda col,hf=sHashFunc:hf % string.join(col,"||'|'||"), lstCols)
	if ( len(lstCols) == 1 ):
		return lstCols[0]
	elif ( len(lstCols) > 1 ):
		return sHashFunc % string.join(lstCols, "||")
	else:
		return ''

def gen_id_and_hash_cols( lstTabSchema, cls )
	# Get a list of id columns.

	# Combine id coumns using the class id seperator.

	# Itterate over every schema item.
		# Filter out id columns, "tran_id", and "conflicting".

	# Return the id column and hash column
	return id_col, hash_col
	pass

# Requires: <ids> does not overflow Oracle's limit on the number of items in
#   then in clause.
# Effects: Returns an SQL query for the ids specified by <ids> of spin class 
#   <cls_name>.  The returned records from this query are of the form 
#   (<obj_id>, <obj_hash>).
def gen_ids_sql_query(ids, cls_name):
	# Lookup the schema for the table corresponding to the given class name.
	cls = get_class(db, cls_name)
	table_name = cls._name.table
	lstTabSchema = get_table_schema( db, table_name )

	# Inject a fake schema item for the conflicting column.
	lstTabSchema.append(("(CASE WHEN UPPER(conflicting)='Y' THEN to_Char(LCRepPkg.global_db_id) ELSE '' END)", "varchar2",1))

	# Generate class id and hash columns
	(id_col, hash_col) = gen_id_and_hash_cols( lstTabSchema, cls )

	# Construct complete sql query.
	sql = "SELECT %s id, %s from %s where id in %s" % (id_col, hash_col, table_name, ids)
	return sql

# Effects: Returns an sql query that will agregate the object hash records of 
#   the table corresponding to <cls_name> in <num_buckets> buckets.  Uses the 
#   db cursor <cur> to probe the schema.  The returned records from this query
#   are of the form (<bucket_hash>, <aggr_obj_hash>, <aggr_obj_count>).
def gen_bucketed_sql_query(cur, cls_name, num_buckets):
	pass

# Effects: Returns an sql query that will return only those records which are
#   members of the buckets given by <lstMaxBucketCounts>.  And using the DB
#   cursor <cur> to probe the schema.  Returned records from this query are 
#   the form (<obj_id>, <obj_hash>).  The SQL "IN" clause will be limited to
#   <max_in_size> items, and the SQL query will be constructed to return no
#   more than <max_recs> records.
# Modifies: <lstMaxBucketCounts> - Consumes a subset of entries used in
#   generating the sql query.
def gen_cls_sql_query(cur, cls_name, lstMaxBucketCounts, max_in_size, max_recs):
	pass

def populateRecords( core_id, all_dcs, method, user, rec_counter, sql_query, fnProg, mapRSs):
	DB_FETCH_CHUNK_SIZE=100000

	# Allocate a db connection.
	db = multimaster.getDB( method, user, all_dcs[core_id].getDBName() )

	# Get the cursor for this db connection.
	cur = db.getCursor()

	# Submit the sql query.
	cur.execute(sql_query)

	while 1:
		rs = cur.fetchmany(DB_FETCH_CHUNK_SIZE)
		if g_bDebug: debug("rs[:1]: %s\n" % str(rs[:1]))
		if ( not rs ): break
		if ( mapRSs ):
			if (!mapRSs.has_key(core_id)): mapRSs[core_id] = []
			mapRSs[core_id].extend(rs)
		rec_counter.addRecords(core_id, rs)
		fnProg(len(rs))

# Effects: Submits SQL query, <sql_query>, to the datacenters given in the list 
#   <core_ids>.  Each of these <core_ids> must be a member of the map 
#   <all_dcs>.  The records returned must be in the for (<id>, <hash>) and will
#   be scanned for differences.  This function's memory usage is not bounded,
#   so it is up to the caller to construct <sql_query> such that it does not
#   cause us to run out of memory.  Returns a list of <id>'s that differ 
#   between the datacenters in <core_ids>.  <fnProg> is a callback of the form
#   (lambda nRecs:) where <nRecs> is the number of records processed.
def diffRecords(all_dcs, core_ids, sql_query, fnProg=None, mapRSs=None):
	rec_counter = RecordCounter(core_ids)
	multimaster.branchThreads( core_ids, all_dcs, method, user, populateRecords, (rec_counter, sql_query, fnProg, mapRSs) )
	return rec_counter.getIdDiffs()

# Effects: Returns the total number of records occupied by the differing 
#   buckets and returns a list where each element is a tuple of the form
#   (<bucket_id>, <max_rec_count>), that encodes the max count of records in 
#   that bucket across the entire mesh.
def process_bucket_diffs(bucket_diffs, mapRSs):
	mapBucketCounts = {}
	mapMaxBucketCounts = {}
	for core_id in mapRSs.keys():
		rs = mapRSs[core_id]
		for rec in rs:
			bucket_id = rec[0]
			if (not mapBucketCounts.has_key(bucket_id)):
				bucket_count = 0
				max_bucket_count = 0
			else:
				bucket_count = mapBucketCounts[bucket_id]
				max_bucket_count = mapMaxBucketCounts[bucket_id]
			mapBucketCounts[bucket_id] = bucket_count + rec[2]
			if (rec[2] > max_bucket_count):
				mapMaxBucketCounts[bucket_id] = rec[2]
	lTotDiffObjRecs = 0
	for bucket_id in bucket_diffs:
		lTotDiffObjRecs = lTotDiffObjRecs + mapBucketCounts[bucket_id]
	return (lTotDiffObjRecs, mapMaxBucketCounts.items())

# Effects: Maximum number of items to allow in a SQL "IN" clause is given by 
#   <max_in_size>.  Maximum number of records to process at a time is given by
#   <max_recs>.
#
def check_classes(cur, core_ids, all_dcs, cls_names, skip_cls_names, max_in_size, max_recs):
	println("%s: Performing agregate comparisons." % cls_name)
	bucketed_sql_query = gen_bucketed_sql_query(cur, cls_name, max_in_size)
	mapRSs = {}
	bucket_diffs = diffRecords(all_dcs, core_ids, bucketed_sql_query, mapRSs=mapRSs)
	if ( not bucket_diffs ):
		println("%s: In sync" % cls_name)
	else:
		println("%s: Not in sync: Performing record-level analysis")

		# TODO: change process_bucket_diffs so that it also accounts for sql "in" clause and max_records.
		(lTotDiffObjRecs, lstMaxBucketCounts) = process_bucket_diffs(bucket_diffs, mapRSs)

		# TODO: deal with condition that one of the bucket counts overflows <max_recs>.

		prog_bar = ProgressBar(lTotDiffObjRecs)

		while 1:
			if ( not lstMaxBucketCounts ): break
			sql_query = gen_cls_sql_query(cur, cls_name, lstMaxBucketCounts, max_in_size, max_recs)
			id_diffs = diffRecords(all_dcs, core_ids, sql_query, lambda n,p=prog_bar:p.addToProg(n))
			dump_id_diffs(cls_name, id_diffs)

def main():
	MAX_IN_SIZE=990
	MAX_REC_SIZE=10000000

	try:
		(cls_names, skip_cls_names, ofi, core_ids, verbose, client_hashing, ids) = getOptions()
	except getopt.error:
		sys.stderr.write( str(sys.exc_info()[1]) + "\n" )
		usage()

	all_dcs = multimaster.getAllDcs( method, user )
	global dc_names
	for dc in all_dcs.values():
		dc_names[dc.getID()] = str(dc)

	# If no core ids where specified then use them all.
	if (not core_ids):
		core_ids = all_dcs.keys()

	# Count of errors encountered while looping over classes.
	errs = 0

	# Create a db cursor for use in probing the the schema.
	db = truthdb.DB()
	cur = db.getCursor()

	# If we have a file input object.
	if ( ofi ):
		while 1:
			# Process object ids from he input fil in chunks.
			map_cls_obj_ids = {}
			while get_cls_obj_ids(ofi, map_cls_obj_ids, MAX_IN_SIZE):
				for cls_name, obj_ids in map_cls_obj_ids.items():
					sql_query = gen_ids_sql_query(obj_ids, cls_name)
					id_diffs = diffRecords(all_dcs, core_ids, sql_query, Prog)
					dump_id_diffs(cls_name, id_diffs
				map_cls_obj_ids = {}
	else:
		for cls_name in cls_names:
			if ( cls_name in skip_cls_names ):
				continue

			if ( ids ):
				# Process ids in chunks.
				while ids:
					obj_ids = ids[:MAX_IN_SIZE]
					del ids[:MAX_IN_SIZE]
					sql_query = gen_ids_sql_query(cur, ids, cls_name)
					id_diffs = diffRecords(all_dcs, core_ids, sql_query, Prog)
					dump_id_diffs(cls_name, id_diffs)
				break
			else:
				try:
					check_classes(cur, core_ids, all_dcs, cls_names, skip_cls_names, MAX_IN_SIZE, MAX_REC_SIZE)
				except KeyboardInterrupt:
					sys.stderr.write( "Keyboard interrupt!  Skipping...\n" )
					errs = errs + 1
				except:
					sys.stderr.write( "ERROR checking %s:\n" % cls_name )
					traceback.print_exc()
					errs = errs + 1

	if errs:
		sys.stderr.write( "\nWARNING:  %d errors were encountered!\n" % (errs) )

# Returns an integer major version for the PL/SQL engine.  like 9, 10, 11, etc.
def getPL_SQL_MajorVersion(sPlsqlVersion):
	try:
		return int(re.compile('.*? (\d+).\.*?').match(sPlsqlVersion).group(1))
	except:
		sys.stderr.write("Failed to obtain PL/SQL version from %s." % (sPlsqlVersion))
		raise
	
def getLowestOraVersion(core_ids, all_dcs, method, user):
	# Ask all datacenters what version of oracle they are running.
	sSql = "select banner from v$version where banner like '%PL/SQL%'"
	mapResults = {}
	multimaster.branchThreads( core_ids, all_dcs, method, user, submitSQL, (sSql, mapResults) )
	lstOraVers = mapResults.values()
	debug( "lstOraVers: %s" % str(lstOraVers) )
	try:
		lstOraVers = map(lambda v:int(re.compile('.*? (\d+).\.*?').match(v[0][0]).group(1)), lstOraVers)
	except:
		sys.stderr.write("Failed to obtain PL/SQL version from %s." % str(mapResults))
		raise
	lLowestOraVer = lstOraVers[0]
	for lCurVer in lstOraVers:
		if ( lCurVer < lLowestOraVer ): lLowestOraVer = lCurVer
	return lLowestOraVer

def checkTables( cls_list, skip_list, ids, verbose, client_hashing, core_ids = None ):
	all_dcs = multimaster.getAllDCs( method, user )
	global dc_names
	for dc in all_dcs.values():
		dc_names[dc.getID()] = str(dc)
	if core_ids is None:
		core_ids = all_dcs.keys()

	hash_func = "ora_hash(%s)"
	if ( not client_hashing ):
		if ( getLowestOraVersion(core_ids, all_dcs, method, user) < 10 ):
			hash_func = "dbms_utility.get_hash_value(%s,-2147483647,2147483647)"
	debug( "client_hashing: %s, hash_func: %s\n" % ( client_hashing, hash_func ) )

	db = truthdb.DB()
	errs = 0
	for cls in cls_list:
		if cls in skip_list:
			continue
		try:
			cls = spinobj.getObjectClass( cls )(db)
			checkObjects( user, cls, all_dcs, core_ids, ids, verbose, client_hashing, hash_func )
		except KeyboardInterrupt:
			sys.stderr.write( "Keyboard interrupt!  Skipping...\n" )
			errs = errs + 1
		except:
			sys.stderr.write( "ERROR checking %s:\n" % (cls) )
			traceback.print_exc()
			errs = errs + 1

        # If we have explicit ids, then we only want to check these ids against
        # the first class specified.
        if (ids): break

	return errs

def Prog(nRecs):
	sys.stdout.write("Prog(%s)\n" % nRecs)


def checkObjects( user, cls, all_dcs, core_ids, ids, verbose = 0, client_hashing = 0, hash_func = "(%s)" ):
	cls_name = cls.obj_class

	# First suck up all objects from all DBs
	rec_counter = RecordCounter(cls_name, core_ids)
	lstTabSchema = getTableSchema( core_ids, all_dcs, cls.table_name )
	select_from_clause = genSelectFromClause( cls, lstTabSchema, client_hashing, hash_func )
	multimaster.branchThreads( core_ids, all_dcs, method, user, populateObjects, (rec_counter, client_hashing, hash_func, cls, select_from_clause, ids) )

	sys.stderr.write( "\n%s object diffs:\n" % (cls_name) )

	# Dump all object differences.
	for obj_id in rec_counter.getIdDiffs():
		sys.stdout.write("%s %s\n" % (cls_name, obj_id))

import string, struct, termios, fcntl, tty
# hack for python 1.5.x version of termios that seems to lack TIOCGWINSZ.
if ( not hasattr(termios,"TIOCGWINSZ") ):
	if ( string.find( sys.platform, "linux" ) > -1 ): termios.TIOCGWINSZ=21523
	elif ( string.find( sys.platform, "freebsd" ) > -1 ): termios.TIOCGWINSZ=1074295912
	elif ( string.find( sys.platform, "solaris" ) > -1 ): termios.TIOCGWINSZ=21608

def ioctl_GWINSZ( fo ):
	size = (25, 80)
	if ( fo.isatty() ):
		try:
			size = struct.unpack('hh', fcntl.ioctl(fo.fileno(), termios.TIOCGWINSZ, 'abcd'))
		except:
			pass
	return size

def printProgress( fo, f, sMsg=None ):
	width = ioctl_GWINSZ( fo )[1]
	sPct = "%s%%" % (("%3d" % (100 * f))[-3:])
	sVT_Pct = "\x1b[2K\x0d\x1b[1m%s\x1b[m" % sPct
	sMsg = sMsg[-(width-len(sPct)-13):]
	lTotal = int(max(width - len(sPct) - 3 - len(sMsg), 0))
	lFull = int(max(lTotal * min(f,1.0), 1))
	lUnFull = lTotal - lFull
	sPB = "%s[%s%s%s]%s" % (sVT_Pct, '=' * (lFull-1), '>', ' ' * lUnFull, sMsg)
	fo.write(sPB)
	fo.flush()

class RecordCounter:
	def __init__( self, core_ids ):
		self.core_ids = core_ids
		self.lnum_cores = len(core_ids)
		self.cores_heard_from = []
		self.ltr = 0  # Total recieved records.
		self.lte = 0  # Total expected records.
		self.lts = time.time()
		self.mapObjHashCounts = {} # {obj_id:[last_obj_hash, count]}
#		self.mapObjHashes = {} # {obj_id:last_hash}
		self.lstObjDiffs = []
		self.lock = threading._allocate_lock()

	# lstObjRecs -> [(id1,row1_hash), (id2,row2_hash), ...]
	def addRecords( self, core_id, lstObjRecs, bClientHash = 0 ):
		self.lock.acquire()
		try:
			for obj_rec in lstObjRecs:
				if ( obj_rec == None ):
					continue
				obj_id = obj_rec[0]
				if ( bClientHash ):
					obj_hash = hash(str(obj_rec[1:]))
				else:
					obj_hash = obj_rec[1]
				if (self.mapObjHashCounts.has_key(obj_id)):
					count = self.mapObjHashCounts[obj_id][1]
					last_hash = self.mapObjHashCounts[obj_id][0]
					if ( last_hash != obj_hash ):
						self.lstObjDiffs.append(obj_id)
						del self.mapObjHashCounts[obj_id]
						continue
					count = count + 1
					if ( count == self.lnum_cores):
						del self.mapObjHashCounts[obj_id]
					else:
						self.mapObjHashCounts[obj_id][1] = count
				else:
					if ( not obj_id in self.lstObjDiffs ):
						self.mapObjHashCounts[obj_id] = [obj_hash, 1]
		except Exception, e:
			self.lock.release()
			raise
		self.ltr = self.ltr + len(lstObjRecs)
		self.lock.release()

	def done( self, core_id ):
		pass

	def incTotalExpected( self, core_id, lte ):
		self.lock.acquire()
		if ( not (core_id in self.cores_heard_from)):
			self.cores_heard_from.append(core_id)
		self.lte = self.lte + lte
		self.lock.release()

	def getIdDiffs( self ):
		# Return differing and missing object ids.
		return self.lstObjsDiffs + self.mapObjHashCounts.keys()

	def resetStartTime( self ):
		self.lts = time.time()

	# lts - time started
	# ltr - # total recieved
	# lte - # total expected
	def calcETA( self ):
		lct = time.time() # current time.
		lts = min(self.lts, lct - 1)
		ltr = min(self.ltr, self.lte)
		ltd = lct - lts
		lEta = (self.lte - ltr) * (float(ltd) / ltr)
		lhs = int(lEta / 60 / 60)
		lms = int((lEta / 60) - (lhs * 60))
		lss = int(lEta - (lhs * 60 * 60) - (lms * 60))
		return " ETA: %.2d:%.2d:%.2d" % (lhs, lms, lss)

	def printProgress( self, fo ):
		if ( len(self.cores_heard_from) == len(self.core_ids) ):
			printProgress( fo, float(self.ltr)/self.lte, self.calcETA() )

def populateObjects( core_id, all_dcs, method, user, rec_counter, client_hashing, hash_func, cls, select_from_clause, ids ):
	DB_FETCH_CHUNK_SIZE=100000
	BIND_VAL_CHUNK_SIZE=100

	# Allocate a db connection.
	db = multimaster.getDB( method, user, all_dcs[core_id].getDBName() )

	# Get the cursor for this db connection.
	cur = db.getCursor()

	# If we have explicit IDs to check for this class.
	if ids:
		# In case we are running on a pre-7.0 spin without a splitCompoundID method.
		if ( not hasattr(cls, "splitCompoundID") ):
			cls.splitCompoundID = lambda id: string.split(id,'-')

		rec_counter.incTotalExpected(core_id, len(ids))

		sys.stderr.write( "Populating %d %s objects from %s...\n" % (len(ids), cls.obj_class, dc_names[core_id]) )
		ids = ids[:]
		while ids:
			obj_ids = ids[:BIND_VAL_CHUNK_SIZE]
			del ids[:BIND_VAL_CHUNK_SIZE]
			id_columns = tuple(map(lambda f:f.name, cls.getIDFields()))
			sql_id = "to_char(%s)" % string.join(id_columns, "||'" + cls.compound_id_delimiter + "'||")
			in_clause = "in (%s)" % string.join(map(lambda i:":p%d" % i, range(len(obj_ids))),',')
			where_clause = "where %s %s" % (sql_id, in_clause)
			sql_query = select_from_clause + where_clause
			debug("sql_query: '%s'\n" % sql_query)
			cur.execute(sql_query, obj_ids)
			rs = cur.fetchall()
			debug("rs[:1]: %s\n" % str(rs[:1]))
			rec_counter.addRecords(core_id, rs, client_hashing)
			rec_counter.printProgress(sys.stderr)
		rec_counter.done(core_id)
	else:
		# Get the count of records for the given class.
		cur.execute("select count(*) from %s" % cls._table.name)
		cls_rec_count = long(cur.fetchone()[0])
		rec_counter.resetStartTime()
		rec_counter.incTotalExpected(core_id, cls_rec_count)
		sys.stderr.write( "Populating %d %s objects from %s...\n" % (cls_rec_count, cls.obj_class, dc_names[core_id]) )

		# query for all records for diff testing.
		sql_query = select_from_clause
		debug("sql_query: '%s'\n" % sql_query)
		cur.execute(sql_query)
		while 1:
			rs = cur.fetchmany(DB_FETCH_CHUNK_SIZE)
			debug("rs[:1]: %s\n" % str(rs[:1]))
			if ( not rs ): break
			rec_counter.addRecords(core_id, rs, client_hashing)
			rec_counter.printProgress(sys.stderr)
		rec_counter.done(core_id)
	debug( "Done populating from %s...\n" % (dc_names[core_id]) )

# Used to submit small sql queries to a set of cores.
def submitSQL(core_id, all_dcs, method, user, sSql, mapResults):
	# Allocate a db cursor.
	db = multimaster.getDB( method, user, all_dcs[core_id].getDBName() )
	cur = db.getCursor()

	cur.execute(sSql)
	mapResults[core_id] = cur.fetchall()

# Returns (('col1', <data_type>, <col_length>),...)
# Queries all cores and exits with error if a schema diff is detected.
def getTableSchema( core_ids, all_dcs, sTabName ):
	# Calculate the owner of the table.
	sOwner = 'truth'
	if ( string.find(sTabName, ".") > -1 ):
		(sOwner, sTabName) = string.split(sTabName, '.')

	# Grab the column schema info for this table from all cores.
	sSql = "select lower(column_name), lower(data_type), data_length from dba_tab_columns where lower(owner)='%s' and lower(table_name)='%s'" % (sOwner, sTabName)
	mapResults = {}
	multimaster.branchThreads( core_ids, all_dcs, method, user, submitSQL, (sSql, mapResults) )
	lstTabSchemas = mapResults.values()
#	debug("lstTabSchemas: %s" % str(lstTabSchemas))

	# Make sure all the schemas are the same.
	lstS1 = lstTabSchemas[0]
	lstS1.sort()
	for lstCurS in lstTabSchemas:
		lstCurS.sort()
		if ( lstS1 != lstCurS ):
			sys.stderr.write("%s: Schema for table %s do not match throughout the mesh!\nlstTabSchemas: %s" % (sys.argv[0], sTabName, lstTabSchemas))

	# Return the first table schema.
	return lstS1

# The goal of this function is to pack table columns using as few server-side
# hash invocations as possible.  The reason for the need to do this is that
# Oracle has an upper limit of 4000 characters for concatinated items.  The
# algorythm below sorts the columns by length and collects them together into
# bundles that are no longer than 4000 characters long.
def genHashCol( lstTabSchema, sHashFunc, lstOtherCols ):
	MAX_COL_LEN=4000
	# Sort the table schema by data length.
	lstTabSchema.sort(lambda x,y:x[2]-y[2])

	# Itterate over every column in the table schema
	lstCols = []
	lstCol = []
	lLen = 0
	for lstCurCol in lstTabSchema:
		if (lstCurCol[0] in lstOtherCols):
			lCurColLen = lstCurCol[2]
			sCurCol = lstCurCol[0]
			if ( lstCurCol[1] == "date" ):
				sCurCol = "hextoraw(rawtohex(%s))" % sCurCol
			if ( lstCol and (lCurColLen > (4000 - lLen - 1)) ):
				lstCols.append(lstCol)
				lstCol = []
				lLen = 0
			else:
				lstCol.append(sCurCol)
			lLen = lLen + lstCurCol[2] + 1

	if ( lstCol ): lstCols.append(lstCol)
	lstCols = map(lambda col,hf=sHashFunc:hf % string.join(col,"||'|'||"), lstCols)
	if ( len(lstCols) == 1 ):
		return lstCols[0]
	elif ( len(lstCols) > 1 ):
		return sHashFunc % string.join(lstCols, "||")
	else:
		return ''

def genClientHashCols( lstTabSchema, lstOtherCols ):
	lstCols = []
	for lstCurCol in lstTabSchema:
		if (lstCurCol[0] in lstOtherCols):
			if ( lstCurCol[1] == "date" ):
				lstCols.append("hextoraw(rawtohex(%s))" % lstCurCol[0])
			elif ( lstCurCol[1] == "number" ):
				lstCols.append("to_char(%s)''" % lstCurCol[0])
			else:
				lstCols.append(lstCurCol[0])
	return string.join(lstCols, ",")

def genSelectFromClause( cls, lstTabSchema, client_hashing, hash_func ):
	# In case we are running on a pre-7.0 spin without a compound_id_delimiter.
	if (not hasattr( cls, "compound_id_delimiter" ) ):
		cls.compound_id_delimiter = '-'

	# Calculate the various parts of the sql query.
	id_fields = cls.getIDFields()
	cls_fields = cls.getFields()
	cls_fields = filter(lambda f:(not (f.name in ('tran_id','conflicting'))), cls_fields)
	id_columns = tuple(map(lambda f:f.name, id_fields))
	id_comp_column = "to_char(%s) as id" % string.join(id_columns, "||'%s'||" % cls.compound_id_delimiter)
	other_columns = map(lambda f:f.name, filter(lambda f,id_columns=id_columns:(not (f.name in id_columns)), cls_fields))
	hash_column = "null"
	if ( other_columns ):
		if ( client_has;hing ):
			hash_column = genClientHashCols(lstTabSchema, other_columns)
		else:
			hash_column = genHashCol(lstTabSchema, hash_func, other_columns)
	hash_column = hash_column + "||(CASE WHEN UPPER(conflicting)='Y' THEN to_Char(LCRepPkg.global_db_id) ELSE '' END)"
	return "select %s, %s from %s " % (id_comp_column, hash_column, cls._table.name)

def getOptions():
	(tt, args) = getopt.getopt( sys.argv[1:], "c:d:x:", ["sql", "debug", "simple", "verbose", "client_hashing", "file="] )
	odict = {}
	for t in tt:
		s = t[0]
		while (s[0] == "-"):		# Strip leading '-'s
			s = s[1:]
		odict[s] = t[1]

	if odict.has_key( "c" ):
		cls_list = string.split( odict["c"], "," )
	else:
		cls_list = spinobj.getMMClassNames()

	if odict.has_key( "x" ):
		skip_list = string.split( odict["x"], "," )
	else:
		skip_list = []

	if odict.has_key( "d" ):
		core_ids = map( long, string.split( odict["d"], "," ) )
	else:
		core_ids = None

	verbose = 0
	if odict.has_key( "verbose" ):
		sys.stderr.write("TODO: implement verbose output of diffs.\n")
		sys.exit(1)
		verbose = 1

	client_hashing = 0
	if odict.has_key( "client_hashing" ):
		client_hashing = 1

	if odict.has_key( "sql" ):
		truthdb.debug = 1

	if odict.has_key( "debug" ):
		global g_bDebug
		g_bDebug = 1

	fname = odict.get("file")
	ofi = None
    if ( fname == '-' ):
		ofi = sys.stdin
	else:
		ofi = open(fname)

	return (cls_list, skip_list, ofi, core_ids, verbose, client_hashing, args)

#------------------------------------------------------------------------------
if __name__ == "__main__":
#------------------------------------------------------------------------------
	main ( )

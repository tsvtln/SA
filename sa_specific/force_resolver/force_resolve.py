#!/opt/opsware/bin/python -u
#                      -*- Mode: Python ; tab-width: 4 -*- 

# This script attempts to resolve all multimaster conflicts.  It does so by
# synchronizing all conflicting transactions from either the core of origin
# for that transaction or a specified core.  It most likely will resolve
# only a fraction of all conflicts.  A second pass will generally resolve
# a few more.  Some may never be resolvable via this automated script and must
# be manually resovled.

# This script will only work in Babbage and later installations.

import sys
import os
import string
import getopt
import types
import time
import traceback
import shutil
import tempfile
import threading

sys.path.append( "/lc/blackshadow" )
sys.path.append( "/cust/usr/blackshadow" )
sys.path.append( "/cust/usr/blackshadow/spin" )
sys.path.append( "/cust/ldapmodule" )
sys.path.append( "/opt/opsware/corelibs" )
sys.path.append( "/opt/opsware" )
sys.path.append( "/opt/opsware/spin" )
sys.path.append( "/opt/opsware/pylibs" )
sys.path.append( "/soft/blackshadow/spin" )# For development
if not os.environ.has_key( "SPIN_DIR" ):
	os.environ["SPIN_DIR"] = "/cust/usr/blackshadow/spin"
try:
	import truthdb
	import spinobj
	import truthtable
	import spinconf
	import multimaster
	from spinerror import *
except ImportError:
	sys.stderr.write( "Unable to import Data Access Engine libraries: %s, %s.  Is the Data Access Engine installed on this host?\n" % sys.exc_info()[0:2] )
	sys.exit( 1 )


method = "multimaster.forcefulResolver()"
default_threads = 1


def usage():
	
	sys.stderr.write( """Usage:  force_resolve.py [--sql] [--debug] [--from <core-id>] [--refresh] [--cache fname] [--maxsize dmlcount] [-t <num>] [tran_id ...]
  --sql = Print out SQL as it's executed.
  --debug = Print out Multimaster Job status messages.
  --from <core-id> = Sync transactions from the specified core
      instead of the core of origin.
  --refresh = Refresh the cached conflict data before resolving.
  --cache = Use this cache file instead of the standard one.
      This can be used to prevent collisions with other running MM processes.
      If the file doesn't exist, it is created as a copy of the standard one.
  --maxsize <dmlcount> = Skip transactions with more DMLs than this.
  -t <num> = The number of threads to use when resolving conflicts.
      Specifying anything other than 1 implies that conflicts can be resolved in
	  an arbitrary order.  This will fail if transaction depend on eachother,
	  for instance if one references a foreign key inserted by another.
  tran_id = Sync just these transactions, in the order supplied.
      If not supplied, all conflicting transactions are sync'd.\n""" )
	sys.exit( 1 )


def main():

	try:
		(odict, args) = getOptions()
	except getopt.error:
		sys.stderr.write( str(sys.exc_info()[1]) + "\n" )
		usage()
		
	# We do this here so that problems are reported after usage errors.
	import init

	user = os.environ.get("USER", os.environ.get("LOGNAME", "root"))
	tran_ids = map( long, args )
	
	if odict.has_key( "sql" ):
		truthdb.debug = 1
	if odict.has_key( "debug" ):
		multimaster.debug = 1

	# Use our own copy of the cache file
	if odict.has_key( "cache" ):
		old_fname = os.path.join( spinconf.get( "spin.dir" ), multimaster.conflicts_fname )
		new_fname = os.path.join( spinconf.get( "spin.dir" ), os.path.basename( odict["cache"] ) )
		multimaster.conflicts_fname = os.path.basename( new_fname )	# Tricky, tricky!
		if os.path.exists( old_fname ) and not os.path.exists( new_fname ):
			shutil.copy( old_fname, new_fname )

	if tran_ids:
		fails = resolveSome( user, tran_ids, odict["from"], odict["t"], odict["maxsize"] )
	else:
		fails = resolveAll( user, odict["from"], odict.has_key("refresh"), odict["t"], odict["maxsize"] )

	sys.exit( fails )
	

def resolveAll( user, from_core_id = None, refresh = 0, n = default_threads, maxsize=0 ):

	# Get the conflict data
	print "Getting the conflict data..."
	# Can we use the count_only arg?
	if "count_only" in multimaster.getConflicts.func_code.co_varnames:
		# TODO:  Can we use the async arg and print progress bars?
		con_data = multimaster.getConflicts( user, refresh_cache=refresh, count_only=1 )
	else:
		con_data = multimaster.getConflicts( user, refresh_cache=refresh )

	# Sort the conflicts by publish date.
	# This ensures foreign-keys will be maintained, etc.
	conflicts = con_data["conflicts"]
	conflicts.sort( multimaster.byPubDate )
	tran_ids = map( lambda x: x["tran_id"], conflicts )

	print "Resolving %s conflicts..." % (len(tran_ids))
	return resolveList( user, tran_ids, from_core_id, n, maxsize )


def resolveSome( user, tran_ids, from_core_id = None, n = default_threads, maxsize=0 ):

	print "Synchronizing the contents of %s transactions..." % (len(tran_ids))
	return resolveList( user, tran_ids, from_core_id, n, maxsize )


def resolveList( user, tran_ids, from_core_id = None, n = default_threads, maxsize=0 ):

	all_count = len(tran_ids)
	fails = []
	skips = []
	all_dcs = multimaster.getAllDCs( method, user )
	branchThreads( n, resolverThread, (user, all_dcs, tran_ids, skips, fails, from_core_id, maxsize) )
	print "Done.  %s succeeded, %s skipped, %s failed." % (all_count - len(fails) - len(skips), len(skips), len(fails))
	return len(fails)


# This function is destructive to tran_ids.  Caller beware.
def resolverThread( user, all_dcs, tran_ids, skips, fails, from_core_id = None, maxsize=0 ):

	while 1:

		try:
			tran_id = tran_ids.pop( 0 )
		except IndexError:
			break

		tran_str = truthdb.longAsString( tran_id )
		(seq, core_id) = truthdb.parseGlobalID( tran_id )
		db = multimaster.getDB( method, user, all_dcs[core_id].getDBName() )
		t = spinobj._Transaction( db, tran_id )
		dml_count = t.getChildCount( "_TransactionDML" )

		if maxsize and (dml_count > maxsize):
			sys.stdout.write( "%s: Skipping %s (%s DMLs)...\n" % (getTimeString(), tran_str, dml_count))
			skips.append( tran_id )
			continue

		# Sync the transaction from the core of origin or the specified core
		# regardless of what the diffs are.  POW!
		if (from_core_id != None):
			core_id = from_core_id
		sys.stdout.write( "%s: Sync %s from %s (%s DMLs)...\n" % (getTimeString(), tran_str, truthdb.longAsString(core_id), dml_count) )
		# TODO:  Can we use the async arg and print progress bars?
		sync = multimaster.syncTransaction( user, tran_id, core_id )

		# If the sync succeeded, mark it resolved
		if sync["error"]:
			err = ["%s: %s Failed:\n" % (getTimeString(), tran_str)]
			obj_sync = sync["object_syncs"][-1]
			for d in obj_sync["actions"]:
				if d["error"]:
					msg = d["error_msg"]
					err.append( "    At %s:  %s (%s)\n" % (truthdb.longAsString(d["core_id"]),
														   d["error_name"], msg) )
			sys.stdout.write( string.join( err, "" ) )
			fails.append( tran_id )
		else:
			multimaster.markResolved( user, tran_id )
			sys.stdout.write( "%s: %s OK.\n" % (getTimeString(), tran_str) )


def getTimeString():
	return time.strftime("%Y-%m-%d_%H:%M:%S",time.gmtime(time.time()))


def branchThreads( n, f, args ):

	# Never mind if there's only going to be one thread
	if (n == 1):
		apply( f, args )

	else:
		threads = []
		for tid in range(n):
			thread = threading.Thread( target=f, args=args )
			threads.append( thread )
			thread.start()
		for thread in threads:
			thread.join()


def getOptions():

	(tt, args) = getopt.getopt( sys.argv[1:], "t:", ["sql", "debug", "from=", "refresh", "cache=", "maxsize="] )
	odict = {}
	for t in tt:
		s = t[0]
		while (s[0] == "-"):		# Strip leading '-'s
			s = s[1:]
		if not odict.has_key( s ):
			odict[s] = []
		odict[s] = t[1]

	if odict.has_key( "n" ):
		global commit
		commit = 0

	if odict.has_key( "from" ):
		odict["from"] = int( odict["from"] )
	else:
		odict["from"] = None

	odict["t"] = int( odict.get( "t", default_threads ) )
	odict["maxsize"] = int( odict.get( "maxsize", 0 ) )

	return (odict, args)


#------------------------------------------------------------------------------
if __name__ == "__main__":
#------------------------------------------------------------------------------
	main ( )



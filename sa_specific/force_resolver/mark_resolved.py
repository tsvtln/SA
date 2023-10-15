#!/opt/opsware/bin/python -u
#                      -*- Mode: Python ; tab-width: 4 -*- 

# This script attempts to mark a given list of multimaster conflicts as resolved.

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
sys.path.append( "/opt/opsware/corelibs" )
sys.path.append( "/cust/ldapmodule" )
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


method = "multimaster.markResolved()"
default_threads = 1


def usage():
	
	sys.stderr.write( """Usage:  mark_resolved.py [--sql] [-t <num>] tran_id [...]
  --sql = Print out SQL as it's executed.
  -t <num> = The number of threads to use.
  tran_id = The transactions to mark resolved.\n""" )
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

	fails = markResolved( user, tran_ids, odict["t"] )

	sys.exit( fails )
	

def markResolved( user, tran_ids, n = default_threads ):

	all_count = len(tran_ids)
	fails = []
	all_dcs = multimaster.getAllDCs( method, user )
	branchThreads( n, resolverThread, (user, all_dcs, tran_ids, fails) )
	print "Done.  %s succeeded, %s failed." % (all_count - len(fails), len(fails))
	return len(fails)


# This function is destructive to tran_ids.  Caller beware.
def resolverThread( user, all_dcs, tran_ids, fails ):

	while 1:

		try:
			tran_id = tran_ids.pop( 0 )
		except IndexError:
			break

		tran_str = truthdb.longAsString( tran_id )

		sys.stdout.write( "%s Marking %s...\n" %
						  ( (time.strftime("%Y-%m-%d_%H:%M:%S",time.gmtime(time.time()))),
							tran_str ) )
		res = multimaster.markResolved( user, tran_id, all_dcs=all_dcs )

		errs = []
		for d in res:
			if d["error"]:
				msg = d["error_msg"]
				if (len(msg) > 80):
					msg = msg[:80] + "..."
				errs.append( "    At %s:  %s (%s)\n" % (truthdb.longAsString(d["core_id"]), d["error_name"], msg) )
		if errs:
			errs.insert( 0, "%s Failed:\n" % (tran_str) )
			sys.stdout.write( string.join( errs, "" ) )
			fails.append( tran_id )
		else:
			sys.stdout.write( "%s %s OK.\n" % ( (time.strftime("%Y-%m-%d_%H:%M:%S",time.gmtime(time.time()))), tran_str) )


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

	(tt, args) = getopt.getopt( sys.argv[1:], "t:", ["sql"] )
	odict = {}
	for t in tt:
		s = t[0]
		while (s[0] == "-"):		# Strip leading '-'s
			s = s[1:]
		if not odict.has_key( s ):
			odict[s] = []
		odict[s] = t[1]

	odict["t"] = int( odict.get( "t", default_threads ) )

	if not args:
		usage()
		
	return (odict, args)


#------------------------------------------------------------------------------
if __name__ == "__main__":
#------------------------------------------------------------------------------
	main ( )



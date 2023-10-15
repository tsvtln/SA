#!/opt/opsware/bin/python2 -u
#                      -*- Mode: Python ; tab-width: 4 -*- 

import sys
import os
import string
import getopt
import types
import time
import traceback
try:
	import warnings
	# Disable DeprecationWarnings
	warnings.simplefilter('ignore', DeprecationWarning)
except ImportError:
	pass

sys.path.append( "/lc/blackshadow" )
sys.path.append( "/cust/usr/blackshadow" )
sys.path.append( "/cust/usr/blackshadow/spin" )
sys.path.append( "/cust/ldapmodule" )
sys.path.append( "/opt/opsware/corelibs" )
sys.path.append( "/opt/opsware" )
sys.path.append( "/opt/opsware/spin" )
if (sys.version[0] == "2"):
	sys.path.append( "/opt/opsware/pylibs2" )
else:
	sys.path.append( "/opt/opsware/pylibs" )
sys.path.append( "/soft/blackshadow/spin" )# For development
if not os.environ.has_key( "SPIN_DIR" ):
	os.environ["SPIN_DIR"] = "/cust/usr/blackshadow/spin"
try:
	import truthdb
	import spinobj
	import truthtable
	import multimaster
	import spinconf
	from spinerror import *
except ImportError:
	sys.stderr.write( "Unable to import Data Access Engine libraries: %s, %s.  Is the Data Access Engine installed on this host?\n" % sys.exc_info()[0:2] )
	sys.exit( 1 )

debug = 0
method = "table_checker"
dc_names = {}


def usage():
	
	sys.stderr.write( "Usage:  table_checker.py [--sql] [--debug] [-c <obj_classes>] [-x <obj_classes>] [--file fname] [--simple] [--no_desc] [--from <core_id>] [-d <core_ids>] [id ...]\n" )
	sys.stderr.write( "  'obj_classes' is a comma-seperated list of Spin class name such as Device.\n" )
	sys.stderr.write( "    If -c is not supplied, all object classes will be checked.\n" )
	sys.stderr.write( "    If -x is supplied, those object classes will be avoided.\n" )
	sys.stderr.write( "  If 'file' is supplied, it should contain the output from a previous --simple run.\n" )
	sys.stderr.write( "    Just those objects will be checked; -c, -x, and any ids are ignored.\n" )
	sys.stderr.write( "  'simple' will output only object names and IDs, allowing easier parsing.\n" )
	sys.stderr.write( "  'no_desc' will not report differences in description fields.\n" )
	sys.stderr.write( "  'core_ids' is a comma-seperated list of all cores to check.\n" )
	sys.stderr.write( "    If not supplied, all cores in the mesh are checked.\n" )
	sys.stderr.write( "  If 'from' is supplied, only objects existing in that core will be checked.\n" )
	sys.stderr.write( "    Otherwise, objects in all cores will be checked.\n" )
	sys.stderr.write( "  If no IDs are supplied, all objects are checked.\n" )
	sys.exit( 1 )


def main():

	try:
		(cls_list, skip_list, fname, core_ids, from_core_id, simple, no_desc, ids) = getOptions()
	except getopt.error:
		sys.stderr.write( str(sys.exc_info()[1]) + "\n" )
		usage()

	if fname:
		errs = checkFromFile( fname, simple, no_desc, core_ids, from_core_id )
	else:
		errs = checkTables( cls_list, skip_list, ids, simple, no_desc, core_ids, from_core_id )
	if errs:
		sys.stderr.write( "\nWARNING:  %d errors were encountered!\n" % (errs) )


def checkFromFile( fname, simple, no_desc, core_ids=None, from_core_id=None ):

	d = {}
	f = open( fname )
	while 1:
		l = f.readline()
		if not l:
			break
		(cls, obj_id) = string.split( string.strip(l), None, 1 )
		if not d.has_key( cls ):
			d[cls] = []
		d[cls].append( obj_id )
	f.close()

	clss = d.keys()
	clss.sort()
	errs = 0
	for cls in clss:
		errs = errs + checkTables( [cls], [], d[cls], simple, no_desc, core_ids, from_core_id )

	return errs

		
def checkTables( cls_list, skip_list, ids, simple, no_desc, core_ids = None, from_core_id = None ):

	user = os.environ.get("USER", os.environ.get("LOGNAME", "root"))
	all_dcs = multimaster.getAllDCs( method, user )
	global dc_names
	for dc in all_dcs.values():
		dc_names[dc.getID()] = str(dc)
	if core_ids is None:
		core_ids = all_dcs.keys()

	errs = 0
	for cls in cls_list:
		if cls in skip_list:
			continue
		try:
			cls = spinobj.getObjectClass( cls )
			checkObjects( user, cls, all_dcs, core_ids, ids, from_core_id, simple, no_desc )
		except KeyboardInterrupt:
			sys.stderr.write( "Keyboard interrupt!  Skipping...\n" )
			errs = errs + 1
		except:
			sys.stderr.write( "ERROR checking %s:\n" % (cls) )
			traceback.print_exc()
			errs = errs + 1

	return errs


def populateObjects( core_id, all_dcs, method, user, all_objects, cls, ids ):

	d = {}
	all_objects[core_id] = d
	db = multimaster.getDB( method, user, all_dcs[core_id].getDBName() )
	if ids:
		sys.stderr.write( "Populating %d %s objects from %s...\n" % (len(ids), spinobj.getClassName(cls), dc_names[core_id]) )
		for id in ids:
			try:
				obj = cls( db, id )
				d[obj.getID()] = obj
			except KeyboardInterrupt:
				raise
			except DBNotFoundError:
				pass
	else:
		o = cls( db )
		sys.stderr.write( "Populating %d %s objects from %s...\n" % (o.getCount(), spinobj.getClassName(cls), dc_names[core_id]) )
		for obj in o.getList():
			d[obj.getID()] = obj
	if debug:
		sys.stderr.write( "Done populating from %s...\n" % (dc_names[core_id]) )


def checkObjects( user, cls, all_dcs, core_ids, ids, from_core_id = None, simple = 0, no_desc = 0 ):

	# Make sure we include the --from DB
	if from_core_id and from_core_id not in core_ids:
		core_ids.append( from_core_id )

	# First suck up all objects from all DBs
	all_objects = {}  # {core_id : { obj_id : obj } }
	multimaster.branchThreads( core_ids, all_dcs, method, user, populateObjects, (all_objects, cls, ids) )

	sys.stderr.write( "Comparing %s objects...\n" % (spinobj.getClassName(cls)) )

	# Transform into a structure that's easier to handle.
	objects = {}  # { obj_id : { core_id : obj } }
	for (core_id, d) in all_objects.items():
		for (id, obj) in d.items():
			if not objects.has_key( id ):
				objects[id] = {}
			objects[id][core_id] = obj

	# Now walk through them all
	for id in objects.keys():

		# Skip it if it doesn't exist in the source core.
		if from_core_id and not objects[id].has_key( from_core_id ):
			continue

		# Get a sample object.
		obj = objects[id].values()[0]
		if debug:
			sys.stderr.write( "Comparing %s...\n" % (obj) )

		# Check if any are missing.
		found = []
		missing = []
		if (len(objects[id].keys()) != len(core_ids)):
			if simple:
				print obj.obj_class, obj.getIDString()
				continue  # No need to check for other diff types.
			else:
				for core_id in core_ids:
					if objects[id].has_key( core_id ):
						found.append( dc_names[core_id] )
					else:
						missing.append( dc_names[core_id] )
				print "Object %s exists in %s but not in %s" % (obj, found, missing)

		# Compare each core against the others.
		# We only care about pairs where they both exist.
		diffs = {}
		for i in range( len( core_ids ) ):
			
			this_core_id = core_ids[i]
			this_obj = objects[id].get( this_core_id )
			if (this_obj is None):
				continue

			for other_core_id in core_ids[i+1:]:

				other_obj = objects[id].get( other_core_id )
				if (other_obj is None):
					continue
					
				if debug:
					sys.stderr.write( "%s vs. %s...\n" % (dc_names[this_core_id], dc_names[other_core_id]) )

				for field in this_obj.dict.keys():
					if (field == "tran_id"):
						continue
					if no_desc and (field[-4:] == "desc"):
						continue		# There's problem with CRs being dropped during replication
					if (this_obj[field] != other_obj[field]):
						this_val = this_obj[field]
						other_val = other_obj[field]
						if (string.lower(field[-3:]) == "_dt"):
							if this_val:
								this_val = "%s (%s)" % (time.asctime( time.gmtime( this_val ) ), this_val)
							if other_val:
								other_val = "%s (%s)" % (time.asctime( time.gmtime( other_val ) ), other_val)
						key = "%s and %s" % (dc_names[this_core_id], dc_names[other_core_id])
						if not diffs.has_key( key ):
							diffs[key] = []
						diffs[key].append( "\t%s: %s vs. %s" % (field, repr(this_val), repr(other_val)) )

		# Were there any diffs?
		if diffs:
			if simple:
				print obj.obj_class, obj.getIDString()
			else:
				for (key, l) in diffs.items():
					print "Object %s differs between %s:" % (obj, key)
					print string.join( l, "\n" )
			continue  # No need to check for other diff types.
		elif missing:
			# There were no diffs, but some are missing.
			continue

		# Check if they're all locked.
		# If it's locked anywhere, it's locked everywhere because we know it's in sync.
		if obj["conflicting"]:
			if simple:
				print obj.obj_class, obj.getIDString()
			else:
				print "Object %s is in sync but locked at all DBs." % (obj)
			continue

		# All is well.
		if debug:
			print "Object %s is the same in all cores." % (obj)


def getOptions():

	(tt, args) = getopt.getopt( sys.argv[1:], "c:d:x:", ["sql", "debug", "simple", "no_desc", "from=", "file="] )
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

	if odict.has_key( "from" ):
		from_core_id = long(odict["from"])
	else:
		from_core_id = None

	if odict.has_key( "no_desc" ):
		no_desc = 1
	else:
		no_desc = 0

	if odict.has_key( "simple" ):
		simple = 1
	else:
		simple = 0

	if odict.has_key( "sql" ):
		truthdb.debug = 1

	if odict.has_key( "debug" ):
		global debug
		debug = 1

	return (cls_list, skip_list, odict.get("file"), core_ids, from_core_id, simple, no_desc, args)


#------------------------------------------------------------------------------
if __name__ == "__main__":
#------------------------------------------------------------------------------
	main ( )


	
		      

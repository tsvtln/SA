#
# module: gac_audit.py
#
# Use gacutil.exe to obtain inventory of the Global Assembly Cache.
# Then, beneath location 'gac_dir_root', create a directory named for each 
# assembly. In that directory, create a file for each attribute of the 
# assembly, and store the assembly attribute and value in that file.
#
# This script ignores the cache of ngen files, dealing only with the
# GAC assemblies.
#
# Paul Kennedy   paul@opsware.com
# 19 November 2005
#

import os
import string
from coglib import lcos

gac_dir_root = "c:\\temp\\audit\\gac"
gacutil = "gacutil.exe /l /nologo"
temp_file = "c:\\temp\\gac.txt"

start_string = "The Global Assembly Cache contains the following assemblies"
end_string = "The cache of ngen files contains the following entries"

(ec, titles, sout, serr) = lcos.capture3_ex( gacutil, timeout = 300 )

lines = []
if( ec == 0 ):
	f = open( temp_file, "wb" )
	f.write( sout )
	f.close
	f = open( temp_file, "r" )
	lines = f.readlines()
	f.close()
	os.unlink( temp_file )
else:
	print "gacutil.exe run failed: exis status: %s" % ec
	print "Stderr: %s" % serr
	
try:
	os.mkdir( gac_dir_root )
except OSError, (errno,strerror):
	# check for file exists, if so, continue
	if( errno == 17):
		pass
	else:
		raise
except:
	raise

for line in lines:
	seek = string.find( line, start_string )
	if seek is not -1:
		continue
	seek = string.find( line, end_string )
	if seek is not -1:
		break
		
	# line is now something like the following:
	#  'System.EnterpriseServices, Version=1.0.5000.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a, Custom=null'
		
	line = string.lstrip( string.rstrip( line ) )
	
	if( len( line ) == 0 ):
		continue
		
	wl = string.split( string.lstrip(line), ',')
	
	try:
		os.mkdir( os.path.join( gac_dir_root, wl[0]) )
	except OSError, (errno,strerror):
		# check for file exists, if so, continue
		if( errno == 17):
			pass
		else:
			raise

	for c in range( 1, len( wl ) ):
		fname = string.split( string.lstrip(string.rstrip(wl[c])), '=' )
		f = open( os.path.join( gac_dir_root, wl[0], fname[0] ), "wb" )
		f.write( string.lstrip(string.rstrip(wl[c])) )
		f.close()

#
# module: machine_config_audit.py
#
# Parse the contents of the XML config file: machine.config
# this file is located in the .Net Framework config directory.
# Then, beneath location 'machine_config_dir_root', create a directory
# named for each importatn attribute. 
# In that directory, create a file for each subattribute of the attribute
# in each file, store the subattribute name and value.
#

import os
import string

# Some constants
machine_config_dir_root = "c:\\temp\\audit\\machine_config"
dotnetconfig = 'Microsoft.NET\\Framework\\v1.1.4322\\CONFIG'
attribute_dict = {'<processModel' : [ '/>', '>', '/processModel>' ],
					'<httpRuntime': [ '/>', '>', '/httpRuntime>' ], 
					'<connectionManagement': [ '/connectionManagement>' ], 
					'<pages' : [  '/>', '>' '/pages>' ], 
					'<httpClientChannel' : [ '/>', '>', '/httpClientChannel>' ], 
					'<compilation' : [ '/>', '>', '/compilation>' ]}

debug = 0

# Locate machine.config
windowsdir = os.environ['SystemRoot']
machine_config = os.path.join( windowsdir, dotnetconfig, 'machine.config' ) 

f = open( machine_config, "rb" )
lines = f.readlines()
f.close()

try:
	os.mkdir( machine_config_dir_root )
except OSError, (errno,strerror):
	# check for file exists, if so, continue
	if( errno == 17):
		pass
	else:
		raise
except:
	raise

seeking_end_tag = 0
seeking_end_key = ''
payload = ''
for line in lines:
	line = string.lstrip( string.rstrip( line ) ) 

	if seeking_end_tag == 0:		
		for attribute in attribute_dict.keys():

			seek_begin = string.find( string.lower(line), string.lower(attribute) )
			if seek_begin is -1:
				continue

			seeking_end_tag = 1
			seeking_end_key = attribute
			end_values = attribute_dict[attribute]

			dirname = os.path.join( machine_config_dir_root, attribute[1:] )

			try:
				os.mkdir( dirname )
			except OSError, (errno,strerror):
				# check for file exists, if so, continue
				if( errno == 17):
					pass
				else:
					raise
			except:
				raise

			payload = line[seek_begin + len(attribute):]
		
			# Find the closing tag (any allowed value)
			for value in end_values:
				seek_end = string.find( string.lower(payload), string.lower(value) )
				if seek_end is -1:
					continue
				else:
					# Now we have the full set of attributes
					payload = payload[:seek_end]
					if debug: 
						print "Total Payload for '%s': %s" % (attribute,payload)
					
					# Now parse out the value
					pairs = string.split( payload )
					for nv in pairs:
						if( string.find( nv, '=') == -1):
							continue
						else:
							name_value = string.split( nv, '=' )
							if debug: 
								print "Name: '%s', value: '%s'" % ( name_value[0], name_value[1])
							
							# Create file and add name value pair to it.
							f = open( os.path.join( machine_config_dir_root, attribute[1:], name_value[0]), "wb" )
							f.write( nv )
							f.close()

					if debug:
						print ""
					payload = ''
					seeking_end_key = ''
					seeking_end_tag = 0
					break
	else:
		end_values = attribute_dict[seeking_end_key]
		for value in end_values:
			seek_end = string.find( string.lower(line), string.lower(value) )
			if seek_end is -1:
				continue
			else:
				# Now we have the full set of attributes
				payload = payload + line[:seek_end]
				if debug:
					print "Total Payload for '%s': %s" % (attribute,payload)
								
				# Now parse out the value
				pairs = string.split( payload )
				for nv in pairs:
					if( string.find( nv, '=') == -1):
						continue
					else:
						name_value = string.split( nv, '=' )
						if debug: 
							print "Name: '%s', value: '%s'" % ( name_value[0], name_value[1])
						
						# Create file and add name value pair to it.
						f = open( os.path.join( machine_config_dir_root, attribute[1:], name_value[0]), "wb" )
						f.write( nv )
						f.close()

				payload = ''
				seeking_end_key = ''
				seeking_end_tag = 0
				
				break
		if( seeking_end_tag == 1):
			payload = payload + line


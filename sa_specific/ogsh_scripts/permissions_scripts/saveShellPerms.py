#!/lc/bin/python

########################################
# This script is setup to dump your permission state
# to a shell script filled with the commands to grant
# the current permission state
# you can use this if you 
# want a known state to fall back against
########################################

import os
import re
import string
import time

# constants for the aaa shell-perm options
serverGroupConstraint = "-g "
facilityConstraint = "-f "
customerConstraint = "-c "
loginConstraint = "-l "

# open a restore file for writing
restoreFileTime = time.time()
restoreFile = open("restoreShellPerms%f.sh" % (restoreFileTime),"w+")

# write the shell line
restoreFile.write("#!/bin/sh\n")

# grab the existing usergroups
userGroups = os.listdir("/opsw/Permissions/UserGroups")

# grab the operations for each usergroup
for group in userGroups:
	operations = os.listdir("/opsw/Permissions/UserGroups/%s/operations/" % group)

	# grab the permissions for each operation
	for op in operations:

		permFile = open("/opsw/Permissions/UserGroups/%s/operations/%s" % (group,op) , "r")
		permList = permFile.read()
		permFile.close()
		if op!="launchGlobalShell":
			permList = string.split(permList,"\n")
		
		# create a command to grant that permission
		for line in permList:
			# extract constraints from permission line

			# check for server group
			match = re.match(r'.*Group:\s*([\w ]*)\s\(', line)	
			if match != None:
				serverGroupString = serverGroupConstraint+'"Public/'+match.group(1)+'"'
			else:
				serverGroupString = ""

			# check for facility 
			match = re.match(r'.*Facility:\s*([\w ]*)\s\(', line)
			if match != None:
				# extra check for bug in 5.1 (Group shown as Facility in relayRdpToServer file)
				if op == "relayRdpToServer":
					facilityString=serverGroupConstraint+'"Public/'+match.group(1)+'"'
				else:
					facilityString = facilityConstraint+'"'+match.group(1)+'"'
			else:
				facilityString = ""	
			
			# check for customer
			match = re.match(r'.*Customer:\s*([\w ]*)\s\(', line)
			if match != None:
				customerString = customerConstraint+'"'+match.group(1)+'"'
			else:
				customerString = ""

			# check for login
			match = re.match(r'.*Login:\s*([\w ]*)', line)
			if match != None:
				loginString = loginConstraint+'"'+match.group(1)+'"'
			else:
				loginString = ""

			if op=="launchGlobalShell" or loginString != "" or customerString!="" or facilityString!="" or serverGroupString!="":
				restoreFile.write("aaa shell-perm grant -o %s -u \"%s\" %s %s %s %s\n" % (op,group,serverGroupString,facilityString,customerString,loginString) )

restoreFile.close()


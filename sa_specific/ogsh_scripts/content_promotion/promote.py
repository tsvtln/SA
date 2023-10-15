#!/usr/bin/python

import sys
import re

import promotion_lib
from ocli_lib import folder

from environment_map import environment_usergroup_map

def usage():
	print "usage: %s <full path to folder> <environment name> [<notes to be appended>]" % (sys.argv[0])
	print
	print "Environment name can be one of %s" % (environment_usergroup_map.keys())
	print
	sys.exit(1)

def main(foldername, environment, notes=""):
	access_level = "READ"
	usergroup = environment_usergroup_map[environment]

	fldr = folder.Folder(folder_name=foldername)
	fldr.addACL(usergroup, access_level)

	promotion_lib.updateDesc(fldr, environment)

	if environment == "DEV":
		# we're promoting to DEV, we should also add write access for this object
		access_level = "WRITE"
		fldr.addACL(usergroup, access_level)

	if environment == "QA":
		# we're promoting out of DEV, we should remove write access from this object
		usergroup = environment_usergroup_map["DEV"]
		access_level = "WRITE"
		fldr.removeACL(usergroup, access_level)
		# since removing write access removes _all_ access, we have to add back READ access
		access_level = "READ"
		fldr.addACL(usergroup, access_level)

	if notes:
		promotion_lib.addNotes(fldr, notes, "promotion", environment)
	return

if __name__ == "__main__":
	if len(sys.argv) != 3 and len(sys.argv) != 4:
		print "Expected 2 or 3 arguments, got %s" % (len(sys.argv) - 1)
		usage()

	notes = ""
	if len(sys.argv) > 3:
		notes = sys.argv[3]

	main(sys.argv[1], sys.argv[2], notes)

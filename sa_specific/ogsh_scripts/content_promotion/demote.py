#!/usr/bin/python

# send the folder all the way back to the DEV state

import sys

import promotion_lib
from ocli_lib import folder
from environment_usergroup_map import environment_usergroup_map

def usage():
	print "usage: %s <full path to folder> [<notes to be appended>]" % (sys.argv[0])
	print
	sys.exit(1)


def main(foldername, notes=""):
	access_level = "READ"

	fldr = folder.Folder(folder_name=foldername)
	promotion_lib.updateDesc(fldr, "DEV")

	for env in environment_usergroup_map.keys():
		if env == "DEV":
			# don't remove access from the DEV group, they'll still get access after demotion
			continue
		usergroup = environment_usergroup_map[env]
		fldr.removeACL(usergroup, access_level)

	# give the DEV group write access to the folder again
	usergroup = environment_usergroup_map["DEV"]
	access_level = "WRITE"
	fldr.addACL(usergroup, access_level)

	if notes:
		promotion_lib.addNotes(fldr, notes, "demotion", "DEV")

	return

if __name__ == "__main__":
	if len(sys.argv) != 2 and len(sys.argv) != 3:
		print "Expected 1 or 2 arguments, got %s" % (len(sys.argv) - 1)
		usage()

	notes = ""
	if len(sys.argv) > 2:
		notes = sys.argv[2]

	main(sys.argv[1], notes)

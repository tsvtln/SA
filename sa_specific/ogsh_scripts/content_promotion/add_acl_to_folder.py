#!/usr/bin/python

import sys

from ocli_lib import folder

def usage():
	print "usage: %s <full path to folder> <usergroup name> <access level>" % (sys.argv[0])
	print
	sys.exit(1)


def main(foldername, usergroup, access_level):
	#print "Finding or creating folder %s." % (foldername)
	fldr = folder.Folder(folder_name=foldername)
	fldr.addACL(usergroup, access_level)
	print "%s level access added to folder \"%s\" for user group %s." % (access_level, foldername, usergroup)
	return

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "Expected 3 arguments, got %s" % (len(sys.argv) - 1)
		usage()

	main(sys.argv[1], sys.argv[2], sys.argv[3])

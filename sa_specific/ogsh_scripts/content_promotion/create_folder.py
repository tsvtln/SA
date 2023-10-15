#!/usr/bin/python

import sys
import string
import os
import time

from ocli_lib import common
from ocli_lib import policy
from ocli_lib import folder

def usage():
	print "usage: %s <full path to folder> [<folder description>]" % (sys.argv[0])
	print
	sys.exit(1)


def main(foldername, desc=""):
	if foldername[-1] == "/":
		foldername = foldername[:-1]

	print "Finding or creating folder %s." % (foldername)
	fldr = folder.Folder(folder_name=foldername, folder_desc=desc)
	print "Promoting folder to DEV."
	import promote
	promote.main(foldername, "DEV")
	#print "Removing ACLs for Advanced Users group."
	#fldr.removeACL("Advanced Users", "WRITE")
	print "Done."
	print fldr.id
	return

if __name__ == "__main__":
	if len(sys.argv) != 2 and len(sys.argv) != 3:
		print "Expected 1 or 2 arguments, got %s" % (len(sys.argv) - 1)
		usage()

	desc = ""
	if len(sys.argv) > 2:
		desc = sys.argv[2]

	main(sys.argv[1], desc)

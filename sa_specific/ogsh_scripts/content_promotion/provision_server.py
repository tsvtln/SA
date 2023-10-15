#!/usr/bin/python


import sys
import re

import promotion_lib
from ocli_lib import folder
from ocli_lib import pool_server

from environment_map import environment_map

def usage():
	print "usage: %s <server name> <full path to folder>" % (sys.argv[0])
	print
	sys.exit(1)

def main(servername, foldername, notes=""):

	# get the OS sequence id from the folder
	# the assumption is that there is only one OS sequence per folder
	# which is the setup we created at ML for BZ,Orchestrator,Remedy,SAS 
	# integration
	fldr = folder.Folder(folder_name=foldername)
	seqs = fldr.getOSSequences()
	seq_id = seqs[0]

	# get the server and kickoff the prov
	srv = pool_server.PoolServer(server_name=servername)
	job_id = srv.provisionServer(seq_id)
	print "Job id: %s" % (job_id)

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Expected 2 arguments, got %s" % (len(sys.argv) - 1)
		usage()

	main(sys.argv[1], sys.argv[2])

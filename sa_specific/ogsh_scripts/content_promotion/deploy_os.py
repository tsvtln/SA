#!/usr/bin/python
# this is the script that is called by Orchestrator to start a build
# inputs:
#  full folder path (this script will find the OS sequence that's in the folder)
#  environment name (this script will find the server name(s) for this env)

import sys
import re

import promotion_lib
from ocli_lib import folder
from ocli_lib import pool_server

from environment_map import environment_testserver_map

def usage():
	print "usage: %s <full path to folder> <environment name>" % (sys.argv[0])
	print
	sys.exit(1)

def main(foldername, envname):

	# get the OS sequence id from the folder
	# the assumption is that there is only one OS sequence per folder
	# which is the setup we created at ML for BZ,Orchestrator,Remedy,SAS 
	# integration
	fldr = folder.Folder(folder_name=foldername)
	seqs = fldr.getOSSequences()
	seq_id = seqs[0]

	# get the server and kickoff the prov
	srvs = environment_testserver_map[envname]
	if not srvs:
		print "No servers defined for environment %s, not kicking off any builds." % (envname)
		return

	for srv in srvs:
		try:
			srv = pool_server.PoolServer(server_name=srv)
		except:
			print "Error getting server record"
			print "Skipping server %s" % (srv)

		try:
			job_id = srv.provisionServer(seq_id)
			print "Building server %s, job id: %s" % (srv, job_id)
		except:
			print "Error kicking off OS build"
			print "Skipping server %s" % (srv)


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Expected 2 arguments, got %s" % (len(sys.argv) - 1)
		usage()

	main(sys.argv[1], sys.argv[2])

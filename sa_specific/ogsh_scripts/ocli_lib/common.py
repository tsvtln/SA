#!/usr/bin/python

# This module abstracts some of the complexities of using the CLI in the OGSH
# and exposes simple Python methods.

import os, sys, string
import popen2
import time

DEBUG=0
server_apis = "/opsw/api/com/opsware/server/ServerService/method"
folder_apis = "/opsw/api/com/opsware/folder/FolderService/method"
policy_apis = "/opsw/api/com/opsware/swmgmt/SoftwarePolicyService/method"

def debug(msg):
	if DEBUG:
		print "(%s) DEBUG: %s" % (time.ctime(time.time()), msg)

def runCommand(cmd):
	# for some reason I can't begin to imagine, setting DEBUG=1 seems to prevent
	# the wait() call from hanging when there is a sizable amount of output
	# (ex. error parsing the ini)
	DEBUG=1
	debug(cmd)
	# We use popen2.Popen4() because it allows us to capture both stdout and
	# stderr, interleaved.  
	# This requires python 2.x

	popen_obj = popen2.Popen4(cmd)
	rv = popen_obj.wait()
	output = popen_obj.fromchild.read()
	DEBUG=0
	return rv, output

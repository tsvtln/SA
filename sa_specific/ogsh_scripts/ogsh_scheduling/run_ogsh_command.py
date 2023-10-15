#!/opt/opsware/bin/python

# run_ogsh_command.py

import sys
import os
import string

mydir = os.path.dirname(sys.argv[0])
ogsh_cmd = "/opt/opsware/ogfs/bin/ogsh"

def usage():
	print "usage: run_ogsh_command.sh [-v] <user> <command to run>" 
	print 
	sys.exit(1)

def getpass(username):
	userdbfile = os.path.join(mydir, "userdb")
	userdb = open(userdbfile, "r")
	userdict = eval(userdb.read())
	try:
		return userdict[username]
	except KeyError:
		print "Couldn't find password for user %s in the userdb." % (username)
		sys.exit(1)

def runCommand(cmd):
	cmdfileobj = os.popen(cmd)
	output = cmdfileobj.read()
	rv = cmdfileobj.close()
	return rv, output

def main(args):

	if len(args) != 4 and len(args) != 5: 
		usage()

	verbose = 0
	if args[1] == "-v":
		verbose = 1
		args.remove("-v")

	username = args[1]
	cmd = args[2]

	password = getpass(username)
	cmd = "%s -u %s -p %s \"%s\"" % (ogsh_cmd, username, password, cmd)
	#print "user, pass, cmd = %s,%s,%s" % (username, password, cmd)

	if verbose:
		pass
		#print "Running the OGSH command"
	rv, output = runCommand(cmd)

	if verbose:
		if not rv:
			rv = "success (0)"
		#print "Command returned %s, output: \n%s" % (rv, output)
		print output
	

if __name__ == "__main__":
	main(sys.argv)


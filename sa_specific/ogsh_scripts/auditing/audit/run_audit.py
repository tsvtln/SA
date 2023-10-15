#!/usr/bin/python

# TODO: 
# fuller:
# add support for emailing people on success, failure
#   - add info on what user ran the audit
# generate CSV file with matrix for all checks on all servers
# more verbose output going to a log 
# be able to send snmp traps on failure
# store audit configs as custom attributes
# x add reason for failure to cust attr
# add ability to have a list of acceptable outputs
# add ability to specify non-acceptable output (and a list of them)
# add flag to ignore non-zero return status for silly commands
# parallelize execution across servers
# mark unreachable servers w/ failure

# deeper:
# add support for variables - substitute any @name@ strings in the conf file before parsing it
# add support for checking a set of pkgs and patches - read SW inventory from database and grep on that
# add support for other abstract concepts.  Ex. listening on a port, running a anamed process, has a named user, etc.


import sys,string,re,os,ConfigParser
import custattr

comment_regex = re.compile("#.*$")
results = {"overall":[0,0]}


def testFailed(sectname, reason=None):
	custattr.testFailed(sectname, reason)
	results[sectname][1] = results[sectname][1] + 1


def testPassed(sectname):
	results[sectname][0] = results[sectname][0] + 1


def formatResults():
	ret = ""
	for key in results.keys():
		if key == "overall":
			continue
		ret = ret + "  %s: %s / %s\n" % (key, results[key][0], results[key][1] + results[key][0])
		results["overall"][0] = results["overall"][0] + results[key][0]
		results["overall"][1] = results["overall"][1] + results[key][1]

	ret = ret + "  Overall: %s / %s\n" % (results["overall"][0], results["overall"][1] + results["overall"][0])
	return ret

def stripComments(filecontents):
	return comment_regex.sub("",filecontents)

def getFileContents(filename, serverdir):
	if filename[0] == "/": 
		filename = filename[1:]
	filepath = os.path.join(serverdir, filename)
	if not os.path.isfile(filepath):
		return None
	f = open(filepath)
	contents = f.read()
	# doesn't matter if we strip the comments, as we're looking from the 
	# beginning of the string anyway
	return contents
	#return stripComments(contents)


def runConfFileTest(cp, sectname, serverdir):
	if cp.has_option(sectname, "separator"):
		separator = cp.get(sectname, "separator")
		separator = string.strip(separator)
	else:
		separator = "[:=]" # colon or equal sign

	# get the filecontents
	filename = cp.get(sectname, "filename")
	contents = getFileContents(filename, serverdir)
	failurereason = ""

	if not contents:
		testFailed(sectname, "Can't find file %s." % (filename))
		return None

	# for each nvpair option specified, formulate a regex and look for it 
	# in the file
	options = cp.options(sectname)
	for option in options:
		if option[:6] != "nvpair":
			# skip it
			continue

		nvpair = cp.get(sectname, option)
		name,val = string.split(nvpair, "=", 2)
		
		regex = "^\s*%s%s\s*%s" % (name, separator, val)

		mo = re.search(regex, contents, re.MULTILINE)
		if not mo:
			# check to see if the name exists w/ a different value, or not at all
			regex = "^\s*%s%s(.*)" % (name, separator)
			mo = re.search(regex, contents, re.MULTILINE)
			if not mo:
				testFailed(sectname, "The key '%s' was not found." % (name))
			else:
				actualval = string.strip(mo.groups(0)[0])
				testFailed(sectname, "The key '%s' was found, but it had value '%s' instead of the expected '%s'." % (name, actualval, val))

			#print "  Config item (%s) not found!" % (nvpair)
			#testFailed(sectname, "key-value pair for %s not found" % nvpair)
		else:
			#print "  Found config item %s." % (nvpair)	
			testPassed(sectname)


def runCommandTest(cp, sectname, serverdir):
	cmd = cp.get(sectname, "command")
	cmd = 'rosh "%s 2>&1"' % (cmd)
	f = os.popen(cmd)
	output = string.strip(f.read())
	rv = f.close()
	
	if rv:
		reason = "exit status = %s\noutput=%s" % (rv, output)
		testFailed(sectname, reason)
		return
		
	if not cp.has_option(sectname, "expectedoutput"):
		# we're good, we just wanted to make sure the rv was 0
		testPassed(sectname)
	else:
		expectedoutput = cp.get(sectname, "expectedoutput")
		expectedoutput = string.strip(expectedoutput)
		if output == expectedoutput:
			testPassed(sectname)
		else:
			reason = "Expected output=%s\nActual output=%s" % (expectedoutput, output)
			testFailed(sectname, reason)


def runTest(cp, sectname, serverdir):
	# reads in a test from the conf file and calls the appropriate logic for that
	# test type
	type = cp.get(sectname, "type")
	results[sectname] = [0,0]
	if type == "conffile":
		runConfFileTest(cp, sectname, serverdir)
	elif type == "runcommand":
		runCommandTest(cp, sectname, serverdir)
	else:
		print "  Unknown type %s, skipping." % (type)
	return
	

def main(conffile, serverdir):
	# TODO this will need to be refactored to happen once/server instead of
	# once/server/conffile
	custattr.clearFailedTests()

	#print conffile, serverdir
	cp = ConfigParser.ConfigParser()
	cp.read(conffile)
	for sect in cp.sections():
		if sect == "Options":
			continue
		#print "Processing '%s'." % (sect)
		runTest(cp, sect, serverdir)
	print formatResults()
	sys.exit(results["overall"][1])

main(sys.argv[1], sys.argv[2])	



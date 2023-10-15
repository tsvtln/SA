#!/usr/bin/python

# contains methods for creating and clearing the custom attributes dealing w/ 
# ogsh audit results

# this assumes you are in the dir server/files/user

import string, os

cadir = "../../CustAttr"
failed_prefix = "failed_test_"

def condenseTestName(testname):
	testname = string.replace(testname, ' ', '')
	testname = string.replace(testname, '/', '_')
	testname = string.replace(testname, '\\', '_')
	testname = failed_prefix + testname
	return testname

def clearFailedTests():
	cas = os.listdir(cadir)
	for ca in cas:
		if ca[:len(failed_prefix)] == failed_prefix:
			# this cust attr has the form of a failed test, lets delete it
			#print "would delete %s" % (ca)
			os.remove(cadir + '/' + ca)

def testFailed(sectname, failurereason=None):
	testname = condenseTestName(sectname)
	ca = open(cadir + '/' + testname, 'a')
	ca.write(failurereason + "\n")
	ca.close()
	

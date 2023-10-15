#!/opt/opsware/bin/python
# Version 6
# Contact tsvtln
#
import sys, time
sys.path.append("/opt/opsware/pylibs")

from getpass import *

from pytwist import *
from pytwist.com.opsware.search import Filter
from pytwist.com.opsware.compliance.sco import *
from pytwist.com.opsware.job import *

ts = twistserver.TwistServer()
js = ts.job.JobService

verbose = 0

# Result codes in JobInfoVO
result_dict={
        0: 'STATUS_ABORTED',
        1: 'STATUS_ACTIVE',
        2: 'STATUS_CANCELLED',
        3: 'STATUS_DELETED',
        4: 'STATUS_FAILURE',
        5: 'STATUS_PENDING',
        6: 'STATUS_SUCCESS',
        7: 'STATUS_UNKNOWN',
        8: 'STATUS_WARNING',
        9: 'STATUS_TAMPERED',
        10: 'STATUS_STALE',
        11: 'STATUS_BLOCKED',
        12: 'STATUS_RECURRING',
        13: 'STATUS_EXPIRED',
        14: 'STATUS_ZOMBIE'
}


def usage(name):
	print "usage: %s <job id>" % name

# Utility function to dump all info about an object
def introspect(object, depth=0):
	print "%s%s: %s" % (depth * "\t", object, dir(object))
	depth = depth + 1
	for x in dir(object):
		subobj = getattr(object,x)
		print "%s%s: %s (%s)" % (depth * "\t", x, subobj, dir(subobj))
		if dir(subobj) != [] :
			introspect(subobj, depth = depth + 1)
			print 

def cancelJob(jobID):

	filter = Filter()
	#filter.expression = ''
        filter.expression = 'job_session_id = "%s"' % jobID
	jobs = js.findJobRefs( filter )

	if len(jobs) <> 1:
		print "Job %s not found" % jobID
		sys.exit(1)

	jobref = jobs[0]
	jobinfo = js.getJobInfoVO(jobref)
	
	if (jobinfo.status not in [5,11,12]):
		print "Job %s cannot be cancelled.  The status is currently '%s'" % (jobID, result_dict[jobinfo.status])
		sys.exit(1)

	#Unblock the job
	try: 
		js.cancelBlockedJob( jobref )
		print "Job %s cancelled" % jobID
	except:
		print "Unknown problem when cancelling."
		print "Check that you are in a group with the following permissions"
		print "\tView All Jobs"
		print "\tEdit All Jobs"
		raise
		sys.exit(1)


def getCredentials():
        print "Opsware Username:",
        username = sys.stdin.readline()
        password = getpass('Opsware Password:')
        return str.strip(username),str.strip(password)


if __name__ == "__main__":
	if len(sys.argv) <> 2:
                usage(sys.argv[0])
                sys.exit(0)

	jobID  = sys.argv[1]

        username,password = getCredentials()
        try:
                ts.authenticate(username,password)
        except:
                print "Could not login to core"
                sys.exit(1)

	cancelJob(jobID)


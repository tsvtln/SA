import os
import sys
import time
import types
import string
import re
import traceback
import thread
import threading
import Queue
import imp
import smtplib
import exceptions
import copy

sys.path.append('/opt/opsware')

from librpc import rpcdate

from coglib import lcos
from coglib import platform
from coglib import cronbot

from coglib import spinwrapper

from opsware_common import errors

from waybot.base import logger
from waybot.base import commando
from waybot.base import deliverance
from waybot.base import spinaccess
from waybot.base import twistaccess
from waybot.base import dc_cache
from waybot.base import lock
from waybot.base import obscura
from waybot.base import encrypto
from waybot.base import signor
from waybot.base import conf
from waybot.base import switch
from waybot.base import modern
from waybot.base import spike
from waybot.base import library
from waybot.base import formtypes
from waybot.base import janitor
from waybot.base import notify

from waybot.base import error

from waybot.base.auth import query
from waybot.base.auth import cache
from waybot.base.auth import modify

from waybot.base.sched import CronSpec

from waybot.base.js import schedule

spin    = spinaccess.spin
ro_spin = spinaccess.ro_spin
e_spin  = spinaccess.edge_spin

# make a script specific logger
way_version = None


# constant for user_tag key name
USER_TAG="USER_TAG"

#constant for blocked reason
BLOCKED_REASON="BLOCKED_REASON"

#constant for cancelled reason
CANCELED_REASON="CANCELED_REASON"

# constant for the fixed "type" of job.  although this is technically free-form,
# this value should be in a lookup table, so treat it as such.
JOB_TYPE="JOB_TYPE"

# id of the session that represents the single overall id for a set of sessions.
JOB_ID="JOB_ID"

# ids of the next/previous sessions in a chain of sessions.
NEXT_SESSION_ID="NEXT_SESSION_ID"
PREV_SESSION_ID="PREV_SESSION_ID"

# Sessions that were active at the time of restart are no longer valid.
# They might even report additional status but since we've lost our
# internal state there's nothing for it.  So we mark those sessions as
# ZOMBIE.  This fixes bug 21260.
#
def tagZombieSessions():
	srvc_inst_id = deliverance.get_my_srvc_inst_id()
	restrict = {"srvc_inst_id": srvc_inst_id, "status": "ACTIVE"}
	print "Getting list of active sessions with srvc_inst_id %s ..." % srvc_inst_id

	session_list = spin.Session.getAll( restrict = restrict )
	print "Here's the list of sessions we'll be zombifying:"
	for session in session_list:
		print session['session_id']
	for session in session_list:
		print "Attempting to mark session %s as zombie..." % session['session_id']
		try:
			signor.sign_and_update( session, status = "ZOMBIE" )
			# sd = TruthSessionData( session_id )
		except error.waybot_VerifyUpdateFailure:
			# Ooops.  Someone's been naughty ... probably.  In any
			# case, the session's now been marked "TAMPERED", so
			# there's nothing for us to do...
			tb = string.join( apply( traceback.format_exception, sys.exc_info() ), "")
			print ( "tagZombieSessions(): Session %s has been tampered with.  NOT marking this session as ZOMBIE:\n%s" % (session['session_id'], tb) )
		except:
			# We couldn't load the session data, but not because of a
			# tampered session.  Since we don't know what's going on at
			# this point, we shouldn't touch the session.  But we will
			# at least log the fact that we should have marked it as ZOMBIE
			# but didn't.
			tb = string.join( apply( traceback.format_exception, sys.exc_info() ), "")
			print ( "tagZombieSessions(): signor.sign_and_update() of session %s failed for an unexpected reason.  NOT marking this session as ZOMBIE:\n%s" % (session['session_id'], tb) )


deliverance.register_self(1018)
tagZombieSessions()

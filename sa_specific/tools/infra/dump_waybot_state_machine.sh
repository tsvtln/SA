#!/bin/sh

# Extract the basename of this script.
sName="`basename $0`"
sWayOpletFileName="${sName}_oplet.py"
sWayOpletFilePath="/opt/opsware/waybot/base/way/bidniss/${sWayOpletFileName}"

# lay down the clear container caches oplet into the waybot:
cat <<WAY_OPLET_CODE > "$sWayOpletFilePath"
import sys
import time
import string

from waybot.base import oplet_common
from waybot.base import way_access
from waybot.base import way_auth
from waybot.base import script
from waybot.base import deliverance
from waybot.base import spike
from waybot.base import error

HISTORY_LEN = 10
TIME_FORMAT = "%m/%d/%y <b>%H:%M:%S</b>"

NUM_SERVERS = deliverance.m.numServers()

notes = '''Notes:<ol>
<li>The <b>Next Handler</b> column shows the next <i>scheduled</i> handler.
This handler will not run if it is pre-empted by an asynchronous handler; in
normal operation, timeout_handler is pre-empted by putResults.</li>
<li>If the time in the <b>Next Handler</b> column is shown in bold then it is
in the past (at the time this page was drawn) and the handler is either running
or is waiting on the work queue.  Only <b>%s</b> (current number of state machine server threads) handlers can be running at a time, any more are waiting in the work queue.</li>
<li>The data displayed here is gathered <i>without</i> locking the state
machine data structures representing each command. This means a handler name
may appear in the <b>Next Handler</b> column and at the tail of the
<b>History</b> column. This affects display of this page only, thus it will
appear correctly when this page is refreshed.</li>
<li>A message stating that the state machine is empty means that there are no
commands in the state machine.</li>
<li>A message stating that the state machine is quiescent means that there are
commands in the state machine but none of them have a scheduled
<b>Next Handler</b> which means that they are parked in the state machine
waiting to be cleaned up when the session which owns them is cleaned up.</li>
<li>Only the last %s handlers are shown in <b>History</b> column, to see all the handlers click on the ID in the <b>Command ID</b> column.</li>
<li>By convention, synchronous handlers are typically named like
<i>lock</i>_handler (with trailing _handler) and asynchronous handlers are
typically named like <i>putResults</i> (in camelCase).</li>
</ol>''' % (NUM_SERVERS, HISTORY_LEN)

def opletMain( self, args ):
	from waybot.base import script
	
	#---user = way_auth.authorize( self, hive, args )
	#---if not user:
	#---	return
#	credentials, user = way_auth.authenticate( self, hive, args )
#	if not user:
#		return
	#---if not way_access.giveTheBidniss(user):
	#---	way_access.bidnissDenied( self )
	#---	return
#	try:
#		spike.authorize( credentials, ["Way.Administrator"] )
#	except error.spike_PermissionDenied:
#		way_access.bidnissDenied( self )
#		return
	
	meta = ""
	if args.has_key('refresh_rate'):
		refresh_rate = args["refresh_rate"][0]
		meta = meta + '\n<meta http-equiv="Refresh" content="%s">\n' % refresh_rate

	oplet_common.draw_header( self, "Delivery State Machine", meta=meta)

	things = deliverance.dumpMachineState()

	if things:
		items = filter( lambda i: i[1][0] != None, things.items() )

		if items:
			now = time.time()

			self.page.write( '<h1>Delivery State Machine Commands</h1>'
							 'Current time is %s<br><br>'
							 % time.strftime( TIME_FORMAT, time.gmtime( now )))

			self.page.write( '<table border="1">'
							 '<tr><td>Command ID</td><td>Next Handler</td><td>History</td></tr>' )

			items.sort( lambda x, y: cmp( x[0], y[0] ))
			items.reverse()  # get newer (higher numbered) commands first

			for (id, (next, history_list)) in items:

				command = '<a href="/way/checkCommand.py?command_id=%s">%s</a>'\
						  % (id, id)

				what, when = next
				when_str = time.strftime( "%H:%M:%S", time.gmtime( when ))
				if when < now: when_str = '<b>%s</b>' % when_str

				next = "%s~%s" % (when_str, what)

				l = []
				for what, when in history_list[-HISTORY_LEN:]:
					when_str = time.strftime( "%H:%M:%S", time.gmtime( when ))
					l.append( "%s~%s" % (when_str, what))

				history = string.join( l, ", " )

				if len( history_list ) > HISTORY_LEN:
					history = "... " + history

				self.page.write( '<tr>%s</tr>' % ('<td>%s</td>' * 3)
								 % (command, next, history))

			self.page.write( '</table>\n<BR>\n' )
		else:
			self.page.write( '<BR><B>The delivery state machine is quiescent</B><BR>' )
	else:
		self.page.write( '<BR><B>The delivery state machine is empty</B><BR>' )

	self.page.write( notes )
		
	self.page.write( "<p><a href='stateMachine.py?refresh_rate=5'>refresh page "
					 "every 5 seconds</a>\n")

	oplet_common.draw_footer( self )


if __name__ == '__builtin__':   
	try:
		opletMain(self, args)
	except:
		oplet_common.handle_traceback(self)

WAY_OPLET_CODE

# if there was an error while writting out the waybot oplet, then bail out.
if ( [ $? -ne 0 ]; ) then {
  echo "$0: Failed to write out '$sWayOpletFilePath'."
  echo $0: Is this a 6.x+ waybot box?
  exit $?
} fi

# Invoke the python code to execute this oplet:
cat <<WAY_OPLET_INVOKER_BLOB | /opt/opsware/bin/python -c 'import sys,string; eval(compile(string.join(sys.stdin.readlines(),""),"way_oplet_invoker_blob","exec"));'
import sys;
sys.path.append("/opt/opsware/pylibs");
from coglib import certmaster,urlopen;
(url_obj,headers)=urlopen.httpReply(urlopen.httpUrlRequest("https://localhost:1018/way/bidniss/${sWayOpletFileName}",ctx=certmaster.getContextByName("spin","spin.srv","opsware-ca.crt"),connect_timeout=
60,read_timeout=60,write_timeout=60));
info_str=""
add_str = url_obj.read()
while add_str:
  info_str = info_str + add_str
  add_str = url_obj.read()
print info_str
WAY_OPLET_INVOKER_BLOB


#!/bin/sh

# Extract the basename of this script.
sName="`basename $0`"
sWayOpletFileName="${sName}_oplet.py"
sWayOpletFilePath="/opt/opsware/waybot/base/way/bidniss/${sWayOpletFileName}"

# lay down the clear container caches oplet into the waybot:
cat <<WAY_OPLET_CODE > "$sWayOpletFilePath"
import time
import sys

from waybot.base import oplet_common
from waybot.base import deliverance
from waybot.base import way_srvc_lb
from waybot.base import writer
from waybot.base import jailhouse

time_format = "%m/%d/%y <b>%H:%M:%S</b>"

if args.has_key( "new" ):
	if args[ "new" ][0] == "D":
		deliverance.startServer()

	elif args[ "new" ][0] == "W":
		writer.startServer()

	self.send_response( 302 )
	self.send_header( "Location", "/way/bidniss/serverThreads.py" )
	self.end_headers()

else:
	oplet_common.draw_header( self, "Deliverance Server Threads" )

	servers = deliverance.getServerStats()

	now = time.time()

	self.page.write( '<h1>Deliverance Server Threads</h1>\n'
					 'Total commands: %s, Current time: %s<br><br>'
					 % (len( deliverance.m ),
						time.strftime( time_format, time.gmtime( now ))))

	if servers:
		self.page.write( '<table border="1"><tr>'
						 '<td>Thread #</td>'
						 '<td>Requests</td>'
						 '<td>Last Sleep Time</td>'
						 '<td>Last Wake Time</td>'
						 '<td>Wedge Factor</td></tr>\n' )

		for x in servers:

			if x[2]:
				sleep = time.strftime( time_format, time.gmtime( x[2] ) )
			else:
				sleep = "---"

			if x[3]:
				wake = time.strftime( time_format, time.gmtime( x[3] ) )
			else:
				wake = "---"

			# is the thread awake ?
			if x[2] and x[3] and x[3] > x[2]:
				awake_for = now - x[3]

				if awake_for < 10:
					wedge = "low"

				elif awake_for < 60:
					wedge = "medium"

				else:
					wedge = "<b>high</b>"

			else:
				wedge = "not"

			self.page.write( '<tr><td>%s</td><td>%s</td><td>%s</td>'
							 '<td>%s</td><td>%s</td></tr>\n' % 
							 (x[0], x[1], sleep, wake, wedge) )

		self.page.write( '</table>' )
	else:
		self.page.write( '<B>No server threads currently running !</B>' )

	self.page.write( "These threads manage the state transitions in the life-"
					 "cycle of each command.  Most state transitions occur "
					 "instantaneously, but some will take several seconds. "
					 "Command writeback to the Spin is now handled by a "
					 "separate state machine below.  Command proxying is "
					 "handled by separate state machines below.<br>" )

	self.page.write( '<br>Don\'t <a href="/way/bidniss/serverThreads.py?new=D">'
					 'start a new thread</a> unless the currently running '
					 'threads are wedged !<hr>' )


	servers = writer.getServerStats()

	self.page.write( '<h1>Spin Writer Server Threads</h1>\n'
					 'Total commands: %s, Current time: %s<br><br>'
					 % (len( writer.m ),
						time.strftime( time_format, time.gmtime( now ))))

	if servers:
		self.page.write( '<table border="1"><tr>'
						 '<td>Thread #</td>'
						 '<td>Requests</td>'
						 '<td>Last Sleep Time</td>'
						 '<td>Last Wake Time</td>'
						 '<td>Wedge Factor</td></tr>\n' )

		for x in servers:

			if x[2]:
				sleep = time.strftime( time_format, time.gmtime( x[2] ) )
			else:
				sleep = "---"

			if x[3]:
				wake = time.strftime( time_format, time.gmtime( x[3] ) )
			else:
				wake = "---"

			# is the thread awake ?
			if x[2] and x[3] and x[3] > x[2]:
				awake_for = now - x[3]

				if awake_for < 30:
					wedge = "low"

				elif awake_for < 120:
					wedge = "medium"

				else:
					wedge = "<b>high</b>"

			else:
				wedge = "not"

			self.page.write( '<tr><td>%s</td><td>%s</td><td>%s</td>'
							 '<td>%s</td><td>%s</td></tr>\n' % 
							 (x[0], x[1], sleep, wake, wedge) )

		self.page.write( '</table>' )
	else:
		self.page.write( '<B>No server threads currently running !</B>' )

	self.page.write( "These threads manage the command writeback to the Spin. "
					 "Most write take less than 2 seconds but commands "
					 "with very large results dictionaries may take more than "
					 "a minute.<br>" )

	self.page.write( '<br>Don\'t <a href="/way/bidniss/serverThreads.py?new=W">'
					 'start a new thread</a> unless the currently running '
					 'threads are wedged !<hr>' )

	distribution, soonest, latest = jailhouse.statistics()

	if distribution:
		self.page.write( '<hr><h1>Jail House</h1>' )
		self.page.write( 'First parole: %s<br>\n' % time.ctime( soonest ) )
		self.page.write( 'Last  parole: %s<br>\n' % time.ctime( latest ) )

		self.page.write( '<table border="1">'
						 '<tr><td colspan="2">Jailhouse Distribution</td></tr>'
						 '<tr><td>Handler</td><td>Count</td></tr>' )

		num = 0
		
		for key, val in distribution.items():
			self.page.write( '<tr><td>%s</td><td>%s</td></tr>' % (key, val) )

			num = num + val

		self.page.write( '<tr><td>total</td><td>%s</td></tr>'
						 '</table>' % num )

	else:
		self.page.write( '<br>The Jailhouse is empty' )

	self.page.write( '<hr><h1>Command Proxy Threads</h1>' )
	proxy_stats = way_srvc_lb.getMachineStats()

	for way_svc, servers in proxy_stats:
		if way_svc['id'] != way_srvc_lb.get_my_srvc_inst_id():
			self.page.write( '<h2>%s (%s)</h2>' % ( way_svc['system_name'], way_svc['data_center_name'] ) )
			if servers:
				self.page.write( '<table border="1"><tr>'
								 '<td>Thread #</td>'
								 '<td>Requests</td>'
								 '<td>Last Sleep Time</td>'
								 '<td>Last Wake Time</td>'
								 '<td>Wedge Factor</td></tr>\n' )
				for x in servers:

					if x[2]:
						sleep = time.strftime( time_format, time.gmtime( x[2] ) )
					else:
						sleep = "---"

					if x[3]:
						wake = time.strftime( time_format, time.gmtime( x[3] ) )
					else:
						wake = "---"

					# is the thread awake ?
					if x[2] and x[3] and x[3] > x[2]:
						awake_for = now - x[3]

						if awake_for < 10:
							wedge = "low"

						elif awake_for < 60:
							wedge = "medium"

						else:
							wedge = "<b>high</b>"

					else:
						wedge = "not"

					self.page.write( '<tr><td>%s</td><td>%s</td><td>%s</td>'
									 '<td>%s</td><td>%s</td></tr>\n' % 
									 (x[0], x[1], sleep, wake, wedge) )

				self.page.write( '</table>' )
			else:
				self.page.write( '<B>No server threads currently running !</B>' )

	oplet_common.draw_footer( self )

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


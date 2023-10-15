#! /opt/opsware/bin/python

VERSION="1.0"

import os, sys, string
sys.path.append("/opt/opsware/pylibs")
sys.path.append("/opt/opsware/spin")
import truthdb
from coglib import spinwrapper
from coglib import certmaster
ctx=certmaster.getContext("/var/opt/opsware/crypto/spin/spin.srv")
s=spinwrapper.SpinWrapper(ctx=ctx)

# methods
def check_db_conn(dbname):
	try:
		db = truthdb.DB(dbname)
		cur = db.getCursor()
		# cur.execute( "select * from dual" )
		cur.execute( "select * from accounts" )
		# cur.fetchall()
		return "db conn ok"
	except:
		return "** DB CONN FAIL **"

def check_ping_conn(ipaddr):
	try:
		if os.system("ping -c 1 %s >/dev/null 2>&1" % (ipaddr)) == 0:
			return "ping ok"
		else:
			return "** PING FAIL **"
	except:
		return "** INTERNAL FAILURE **"


# main
DCs = s.DataCenter.getIDList()  # [751L, 752L]

print "\nPrint datacenter (DC) and realm info, Kevin M, SEG SA, HP Inc., Cupertino CA."
print "Version %s\n" % VERSION

print "	o"
for dcid in DCs:
	print "	.\n	."
	dc = s.DataCenter.get(id = dcid)
	ontogeny = dc['ontogeny']
	print "	[%s|%s|%s|%s|%s]" % (		\
		dc['display_name'], 		\
		dc['data_center_name'],		\
		ontogeny,			\
		dc['status'],			\
		dcid				\
		)

	if ontogeny != 'SATELLITE':
		tns = s.sys.getAllConf()['truth.tnsname']
		# tns = s.DataCenter.getTNSName(id = dcid)
		sys.stdout.write("	.  |   tns: %s (%s)" % (	\
			tns, check_db_conn(tns)				\
			))
		print
	
		try:
			cdc = s.multimaster.getCentralSpinDataCenter()
			cdcid = cdc["data_center_id"]
			print "	.  |MM Cen: %s" % (		\
				("no", "yes")[cdcid == dcid]	\
				)
		except:
			pass
	
		sp = s.DataCenter.getSpinURL(id = dcid)
		spip = string.split(string.split(sp, "/")[2], ":")[0]
		print "	.  |P spin: %s (%s)" % (sp, check_ping_conn(spip))
	
		try:
			mmsp = s.multimaster.getCentralSpinURL()
			spip = string.split(string.split(mmsp, "/")[2], ":")[0]
			print "	.  |MMspin: %s (%s)" % (mmsp, check_ping_conn(spip))
		except:
			pass
	
		twists = s.DataCenter.getTwistIPs(id = dcid)
		ntwists = len(twists)
		sys.stdout.write("	.  |twists: ")
		for tw in twists:
			sys.stdout.write("%s (%s)" % (tw, check_ping_conn(tw)))
			ntwists = ntwists - 1
			if (ntwists > 0):
				sys.stdout.write(", ")
		print
	
		hubs = s.DataCenter.getHubIPs(id = dcid)
		nhubs = len(hubs)
		sys.stdout.write("	.  |  hubs: ")
		for hu in hubs:
			sys.stdout.write("%s (%s)" % (hu, check_ping_conn(hu)))
			nhubs = nhubs - 1
			if (nhubs > 0):
				sys.stdout.write(", ")
		print
	
		try:
			slices = s.DataCenter.getDictValue(id = dcid, 		\
				key = '__OPSW_slice_ips')
			print "	.  |slices: %s" % (				\
				string.strip(slices)				\
				)
		except:
			pass
	


	# REALMs = [ 0, ]	# Show TRANSITIONAL realm
	REALMs = []
	REALMs.append(s.DataCenter.getRealm(id = dcid)['realm_id'])     # ['10751L']
	otherrealms = s.DataCenter.getOtherRealms(id = dcid)
	for ri in range(len(otherrealms)):
		REALMs.append(otherrealms[ri]['realm_id'])

	for r in REALMs:
		realm = s.Realm.get(id = r)
		print "	.  [%s|%s|%s]" % ( realm['realm_name'],			\
			realm['display_name'], r				\
			)

		print "	.  .  |BW -> core: %s (%s)" % (				\
			s.Realm.getBWToCore(id = r),				\
			("** NOT REACHABLE **", "reachable")			\
				[s.Realm.isRealmReachable(id = r)] 		\
			)

		gcconf = s.Realm.getGatewayConf(id = r)
		for g in range(len(gcconf)):
			sys.stdout.write("	.  .  |Gateway   : %s" % (	\
					gcconf[g]['node']			\
				))

			sys.stdout.write("|ports (aip): %s,%s,%s" % (		\
				gcconf[g]['admin_port'],			\
				gcconf[g]['ident_port'],			\
				gcconf[g]['proxy_port']				\
				))

			gwip = gcconf[g]['ip']
			print "|%s (%s)" % (					\
					gwip, check_ping_conn(gwip)		\
				)


		print "	.  ."

print "	.\n	o\n"

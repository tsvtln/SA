#!/opt/opsware/bin/python
# fw-rules.py --
# PURPOSE
# 	Control Network Security Access Levels within the OGSH.


import os,sys,getopt,string

sys.path.append('/opt/opsware/pylibs')

from pytwist import *

#################################################
# 
#################################################

HUB_KERNEL=string.strip(os.popen("uname -s").read())



#################################################
# fetch and cache basegid from twist
#################################################

basegid=None

def getBaseGid():
	global basegid
	if basegid!=None:
		return basegid
	
	bail=0
	try:
		ts = twistserver.TwistServer('localhost')
		basegid=int(ts._makeCall('fido/ejb/session/UserFacade','getDefaultHubGid',[]))
	except:
		bail=1
		
	if bail:
		sys.stderr.write("fw-rules.py cannot fetch getDefaultHubGid from the twist.\n")
		sys.stderr.write("The twist must be running for the firewall to be configured.\n")
		sys.exit(1)
	return basegid

#################################################
#
#################################################

def run(cmd):
	print cmd
	return os.system(cmd)

#################################################
#
#################################################

class FWChain:

	def __init__(self,level):
		self.name="OGFS_Level_%d" % (level)
		self.basegid=None
		self.level=level
		self.rules=[]		

	def addRule(self,frag):
		self.rules.append( frag )

	def getGID(self):
		if self.basegid==None:
			self.basegid=getBaseGid()+self.level
		return self.basegid


def fwChainLoader(conf=None):
	default='/etc/opt/opsware/hub/fw.conf'
	fwconf=None
	if conf:
		fwconf=conf
	else:
		if os.path.isfile(default):
			fwconf=default
		elif os.path.isfile('fw.conf'):
			fwconf='fw.conf'

	if not fwconf:
		print "Firewall rules '%s' are missing!" % (default)
		sys.exit(1)
	db={}
	lines=open(fwconf,'r').readlines()
	for l in lines:
		s=string.strip(l)
		i=string.find(s,'#')
		if i>=0:
			s=s[:i]
		if s:
			x=string.split(s,':')
			try:
				level=int(x[0])
			except:
				print "Error in file",fwconf
				print "Line:",l
				continue
			if level>=0 and level<=7:
				if db.has_key(level):
					db[level].append(s[2:])
				else:
					db[level]=[s[2:]]
	chains=[]
	for level in range(8):
		if db.has_key(level):
			chain=FWChain(level)
			for frag in db[level]:
				chain.addRule(frag)
			chains.append(chain)
	return chains
		
#################################################
# Load all the chains from the config file
#################################################

chains=fwChainLoader()

#################################################
# iptables drivers
#################################################

def installChain_ipt(chain):
	cmds=[]
	cmds.append("iptables -N %s" % (chain.name))
	for frag in chain.rules:
		cmds.append('iptables -A %s %s  -m owner --gid-owner %d' % (chain.name,frag,chain.getGID()))
	cmds.append("iptables -A OUTPUT -j %s" % (chain.name))
	for cmd in cmds:
		rv=run(cmd)
		if rv:
			print "command '%s' failed" % (cmd)

def removeChain_ipt(chain):
	lines=os.popen("iptables -n -L OUTPUT").readlines()
	lines=lines[2:]
	rnum=1
	for l in lines:
		s=string.split(string.strip(l))
		if len(s):
			if s[0]==chain.name:
				cmd="iptables -D OUTPUT %d" % (rnum)
				run(cmd)
				break
			rnum=rnum+1

	lines=os.popen("iptables -n -L").readlines()
	lines=lines[2:]

	chainExists=0
	for l in lines:
		s=string.split(string.strip(l))
		if len(s)>1:
			if s[0] == 'Chain' and s[1] == chain.name:
				chainExists=1
				break
	if not chainExists:
		return

	while 1:
		lines=os.popen("iptables -n -L '%s'" % (chain.name)).readlines()
		lines=lines[2:]
		if lines:
			cmd="iptables -D '%s' 1" % (chain.name)
			run(cmd)
		else:
			break

	run("iptables -X '%s'" % (chain.name))

#################################################
#
#################################################

def firewall_down_linux():
	for chain in chains:
		removeChain_ipt(chain)

def firewall_up_linux():
	firewall_down_linux()

	for chain in chains:
		installChain_ipt(chain)

#################################################
#
#################################################

def firewall_down_sunos(show_error=1):
	import dtrace_filter
	try:
		dtrace_filter.stop()
	except:
		pass

def firewall_up_sunos():
	import dtrace_filter
	dtrace_filter.start(chains)

#################################################
#
#################################################

def firewall_up():
	if HUB_KERNEL == "Linux":
		
		firewall_up_linux()
		
	elif HUB_KERNEL == "SunOS":
		
		firewall_up_sunos()

def firewall_down():
	if HUB_KERNEL == "Linux":
		
		firewall_down_linux()
		
	elif HUB_KERNEL == "SunOS":
		
		firewall_down_sunos()

############### USAGE ##################

def usage():
	print "%s add|remove|show" % (sys.argv[0])

if len(sys.argv)!=2:
	usage()
	sys.exit(1)

############### DO STUFF ###############

if sys.argv[1] == "add":
	firewall_up()
	
elif sys.argv[1] == "remove":
	firewall_down()
	
elif sys.argv[1] == "show":
	if HUB_KERNEL == "Linux":
		for chain in chains:
			print chain.name, chain.getGID()
			for frag in chain.rules:
				print "\t%s" % (frag)
	elif HUB_KERNEL == "SunOS":
		import dtrace_filter
		dtrace_filter.show(chains)

else:
	print "command '%s' is not recognized" % (sys.argv[1])
	usage()	
	sys.exit(1)

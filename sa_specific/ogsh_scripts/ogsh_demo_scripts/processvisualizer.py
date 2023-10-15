#!/usr/bin/env python
#                      -*- Mode: Python ; tab-width: 4 -*- 
# 
# ogfsdriver.py -- 
# 
# 

import os
import sys
import time
import string
import shutil
import getopt
import getpass
import thread

true=1
false=0

#######################################
#
#######################################

def sitemapthread(user,mydir,tmpdir,mid):
	warn("Verifying remote capture directory on target %s\n" % (mid))
	mpath='/opsw/.Server.ID/%s/files/root' % (mid)
	if not os.path.isdir(mpath):
		mpath='/opsw/Server/@/%s/files/root' % (mid)
		if not os.path.isdir(mpath):
			warn("The ogfs path to %s is not available\n" % (mpath))
			warn("ABORT capture\n")
			os._exit(1)
	rdir = os.path.join('/tmp','sitemap-'+user) # must be fully qualified
	rtmp = os.path.join(mpath,rdir[1:]) # strip off leading '/'
	if not os.path.isdir(rtmp):
		try:
			os.mkdir(rtmp)
		except:
			warn("Cannot create %s\n" % (rtmp))
			os._exit(1)

	sm=os.path.join(mydir,'sitemap.py')
	if not os.path.isfile(sm):
		warn("Local sitemap.py program is missing: %s\n" % (sm))
		os._exit(1)

	warn("Verifying remote lsof binary %s\n" % (mid))
	if not os.path.isfile(os.path.join(mpath,'usr','sbin','lsof')):
		warn("Remote copy of lsof is missing of target host: %s\n" % (mid))
		os._exit(1)
	
	if 1:
		warn("Copy sitemap.py to target host %s\n" % (mid))
		shutil.copy(os.path.join(mydir,'sitemap.py'),os.path.join(rtmp,'sitemap.py'))
	else:
		warn("Copy compressed sitemap.py to target host %s\n" % (mid))
		cmd=[]
		cmd.append('/bin/gzip -c %s | /opsw/bin/ttlg -i %s -d %s -l root "/bin/zcat > sitemap.py"')
		cmd=string.join(cmd) % (os.path.join(mydir,'sitemap.py'),mid,rdir)
		rv=os.system(cmd)
		if rv:
			warn("Capture on host %s failed\n" % (mid))
			os._exit(1)

	warn("Capturing process information on target host %s\n" % (mid))
	
	cmd=[]
	cmd.append("/opsw/bin/ttlg -i %s -l root -d %s" % (mid,rdir))
	cmd.append("\"/bin/sh -c '/opt/OPSW/bin/python ./sitemap.py --capture - --cache %s.cache" % (mid))
	cmd.append("< /dev/null 2> /dev/null | /bin/gzip -c - > %s.cap.gz'\"" % (mid))
	cmd=string.join(cmd)
	rv=os.system(cmd)
	if rv:
		warn("Capture on host %s failed\n" % (mid))
		os._exit(1)
		
	warn("Transfering capture file from host %s\n" % (mid))
	rv=os.system('/bin/gunzip -c %s > %s' % (os.path.join(rtmp,mid+'.cap.gz'),os.path.join(tmpdir,mid+'.cap.new')))
	if rv:
		warn("Local decompress of capture from host %s failed\n" % (mid))
		os._exit(1)
		
	try:
		os.rename(os.path.join(tmpdir,mid+'.cap.new'),os.path.join(tmpdir,mid+'.cap'))
	except:
		warn("Final rename of capture file failed\n")
		os._exit(1)

	warn("End capture on target %s\n" % (mid))

#######################################
#
#######################################

shortargs="c:o:mrh"
longargs={"capture=":["file","Capture openfile database to 'file'."],
		  "merge":["","Merge all captures in the outdir."],
		  "tmpdir=":["path","Temporary directory, defaults to ~/.sitemap."],
		  "reset":["","Clear out tmpdir"],
		  "help":["","Help!"],
		  }

def warn(msg):
	sys.stderr.write(msg)
	
def usage():
	print "ogfsdriver.py [options]"
	for k,v in longargs.items():
		if k[-1]=='=':
			a=k[:-1]
		else:
			a=k
		print '  %9s\t%s\t%s' % ('--'+a,v[0],v[1])

	sys.exit(0)

def main(argv):

	t0=time.time()

	reset=false
	merge=false
	capture=[]
	tmpdir="~/.sitemap"

	if len(argv)==0:
		usage()
		
	user=getpass.getuser()
	mydir=os.path.split(sys.argv[0])[0]
	
	# args
	(optlist, argv) = getopt.getopt( argv, shortargs, longargs.keys() )
	for (var, val) in optlist:
		while (var[0] == "-"):		# Strip leading '-'s
			var = var[1:]
		if var in ("m","merge"):
			merge = true
		elif var in ("c", "capture"):
			capture.append(val)
		elif var in ("t", "tmpdir"):
			tmpdir=val
		elif var in ("r", "reset"):
			reset=true
		elif var in ("h", "help"):
			usage()

	tmpdir=os.path.expanduser(tmpdir)
	
	if not os.path.isdir(tmpdir):
		try:
			os.mkdir(tmpdir)
		except:
			warn("Cannot create tmpdir==%s\n" % (tmpdir))
			sys.exit(1)

	if reset:
		os.system("/bin/rm -rf %s/*.cap" % (tmpdir))

	capfiles=[]
	# verify target hosts
	for mid in capture:
		cap=os.path.join(tmpdir,mid+'.cap')
		capfiles.append(cap)
		if os.path.isfile(cap):
			try:
				os.remove(cap)
			except:
				warn("Error removing old capture file: %s\n" % (cap))
				sys.exit(1)			

	warn("Starting captures on: %s\n" % (string.join(capture,',')))
	t1=time.time()
	# scatter: run sitemap.py --capture on each host in parallel
	for mid in capture:
		thread.start_new_thread(sitemapthread,(user,mydir,tmpdir,mid))

	# gather: wait till all are done
	while 1:
		alldone=true
		for cap in capfiles:
			if not os.path.isfile(cap):
				alldone=false
				break
		if alldone:
			break
		time.sleep(1.5)
		
	t2=time.time()
	
	warn("Captures completed in %5.2lf seconds\n" % (t2-t1))

	# merge results
	if merge:
		caps=[]
		files=os.listdir(tmpdir)
		for f in files:
			if string.split(f,'.')[-1] == 'cap':
				caps.append(os.path.join(tmpdir,f))

		if len(caps)==0:
			warn("No capture files in %s\n" % (tmpdir))
			sys.exit(1)
			
		warn("merging[%s]: %s\n" % (tmpdir,string.join(map(lambda x: os.path.split(x)[-1],caps),',')))

		cmd=[]
		a=cmd.append
		a(os.path.join(mydir,'sitemap.py'))
		output=os.path.join(tmpdir,'output')
		if os.path.isfile(output):
			os.remove(output)
		a('--xml %s.xml --pkl %s.pkl' % (output,output))
		for c in caps:
			a('--load %s' % (c))
		a('> /dev/null')
		rv=os.system(string.join(cmd))
		if rv:
			warn("Merged failed for captures: %s\n" % (string.join(caps,',')))
			sys.exit(1)
		if not os.path.isfile(output+'.xml'):
			warn("Merge produced no output\n")
			sys.exit(1)
		xml=open(output+'.xml').read()
		sys.stdout.write(xml)
		t3=time.time()		
		warn("Merge completed in %5.2lf seconds\n" % (t3-t2))
		warn("Scan completed in %5.2lf seconds\n" % (t3-t0))
			

#######################################
#
#######################################

if __name__ == "__main__":
	main(sys.argv[1:])


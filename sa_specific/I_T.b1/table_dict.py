#!/opt/opsware/bin/python -u

import string, sys, time, os

if len(sys.argv) == 3:
	truths_txt = sys.argv[1]
	oc = sys.argv[2]
else:
	print 'Usage: %s <truths.txt> <ObjectClass>' % sys.argv[0]
	sys.exit(1)

sys.stderr.write('%s %s\n' % (time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time())), 'begin'))

f = open( truths_txt )
truths = map( string.strip, f.readlines() )
f.close()

numtruths = len(truths)
sys.stderr.write('%s %s %s\n' % (numtruths, 'truths are working on', oc))
countdict = {}

getTableProggyWithArgs = '%s %s' % ('/opt/opsware/bin/python gettableinfo.py', oc)
sys.stderr.write(getTableProggyWithArgs)
f = os.popen(getTableProggyWithArgs)
(table_name,column_name)=string.split(f.readline() )
f.close()

truth_string = string.join(truths)
javabin='java'
if (os.environ.has_key('JAVABIN')):
  javabin = os.environ['JAVABIN']
javaProggyWithArgs = '%s %s %s %s %s %s' % (javabin, 'TableIdFetcher', oc, table_name, column_name, truth_string)
sys.stderr.write(javaProggyWithArgs)

# java TableIdFetcher DataCenter `./gettableinfo.py DataCenter` `cat /tmp/truths.txt`

f = os.popen(javaProggyWithArgs)
l = f.readline()
while l:
	k = string.strip(l)
	if countdict.has_key(k):
		count = countdict[k] + 1
	else:
		count = 1
	countdict[k] = count
	l = f.readline()
f.close()

sys.stderr.write('%s %s %s\n' % (time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time())), len(countdict), 'items total'))
keys = countdict.keys()
keys.sort()
for key in keys:
	count = countdict[key]
	if count != numtruths:
		print oc, key
sys.stderr.write('%s %s\n' % (time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time())), 'end'))

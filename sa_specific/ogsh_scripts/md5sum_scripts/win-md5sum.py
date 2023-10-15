import md5
import string
import sys
import os

def hexlify(s):
	acc = []
	def munge(byte, append=acc.append, a=ord('a'), z=ord('0')):
		if byte > 9: append(byte+a-10)
		else: append(byte+z)
	for c in s:
		hi, lo = divmod(ord(c), 16)
		munge(hi)
		munge(lo)
	return string.join(map(chr, acc), '')

f = open(sys.argv[1])
windir = os.environ.get("WINDIR")

for i in f.readlines():
	foo = windir + "\system32\\" + i
	path = string.rstrip(foo)

	if not os.access(path, os.R_OK):
		print "couldn't access file %s" % path
#		continue

	m = md5.new()
	g = open(path)

	for line in g.readlines():
		m.update(line)

	g.close()

	print "%s\t%s\t%s" % (path, os.path.getmtime(path), hexlify(m.digest()))

f.close()

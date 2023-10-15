#!/opt/OPSW/bin/python

import md5
import string
import sys
import os

ignore_files = [ "/etc/utmp", "/etc/utmpx" ]

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

def process(file):
	if file in ignore_files:
		return

	if os.path.isdir(file) and not os.path.islink(file):
		for j in os.listdir(file):
			process(file + "/" + j)	

	elif os.path.isfile(file) and not os.path.islink(file):
		m = md5.new()
		f = open(file)

		for line in f.readlines():
			m.update(line)

		f.close()

		print "%s\t%s\t%s" % (file, os.path.getmtime(file), hexlify(m.digest()))

if len(sys.argv) < 2:
	print "Error: no files specified"
	sys.exit(1)

for i in sys.argv[1:]:
	if not os.path.exists(i):
		continue

	process(i)

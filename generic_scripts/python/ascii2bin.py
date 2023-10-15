#!/opt/OPSW/bin/python
# Written for Staples POC to be able to encode and decode binary to store in
# custom attributes using the OGSH 

import uu, sys

def usage():
	print "usage: %s <input file> <output file>" % (sys.argv[0])
	sys.exit(1)

if len(sys.argv) != 3:
	usage()

infilename = sys.argv[1]
outfilename = sys.argv[2]

infile = open(infilename, "rb")
outfile = open(outfilename, "wb")

uu.decode(infile, outfile)

print "Successful."




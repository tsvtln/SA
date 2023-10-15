import imp
import sys
import os
import base64
import gzip
os.write(1,"CODE\n")
n=sys.stdin.readline()
n=n[:len(n)-1]
e=sys.stdin.readline()
l=int(sys.stdin.readline())
s=""
while(len(s)<l):s=s+os.read(0,l-len(s))
os.write(1,"OK\n")
m=imp.new_module(n)
exec compile(gzip.zlib.decompress(base64.decodestring(s)),n,"exec") in m.__dict__
exec e in m.__dict__
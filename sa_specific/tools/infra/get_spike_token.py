import sys,getpass
from coglib import certmaster
ctx = certmaster.getContext("/var/opt/opsware/crypto/spin/spin.srv")
from librpc.xmlrpc import lcxmlrpclib
from librpc import SSLTransport
way = lcxmlrpclib.Server('https://way:1018/wayrpc.py', transport=SSLTransport.SSLTransport(ctx=ctx))
sys.stdout.write("%s\n" % way.spike.authenticate({'username':sys.argv[1],'password':getpass.getpass("password: ")}))


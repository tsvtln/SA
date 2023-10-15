import sys

from coglib import certmaster
from coglib import spinwrapper
ctx = certmaster.getContext("/var/opt/opsware/crypto/spin/spin.srv")
from librpc.xmlrpc import lcxmlrpclib
from librpc import SSLTransport

spin = spinwrapper.SpinWrapper()
way = lcxmlrpclib.Server('https://127.0.0.1:1018/wayrpc.py', transport=SSLTransport.SSLTransport(ctx=ctx))

dc_id = spin.sys.getDCFromDB()['id']
job = {}
job["script"] = "opsware.agent_reach.check_reachability"
job["session_desc"] = "(manual) Automated Communications Test for core: %s" % dc_id
job["username"] = "$spin"
job["sync"] = 0 # Run asynchronously
job["acct_id"] = None
job["params"] = { "dc_ids":[dc_id], "recurse_dcs":1, "incl_unreach_dcs":1 }

sys.stdout.write("About to execute: %s\nContinue? (y/n)\n" % job["session_desc"])
if ( not (sys.stdin.read(1) in "yY") ):
  sys.exit(0)

sys.stdout.write("Session ID: %s\n" % way.script.run( job ))


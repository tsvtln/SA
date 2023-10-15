#!/opt/opsware/bin/python -i
import sys
sys.path.append("/opt/opsware/pylibs")

from coglib import certmaster
ctx = certmaster.getContext("/var/opt/opsware/crypto/spin/spin.srv")
from librpc.xmlrpc import lcxmlrpclib
from librpc import SSLTransport

from coglib import spinwrapper
spin = spinwrapper.SpinWrapper()

gw_list = []
for gc in spin.sys.getDCFromDB(spin.sys.getDB()).getGatewayConf():
  gw_list.append((gc['ip'],gc['proxy_port']))

def get_agent_raw( ip, gw_list=None, realm=None, rpc="rpc.py" ):
  return lcxmlrpclib.Server('https://%s:1002/%s' % (ip, str(rpc)), 
    transport=SSLTransport.SSLTransport(ctx=ctx, realm=realm, gw_list=gw_list))

def get_agent( dvc_id, rpc="rpc.py" ):
  dvc = spin.Device.get( dvc_id )
  realm = dvc.getRealm()
  if ( realm['realm_type'] != 'TRANSITIONAL' ):
    realm_name = realm['realm_name']
  else:
    realm_name = None
  return get_agent_raw( dvc['management_ip'], gw_list=gw_list, realm=realm_name, rpc=rpc )

print """The following functions are avaiable to obtain an agent wrapper by IP or Device
ID:  (intended to be used from python interactive interpreter with '-i' flag)

 o get_agent_raw( ip, gw_list=None, realm=None, rpc="rpc.py" )
 o get_agent( dvc_id, rpc="rpc.py" )
"""

if ( len(sys.argv) > 1 ):
  agent = get_agent( sys.argv[1] )  
  print "agent.cogbot.getVersion(): " + str(agent.cogbot.getVersion())
sys.path.append("/opt/opsware/pylibs")
from librpc.xmlrpc import lcxmlrpclib
from librpc import SSLTransport
from coglib import certmaster

spin = spinwrapper.SpinWrapper()

# Get the gw_list for my DC.
my_gw_list = map(lambda gc:(gc['ip'],gc['proxy_port']), spin.sys.getDCFromDB().getGatewayConf())

# get all root datacenters:
dcs = filter(lambda dc:dc['id']<10000, spin.DataCenter.getAll(restrict={'status':'ACTIVE'}))
dcs.sort(lambda x,y:cmp(x['data_center_id'],y['data_center_id']))

# Cache the datacenter objects in this mesh into a dict.
map_dcs = {}
for dc in dcs:
  map_dcs[dc['id']] = dc

ctx = certmaster.getContext("/var/opt/opsware/crypto/spin/spin.srv")

# Create a new spin object for every data center's primary spin.
dc_spins = {}
for dc in dcs:
  dc_spins[dc['id']] = spinwrapper.SpinWrapper()
  dc_spins[dc['id']].server = lcxmlrpclib.Server("https://spin:1004/spinrpc.py", transport=SSLTransport.SSLTransport(ctx=ctx, realm=dc.getRealm()['realm_name'], gw_list=my_gw_list))


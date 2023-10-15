import gzip,sys,cPickle
from librpc.xmlrpc import lcxmlrpclib
from librpc import SSLTransport
from coglib import certmaster,spinwrapper

spin = spinwrapper.SpinWrapper()

# Get the gw_list for my DC.
my_gw_list = map(lambda gc:(gc['ip'],gc['proxy_port']), spin.sys.getDCFromDB().getGatewayConf())

# get all root datacenters:
dcs = spin.DataCenter.getAll(restrict={'status':'ACTIVE',"ontogeny":"PROD"})
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

fn = sys.argv[1]
if ( fn[-7:] != ".pkl.gz" ): fn = "%s.pkl.gz" % fn
sys.stderr.write("Data will be stored to \"%s\".\n" % fn)
of = gzip.open(fn, "w")

for dc_id in dc_spins.keys():
  dc_spin = dc_spins[dc_id]
  sys.stderr.write("Dumping sent transaction timing from DC %d\n" % dc_id)
  tt = map(lambda i:(i[0], i[1].date(), i[1].date()), dc_spin._Transaction.getList(restrict={"replicate_flg":1}, omit={"publish_dt":None,"create_dt":None}, fields=["create_dt", "publish_dt"]))
  cPickle.dump({"dc_id":dc_id, "tt":tt}, of)
  sys.stderr.write("Dumping recieved transaction timing from DC %d\n" % dc_id)
  tl = map(lambda i:(i[0], i[1].date(), i[2].date()), dc_spin._TransactionLog.getList(fields=["publish_dt","receive_dt"]))
  cPickle.dump({"dc_id":dc_id, "tl":tl}, of)

sys.stderr.write("done.\n")

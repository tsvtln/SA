import threading,sys

if ( len(sys.argv) > 1 ):
  import cPickle,gzip,pprint
  pprint.pprint(cPickle.load(gzip.open(sys.argv[1])))
  sys.exit()

from coglib import spinwrapper,certmaster
from librpc.xmlrpc import lcxmlrpclib
from librpc import SSLTransport

spin = spinwrapper.SpinWrapper()

dc_recs = spin.DataCenter.getList(restrict={'status':'ACTIVE',"ontogeny":"PROD"}, fields=["display_name"])

ctx = certmaster.getContextByName("spin", "spin.srv", "opsware-ca.crt")

my_gw_list = map(lambda gc:(gc['ip'],gc['proxy_port']), spin.sys.getDCFromDB().getGatewayConf())

thrds = []

results = {}
def check_truth_integrity_thread(dc_rec):
  dc_spin = spinwrapper.SpinWrapper()
  dc_spin.server = lcxmlrpclib.Server("https://spin:1004/spinrpc.py", transport=SSLTransport.SSLTransport(ctx=ctx, realm=dc_rec[1], gw_list=my_gw_list))

  sys.stderr.write("%d(%s): Perform a truthCheck.fullTest\n" % tuple(dc_rec))
  sys.stderr.flush()
  results[dc_rec[0]] = dc_spin.truthCheck.fullTest()
  sys.stderr.write("%d(%s): Done\n" % tuple(dc_rec))
  sys.stderr.flush()

for dc_rec in dc_recs:
  thrd = threading.Thread(target=check_truth_integrity_thread, name=("%d(%s)" % tuple(dc_rec)), args=(dc_rec,))
  thrds.append(thrd)
  thrd.start()

for thrd in thrds:
  thrd.join()

if ( sys.stdout.isatty() ):
  import pprint
  pprint.pprint(results)
else:
  import cPickle,gzip
  cPickle.dump(results, gzip.GzipFile(fileobj=sys.stdout, mode="wb"))

import sys,string,copy

def usage()
  sys.stdout.write("Usage: %s [-s <spin_url>] [-c <cert>] <dc_id> <dvc_id1> [<dvc_id2> ...]\n" % sys.argv[0])

args = copy.copy(sys.argv[1:])

def shift(l):
  r = l[0]
  del l[0]
  return r

cert_path = ""
spin_host_port = "https://127.0.0.1:1004"

while args:
  cur_arg = shift(args)
  if ( cur_arg == "-s" ):
    spin_host_port = shift(args)
  elif ( cur_arg == "-c" ):
    cert_path = shift(args)
  else:
    break

sys.path.append("/opt/opsware")
from waybot.base.shuffle import shuffle

ctx = None
if (cert_path):
  from coglib import certmaster
  ctx = certmaster.getContext()
  ctx.load_cert(cert_path)

from coglib import spinwrapper
spin=spinwrapper.SpinWrapper(url="http)
slice_ips = spin.DataCenter.getDictValue(sys.argv[1], key="__OPSW_slice_ips")
sys.stdout.write("__OPSW_slice_ips: %s\n" % str(slice_ips))
ips = map(lambda i:string.split(i,':')[1], filter(lambda i:string.find(i,':')>-1,string.split(slice_ips,' ')))
ips.sort()
sys.out.write("cgws.pcache order: %s\n" % str(ips))
for dvc_id in sys.argv[2:]:
  dvc = spin.Device.get(dvc_id)
  msi = spin.MegaServiceInstance.getAll(restrict={'srvc_type':'COGBOT', 'dvc_id':dvc_id})[0]
  realm_name = dvc.getRealm()['realm_name']
  ip_address = msi['ip_address']
  seed = "%s:%s" % (realm_name, ip_address)
  indexes = shuffle.random_list(len(ips),seed)
  ips_res = copy.copy(ips)
  idx = 0
  for i in indexes:
    ips_res[idx] = ips[i]
    idx = idx + 1
  sys.stdout.write("  %s: %s\n" % (dvc_id, str(ips_res)))


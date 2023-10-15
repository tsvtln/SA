from coglib import spinwrapper
import opsware_common,sys,time

spin = spinwrapper.SpinWrapper()

dc = spin.sys.getDCFromDB()
sys.stdout.write("DataCenter: %s(%d)\n" % (dc['display_name'],long(dc['id'])))

try:
  slice_ips = dc.getDictValue(key="__OPSW_slice_ips")
except opsware_common.errors.OpswareError, e:
  sys.stdout.write("DataCenter %s does not have a \"__OPSW_slice_ips\" key.\n" % repr(dc['display_name']))
  sys.exit(1)

sys.stdout.write("__OPSW_slice_ips: %s\n" % slice_ips)

ips = map(lambda i:string.split(i,':')[1], filter(lambda i:string.find(i,':')>-1,string.split(slice_ips,' ')))
sys.stdout.write("parsed ips: %s\n\n" % repr(ips))

sys.stdout.write("current time from the spin on each of these slices:\n")
for ip in ips:
  sys.stdout.write("%s: " % ip)
  sys.stdout.flush()
  try:
    spin_time = spinwrapper.SpinWrapper(url="https://%s:1004" % ip).sys.time()
    sys.stdout.write("%s (dt: %ss)\n" % (repr(time.ctime(spin_time)),int(time.time()-spin_time)))
  except:
    sys.stdout.write("ERR: %s\n" % str(sys.exc_info()[1]))

import traceback,sys,string
from librpc.xmlrpc import lcxmlrpclib
from librpc import SSLTransport
from coglib import certmaster,spinwrapper

def format_rows(rows, col_sep=' ', just_fn=lambda c:'-'):
  if ( not rows ): return ''
  num_cols = len(rows[0])
  col_maxes = range(num_cols)
  for cur_col in col_maxes:
    col_maxes[cur_col] = max(map(lambda r,cc=cur_col:len(str(r[cc])), rows))
#  fmt = string.join(["%%-%ds"] * num_cols, col_sep) % tuple(col_maxes)
  fmt = string.join(map(lambda c,just_fn=just_fn: "%%%%%s%%ds" % just_fn(c), range(num_cols)), col_sep) % tuple(col_maxes)
  return string.join(map(lambda r,f=fmt:f % r, rows), '\n') + '\n'

def just_fn(i):
  if ( i==0 ): return '-'
  else: return ''

def last_ex():
  return string.join( apply( traceback.format_exception, sys.exc_info() ), "")

sys.stdout.write("Vault Stats:\n\n")
sys.stdout.flush()

spin = spinwrapper.SpinWrapper()
dc_recs = spin.DataCenter.getList(restrict={'status':'ACTIVE','ontogeny':'PROD'},fields=['display_name', 'data_center_name'])

for dc_rec in dc_recs:
  sys.stdout.write("%s(%d/%s):\n\n" % (dc_rec[2], dc_rec[0], dc_rec[1]))
  sys.stdout.flush()

  try:
    cgw_realm = dc_rec[1]
    ctx = certmaster.getContextByName("spin","spin.srv","opsware-ca.crt")
    gw_list = (("127.0.0.1", 3002),)
    vault = lcxmlrpclib.Server('http://mmopsw:5678', transport = SSLTransport.SSLTransport(ctx=ctx, realm=cgw_realm, gw_list=gw_list))
    status = vault.rpc.getStatus().items()
    status.sort(lambda a,b:cmp(a,b))
    sys.stdout.write("Status:\n%s\n\n" % format_rows(status, col_sep='|', just_fn=just_fn))
    sys.stdout.flush()
    stats = vault.rpc.getStatistics().items()
    stats.sort(lambda a,b:cmp(a,b))
    sys.stdout.write("Statistics:\n%s\n\n" % format_rows(stats, col_sep='|', just_fn=just_fn))
    sys.stdout.flush()
  except:
    sys.stdout.write("Unexpected Exception:\n%s\n\n" % last_ex())
    sys.stdout.flush()

  


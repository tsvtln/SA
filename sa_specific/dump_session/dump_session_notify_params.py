from coglib import spinwrapper

spin = spinwrapper.SpinWrapper()

sids = spin.Session.getIDList()

tot_count = spin.Session.getCount()

cur_count = 1

for sid in sids:
  sys.stderr.write('%d/%d\r' % (cur_count, tot_count))
  params = spin.Session.getParams(id=sid)
  if ( params.has_key('$notify_params') ):
    try:
      #sys.stdout.write('%s: %s\n' % (sid, str(params['$notify_params']['on_success'][0][1]['recipient_addrs'])))
      sys.stdout.write('%s: %s\n' % (sid, str(params['$notify_params'])))
      sys.stdout.flush()
    except:
      sys.stdout.write('%s: %s\n' % (sid, 'error'))
      sys.stdout.flush()
  cur_count = cur_count + 1

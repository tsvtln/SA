import sys
from coglib import spinwrapper

spin = spinwrapper.SpinWrapper(url="http://127.0.0.1:1007")

def msg(s, args=None):
  if ( args is not None ):
    s = s % args
  sys.stdout.write(s)
  sys.stdout.flush()

# id of the default user group role.
ar_dug_ids = spin._AAARole.getIDList(restrict={'role_type':'USER_GROUP','rolespace':'OPSWARE','namespace':'OPSWARE','role_name':'DEFAULT_USER_GROUP'})
if ( len(ar_dug_ids) > 1 ):
  msg("WARNING: %s: more than a single default user group role.\n", (repr(ar_dug_ids),))
ar_dug_id = ar_dug_ids[0]

# List of user ids already associated with the default user group role.
ar_dug_uids = map(lambda i:i[1], spin._AAARole.getChildList(child_class='_AAARoleUser', id=ar_dug_id, fields=['user_id']))

# list of all active user ids.
active_urs = spin._AAAAaaUser.getList(restrict={'account_status':'ACTIVE'}, fields=['username'])

# itterate through all active user ids:
# Filter out all active user ids that don't show up as a child of the default user group role.
urs = filter(lambda ur,ar_dug_uids=ar_dug_uids:ur[0] not in ar_dug_uids, active_urs)

if ( len(urs) > 0 ):
  msg("%d users are missing their default user group role attachment.\nWould you like to fix these? (y/n) ", (len(urs),))
  a = sys.stdin.read(1)
  if ( a in "yY" ):
    msg("Fixing: ")
    for ur in urs:
      msg("%s ",( ur[1],))
      spin._AAARoleUser.new(user_id=ur[0], role_id=ar_dug_id)
    msg("\nDone.\n")
  else:
    msg("Not fixing.\n")
else:
  msg("No active users are missing their default user group role attachment.\n")  

import sys
from coglib import spinwrapper
spin = spinwrapper.SpinWrapper(url="http://127.0.0.1:1007")

if ( len(sys.argv) < 3 ):
  sys.stdout.write("Usage: %s <rc_id> <account_id1> [<account_id2> ...]\n")
  sys.exit(1)

rc_id = sys.argv[1]
acct_ids = sys.argv[2:]

spin.RoleClass.removeAccounts(id=rc_id, child_ids=acct_ids)
sys.stdout.write("OK\n")


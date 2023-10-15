import sys
from coglib import spinwrapper
spin = spinwrapper.SpinWrapper(url="http://127.0.0.1:1007")

if ( len(sys.argv) < 3 ):
  sys.stdout.write("Usage: %s <rc_id> <platform_id1> [<platform_id2> ...]\n")
  sys.exit(1)

rc_id = sys.argv[1]
plat_ids = sys.argv[2:]

spin.RoleClass.addPlatforms(id=rc_id, child_ids=plat_ids)
sys.stdout.write("OK\n")


import sys

from coglib import spinwrapper

spin = spinwrapper.SpinWrapper()

cs = spin.sys.getClasses()

cns = filter(lambda cn:cn[:4]=='_AAA', map(lambda c:c['name'], cs))

for cn in cns:
  objs = getattr(spin, cn).getAll()
  for obj in objs:
    sys.stdout.write("%s\n" % obj)
    sys.stderr.write(".")
    sys.stderr.flush()



#!/lc/bin/python

import sys
import os
import string

sys.path.extend(['/lc/blackshadow', '/cust/usr/blackshadow', '/cust/usr/blackshadow/spin', '/lc/blackshadow/coglib'])

os.environ['SPIN_DIR'] = '/cust/usr/blackshadow/spin'

import truthdb
import spinobj

if len(sys.argv) == 2:
        oc = sys.argv[1]
else:
        print 'Usage: %s <ObjectClass>' % sys.argv[0]
        sys.exit(1)

cls = spinobj.getObjectClass(oc)
db = truthdb.DB()
tablename = cls(db)._table.name
pkeys = []
for field in cls(db).getIDFields():
	pkeys.append(field.name)
print "%s %s" % (tablename, string.join(pkeys, ','))

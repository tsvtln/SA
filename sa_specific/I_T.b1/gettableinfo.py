#!/opt/opsware/bin/python

import sys
import os
import string

sys.path.extend(['/opt/opsware/pylibs', '/opt/opsware/spin'])

os.environ['SPIN_DIR'] = '/opt/opsware/spin'

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

#!/opt/opsware/bin/python -u

import string, sys, time, os, pwd

if len(sys.argv) == 2:
        oc = sys.argv[1]
else:
        print 'Usage: %s <ObjectClass>' % sys.argv[0]
        sys.exit(1)

sys.stderr.write('%s %s\n' % (time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time())), 'begin'))

sys.path.append( "/opt/opsware/corelibs" )
sys.path.append( "/opt/opsware" )
sys.path.append( "/opt/opsware/spin" )
sys.path.append( "/opt/opsware/pylibs" )
try:
    import truthdb
    import spinobj
    import truthtable
    import multimaster
    import spinconf
except ImportError:
    sys.stderr.write( "Unable to import Data Access Engine libraries: %s, %s.  Is the Data Access Engine installed on this host?\n" % sys.exc_info()[0:2] )
    sys.exit( 1 )

debug = 0

user = pwd.getpwuid(os.getuid())[0]
method = sys.argv[0]

all_dcs = multimaster.getAllDCs(method, user)

numtruths = len(all_dcs)
sys.stderr.write('%s %s %s\n' % (numtruths, 'truths are working on', oc))
countdict = {}

cls = spinobj.getObjectClass(oc)
mydb = truthdb.DB()
table_name = cls(mydb)._table.name
id_fields = map(lambda f:f.name, cls(mydb).getIDFields())
id_columns = string.join(id_fields, ",")

for dc_id in all_dcs.keys():
  db = multimaster.getDB(method, user, all_dcs[dc_id].getDBName())
  cur = db.getCursor()
  cur.execute("select %s from %s" % (id_columns, table_name))
  while 1:
    rs = cur.fetchmany(100000)
    if ( not rs ): break
    for r in rs:
      obj_id = string.join(map(lambda i:str(i),r),"-")
      count = -1
      if (countdict.has_key(obj_id)):
        count = countdict[obj_id] + 1
      else:
        count = 1
      countdict[obj_id] = count

sys.stderr.write('%s %s %s\n' % (time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time())), len(countdict), 'items total'))
keys = countdict.keys()
keys.sort()
for key in keys:
        count = countdict[key]
        if count != numtruths:
                print oc, key
sys.stderr.write('%s %s\n' % (time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time())), 'end'))

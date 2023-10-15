import sys, os, string, pwd
import truthdb, spinobj, multimaster

sys.stdout.write("Attempting to connect to every DB in the mesh...\n")

mydb = truthdb.DB()

user = pwd.getpwuid(os.getuid())[0]
method = sys.argv[0]

all_dcs = multimaster.getAllDCs(method, user)
for dc_id in all_dcs.keys():
  db = multimaster.getDB(method, user, all_dcs[dc_id].getDBName())
  cur = db.getCursor()
  cur.execute("select banner from v$version where banner like '%PL/SQL%'")
  rec = cur.fetchone()
  sys.stdout.write("%s (%s): %s: '%s'\n" % (spinobj.DataCenter(mydb,dc_id)['data_center_name'], str(dc_id), str(db), rec[0]))


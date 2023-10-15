self.send_response(200)
self.send_header("Content-type", "text/html")
self.end_headers()

from acsbarlib import config
from barbot import barbotrpc
from barbot import barbot
import pprint
import string

self.wfile.write("<xmp>")

self.wfile.write("%s\n\n" % dir(barbot))

# Manually invoke the barbot.doBackup() function.
# (Should be generalized to scan through all cronjobs and find it instead of assuming
# entry #6)
#func = hive.cronbot.jobs[6].func
#self.wfile.write("hive.cronbot.jobs[6].func: %s\n" % str(func))
#if (string.find(str(func),"doBackup") > -1):
#  self.wfile.write("Executing barbot.doBackup()\n")
#  func()
#  self.wfile.write("done invoking doBackup()\n\n")

state_obj=hive.barbot.getState()
o2={'should_run': state_obj.should_run_flg,'inc_interval' : state_obj.inc_interval_int,'full_interval' : state_obj.full_interval_int,'next_full' : state_obj.next_full_int}
self.wfile.write("%s\n\n" % pprint.pformat(o2))

self.wfile.write("acsbarlib.config.getConfig(hive): (from acsbarconfig.db)\n" + pprint.pformat(config.getConfig(hive)))
self.wfile.write("</xmp>")


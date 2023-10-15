self.send_response(200)
self.send_header("Content-type", "text/html")
self.end_headers()

import truthdb, spinobj, spinconf

db = truthdb.DB()

self.wfile.write("<pre>\n")

self.wfile.write("spinobj.isPrimarySpin(db): %s\n" % str(spinobj.isPrimarySpin(db)))

dc = spinobj.DataCenter( db, truthdb.getDCID() )

dvc = dc.getPrimarySpinDevice()

self.wfile.write("dvc: %s\n" % str(dvc))
self.wfile.write("spin.my_dvc_id: %s\n" % spinconf.get("spin.my_dvc_id"))

self.wfile.write("</pre>\n")

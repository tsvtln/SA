self.send_response(200)
self.send_header("Content-type", "text/html")
self.end_headers()

self.wfile.write("hive.config['identconf']: %s\n" % str(hive.config['identconf']))
self.wfile.write("hive.config['tunnelconf']: %s\n" % str(hive.config['tunnelconf']))

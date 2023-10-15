#                      -*- Mode: Python ; tab-width: 4 -*- 

import sys
import traceback
import string
import cgi
import resource


import checkperms

def getDoc():
	rlimits = []
	for k in resource.__dict__.keys():
		if k[:7] == "RLIMIT_":
			rlimits.append(k)
	rlimits.sort()
	o = []
	o.append("<table>")
	for r in rlimits:
		l = resource.getrlimit(getattr(resource, r))
		o.append("<tr><td>%s</td><td>%s</td></tr>" % (r, l))
	o.append("</table>")
	return string.join(o, "\n")


########################################################################################
def opletMain( self, args, pagestatus ):

        checkperms.checkPerms( self.peerinfo, allowed_certs = ["spin", "spin-developer", "spog-developer"] )
        pagestatus.setDescription( "ulimit.py" )

        try:
                s = getDoc()
        except:
                l = apply( traceback.format_exception, sys.exc_info() )
                s = "Huh?\n<pre>%s</pre>" % (cgi.escape(string.join(l, "")))

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", str(len(s)))
        self.end_headers()
        self.wfile.write(s)


#-------------------------------------------------------------------------------
if __name__ == "__builtin__":
        opletMain( self, args, pagestatus )
#-------------------------------------------------------------------------------

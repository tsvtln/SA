import pytwist,sys
ts = pytwist.twistserver.TwistServer()
from pytwist.com.opsware.server import ServerRef
sys.stdout.write(ts._makeCall("com.opsware.server.ServerService", "readConfigFile", (ServerRef(sys.argv[1]), sys.argv[2], "")))

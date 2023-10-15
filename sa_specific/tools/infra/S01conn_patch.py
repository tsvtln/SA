from M2Crypto.SSL.Connection import Connection
import sys,os

mthd_srcs = ("""def send(self, data):
  self.log_data("send", data)
  return self.send_orig(data)
""",
  """def write(self, data):
  self.log_data("write", data)
  return self.write_orig(data)
""",
  """def read(self, size=4096):
  data = self.read_orig(size)
  self.log_data("read", data)
  return data
""",
  """def recv(self, size=4096):
  data = self.recv_orig(size)
  self.log_data("recv", data)
  return data
""",
  """def log_data(self, op, data):
  if ( os.path.exists(logfile) ):
    data_len = -1
    try:
      data_len = len(data)
    except:
      pass
    log_label = "%s-%s" % (('%s:%s' % self.socket.getsockname()), ('%s:%s' % self.socket.getpeername()))
    msg = "%s: %s(%d): %s\\n" % (log_label, op, data_len, repr(data))
    try:
      f = open(logfile, "a")
      f.write(msg)
    finally:
      f.close()
""")

exec """import os
logfile = %s
""" % repr(os.path.join(hive.conf.get("logpath"), "coglib_ssl_data.log")) in Connection.__dict__

for mthd_src in mthd_srcs:
  mthd_co = compile(mthd_src, "S01conn_patch.py<string>", "exec")
  mthd_name = mthd_co.co_names[0]
  if ( hasattr(Connection, mthd_name) ):
    mthd_name_orig = "%s_orig" % mthd_name
    setattr(Connection, mthd_name_orig, getattr(Connection, mthd_name))
    sys.stderr.write("%s: Backed up origonal method %s of Connection class.\n" % ("conn_patch", repr(mthd_name)))
    sys.stderr.flush()
  exec mthd_co in Connection.__dict__
  sys.stderr.write("%s: Injected new method %s into Connection class.\n" % ("conn_patch", repr(mthd_name)))
  sys.stderr.flush()

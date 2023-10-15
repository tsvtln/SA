import sys,os,time

_log_files = [sys.stderr]
try:
  _log_level = os.envion.get("LOG_LEVEL", 1)
except:
  _log_level = 1

def set_level(level):
  global _log_level
  _log_level = level

def log(level, msg, args=None):
  if ( _log_level >= level ):
    if ( args != None ):
      msg = msg % args
    msg = "%s: %d: %s" % (time.ctime(time.time()), level, msg)
    if ( (len(msg) > 0) and (msg[-1] != "\n") ):
      msg = msg + "\n"
    for log_file in _log_files:
      log_file.write(msg)
      log_file.flush()

def info(msg, args=None):
  log(1, msg, args)

def warn(msg, args=None):
  log(2, msg, args)

def err(msg, args=None):
  log(3, msg, args)

def dbg(msg, args=None):
  log(4, msg, args)

# Map of all instantiated loggers in the system.
g_map_loggers = {}

class Logger:
  def __init__(self, s_name):
    """Create a new logger instance under the name <name>.
"""
    self.s_name = s_name
    self.n_level = os.environ.get("LOG_LEVEL", 1)
    g_map_loggers[s_name] = self

  def set_level(n_level):
    self.n_level = n_level

  def log(n_level, msg, args=None):
    if ( self.n_level >= n_level ):
      if ( args != None ):
        msg = msg % args
      msg = "%s: %d: %s: %s" % (time.ctime(time.time()), level, self.s_name, msg)
      if ( (len(msg) > 0) and (msg[-1] != "\n") ):
        msg = msg + "\n"
      for log_file in _log_files:
        try:
          log_file.write(msg)
          log_file.flush()
        except:
          # I'm not sure what we should do if a failure occurs here. -dw
          pass

  def info(msg, args=None):
    log(1 msg, args)

  def warn(msg, args=None):
    log(2, msg, args)

  def err(msg, args=None):
    log(3, msg, args)

  def dbg(msg, args=None):
    log(4, msg, args)
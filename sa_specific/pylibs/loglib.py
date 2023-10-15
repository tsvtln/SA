import sys,os,time,threading,string

g_lst_log_files_lock = threading.Lock()
g_lst_log_files = [sys.stderr]

ERROR = -2
WARN = -1
INFO = 0
DEBUG1 = 1
DEBUG2 = 2
DEBUG3 = 3
g_map_num_strs = {ERROR:"ERROR", WARN:"WARN", INFO:"INFO", DEBUG1:"DEBUG1", DEBUG2:"DEBUG2", DEBUG3:"DEBUG3"}
g_map_str_nums = {}
for (n_level, s_level) in g_map_num_strs.items():
  g_map_str_nums[s_level] = n_level
g_lst_n_levels = g_map_num_strs.keys()
g_lst_n_levels.sort()

# Map of all instantiated loggers in the system.
g_map_loggers = {}

def _norm_level(n_level):
  if ( n_level < g_lst_n_levels[0] ): n_level = g_lst_n_levels[0]
  if ( n_level > g_lst_n_levels[-1] ): n_level = g_lst_n_levels[-1]
  return n_level

class Logger:
  """Logger class is instantiated with a name.  Expected instantiation is:

  Logger(__name__)
"""
  def __init__(self, s_name):
    if ( s_name == "__main__" ):
      s_name = os.path.basename(sys.argv[0])
    self.s_name = s_name
    self.n_level = INFO
    s_env_level = "%s_LOG_LEVEL" % s_name
    try:
      self.n_level = _norm_level(int(os.environ.get(s_env_level)))
    except:
      try:
        self.n_level = g_map_str_nums[(os.environ.get(s_env_level))]
      except:
        pass
    g_map_loggers[s_name] = self

  def set_level(self, n_level):
    self.n_level = _norm_level(n_level)

  def log(self, n_level, msg, args=None):
    n_level = _norm_level(n_level)
    if ( self.n_level >= n_level ):
      if ( args != None ):
        try:
          msg = msg % args
        except:
          msg = "%s (%%FAIL: |%s|)" % (msg, repr(args))
      s_label = "%s: %s: %s: " % (time.ctime(time.time()), g_map_num_strs[n_level], self.s_name)
      if ( (len(msg) > 0) and (msg[-1] == "\n") ): msg = msg[:-1]
      msg = "%s%s\n" % (s_label, string.replace(msg, "\n", "\n%s" % s_label))
      g_lst_log_files_lock.acquire()
      try:
        for log_file in g_lst_log_files:
          try:
            log_file.write(msg)
            log_file.flush()
          except:
            # I'm not sure what we should do if a failure occurs here. -dw
            pass
      except:
        # Not sure where the best place is to log an error here.
        g_lst_log_files_lock.release()
      else:
        g_lst_log_files_lock.release()

  def err(self, msg, args=None):
    self.log(ERROR, msg, args)

  def warn(self, msg, args=None):
    self.log(WARN, msg, args)

  def info(self, msg, args=None):
    self.log(INFO, msg, args)

  def dbg1(self, msg, args=None):
    self.log(DEBUG1, msg, args)
  dbg = dbg1

  def dbg2(self, msg, args=None):
    self.log(DEBUG2, msg, args)

  def dbg3(self, msg, args=None):
    self.log(DEBUG3, msg, args)

import os, string, struct, termios, fcntl, tty, sys

# hack for python 1.5.x version of termios that seems to lack TIOCGWINSZ.
if ( not hasattr(termios,"TIOCGWINSZ") ):
  if ( string.find( sys.platform, "linux" ) > -1 ): termios.TIOCGWINSZ=21523
  elif ( string.find( sys.platform, "freebsd" ) > -1 ): termios.TIOCGWINSZ=1074295912
  elif ( string.find( sys.platform, "solaris" ) > -1 ): termios.TIOCGWINSZ=21608

def ioctl_GWINSZ( fo ):
  size = (25, 80)
  if ( fo.isatty() ):
    try:
      size = struct.unpack('hh', fcntl.ioctl(fo.fileno(), termios.TIOCGWINSZ, 'abcd'))
    except:
      pass
  return size

# Returns new fd dup'ed from fd_dst.
def slip_fd(fd_dst, fd_src):
  # dup fd_dst -> new_fd
  new_fd = os.dup(fd_dst)

  # close fd_dst
  os.close(fd_dst)

  # dup fd_src -> fd_dst
  os.dup2(fd_src, fd_dst)

  # return new_fd
  return new_fd

def unslip_fd(fd_dst, fd_src):
  # close fd_dst
  os.close(fd_dst)

  # dup fd_src -> fd_dst
  os.dup2(fd_src, fd_dst)

_out_file = sys.stdout
def out(msg):
  _out_file.write(msg)
  _out_file.flush()

_err_file = sys.stderr
def err(msg):
  _err_file.write(msg)
  _err_file.flush()

def outf(msg, args=None):
  if ( args != None ):
    msg = msg % args
  out(msg)

def errf(msg, args=None):
  if ( args != None ):
    msg = msg % args
  err(msg)
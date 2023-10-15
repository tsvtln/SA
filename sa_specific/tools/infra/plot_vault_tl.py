##
#
# This utility will generate an xplot.org compatible plot file based upon an
# input file containing records of the following form:
#
#    <recv_dt> <tran_id> <publish_dt> <dml_count> <recv_buf_size> <dst_dc_id>
#
# There is a vault runtime patch, 4639632828_dp3, that allows the vault to
# generate such records from incoming transaction messages.
#
# The key data being captured here is the <recv_buf_size>.  This data, when
# analyzed in the context of a NR spike, can differentiate between a network /
# opswgw mesh bottleneck vs a vault / database bottleneck.
#

import sys,os,traceback,string

def last_ex():
  return string.join( apply( traceback.format_exception, sys.exc_info() ), "")

def msg(s, args=None):
  if ( args is not None ):
    s = s % args
  sys.stdout.write(s)
  sys.stdout.flush()

class Plot:
  ybox_height = 100
  xmin = None
  xmax = None

  def __init__(self, ybox_num=0, yunits=""):
    self.ymin = None
    self.ymax = None
    self.yrmin = ybox_num * Plot.ybox_height
    self.yrmax = (ybox_num+1) * Plot.ybox_height
    self.yunits = yunits
    self.pts = []
#    self.colors = []

  def emit_bounds_box(self, fo, color):
#    print self.ymin, self.ymax, self.yrmin, self.yrmax
    xpad = (Plot.xmax-Plot.xmin)/20.0
    ypad = (self.yrmax-self.yrmin)/20.0
    fo.write("invisible %f %f\n" % (Plot.xmin, self.yrmin-5))
    fo.write("invisible %f %f\n" % (Plot.xmax, self.yrmax+5))

    # Upper bound
    fo.write("line %f %f %f %f %d\n" % (Plot.xmin, self.yrmax, Plot.xmax, self.yrmax, color))
    fo.write("btext %f %f\n" % (Plot.xmin + xpad, self.yrmax))
    fo.write("%f %s\n" % (self.ymax, self.yunits))

    # Zero line:
    if ( (self.ymin < 0) and (self.ymax > 0) ):
      yrzero = self.yrmin + (Plot.ybox_height*((0.0 - self.ymin)/(self.ymax - self.ymin)))
      fo.write("line %f %f %f %f %d\n" % (Plot.xmin, yrzero, Plot.xmax, yrzero, color))

    # Lower bound
    fo.write("line %f %f %f %f %d\n" % (Plot.xmin, self.yrmin, Plot.xmax, self.yrmin, color))
    fo.write("atext %f %f\n" % (Plot.xmin + xpad, self.yrmin))
    fo.write("%f %s\n" % (self.ymin, self.yunits))

  def emit_key(self, fo, colors):
    ypad = (self.yrmax-self.yrmin)/20.0
    y = self.yrmax - ypad
    xpad = (Plot.xmax-Plot.xmin)/20.0
    xdelta = xpad/5.0
    for color in colors:
      y = y - ypad
      fo.write("line %f %f %f %f %d\n" % (Plot.xmin+xpad, y, Plot.xmin+xpad+xdelta, y, color))
      fo.write("rtext %f %f\n" % (Plot.xmin+xpad+xdelta, y))
      fo.write("%d\n" % color)

  def y_to_yr(self, y):
    return self.yrmin + (Plot.ybox_height*((y-self.ymin)/(self.ymax-self.ymin)))

  def emit_points(self, fo):
    for pt in self.pts:
      fo.write(". %f %f %d\n" % (pt[0], self.y_to_yr(pt[1]), pt[2]))

  def emit_lines(self, fo):
    if ( (self.ymin < 0) and (self.ymax > 0) ):
      yrzero = self.yrmin + (Plot.ybox_height*((0.0 - self.ymin)/(self.ymax - self.ymin)))
    else:
      yrzero = self.yrmin
    for pt in self.pts:
      fo.write("line %f %f %f %f %d\n" % (pt[0], self.y_to_yr(pt[1]), pt[0], yrzero, pt[2]))

  def add_point(self, x, y, color):
    if ( (Plot.xmin is None) or (x < Plot.xmin) ): Plot.xmin = x
    if ( (Plot.xmax is None) or (x > Plot.xmax) ): Plot.xmax = x
    if ( (self.ymin is None) or (y < self.ymin) ): self.ymin = y
    if ( (self.ymax is None) or (y > self.ymax) ): self.ymax = y
#    if ( color not in self.colors ): self.colors.append(color)
    self.pts.append((x, y, color))

  def stddev_fit(self, mult=2.5):
    print self.ymin, self.ymax
    mean = sum(map(lambda i:i[1], self.pts))/len(self.pts)
    print "mean: %f" % mean
    stddev = (sum(map(lambda i,mean=mean:(mean-i[1])**2, self.pts))/len(self.pts))**0.5
    print "stddev: %f" % stddev
    ymin = max(mean-(mult*stddev), self.ymin)
    ymax = min(mean+(mult*stddev), self.ymax)
    self.ymin = None
    self.ymax = None
    print len(self.pts)
    pts = self.pts
    self.pts = []
    for pt in pts:
      if ( pt[1] >= ymin and pt[1] <= ymax ):
        apply(self.add_point, pt)
    print self.ymin, self.ymax
    print len(self.pts)

def main():
  if ( len(sys.argv) != 2 ):
    msg("Usage: %s <tl.log>\n\n" & sys.argv[0])
    sys.exit()

  f_size = None

  fn = sys.argv[1]
  if ( fn == "-" ):
    f = sys.stdin
    fn = "stdin-%d" % int(time.time())
  else:
    f = open(fn)
    f_size = os.fstat(f.fileno())[6]

  ofn = "%s.xplot" % fn

  msg("%s -> %s\n", (fn, ofn))

  fo = open(ofn, "w")

  fo.write("""timeval double
title
(TODO: fix) transaction lag vs recv_dt (top) / dml_count count vs recv_dt (bottom)
xlabel
recv_dt (epoch)
ylabel
lag sec (top) / dml_cnt (bottom)
""")

  plot_lag = Plot(2, "sec")
  plot_recv_buf = Plot(1, "bytes")
#  plot_freq = Plot(1, "#tran
  plot_dml_count = Plot(0, "#dml")

  src_dc_ids = []

  cur_pct = 0
  while 1:
    try:
      cur_line = f.readline()
      if ( cur_line == "" ):
        break
      recv_dt, tran_id, publish_dt, dml_count, recv_buf, dst_dc_id = string.split(string.strip(cur_line), " ")
      recv_dt = float(recv_dt)/1000
      tran_id = int(tran_id)
      publish_dt = float(publish_dt)/1000
      dml_count = float(dml_count)
      recv_buf = float(recv_buf)
      dst_dc_id = int(dst_dc_id)

      src_dc_id = tran_id % 1000
      if (src_dc_id not in src_dc_ids): src_dc_ids.append(src_dc_id)
      plot_lag.add_point(recv_dt, (recv_dt-publish_dt), src_dc_id)
      plot_recv_buf.add_point(recv_dt, recv_buf, src_dc_id)
      plot_dml_count.add_point(recv_dt, dml_count, src_dc_id)

      cur = f.tell()
      new_cur_pct = float(cur)/float(f_size)*100
      if ( int(new_cur_pct) > int(cur_pct) ):
        cur_pct = new_cur_pct
        msg("\r%d/%d (%.3f%%)", (cur, f_size, cur_pct))
    except KeyboardInterrupt, e:
      msg("\nAborting processing log records\n")
      break

  # Shape up the Y min/max
  plot_lag.stddev_fit()
  plot_dml_count.ymin = 0

  # Emit bounding boxes for each plot.
  plot_lag.emit_bounds_box(fo, 0)
  plot_lag.emit_key(fo, src_dc_ids)
  plot_recv_buf.emit_bounds_box(fo, 0)
  plot_dml_count.emit_bounds_box(fo, 0)

  # Emit data for each plot.
  plot_lag.emit_points(fo)
  plot_recv_buf.emit_points(fo)
  plot_dml_count.emit_lines(fo)

  msg("\nDone.\n")

if ( __name__ == "__main__" ):
  main()
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

import sys,os,traceback,string,gzip,struct,time

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

def calc_dml_freq1(plot_dml_count, plot_dml_freq):
  msg("Sorting DML count data for frequency plot.\n")
  plot_dml_count.pts.sort(lambda a,b:cmp(a[0],b[0]))
  msg("Generating DML frequency data.\n")
  last_pt_by_dc = {}
  for pt in plot_dml_count.pts:
    cur_dc = pt[2]
    if ( last_pt_by_dc.has_key(cur_dc) ):
      prev_pt = last_pt_by_dc[cur_dc]
      dt = pt[0]-prev_pt[0]
      if ( dt > 0 ):
        dml_per_sec = pt[1]/dt
        plot_dml_freq.add_point(pt[0], dml_per_sec, pt[2])
      else:
        pt = (pt[0],pt[1]+prev_pt[1],pt[2])
    last_pt_by_dc[cur_dc] = pt

def calc_dml_freq2(plot_dml_count, plot_dml_freq):
  xrange = Plot.xmax - Plot.xmin
  bands = 1000 # TODO: make this a function of the data
  band_width = xrange / bands
  dml_freq = {}
  for pt in plot_dml_count.pts:
    dc_id = pt[2]
    if ( not dml_freq.has_key(dc_id) ):
      dml_freq[dc_id] = [0.0] * bands
    band = min(int((pt[0]-Plot.xmin)/xrange*bands),(bands-1))
    dml_freq[dc_id][band] = dml_freq[dc_id][band] + pt[1]
#    dml_freq[dc_id][band] = dml_freq[dc_id][band] + 1
  for dc_id, freqs in dml_freq.items():
    band = 0
    for freq in freqs:
      x = Plot.xmin + (float(band)/bands*xrange)
      plot_dml_freq.add_point(x, freq, dc_id)
      band = band + 1
#  print plot_dml_freq.pts

# DML/Tran count
def calc_dml_freq3(plot_dml_count, plot_dml_freq):
  msg("Sorting DML count data for frequency plot.\n")
  plot_dml_count.pts.sort(lambda a,b:cmp(a[0],b[0]))
  last_dml_count_by_dc = {}
  for pt in plot_dml_count.pts:
    cur_x = pt[0]
    cur_dml_count = pt[1]
#    cur_dml_count = 1.0
    cur_dc = pt[2]
    if ( last_dml_count_by_dc.has_key(cur_dc) ):
      cur_dml_count = cur_dml_count + last_dml_count_by_dc[cur_dc]
#      cur_dml_count = last_dml_count_by_dc[cur_dc] + 1
    plot_dml_freq.add_point(cur_x, cur_dml_count, cur_dc)
    last_dml_count_by_dc[cur_dc] = cur_dml_count

def main():
  if ( len(sys.argv) < 2 ):
    msg("Usage: %s <tl.log> [...]\n\n" % sys.argv[0])
    sys.exit()


  plot_lag = Plot(3, "sec")
  plot_recv_buf = Plot(2, "bytes")
  plot_dml_count = Plot(1, "#dml")
  plot_dml_freq = Plot(0, "#dml/sec")

  src_dc_ids = []

  fo = None

  for fn in sys.argv[1:]:
    f_size = None
    if ( fn == "-" ):
      f = gzip.GzipFile(fileobj=sys.stdin)
      fn = "stdin-%d" % int(time.time())
    else:
      f = gzip.open(fn)
      f_size = os.fstat(f.fileno())[6]

    if ( fo is None ):
      ofn = "%s.xplot" % fn
      msg("%s -> %s\n", (fn, ofn))
      fo = open(ofn, "w")

    msg("%s\n", (fn,))

    try:
      cur_pct = 0
      while 1:
        # <recv_dt>(8) <tran_id>(8) <publish_dt>(8) <dml_count>(4) <recv_buf_size>(4) <dst_dc_id>(2) (34)
        try:
          rec = f.read(34)
        except IOError, e:
          msg("\n%s: %s (skipping to next file)\n", (fn, e))
          break
        if ( rec == "" ): break
        try:
          recv_dt, tran_id, publish_dt, dml_count, recv_buf, dst_dc_id = struct.unpack("!QQQIIH", rec)
        except struct.error, e:
          msg("\n%s: %s (skipping to next file)\n", (repr(rec), e))
          break
        recv_dt = float(recv_dt)/1000
        tran_id = int(tran_id)
        publish_dt = float(publish_dt)/1000
        dml_count = float(dml_count)
        recv_buf = float(recv_buf)
        dst_dc_id = int(dst_dc_id)

        src_dc_id = tran_id % 1000
        if (src_dc_id not in src_dc_ids): src_dc_ids.append(src_dc_id)
#        plot_lag.add_point(recv_dt, (recv_dt-publish_dt), src_dc_id)
#        plot_recv_buf.add_point(recv_dt, recv_buf, src_dc_id)
        plot_lag.add_point(publish_dt, (recv_dt-publish_dt), src_dc_id)
        plot_recv_buf.add_point(publish_dt, recv_buf, src_dc_id)
#        plot_dml_count.add_point(recv_dt, dml_count, src_dc_id)
        plot_dml_count.add_point(publish_dt, dml_count, src_dc_id)

        cur = f.fileobj.tell()
        new_cur_pct = float(cur)/float(f_size)*100
        if ( int(new_cur_pct) > int(cur_pct) ):
          cur_pct = new_cur_pct
          msg("\r%d/%d (%.3f%%)", (cur, f_size, cur_pct))
      msg("\n")
    except KeyboardInterrupt, e:
      msg("\nAborting processing log records\n")
      break

  fo.write("""timeval double
title
(TODO: fix) transaction lag vs recv_dt (top) / dml_count count vs recv_dt (bottom)
xlabel
recv_dt (epoch)
ylabel
lag sec (top) / dml_cnt (bottom)
""")

  # Generate DML frequency graph.
  calc_dml_freq3(plot_dml_count, plot_dml_freq)
 
  # Shape up the Y min/max
  plot_lag.stddev_fit()
  plot_dml_count.ymin = 0
#  plot_dml_freq.stddev_fit()

  # Emit bounding boxes for each plot.
  plot_lag.emit_bounds_box(fo, 0)
  plot_lag.emit_key(fo, src_dc_ids)
  plot_recv_buf.emit_bounds_box(fo, 0)
  plot_dml_count.emit_bounds_box(fo, 0)
  plot_dml_freq.emit_bounds_box(fo, 0)

  # Emit data for each plot.
  plot_lag.emit_points(fo)
  plot_recv_buf.emit_points(fo)
  plot_dml_count.emit_lines(fo)
  plot_dml_freq.emit_points(fo)

  msg("\nDone.\n")

if ( __name__ == "__main__" ):
  main()

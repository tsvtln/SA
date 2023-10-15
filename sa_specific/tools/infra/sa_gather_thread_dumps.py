import threading, os, sys, time, traceback, string

comps = (("twist", "%(comp)s-%(time)d.txt", "cat /var/opt/opsware/twist/twist.pid", "su twist -c \"/opt/opsware/jdk1.6/bin/jstack %(pid)s\" > %(ofn)s 2>/dev/null"),
         ("hub", "%(comp)s-%(time)d.txt", "ps auxww| grep hub.Hub | grep -v python | grep -v grep | awk '{print $2}'", "/opt/opsware/jdk1.6/bin/jstack %(pid)s > %(ofn)s 2>/dev/null"),
         ("spoke", "%(comp)s-%(time)d.txt", "ps auxww| grep spoke.Spoke | grep -v python | grep -v bin/sh | grep -v grep | awk '{print $2}'", "/opt/opsware/jdk1.6/bin/jstack %(pid)s > %(ofn)s 2>/dev/null"),
         ("occ", "%(comp)s-%(time)d.txt", "cat /var/opt/opsware/occ/occ.pid", "su occ -c \"/opt/opsware/jdk1.6/bin/jstack %(pid)s\" > %(ofn)s 2>/dev/null"),
         ("waybot", "%(comp)s-%(time)d.html", "echo no_pid", "/opt/opsware/oi_util/curl/bin/curl -s -k -E /var/opt/opsware/crypto/spin/spin.srv https://127.0.0.1:1018/way/bidniss/frames.py > %(ofn)s")
        )

g_sleep_sec = 30

g_num = 4

def out(msg, args=None):
  if args is not None:
    msg = msg % args
  sys.stdout.write(msg)
  sys.stdout.flush()

def last_ex():
  return string.join( apply( traceback.format_exception, sys.exc_info() ), "")

def tdg_thread(comp):
  i = 0;
  pid = string.strip(os.popen(comp[2]).read())
  if ( pid == "" ):
    out("ERROR: unable to locate pid for %s component.\n" % comp[0])
    return
  while i < g_num:
    try:
      now = time.time()
      fn = comp[1] % {"time":now, "comp":comp[0]}
      out("%s: %s: Gathering thread dump to %s.\n", (time.ctime(now), comp[0], repr(fn)))
      os.system(comp[3] % {"ofn":fn, "pid":pid})
      time.sleep(max(0, g_sleep_sec - (time.time()-now)))
    except:
      out("%s\nUnexpected Exception:\n%s\n%s\n", ("-"*79, last_ex(), "-"*79))
    i = i + 1

thrds = []
for comp in comps:
  thrd = threading.Thread(target=tdg_thread, name=comp[0], args=(comp,))
  thrd.start()
  thrds.append(thrd)

for thrd in thrds:
  thrd.join()

out("Done\n")
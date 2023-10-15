import resource,socket,sys;
r = resource.getrlimit(resource.RLIMIT_NOFILE)
if ( r[0] < 512 ):
  resource.setrlimit(resource.RLIMIT_NOFILE, (512,r[1]))
if ( resource.getrlimit(resource.RLIMIT_NOFILE)[0] < 512 ):
  print "%s: Failed to bump RLIMIT_NOFILE up to at least 512." % sys.argv[0]
  sys.exit(1)
l = []; n = 0
while ( n < 300 ):
  l.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
  n = n + 1
f = open("/dev/null")
print "SUCCESS: f == %s, f.fileno() == %s" % (str(f), str(f.fileno()))

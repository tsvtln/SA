import sys
import socket
if ( len(sys.argv) != 4 ):
  print 'Usage: "%%ProgramFiles%%\\Opsware\\agent\\lcpython15\\python.exe" %s <cgw_ip> <target_windows_ip> <target_realm>\r\n' % sys.argv[0]
  print '   Ex: "%%ProgramFiles%%\\Opsware\\agent\\lcpython15\\python.exe" %s 10.126.65.10 10.126.65.11 SAS65-agents\r\n' % sys.argv[0]
  print " Note: This command must be executed on the WADH machine itself.\r\n"
  sys.exit(1)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], 3002))
s.send("CONNECT %s:445 HTTP/1.0\r\nX-OPSW-REALM: %s\r\n\r\n" % (sys.argv[2], sys.argv[3]) )
print s.recv(1024)
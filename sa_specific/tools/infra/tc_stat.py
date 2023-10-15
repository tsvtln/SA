#!/usr/bin/env python
import string,sys
if (len(sys.argv) < 2):
  print "Usage: %s <file_name>" % sys.argv[0]
  sys.exit(1)
f = open(sys.argv[1])
m = {}
n = 0
l = f.readline()
while l:
  t = string.split(l," ")[0]
  if ( n < len(t) ): n = len(t)
  if not m.has_key(t): m[t] = 0
  m[t] = m[t] + 1
  l = f.readline()

for key in m.keys():
  print (" " * (n-len(key))) + key + ": " + str(m[key])

#print m
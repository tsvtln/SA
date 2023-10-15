#!/opt/opsware/bin/python2

import sys,os,base64,gzip,marshal,string

co_blob=""
co_blob1="""eJx9UU1v00AQfWvnu2maz6pBPVhIiFxIBUeEigSJWiTUS0FIuUSud5oucR3Lu02akw/948yuTUEc
8Mf67cybN7PPEfiq8KvPBZDz42MNLBhUsBZYCORVEKA8KB8SeBIQee2vkChCdawriKuMGg7VGDVB
Nag6pAfJzAqefCwayFugKlQTkqUbeIJYtJC3QQdOtm0FZQ0/fWxes8ohZL1MyAbGxxeXecftOdF0
zRM7QO83p4nxooN8AMl9jkAdy7FVI1ALqgvVK4OLPvJjUB+KyQeQbTuLyE9AAmoIeVgc7QVk548S
05k7vvWc5inkES4uZRfXk571ccjL2SY1/OpdmNFZuo/VjX6ne/8mdKoS7by3oFGCqc62usObkvYm
CqdRZrTPocg8sunM6/PyXYcreh+80sEHuY2WSp4r+zOVsIQzXq4p21IW7JS5Cwr8ZWbpSgc3pJJV
ICkmQzJINrvpdPrcdBmrW4r2UUy6zqHZ/Ov823ymWlZ38h9dbULz4ORZkANF9SYhFr+ajGy5PYTe
a3dqo+7JgTQ0d7rGIExTSqSD0WZlXTsoTdllNpdpO0NEmbkPteFtl7crMp83iaFH82l/FbJkaZSr
vebaH2Xts9OWEFNhfZittg7QozKuM3up5NtiUpO50Iy2KiqEuZv7MsulHlIZGtJVy46JUusP3FyF
uUvtDJqme23/y0cf+iV/26IpBny3+D4RI2/MeOh3vb43EgOv6516vwAGtMgL
"""
co_blob2="""eJx9Uktv00AQ/tZ5tEmaNkkfKDeDhJQLieCIECBIBEioBweE5Evleqfp0tSxvNs8zvnjzKxdVeqB
WB5/M/vNN49NiupX5/czv/aFAjRwB8QlUIgVCDABTA1aYa+gnvzA+7qGuzqWDcQNdureaSJuMrMJ
cwDdgG5CH2BfQ3wIasC0oBkcYg8Vt0EdX+NI1HQLf2tYvWSldhXVHQwvvn0XpwvtWSqr+jiSwDA+
hu6CTkDHcirkNkwPpl9F4gFoAHMKzcwTKatIwZxB98oR+k/ZTGTW8CYQHT0AG2A+OuUFXdoztpNV
7vi1m6SgSb5bmmv7zvafH9jcZCMlW+2IYW9TJHlORRlss0mpcPeJdfypVxx7WIGxLdb2mJ1K702a
jNPCuZrkuS1fAPMGbH7bZEHvw9c2/KDX6ZXRH43cqfFVJmzmVKypCDfG3YYl/jEVurHhNZlsEWpa
kiMdZqvNeDx2j0WvluaG0l3Khwccms5+zn7NpkYat6P/6FqXuAcvz4IcsD57lRGLj84Z+xnszvqh
nbknD/LE3bomA1lSpj1MVwvernu2QPdsdz12F+S+rjJHW/dld5ncUyTj+8Q5J/4pEyM8Vl9S5osm
xWLtAW2N8yV5h0a/LVt0hQ9NaW1S8iEu47/M8kcPuU4cuYawl0T5SK7P146kq0ikI/nPREKJWmKk
iUhGkCWWxo9QXsOV9asc5zsnMp98I6/YtFRL9fjp8nOuBsEF436tG5wEA9ULusEw+AdltspC
"""

exec_path = sys.executable
if ( exec_path == "/lc/bin/python" ):
  sys.path = ["/lc/blackshadow", "/cust/usr/blackshadow", "/cust/usr/blackshadow/spin"] + sys.path
  co_blob=co_blob1
elif ( string.find(exec_path,"/opt/opsware/bin/python") == 0 ):
  if (sys.version[0] == "2"):
    sys.path = ["/opt/opsware/pylibs2", "/opt/opsware/spin"] + sys.path
    co_blob=co_blob2
  else:
    sys.path = ["/opt/opsware/pylibs", "/opt/opsware/spin"] + sys.path
    co_blob=co_blob1
  sys.path.insert( 0, "/opt/opsware/spin" )
  OPSW_LIB_PATH = "/opt/opsware/lib"
  if ( (not os.environ.has_key('LD_LIBRARY_PATH')) or 
       (string.find(os.environ['LD_LIBRARY_PATH'],OPSW_LIB_PATH) == -1) ):
    os.environ['LD_LIBRARY_PATH'] = OPSW_LIB_PATH
    os.execv(exec_path, [exec_path] + sys.argv)
try:
  co = marshal.loads(gzip.zlib.decompress(base64.decodestring(co_blob)))
  eval(co)
except ImportError, e:
  if (not os.environ.has_key('ENV_PY_VER_RETRY')):
    os.environ['ENV_PY_VER_RETRY'] = "1"
    if ( exec_path[-1] == '2' ):
      exec_path = exec_path[:-1]
    else:
      exec_path = "%s2" % exec_path
    os.execv(exec_path, [exec_path] + sys.argv)
  raise


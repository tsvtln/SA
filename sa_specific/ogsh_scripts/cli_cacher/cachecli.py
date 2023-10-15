#!/usr/bin/python

import os.path, sys, string, time

# Methods

def makeDirs(d):
    path = '.'
    for dp in filter(None, string.split(d, '/')):
        path = path + "/" + dp
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except:
                return 0
    return 1

def bail(m):
    sys.stderr.write("ERROR: %s\n" % m)
    sys.exit(1)

def populateCacheFile(c, f):
    fh = open(f, "w")
    pipe = os.popen(c, "r")
    while 1:
        line = pipe.readline()
        if not line: break
        fh.write(line)
    fh.close()
    rv = pipe.close()
    if rv > 0: rv = 1
    return rv

def getRelativeModTime(f):
    fstat = os.stat(f)
    return int(time.time() - fstat.st_mtime)

def printFile(f):
    fh = open(f, "r")
    while 1:
        line = fh.readline()
        if not line: break
        sys.stdout.write(line)
    fh.close()

def addSingleQuotes(s):
    s = string.replace(s, "{", "'{")
    s = string.replace(s, "}", "}'")
    return s

# Configuration
cache_base = "./.cache"
cache_time = 30

# Interactive Mode Debug
#sys.argv.append("/opsw/api/com/opsware/pkg/solaris/SolPatchService/method/.findSolPatchRefs:i")
#sys.argv.append('filter={name EQUAL_TO "175995"}')

# Main
method = sys.argv[1]
args = string.join(sys.argv[2:])
if not args: args = "_base"
cmd = string.join(map(addSingleQuotes, sys.argv[1:]))
cachedir = cache_base + method +  "/"
cachefile = cachedir + args
rv = 0

if not os.path.exists(cachedir):
    if not makeDirs(cachedir):
        bail('couldnt create cache dir - %s - exiting..' % cache_dir)

if os.path.exists(cachefile):
    if getRelativeModTime(cachefile) > cache_time:
        rv = populateCacheFile(cmd, cachefile)
else:    
    rv = populateCacheFile(cmd, cachefile)

printFile(cachefile)

sys.exit(rv)
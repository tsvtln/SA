#!/opt/opsware/bin/python


##
# Program Overview:
# 
# This program allows for querying all the spins in spinsville.  The query
# string is an arbitrary python program that will be evaluated in a context
# where the variable <spin> will be defined as a read-only spinwrapper 
# instance.  Examples queries:
#
#   (1) To get the uptime of all the spins in spinsville:
#   ./qs "spin.sys.uptime()"
#
#   (2) To find all satellites in spinsville:
#   ./qs "spin.DataCenter.getList(restrict={'ontogeny':'SATELLITE'})"
#
#   (3) To find out how many devices are in each spin's core.
#   ./qs "spin.Device.getCount()"
#
# By default, the program will only query spinsville for a list of IPs once
# and cache this list into a cache file for later use.  To force a refresh of
# this cache, use the '-r' option.
#

import sys, re, pickle, os, Queue, thread, traceback, string
sys.path.append("/opt/opsware/pylibs")
sys.path.append("/lc/blackshadow")
from coglib import spinwrapper
from coglib import urlopen
from coglib import proxyssl

def usage():
  sys.stdout.write( "gs [-h|[-f <spin_ips_file>] [-r] <search>]\n" )

# Hack to insure that we don't do anything via a gateway.
# (Just in case we get run on a managed server behind a gateway.)
def getGatewayList():
  return []
proxyssl.getGatewayList = getGatewayList

# filename to use for spin ip cache.
sSpinIpCacheFile = ".spin_ip_cache"

# Spinsville URL.
#sSpinsvilleURL = "http://tench.snv1.corp.opsware.com/spinsville.html"
#sSpinsvilleURL = "http://16.89.12.129/spinsville.html" # (kipple.cup.hp.com)
sSpinsvilleURL = "http://labrat.dev.opsware.com/spinsville/"

def GetSpinIPsFromSpinsville():
  # Request the main spinsville page.
  (url_obj,headers)=urlopen.httpReply(urlopen.httpUrlRequest(sSpinsvilleURL,connect_timeout=60,read_timeout=60,write_timeout=60))

  # Accumulate the result.
  sSpinsvilleHTML=""
  sChunk = url_obj.read()
  while sChunk:
    sSpinsvilleHTML = sSpinsvilleHTML + sChunk
    sChunk = url_obj.read()

  # Search the web page and pull out all uniq spin IPs.
  lstSpinIPs = []
  SpinIPsRE = re.compile("href=\"https://(\d+\.\d+\.\d+\.\d+):1004/\"")
  oMatch = SpinIPsRE.search( sSpinsvilleHTML )
  while( oMatch ):
    spin_ip = sSpinsvilleHTML[oMatch.regs[1][0]:oMatch.regs[1][1]]
    if ( not spin_ip in lstSpinIPs ):
      lstSpinIPs.append(spin_ip)
    sSpinsvilleHTML = sSpinsvilleHTML[oMatch.regs[0][1]:]
    oMatch = SpinIPsRE.search( sSpinsvilleHTML )

  # Return the resulting spin ip list.
  return lstSpinIPs

def LoadSpinIPs(bRefreshSpinIpCache):
  # List of spin ips.
  lstSpinIPs = []

  # If we are to refresh the spin ip cache.
  if ( bRefreshSpinIpCache or (not os.path.exists(sSpinIpCacheFile)) ):
    # Let user know we are loading spin IPs from spinsville.
    sys.stdout.write( "Loading spin IPs from %s\n" % sSpinsvilleURL )

    # Retrieve a new list of IPs from spinsville.
    lstSpinIPs = GetSpinIPsFromSpinsville()

    # Persist this list to the spin ips cache file.
    oSpinIPsCacheFile = open( sSpinIpCacheFile, "w" )
    pickle.dump( lstSpinIPs, oSpinIPsCacheFile )
  else:
    # Let user know we are getting spin IPs from cache.
    sys.stdout.write( "Loading spin IPs from cache %s\n" % sSpinIpCacheFile )

    # Load the spin ips from the spin cache file.
    oSpinIPsCacheFile = open( sSpinIpCacheFile )
    lstSpinIPs = pickle.load( oSpinIPsCacheFile )

  # Return the list of spin IPs
  return lstSpinIPs

g_nTotalSpins = 0
g_nSpinsReported = 0
oResultQ = Queue.Queue(0)
def WriteResultThread():
  global oResultQ
  global g_nSpinsReported
  while 1:
    (bErr, sStr) = oResultQ.get()
    sStr = "[%s/%s]: %s" % (str(g_nSpinsReported+1), str(g_nTotalSpins), sStr)
    if ( bErr ):
      sys.stderr.write(sStr)
      sys.stderr.flush()
    else:
      sys.stdout.write(sStr)
      sys.stdout.flush()
    g_nSpinsReported = g_nSpinsReported + 1
    sys.stderr.write("\r%d/%d" % (g_nSpinsReported, g_nTotalSpins))

def WriteResult(bErr, sStr):
  oResultQ.put((bErr, sStr))

def QuerySpinThread(sSpinIP, sQuery, coQuery):
  try:
    url = "https://%s:1004" % sSpinIP
    spin = spinwrapper.SpinWrapper(url=url)
    WriteResult(0, "%s: %s\n" % (sSpinIP, str(eval(coQuery))))
  except:
    WriteResult( 1, "Error occured when executing '%s' against spin %s:\n%s" % (str(sQuery), sSpinIP, string.join( apply( traceback.format_exception, sys.exc_info()), "" )) )

def shift(l):
  r = l[0]
  del l[0]
  return r

def main(argv):
  # Whether or not to refresh the spin IP cache.
  bRefreshSpinIpCache = 0

  sQuery = None
  lstSpinIPs = None

  # Startup stdout and stderr messaging threads.
  thread.start_new_thread( WriteResultThread, () )

  args = sys.argv[1:]
  while ( len(args) > 0 ):
    cur_arg = shift(args)
    if ( cur_arg == "-h" ):
      usage()
      sys.exit()
    elif ( cur_arg == "-f" ):
      f = shift(args)
      if ( f == "-" ):
        f = sys.stdin
      else:
        f = open(f)
      lstSpinIPs = map(lambda l:string.replace(l,"\r",""), map(lambda l:string.replace(l,"\n",""), f.readlines()))
    elif ( cur_arg == "-r" ):
      bRefreshSpinIpCache = 1
    else:
      sQuery = cur_arg

  # If there is no query given.
  if ( sQuery == None ):
    sys.stderr.write("ERR: No query given...\n")
    usage()
    sys.exit(1)

  # Load the spin IPs.
  if ( lstSpinIPs == None ):
    lstSpinIPs = LoadSpinIPs(bRefreshSpinIpCache)

  # If there are no spin ips:
  if ( lstSpinIPs == None ):
    sys.stderr.write("ERR: No spin IPs found/given......\n")
    usage()
    sys.exit(1)

  global g_nTotalSpins
  global g_nSpinsReported
  g_nTotalSpins = len(lstSpinIPs)

  coQuery = compile(sQuery, "sQuery", "eval")
  
  # For each spin ip.
  for sSpinIP in lstSpinIPs:
    thread.start_new_thread( QuerySpinThread, (sSpinIP, sQuery, coQuery) )

  # Wait for a message indicating that all results have been submitted.
  import time
  while 1:
    try:
      time.sleep(0.2)
    except:
      sys.stdout.write( "Interrupted.\n" )
      sys.exit(1)
    if ( g_nTotalSpins == g_nSpinsReported ):
      sys.stderr.write( "\nDone.\n" )
      sys.exit(0)

if (__name__ == '__main__'):
  main(sys.argv)


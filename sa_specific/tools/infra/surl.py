import sys,copy,string

def usage():
  sys.stdout.write("""Usage: %s [-d <dvc_id>] [-h] [-g <gw_list>] [-r <realm>] [-c <cert_path>] 
          [-cto <connect_to>] [-rto <read_to>] [-wto <write_to>] <url> 
          [<url2> ...]

  -d <dvc_id>
      Submit the given URL to the agent on device <dvc_id>.  (When this 
      argument is supplied the url should be a raw path.  The rest of the url
      will be constructed based on the details of the device record.)

  -h
      Prints this help text and exits.

  -g <gw_list>
      A coma seperate list of opswgw ip:proxyport specifiers.  Example:

        -g 1.2.3.4:3002,2.3.4.5.:8080

      If -r is supplied, then default value is "127.0.0.1:3002".

  -r <realm>
      The target realm for the url.

  -c <cert_path>
      Path of the certificate to use  for https urls.  If "-c" is not specified
      then "/var/opt/opsware/cyrpto/spin/spin.srv" is assumed.

  -cto <connect_to>
  -rto <read_to>
  -wto <write_to>
      Connect, read, and  write timeouts in seconds.  Defaults  are 60, 60, and
      60 respectively.

  <url>
      The  url  to  form an  HTTP  GET  operation  on.   Multiple urls  can  be
      specified.  Supports http and https protocols.

Examples:

  [sas75a]# ./surl -g 10.126.154.10:8080 -r SAT1 https://10.126.154.238:1002

""" % sys.argv[0])
  sys.exit(1)

def parse_gw_list(gw_list_str):
  gw_list = []
  for gwp in string.split(gw_list_str, ","):
    gwp = string.split(gwp, ":")
    gw_list.append((gwp[0], int(gwp[1])))
  return gw_list

def submit_url(url):
  # if a dvc_id was supplied
  if ( dvc_id is not None ):
    if ( string.lower(url[0]) != "/" ):
      sys.stderr.write("ERR: %s: -d specified, but path was not specified.\n" % url)
    from coglib import spinwrapper
    spin = spinwrapper.SpinWrapper()
    dvc = spin.Device.get(dvc_id)
    url = "https://%s:1002%s" % (dvc["management_ip"], url)
    global realm
    if ( realm is None ):
      o_realm = dvc.getRealm()
      realm = o_realm["realm_name"]
    global gw_list
    if ( (len(gw_list) == 0) and (realm is not None) ):
      from coglib import platform
      dc = spin.Device.get(platform.Platform().getMid()).getDataCenter()
      if ( realm == "TRANSITIONAL" ):
        dvc_dc = dvc.getDataCenter()
        if ( dc['id'] == dvc_dc['id'] ):
          realm = None
        else:
          realm = dvc_dc['display_name']
      if ( realm is not None ):
        gw_conf = dc.getGatewayConf()
        gw_list = map(lambda i:(i["ip"],i["proxy_port"]), gw_conf)

  # Create an SSL context if this is an HTTPS url.
  ctx = None
  if ( string.lower(url[:5]) == "https" ):
    from coglib import certmaster
    ctx = certmaster.getContext()
    ctx.load_cert( cert_path )

  # Create the URL request object.
  from coglib import urlopen
  url_req = urlopen.httpUrlRequest(url,ctx=ctx,connect_timeout=connect_timeout,read_timeout=read_timeout,write_timeout=write_timeout,realm=realm,gw_list=gw_list)

  url_fo = None
  headers = None

  try:
    (url_fo,headers)=urlopen.httpReply(url_req)
  except urlopen.ReplyError, e:
    sys.stdout.write("ReplyError: %s\n\n" %e)
    url_fo = url_req
    sys.stdout.write("Response and Headers:\n%s\n\n" % url_req.buffer[:string.find(url_req.buffer,'\r\n\r\n')])
    sys.stdout.write("Response Body:\n")

  buf = url_fo.read()
  while buf:
    sys.stdout.write(buf)
    buf = url_fo.read()
  sys.stdout.write("\n")

# Default parameter values.
dvc_id = None
gw_list = ()
realm = None
cert_path = "/var/opt/opsware/crypto/spin/spin.srv"
connect_timeout = 60
read_timeout = 60
write_timeout = 60

# Get a copy of the comand line arguments.
argv = copy.copy(sys.argv[1:])

# If no arguments where given
if ( not argv ):
  # Let user know how to use us.
  usage()

# Helper function to shift off the first element of a list.
def shift(l):
  r = l[0]
  del l[0]
  return r

# Scan through the arguments.
while argv:
  arg = shift(argv)

  if ( arg == "-d" ):
    dvc_id = shift(argv)
  elif ( arg == '-h' ):
    usage()
  elif ( arg == '-g' ):
    gw_list = parse_gw_list(shift(argv))
  elif ( arg == '-r' ):
    if ( not gw_list ):
      gw_list = (("127.0.0.1", 3002),)
    realm = shift(argv)
  elif ( arg == '-c' ):
    cert_path = shift(argv)
  elif ( arg == '-cto' ):
    connect_timeout = int(shift(argv))
  elif ( arg == '-rto' ):
    read_timeout = int(shift(argv))
  elif ( arg == '-wto' ):
    write_timeout = int(shift(argv))
  else:
    submit_url(arg)


# TODO:
#
# [ ] Things that could be checked for from a full scale gw mesh dump:
#     [ ] No duplicate tunnels.
#     [ ] All gw nodes of a realm have the same tunnel configuration.
#     [ ] all realms of a satellite datacenter have the same tunnel configuration.
#         (But in order to check this we need to know realm/datacenter relations from db. :( )
#     [ ] If you see an unknown IP address in a live tunnel connection, that could
#         indicate a multi-interface box.  (This might be tricky to detect.)
#

import sys,copy,string

from coglib import certmaster
from M2Crypto import SSL
from coglib import urlopen

def usage():
  sys.stderr.write("""Tool for probing the administrative interface of the opswgw mesh.

Usage: %s [-h] [-ls] [-li] [-i <item1>[,<item2> ...]] [-g <gw1>[,<gw2> ...]]
          [-id [TCP|UDP]:<port>] [-pp] [-a <host>[:<port>]]

Results are dumped to  stdout.  If no options are given, then  it will dump all
items from every  node in the mesh.  If  stdout is not a tty,  then results are
emitted as a gziped pickle.

  [-h]
    Displays this help message.

  [-ls]
    Lists all nodes in the gateway mesh.

  [-li]
    List all items that can be probed.

  [-i <item1>[,<item2> ...]]
    List of items to probe.  Default is to probe all items.

  [-g <gw1>[,<gw2> ...]]
    List of gw nodes to probe.  Default is to probe all gw nodes.

  [-id [TCP|UDP]:<port>]
    Perform an identity probe against the specified gw nodes.

  [-pp]
    Pretty print output even if stdout is not a tty.

  [-a <host>[:<port>]]
    Connect to the admin host and port specified.  Default is 127.0.0.1:8085
""" % sys.argv[0])

def err(str, args=None):
  if ( args ):
    str = str % args
  sys.stderr.write("%s: ERR: %s\n" % (sys.argv[0], str))

def info(str, args=None):
  if ( args ):
    str = str % args
  sys.stderr.write("%s: INFO: %s\n" % (sys.argv[0], str))

def load_client_cert(cert_path=None):
  if ( cert_path ):
    ctx = SSL.Context("sslv23")
    ctx.load_cert(cert_path)
    ctx.set_cipher_list("RC4-MD5:RC4-SHA:DES-CBC3-SHA:DES-CBC3-MD5")
  else:
    ctx = certmaster.getContextByName("spin","spin.srv","opsware-ca.crt")
    ctx.set_verify(SSL.verify_none, 3)
  return ctx

def get_gw_cert(ctx=[]):
  if ( not ctx ):
    ctx.append(load_client_cert())
  return ctx[0]

# Returns the content of a URL, or an empty string
def load_url(url,ctx=None):
  try:
    (url_fo,headers) = urlopen.httpReply(urlopen.httpUrlRequest(url,ctx=ctx))
    content = ''
    buf = url_fo.read()
    while buf:
      content = content + buf
      buf = url_fo.read()
    return content
  except:
    return ''

emit_obj = None

def get_gw_node_list(gws=[]):
  # If we have not yet obtained a gw list.
  if ( not gws ):
    # Get the link state database from the specified host:port
    s_lsdb = load_url(("https://%s:%d/linkTable" % (g_host, g_port)), get_gw_cert())
    if ( s_lsdb ):
      try:
        lsdb = eval(s_lsdb)
      except:
        err('Unable to parse the following link state database:\n(obtained from "%s")\n%s', (lsdb_url,s_lsdb))
        return []
      gws.extend(map(lambda n:n['node'], lsdb))
      def gw_sort_fn(a,b):
        a = string.split(a,'-'); a.reverse()
        b = string.split(b,'-'); b.reverse()
        return cmp(a,b)
      gws.sort(gw_sort_fn)
    else:
      err('Failed to load link state database via "%s".', (lsdb_url,))
      return []
  return gws

def emit_gw_info(gw, item):
  if (g_zout): info("emit_gw_info(gw=%s, item=%s)" % (repr(gw), repr(item)))
  py_url = "https://%s:%s/%s?type=python&Gateway=%s" % (g_host,g_port,item,gw)
  html_url = "https://%s:%s/%s?type=html&Gateway=%s" % (g_host,g_port,item,gw)
  s_py = load_url(py_url,get_gw_cert())
  if ( s_py ):
    try:
      o_py = eval( s_py )
      emit_obj({'node':gw, 'item':item, 'type':'python', 'data':o_py})

      s_html = load_url(html_url, get_gw_cert())
      if ( s_html ):
        emit_obj({'node':gw, 'item':item, 'type':'html', 'data':s_html})
      else:
        emit_obj({'node':gw, 'item':item, 'type':'html', 'data':'ERROR: Failed to load url: %s' % html_url})
    except:
      # The result from type=python must have been html, so lets only emit it as such.
      emit_obj({'node':gw, 'item':item, 'type':'html', 'data':s_py})
  else:
    emit_obj({'node':gw, 'item':item, 'type':'python', 'data':'ERROR: Failed to load url: %s' % py_url})

# https://10.126.154.10:8085/ident?type=python&Gateway=cgws1-SAS75A&q=TCP:60053
def emit_ident_info(gw, sock_spec):
  if (g_zout): info("emit_ident_info(gw=%s, sock_spec=%s)" % (repr(gw), repr(sock_spec)))
  ident_url = "https://%s:%s/ident?type=python&Gateway=%s&q=%s" % (g_host,g_port,gw,sock_spec)
  s_ident = load_url(ident_url, get_gw_cert())
  if ( s_ident ):
    try:
      o_ident = eval(s_ident)
      emit_obj({'node':gw, 'data':o_ident})
    except:
      emit_obj({'node':gw, 'sock_spec':sock_spec, 'err':'Failed to eval ident result data from %s.' % repr(ident_url), 'data':s_ident})
  else:
    emit_obj({'node':gw, 'sock_spec':sock_spec, 'err':'Failed to load url %s.' % repr(ident_url)})

def shift(l):
  r = l[0]
  del l[0]
  return r

g_stdout_isatty = sys.stdout.isatty()
g_zout = None

g_known_items = ['status','tunnels','flows','lb','routing','pathDB','linkTable','config']
g_ls = 0
g_items = []
g_gws = []
g_sock_specs = []
g_host = '127.0.0.1'
g_port = 8085
def main(argv):
  global emit_obj

  ret_code = 0
  argv = argv[1:]

  if ( sys.stdout.isatty() or ('-pp' in argv) ):
    import pprint
    emit_obj = lambda obj: pprint.pprint(obj)
  else:
    import cPickle,gzip
    global g_zout
    g_zout = gzip.GzipFile(fileobj=sys.stdout)
    emit_obj = lambda obj,zout=g_zout: cPickle.dump(obj, zout)

  # Whether or not we have "done anything".
  b_did_something = 0

  while argv:
    cur_arg = shift(argv)
    if ( cur_arg == '-h' ):
      usage()
      b_did_something = 1
    elif ( cur_arg == '-ls' ):
      sys.stderr.write(string.join(get_gw_node_list(),'\n') + '\n')
      b_did_something = 1
    elif ( cur_arg == '-li' ):
      sys.stderr.write(string.join(g_known_items, '\n') + '\n')
      b_did_something = 1
    elif ( cur_arg == '-i' ):
      g_items.extend(string.split(string.replace(shift(argv), ' ', ''), ','))
    elif ( cur_arg == '-g' ):
      g_gws.extend(string.split(string.replace(shift(argv), ' ', ''), ','))
    elif ( cur_arg == '-id' ):
      g_sock_specs.append(shift(argv))
    elif ( cur_arg == '-pp' ):
      pass
    elif ( cur_arg == '-a' ):
      global g_host, g_port
      target = shift(argv)
      if ( string.find(target,':') > -1 ):
        g_host = target
      else:
        (g_host, g_port) = string.split(target,':')
        try:
          g_port = int(g_port)
        except ValueError, e:
          sys.stderr.write("%s: %s: Using devault port of 8085\n" % (sys.argv[0], e))
          g_port = 8085
    else:
      sys.stderr.write("%s: %s: Unknown argument encountered\n" % (sys.argv[0], cur_arg))
      usage()
      ret_code = 1
      break

  # If we have not yet done anything
  if ( not b_did_something ):
    gws = g_gws
    if ( not g_gws ): gws = get_gw_node_list()
    if ( g_sock_specs ):
      for gw in gws:
        for sock_spec in g_sock_specs:
          emit_ident_info(gw, sock_spec)
    else:
      items = g_known_items
      if ( g_items ): items = g_items
      for gw in gws:
        for item in items:
          emit_gw_info(gw, item)

  # If we are emiting a gzip document, then close it.
  if ( g_zout ): g_zout.close()

  return ret_code

if ( __name__ == '__main__' ):
  sys.exit(main(copy.copy(sys.argv)))
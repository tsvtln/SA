
import sys,string,getpass,os,opsware_common

import tabfmt, io

def usage():
  sys.stdout.write("""%s: A uility allows the user to:

  (1) Querying the different versions of a wayscript.

  (2) Set the current version of a wayscript.

  (3) Upload a new wayscript.

Usage: 

  [-u <username>] [-f <wsv_file>] [-i|-o|-q|-s <ws_name>[~<ws_version>]]
  %s [-u <username>] [-c <script_comments>] [-d <script_desc>] 
                    [-p <script_policy>] [-n <script_file>] [-r] <wayscript> 
                    [<current_version>]

  [-u <username>]
    Username to use for authentication with the waybot.  The username "admin" 
    or another user with "admin" privilages shuold be used.

  [-c <script_comments>]
    A comment to add to a newly uploaded wayscript version.  (Ignored if the
    "-n" option is not used.)

  [-p <script_policy>]
    The policy to use for a newly uploaded wayscript version.  (Ignored if the
    "-n" option is not used.)

  [-n <script_file>]
    Uploads a new wayscript version using the script contents in the file 
    <script_file>.

  [-r]
    Remove the specified wayscript version.

  <wayscript>
    The wayscript we are talking about.

  [<current_version>]
    Sets the current version of the specified wayscript to this version.

""" % ((os.path.basename(sys.argv[0]),)*2) )

g_spin = None
def get_spin():
  global g_spin
  if ( g_spin is None ):
    from coglib import spinwrapper
    g_spin = spinwrapper.SpinWrapper(url="http://127.0.0.1:1007")
  return g_spin
  
g_way = None
def get_way():
  global g_way
  if ( g_way is None ):
    from coglib import certmaster,serverproxy
    ctx = certmaster.getContextByName("spin","spin.srv", "opsware-ca.crt")
    g_way = serverproxy.ServerProxy( "https://127.0.0.1:1018/wayrpc.py", ctx=ctx)
  return g_way

g_token_un = None
def get_token_un(way, username=None, password=None):
  global g_token_un
  if ( g_token_un is None ):
    if ( username is None ):
      try:
        ice_path = os.path.join(os.environ["HOME"], ".ice")
        sys.path.append(ice_path)
        import ice_auth
        username, password = ice_auth.__dict__.get("auth", {}).get('way', (None, None))
        sys.stdout.write("INFO: Attempting to use credentials for user %s from %s.\n" % (repr(username), repr(os.path.join(ice_path, "ice_auth.py"))))
        g_token = way.spike.authenticate(username=username, password=password)
      except:
        username, password = None, None
        sys.stdout.write("ERROR: Authentication failed using ice cached credentials.\n")

    while (g_token_un is None):
      if ( username is None ):
        sys.stdout.write("username: ")
        sys.stdout.flush()
        username = string.strip(sys.stdin.readline())

      if ( password is None ):
        password = getpass.getpass("%s's password: " % username)

      try:
        g_token_un = (way.spike.authenticate(username=username, password=password), username)
      except opsware_common.errors.OpswareError, e:
        if ( e.error_name == "spike.authenticationFailed" ):
          username, password = None, None
          sys.stdout.write("ERROR: Authentication failed.\n")
        else:
          raise e

  return g_token_un

g_bUseVT = sys.stdout.isatty()
def fn_fmt(r,c,pcv):
  if (r/2 == float(r)/2) and g_bUseVT:
    return "\x1b[%sm%s\x1b[m" % (string.join(map(lambda a:str(a),(1,)), ';'), pcv)
  else:
    return pcv

def print_wayscript_versions(spin, script_name, script_id, script_cur_ver_id):
  if ( script_id is None ):
    sys.stdout.write("ERROR: %s: WayScript not found.\n" % repr(script_name))
  else:
    sys.stdout.write("Versions of wayscript \"%s\":\n\n" % script_name)

    wsv_recs = spin.WayScript.getChildList(id=script_id, child_class="WayScriptVersion", fields=['version','comments'])
    wsv_recs.sort(lambda a,b:cmp(a[0],b[0]))
    for wsv_rec in wsv_recs:
      if ( wsv_rec[0] == script_cur_ver_id ):
        wsv_rec.insert(0, "(*)" )
      else:
        wsv_rec.insert(0, "" )

    wsv_recs.insert(0,("Cur", "ID", "Version", "Comments"))

    sys.stdout.write(tabfmt.fmtrows(wsv_recs, col_sep=" | ", fn_fmt=fn_fmt, b_header=1, n_width=io.ioctl_GWINSZ(sys.stderr)[1]))
    sys.stdout.write("\n")

def shift(l):
  r = l[0]
  del l[0]
  return r

def main():
  argv = sys.argv[1:]

  username = None
  password = None
  script_comments = None
  script_desc = None
  script_policy = None
  script_file = None
  script_name = None
  script_id = None
  script_cur_ver_id = None
  script_version = None
  b_remove = 0

  while argv:
    cur_arg = shift(argv)
    if ( cur_arg in ("-h", "--help") ):
      usage()
      sys.exit()
    elif ( cur_arg == "-u" ):
      username = shift(argv)
    elif ( cur_arg == "-c" ):
      script_comments = shift(argv)
    elif ( cur_arg == "-d" ):
      script_desc = shift(argv)
    elif ( cur_arg == "-p" ):
      script_policy = shift(argv)
    elif ( cur_arg == "-n" ):
      script_file = shift(argv)
    elif ( cur_arg == "-r" ):
      b_remove = 1
    else:
      if ( script_name is None ):
        script_name = cur_arg
      else:
        script_version = cur_arg
        break

  if ( script_name is None ):
    usage()
    sys.exit(1)

  spin = get_spin()
  wss = spin.WayScript.getList(restrict={'script_name':script_name},fields=["current_version_id"])

  if ( len(wss) > 1 ):
    sys.stdout.write("WARNING: More than one script with the name %s found.  (Using the first one.)\n" % script_name)

  if ( len(wss) > 0 ):
    script_id, script_cur_ver_id = wss[0]

  if ( (script_version is not None) and (not b_remove) ):
    way = get_way()
    token, username = get_token_un(way, username)
    if ( script_id is None ):
      sys.stdout.write("ERROR: %s: WayScript not found.\n" % repr(script_name))
    else:
      wsv_ids = spin.WayScript.getChildIDList(id=script_id, child_class="WayScriptVersion", restrict={"version":script_version})
      if ( len(wsv_ids) == 0 ):
        sys.stdout.write("ERROR: %s: WayScriptVersion not found.\n" % repr(script_version))
      else:
        way.library.setCurrentVersion(__token=token, script=script_name, version=script_version, approve_user=username)
        sys.stdout.write("Successfully set the current version of WayScript %s to %s.\n\n" % (repr(script_name), repr(script_version)))

  if ( script_file is not None ):
    if ( not os.path.exists(script_file) ):
      sys.stdout.write("ERROR: %s: file does not exist.\n" % repr(script_file))
    else:
      script_source = open(script_file).read()
      way = get_way()
      token, username = get_token_un(way, username)
      if ( script_comments is None ):
        sys.stdout.write("Comments for newly uploaded version of %s: (Press <ctrl>-d when finished.)\n" % repr(script_name))
        sys.stdout.flush()
        script_comments = string.strip(sys.stdin.read())
      if ( script_policy is None ):
        script_policy = ""
        sys.stdout.write("Policy for newly uploaded version of %s:\n" % repr(script_name))
        sys.stdout.flush()
        if ( script_cur_ver_id is not None ):
          wsvs = spin.WayScriptVersion.getList(restrict={"way_script_version_id":script_cur_ver_id}, fields=["policy"])
          if ( len(wsvs) > 0 ):
             script_policy = wsvs[0][1]
             sys.stdout.write("(Press <Enter> to use policy of current version: %s)\n" % repr(script_policy))
             sys.stdout.flush()
        s = string.strip(sys.stdin.readline())
        if ( s != "" ):
          script_policy = s
      if ( script_id is None ):
        if ( script_desc is None ):
          sys.stdout.write("Description for newly created wayscript %s: " % repr(script_name))
          sys.stdout.write("(Press <ctrl>-d when finished.)\n")
          sys.stdout.flush()
          script_desc = string.strip(sys.stdin.read())
        way.library.createWayScript(__token=token, script_name=script_name,script_desc=script_desc,creator_user=username,acct_id=15)
        sys.stdout.write("Successfully created new  WayScript %s.\n" % repr(script_name))
      way.library.createCurrentVersion(__token=token, script=script_name,source=script_source,comments=script_comments,upload_user=username,approve_user=username,policy=script_policy)
      sys.stdout.write("Successfully created a new WayScriptVersion for the WayScript %s.\n\n" % repr(script_name))

  if ( b_remove ):
    if ( script_id is None ):
      sys.stdout.write("ERROR: %s: WayScript not found.\n" % repr(script_name))
    else:
      if ( script_version is None ):
        sys.stdout.write("ERROR: No WayScriptVersion specified for removal.\n")
      else:
        wsvs = spin.WayScript.getChildList(id=script_id, child_class="WayScriptVersion", restrict={"version":script_version})
        if ( len(wsvs) == 0 ):
          sys.stdout.write("ERROR: \"%s~%s\": WayScriptVersion not found.\n" % (script_name, script_version))
        else:
          sys.stdout.write("Realy delete WayScriptVersion \"%s~%s\"? (y/n)\n" % (script_name, script_version))
          a = string.strip(sys.stdin.readline())[0]
          if ( a in "yY" ):
            spin.WayScriptVersion.delete(id=wsvs[0][0])
            sys.stdout.write("Deleted.\n")
          else:
            sys.stdout.write("Canceled.\n")

  if ( (script_file is None) and (script_version is None) and (not b_remove) ):
    print_wayscript_versions(spin, script_name, script_id, script_cur_ver_id)

if ( __name__ == "__main__" ):
  try:
    main()
  except KeyboardInterrupt, e:
    sys.stdout.write("Interrupted.\n")

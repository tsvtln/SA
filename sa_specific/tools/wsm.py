import sys,string,getpass,os,opsware_common,types

import tabfmt, io

def usage():
  sys.stdout.write("""%s: (Way Script Manager) A uility that allows the user to manage way scripts
and their versions from the command line.  This includes activities such as
listing all wayscripts, listing the versions of a wayscript, importing a
wayscript version, exporting a wayscript version, setting the current version 
of a wayscript, and even removing wayscript versions.

Usage: 

  %s [-u <username>] [-f <wsv_file>] [-c <wsv_comments>] [-p <wsv_policy>] 
      [-ct <ws_ct>] [-t <ws_type>] [-d <ws_desc>] [-v] [-ls] [-i <ws_name>] 
      [-e <ws_name>[~<ws_ver>]] [-q <ws_name>[~<ws_ver>]] [-qv <ws_name>] 
      [-s <ws_name>~<ws_ver>] [-r <ws_name>[~<ws_ver>]]

  [-u <username>]
    Username to use for authentication with the waybot.  The username "admin" 
    or another user with "admin" privilages shuold be used.

  [-f <wsv_file>]
    Filename to either import (-i) from or export (-e) to.

  [-c <wsv_comments>]
    Comments to use for a newly imported (-i) wayscript version.

  [-p <wsv_policy>]
    Policy to use for a newly imported (-i) wayscript version.

  [-ct <ws_ct>]
    Code type to use for a newly created wayscript.

  [-t <ws_type>]
    Wayscript Type to use for newly created wayscript.
    Default is "WAYSCRIPT".

  [-d ws_desc]
    Description to use for a newly created wayscript.

  [-v]
    Causes verbose information to emitted, if applicable.

  [-ls]
    List all wayscripts.

  [-i <ws_name>]
    Import a new version of the wayscript given by <ws_name>.  If there is 
    currently no wayscript by the name <ws_name>, then one will be created.
    The contents for the new wayscript version are taken from the file
    specified by the "-f" option.

  [-e <ws_name>[~<ws_ver>]]
    Exports the wayscript version given by "<ws_name>~<ws_ver>" to the file
    given by the "-f" option.  If no file is given, then contents are written
    to a file named "<ws_name>~<ws_ver>".  If no <ws_ver> is given, then we 
    will export the current version.

  [-q <ws_name>[~<ws_ver>]]
    Emits information on the wayscript or wayscript version record from the
    database.

  [-qv <ws_name>]
    Emits a list of wayscript versions for the wayscript given by <ws_name>.
    If "-v" option is added, then emits extra data including "#S" and "#SC",
    which are the number of sessions and session commands respectively that
    the given wayscript version was executed under.

  [-s <ws_name>~<ws_ver>]
    Sets the specified wayscript version as the current version.

  [-r <ws_name>[~<ws_ver>]]
    Attempts to remove the specified waycsript or wayscript version.  Note that
    wayscripts and wayscript versions can only be removed if they are not
    currently being referenced by other objects in the database.  For example,
    a wayscript version must not be referenced by any session, and a wayscript
    must not be referenced by any wayscript versions.

Notes:

Arguments must be specified in order given.  (For example -c needs to
be before -i.)

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
        try:
          username, password = ice_auth.__dict__.get("auth", {}).get('way', (None, None))
          sys.stdout.write("INFO: Attempting to use credentials for user %s from %s.\n" % (repr(username), repr(os.path.join(ice_path, "ice_auth.py"))))
          g_token = way.spike.authenticate(username=username, password=password)
        except:
          sys.stderr.write("ERROR: Authentication failed using ice cached credentials.\n")
          raise
      except:
        username, password = None, None

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
          sys.stderr.write("ERROR: Authentication failed.\n")
        else:
          raise e

  return g_token_un

# Returns: (ws_id, wsv_id)
g_map_wsv = {} # {(<ws_name>, <ws_version>): (ws_id, wsv_id), ...}
def resolve_wsv(ws_name, ws_ver):
  k = (ws_name, ws_ver)
  if ( not g_map_wsv.has_key(k) ):
    ws_id, ws_cur_ver_id = resolve_ws(ws_name)
    wsv_id = None
    if ( ws_id is not None ):
      spin = get_spin()
      wsvs = spin.WayScript.getChildList(id=ws_id, child_class="WayScriptVersion", restrict={"version":ws_ver})
      if ( len(wsvs) > 0 ):
        wsv_id = wsvs[0][0]
    g_map_wsv[k] = (ws_id, wsv_id)
  return g_map_wsv[k]
  
g_map_ws = {} # {<ws_name>: (<ws_id>, <ws_cur_ver_id>), ...}
def resolve_ws(ws_name):
  if ( not g_map_ws.has_key(ws_name) ):
    spin = get_spin()
    wss = spin.WayScript.getList(restrict={"script_name":ws_name}, fields=["current_version_id"])
    if ( len(wss) > 1 ):
      sys.stdout.write("WARNING: More than one script with the name %s found.  (Using the first one.)\n" % ws_name)
    if ( len(wss) > 0 ):
      g_map_ws[ws_name] = wss[0]
    else:
      g_map_ws[ws_name] = (None, None)
  return g_map_ws[ws_name]

def parse_fq_wsv_name(fq_wsv_name):
  n = string.find(fq_wsv_name, "~")
  if ( n > -1 ):
    return fq_wsv_name[:n], fq_wsv_name[n+1:]
  else:
    return fq_wsv_name, None

g_bUseVT = sys.stdout.isatty()
def fn_fmt(r,c,pcv):
  if (r/2 == float(r)/2) and g_bUseVT:
    return "\x1b[%sm%s\x1b[m" % (string.join(map(lambda a:str(a),(1,)), ';'), pcv)
  else:
    return pcv

# Returns: (<keys_items>, <non_keys_items>)
def sep_kv_list(lst, keys):
  keys_items = filter(lambda i,k=keys:i[0] in k, lst)
  non_keys_items = filter(lambda i,k=keys:i[0] not in k, lst)
  return keys_items, non_keys_items
  
def arrange_kv_list(lst, omit=None, top=None, bottom=None):
  if ( omit ):
    lst = filter(lambda i,o=omit:i[0] not in o, lst)
  lst_top = []
  if ( top ):
    lst_top, lst = sep_kv_list(lst, top)
  lst_bottom = []
  if ( bottom ):
    lst_bottom, lst = sep_kv_list(lst, bottom)
  lst_top.sort(lambda a,b:cmp(a[0],b[0]))
  lst.sort(lambda a,b:cmp(a[0],b[0]))
  lst_bottom.sort(lambda a,b:cmp(a[0],b[0]))
  return lst_top + lst + lst_bottom

def strip_kv_list_values(lst):
  return map(lambda i:(i[0], type(i[1])==types.StringType and string.strip(i[1]) or i[1]), lst)

def list_ws():
  spin = get_spin()
  ws_recs = spin.WayScript.getList(fields=["script_name", "script_type", "code_type", "script_desc"])
  ws_recs = map(lambda i:i[1:], ws_recs)
  ws_recs.sort()
  ws_recs.insert(0, ("Name", "Type", "Code Type", "Description"))
  sys.stdout.write("Listing of all WayScripts:\n\n")
  sys.stdout.write(tabfmt.fmtrows(ws_recs, col_sep=" | ", fn_fmt=fn_fmt, b_header=1, n_width=io.ioctl_GWINSZ(sys.stderr)[1]))

g_map_ws_types = {
  "WAYSCRIPT": "library.createWayScript",
  "EXTENSION": "library.createExtensionScript",
  "COGSCRIPT": "library.createCogScript",
  "TTLG":"library.createTTLGScript"
}

def import_ws(username, wsv_file, wsv_comments, wsv_policy, ws_ct, ws_type, ws_desc, ws_name):
  if ( wsv_file is None ):
    sys.stderr.write("ERROR: No file specified.\n")
  else:
    if ( not os.path.exists(wsv_file) ):
      sys.stderr.write("ERROR: %s: file does not exist.\n" % repr(wsv_file))
    else:
      if ( not g_map_ws_types.has_key(ws_type) ):
        sys.stderr.write("ERROR: %s: Invalid value for [-t <ws_type>].  Must be one of: %s\n" % (ws_type, string.join(g_map_ws_types.keys(),", ")))
      else:
        wsv_src = open(wsv_file).read()
        way = get_way()
        token, username = get_token_un(way, username)
        if ( wsv_comments is None ):
          sys.stdout.write("Comments for newly uploaded version of %s: (Press <ctrl>-d when finished.)\n" % repr(ws_name))
          sys.stdout.flush()
          wsv_comments = string.strip(sys.stdin.read())
        ws_id, ws_cur_ver_id = resolve_ws(ws_name)
        if ( wsv_policy is None ):
          wsv_policy = ""
          sys.stdout.write("Policy for newly uploaded version of %s:\n" % repr(ws_name))
          sys.stdout.flush()
          if ( ws_cur_ver_id is not None ):
            spin = get_spin()
            wsv_recs = spin.WayScriptVersion.getList(restrict={"way_script_version_id":ws_cur_ver_id}, fields=["policy"])
            if ( len(wsv_recs) > 0 ):
               wsv_policy = wsv_recs[0][1]
               sys.stdout.write("(Press <Enter> to use policy of current version: %s)\n" % repr(wsv_policy))
               sys.stdout.flush()
          s = string.strip(sys.stdin.readline())
          if ( s != "" ):
            wsv_policy = s
        if ( ws_id is None ):
          if ( (ws_type == "TTLG") and (ws_ct is None) ):
            sys.stdout.write("Code type for newly created wayscript %s:\n" % repr(ws_name))
            sys.stdout.flush()
            ws_ct = string.strip(sys.stdin.readline())
          if ( ws_desc is None ):
            sys.stdout.write("Description for newly created wayscript %s: " % repr(ws_name))
            sys.stdout.write("(Press <ctrl>-d when finished.)\n")
            sys.stdout.flush()
            ws_desc = string.strip(sys.stdin.read())
          ws_create_fn = getattr(way, g_map_ws_types[ws_type])
          ws_create_fn(__token=token, script_name=ws_name, code_type=ws_ct, script_desc=ws_desc, creator_user=username, acct_id=15)
          sys.stdout.write("Successfully created new %s WayScript %s.\n" % (ws_type, repr(ws_name)))
        way.library.createCurrentVersion(__token=token, script=ws_name, source=wsv_src, comments=wsv_comments, upload_user=username, approve_user=username, policy=wsv_policy)
        sys.stdout.write("Successfully created a new WayScriptVersion for the WayScript %s.\n\n" % repr(ws_name))

def export_ws(fq_wsv_name, wsv_file):
  ws_name, ws_ver = parse_fq_wsv_name(fq_wsv_name)
  if ( ws_ver is None ):
    # Use the current version.
    ws_id, wsv_id = resolve_ws(ws_name)
  else:
    ws_id, wsv_id = resolve_wsv(ws_name, ws_ver)
  if ( wsv_id is None ):
    sys.stderr.write("ERROR: %s: WayscriptVersion not found.\n" % fq_wsv_name)
  else:
    spin = get_spin()
    if ( ws_ver is None ):
      ws_ver = spin.WayScriptVersion.getList(restrict={"way_script_version_id":wsv_id}, fields=["version"])[0][1]
    if ( wsv_file is None ):
      wsv_file = "%s~%s" % (ws_name, ws_ver)
    sys.stderr.write("INFO: Exporting to %s.\n" % repr(wsv_file))
    wsv_src = spin.WayScriptVersion.getSource(wsv_id)
    if ( wsv_file == "-" ):
      sys.stdout.write(wsv_src)
    else:
      open(wsv_file, "w").write(wsv_src)

def query_ws(fq_wsv_name):
  ws_name, ws_ver = parse_fq_wsv_name(fq_wsv_name)
  ws_id, ws_cur_ver_id = resolve_ws(ws_name)
  spin = get_spin()
  if ( ws_ver is None ):
    if ( ws_id is None ):
      sys.stderr.write("ERROR: %s: WayScript not found.\n" % repr(ws_name))
    else:
      sys.stdout.write("WayScript %s details:\n\n" % repr(fq_wsv_name))
      rows = spin.WayScript.get(ws_id).data.items()
      rows = strip_kv_list_values(rows)
      rows = arrange_kv_list(rows, omit=["id"], top=["way_script_id"], bottom=["tran_id", "conflicting", "signature"])
      tab = tabfmt.fmtrows(rows, col_sep=" | ", fn_fmt=fn_fmt, b_header=0, n_width=io.ioctl_GWINSZ(sys.stderr)[1])
      bdr = ("-"*string.find(tab,"\n")) + "\n"
      sys.stdout.write(bdr + tab + bdr + "\n")
  else:
    ws_id, wsv_id = resolve_wsv(ws_name, ws_ver)
    if ( wsv_id is None ):
      sys.stderr.write("ERROR: %s: WayScriptVersion not found.\n" % fq_wsv_name)
    else:
      sys.stdout.write("WayScriptVersion %s details:\n\n" % repr(fq_wsv_name))
      rows = spin.WayScriptVersion.get(wsv_id).data.items()
      rows = strip_kv_list_values(rows)
      rows = arrange_kv_list(rows, omit=["id"], top=["way_script_version_id"], bottom=["tran_id", "conflicting", "script_digest", "signature"])
      tab = tabfmt.fmtrows(rows, col_sep=" | ", fn_fmt=fn_fmt, b_header=0, n_width=io.ioctl_GWINSZ(sys.stderr)[1])
      bdr = ("-"*string.find(tab,"\n")) + "\n"
      sys.stdout.write(bdr + tab + bdr + "\n")

def query_versions_ws(ws_name, b_verbose):
  # In case user specified a fq_wsv_name for ws_name.
  ws_name, ws_ver = parse_fq_wsv_name(ws_name)
  ws_id, ws_cur_ver_id = resolve_ws(ws_name)
  if ( ws_id is None ):
    sys.stderr.write("ERROR: %s: WayScript not found.\n" % repr(ws_name))
  else:
    sys.stdout.write("Versions of wayscript \"%s\":\n\n" % ws_name)
    if ( b_verbose ):
      fields = ["version", "policy", "comments"]
    else:
      fields = ['version', 'comments']
    spin = get_spin()
    wsv_recs = spin.WayScript.getChildList(id=ws_id, child_class="WayScriptVersion", fields=fields)
    wsv_recs.sort(lambda a,b:cmp(a[0],b[0]))
    for wsv_rec in wsv_recs:
      if ( b_verbose ):
        wsv_rec.insert(2, spin.WayScriptVersion.getChildCount(id=wsv_rec[0], child_class="SessionCommand"))
        wsv_rec.insert(2, spin.WayScriptVersion.getChildCount(id=wsv_rec[0], child_class="Session"))
      if ( wsv_rec[0] == ws_cur_ver_id ):
        wsv_rec.insert(0, "(*)" )
      else:
        wsv_rec.insert(0, "" )
    if ( b_verbose ):
      wsv_recs.insert(0,("Cur", "ID", "Version", "#S", "#SC", "Policy", "Comments"))
    else:
      wsv_recs.insert(0,("Cur", "ID", "Version", "Comments"))
    sys.stdout.write(tabfmt.fmtrows(wsv_recs, col_sep=" | ", fn_fmt=fn_fmt, b_header=1, n_width=io.ioctl_GWINSZ(sys.stderr)[1]))
    sys.stdout.write("\n")

def set_cur_ver_ws(username, fq_wsv_name):
  way = get_way()
  token, username = get_token_un(way, username)
  ws_name, ws_ver = parse_fq_wsv_name(fq_wsv_name)
  ws_id, wsv_id = resolve_wsv(ws_name, ws_ver)
  if ( ws_id is None ):
    sys.stderr.write("ERROR: %s: WayScript not found.\n" % repr(ws_name))
  else:
    if ( wsv_id is None ):
      sys.stderr.write("ERROR: %s: WayScriptVersion not found.\n" % repr(ws_ver))
    else:
      way.library.setCurrentVersion(__token=token, script=ws_name, version=ws_ver, approve_user=username)
      sys.stdout.write("Successfully set the current version of WayScript %s to %s.\n" % (repr(ws_name), repr(ws_ver)))

def remove_ws(username, fq_wsv_name):
  ws_name, ws_ver = parse_fq_wsv_name(fq_wsv_name)
  ws_id, ws_cur_ver_id = resolve_ws(ws_name)
  ws_id, wsv_id = resolve_wsv(ws_name, ws_ver)
  if ( ws_id is None ):
    sys.stderr.write("ERROR: %s: WayScript not found.\n" % ws_name)
  else:
    if ( wsv_id is None ):
      sys.stderr.write("ERROR: To remove a wayscript, remove its last remaining version.\n" % fq_wsv_name)
    else:
      spin = get_spin()
      cnt = spin.WayScriptVersion.getChildCount(id=wsv_id, child_class="Session")
      if ( cnt > 0 ):
        sys.stderr.write("ERROR: %s: Is in use by %d session%s.\n" % (fq_wsv_name, cnt, (cnt>1) and "s" or ""))
      else:
        cnt = spin.WayScriptVersion.getChildCount(id=wsv_id, child_class="SessionCommand")
        if ( cnt > 0 ):
          sys.stderr.write("ERROR: %s: Is in use by %d session command%s.\n" % (fq_wsv_name, cnt, (cnt>1) and "s" or ""))
        else:
          num_child_wsvs = -1
          if ( wsv_id == ws_cur_ver_id ):
            num_child_wsvs = spin.WayScript.getChildCount(id=ws_id, child_class="WayScriptVersion")
          if ( num_child_wsvs > 1 ):
            sys.stderr.write("ERROR: %s: Can't delete current wayscript version, unless it is the last remaining version.\n" % fq_wsv_name)
          else:
            if ( num_child_wsvs == 1 ):
              sys.stdout.write("%s is last remaining WayScriptVersion.  Really delete entire WayScript %s? (y/n)\n" % (repr(ws_ver),repr(ws_name)))
            else:
              sys.stdout.write("Really delete WayScriptVersion %s? (y/n)\n" % repr(fq_wsv_name))
            a = string.strip(sys.stdin.readline())[0]
            if ( a in "yY" ):
              tid = spin.tran.start()
              try:
                if ( num_child_wsvs == 1 ):
                  spin.WayScript.update(t_id=tid, id=ws_id, current_version_id=None)
                  spin.wayScript.delete(t_id=tid, id=ws_id)
                else:
                  spin.WayScriptVersion.delete(t_id=tid, id=wsv_id)
                sys.stdout.write("Deleted.\n") 
              except:
                try:
                  spin.tran.rollback(t_id=tid)
                except:
                  pass
                raise
              spin.tran.commit(t_id=tid)
            else:
              sys.stdout.write("Canceled.\n")

def shift(l):
  r = l[0]
  del l[0]
  return r

def main():
  argv = sys.argv[1:]

  if ( len(argv) == 0 ):
    usage()
    sys.exit(1)

  username = None
  password = None
  wsv_file = None
  wsv_comments = None
  wsv_policy = None
  ws_ct = None
  ws_type = "WAYSCRIPT"
  ws_desc = None
  b_verbose = 0

  while argv:
    cur_arg = shift(argv)
    if ( cur_arg in ("-h", "--help") ):
      usage()
      sys.exit()
    elif ( cur_arg == "-u" ):
      username = shift(argv)
    elif ( cur_arg == "-f" ):
      wsv_file = shift(argv)
    elif ( cur_arg == "-c" ):
      wsv_comments = shift(argv)
    elif ( cur_arg == "-p" ):
      wsv_policy = shift(argv)
    elif ( cur_arg == "-ct" ):
      ws_ct = shift(argv)
    elif ( cur_arg == "-t" ):
      ws_type = shift(argv)
    elif ( cur_arg == "-d" ):
      ws_desc = shift(argv)
    elif ( cur_arg == "-v" ):
      b_verbose = 1
    elif ( cur_arg == "-ls" ):
      list_ws()
    elif ( cur_arg == "-i" ):
      import_ws(username, wsv_file, wsv_comments, wsv_policy, ws_ct, ws_type, ws_desc, shift(argv))
    elif ( cur_arg == "-e" ):
      export_ws(shift(argv), wsv_file)
    elif ( cur_arg == "-q" ):
      query_ws(shift(argv))
    elif ( cur_arg == "-qv" ):
      query_versions_ws(shift(argv), b_verbose)
    elif ( cur_arg == "-s" ):
      set_cur_ver_ws(username, shift(argv))
    elif ( cur_arg == "-r" ):
      remove_ws(username, shift(argv))
    else:
      sys.stderr.write("ERROR: %s: unexpected argument, ignoring.\n" % cur_arg)

if ( __name__ == "__main__" ):
  try:
    main()
  except KeyboardInterrupt, e:
    sys.stdout.write("Interrupted.\n")

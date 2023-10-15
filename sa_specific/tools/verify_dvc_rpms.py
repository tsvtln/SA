##
#
# Tool to verify RPM remediations against a device.
# 
# Takes into account:
# 
#   o RPMs avialable to the device (unit_id/folder_path/nevra)
#   o RPMs attached to the device via software policies. (unit_id/folder_path/swp/nerva)
# 
# Tool should dump the following:
#
#   o RPMs avialable to the device (unit_id/folder_path/nevra)
#   o SWPs attached to device:
#     o ID of SWP
#     o child RPMs (unit_id/folder_path/nevra)
#     o attached via (device group id, SWP id)
#     o all repo.restrict CAs on SWP
#   o all repo.restrict CAs on device.
# 
# Tool reports:
#
#   o Any RPMs attached to the device via a software policy for which a newer version is avialable
#     (unit_ids)


#   o Reports the folder path for the old and newer RPMs
#   o Reports the SWP for the older RPMs.
#   o Reports all repo.restrict CAs on device.
# 

import sys,cPickle,string,gzip,types

CHUNK_SIZE = 500

def dict_get(dict, key, init_val=None):
  val = dict.get(key, init_val)
  if ( val == init_val ):
    dict[key] = init_val
  return val

def str_id(id):
  if ( type(id) == types.LongType ): return repr(id)[:-1]
  else: return str(id)

def _calc_folder_path(spin, f_id):
  folder_path = ""
  cur_f_id = f_id
  while cur_f_id != "0":
    cur_f_name = spin.Folder.getList(restrict={'folder_id':cur_f_id}, fields=['folder_name'])[0][1]
    folder_path = "/" + cur_f_name + folder_path
    cur_f_id = str_id(spin._FolderFolderLink.getList(restrict={'folder_id':cur_f_id}, fields=['parent_folder_id'])[0][1])
  return folder_path

_folder_paths = {}
def get_folder_path(spin, f_id):
  f_id = str_id(f_id)
  folder_path = _folder_paths.get(f_id,None)
  if ( folder_path == None ):
    folder_path = _calc_folder_path(spin,f_id)
    _folder_paths[f_id] = folder_path
  return folder_path

_folder_accts = {}
def get_folder_accts(spin, fid):
  fid = str_id(fid)
  folder_accts = _folder_accts.get(fid, None)
  if ( folder_accts == None ):
    folder_accts = map(lambda far,str_id=str_id:str_id(far[1]), spin._FolderAccount.getList(restrict={"folder_id":fid}, fields=["acct_id"]))
    _folder_accts[fid] = folder_accts
  return folder_accts

def rpmvercmp_ur(ura, urb):
  return rpmvercmp("%s-%s" % (ura["ver"], ura["rel"]), "%s-%s" % (urb["ver"], urb["rel"]))

# from http://concisionandconcinnity.blogspot.com/2008/12/rpm-style-version-comparison-in-python.html
import re
isalnum = re.compile('[^a-zA-Z0-9]')
isdigit_re = re.compile('^[0-9]+$')
def isdigit(s):
  return (isdigit_re.match(s) is not None)
isalpha_re = re.compile('^[a-zA-Z]+$')
def isalpha(s):
  return (isalpha_re.match(s) is not None)
def rpmvercmp(a, b):
    # If they're the same, we're done
    if a==b: return 0

    def _gen_segments(val):
        """
        Generator that splits a string into segments.
        e.g., '2xFg33.+f.5' => ('2', 'xFg', '33', 'f', '5')
        """
        ret = []
        val = isalnum.split(val)
        for dot in val:
            res = ''
            for s in dot:
                if not res:
                    res = res + s
                elif (isdigit(res) and isdigit(s)) or \
                   (isalpha(res) and isalpha(s)):
                    res = res + s
                else:
                    if res:
                        #yield res
                        ret.insert(0,res)
                    res = s
            if res:
                #yield res
                ret.insert(0,res)
        return ret

    ver1, ver2 = a, b

    # Get rid of the release number
    ver1_rel, ver2_rel = None, None
    if '-' in ver1: ver1, ver1_rel = string.split(ver1,'-')
    if '-' in ver2: ver2, ver2_rel = string.split(ver2,'-')

    l1, l2 = map(_gen_segments, (ver1, ver2))
    while l1 and l2:
        # Get the next segment; if none exists, done
#        try: s1 = l1.next()
#        except StopIteration: s1 = None
        try: s1 = l1.pop()
        except IndexError: s1 = None
#        try: s2 = l2.next()
#        except StopIteration: s2 = None
        try: s2 = l2.pop()
        except IndexError: s2 = None

        if s1 is None and s2 is None: break
        if (s1 and not s2): return 1
        if (s2 and not s1): return -1

        # Check for type mismatch
        if isdigit(s1) and not isdigit(s2): return 1
        if isdigit(s2) and not isdigit(s1): return -1

        # Cast as ints if possible
        if isdigit(s1): s1 = int(s1)
        if isdigit(s2): s2 = int(s2)

        rc = cmp(s1, s2)
        if rc: return rc

    # If we've gotten this far, check release numbers
    if ver1_rel is not None and ver2_rel is not None:
        return rpmvercmp(ver1_rel, ver2_rel)

    return 0

def load_cas(spin, dvc_id):
  return spin.Device.getCustomAttributes(dvc_ids=[dvc_id])[0]

def load_avail_rpms(spin, dvc_id, units):
  err("Loading available RPM unit ids...  ")
  uids = map(str_id, spin.Device.getAvailableRPMIDList(dvc_id))
  for uid in uids:
    dict_get(units, uid, {"avail":1, "id":uid})
  err("%d available RPM unit ids laoded.\n", (len(uids),))

def load_dvc_grps(spin, dvc_id, dvc_grps):
  err("Loading device groups...  ")
  DEVICE_GROUP_STACK = 17
  dvc_grp_recs = spin.Device.getChildList(id=dvc_id, child_class="RoleClass", restrict={"stack_id":DEVICE_GROUP_STACK}, fields=["role_class_short_name"])
  for dvc_grp_rec in dvc_grp_recs:
    dvc_grps[str_id(dvc_grp_rec[0])] = {"name":dvc_grp_rec[1]}
  err("%d device groups loaded.\n", (len(dvc_grp_recs),))

def load_app_pols_on_dvc(spin, dvc_id, app_pols):
  err("Loading software policies on device...  ")
  via = "Device:%s" % str_id(dvc_id)
  app_pol_recs = spin.Device.getChildList(id=dvc_id, child_class="AppPolicy", fields=["app_policy_name"])
  for app_pol_rec in app_pol_recs:
    apr = dict_get(app_pols, str_id(app_pol_rec[0]), {"name":app_pol_rec[1]})
    dict_get(apr, "via", []).append(via)
  err("%d software policies loaded.\n", (len(app_pol_recs),))

def load_app_pols_on_dvc_grps(spin, dvc_grps, app_pols):
  err("Loading software policies on %d device groups...  ", (len(dvc_grps),))
  for dvc_grp_id in dvc_grps.keys():
    via = "RoleClass:%s" % str_id(dvc_grp_id)
    app_pol_recs = spin.RoleClass.getChildList(id=dvc_grp_id, child_class="AppPolicy", fields=["app_policy_name"])
    for app_pol_rec in app_pol_recs:
      apr = dict_get(app_pols, str_id(app_pol_rec[0]), {"name":app_pol_rec[1]})
      dict_get(apr, "via", []).append(via)
  err("Done.\n")

def load_app_pols_on_app_pols(spin, app_pols):
  err("Loading child software policies on %d software policies...  ", len(app_pols))
  apids = app_pols.keys()
  while (len(apids) > 0):
    next_apids = []
    for apid in apids:
      via = "AppPolicy:%s" % str_id(apid)
      appis = spin.AppPolicy.getChildList(id=apid, child_class="AppPolicyPolicyItem", fields=["child_app_policy_id"])
      child_apids = map(lambda i:str_id(i[1]), appis)
      next_apids.extend(child_apids)
      for child_apid in child_apids:
        child_apr = dict_get(app_pols, child_apid, {})
        vias = dict_get(child_apr, "via", [])
        if ( via in vias ): continue
        vias.append(via)
        # We could put the following into a "chunking" type function.
        if ( not child_apr.has_key("name") ):
          app_pol_rec = spin.AppPolicy.getList(restrict={"app_policy_id":child_apid}, fields=["app_policy_name"])[0]
          child_apr["name"] = app_pol_rec[1]
    apids = next_apids
  err("Done.\n")

def load_app_pols_other(spin, app_pols, app_pol_ids):
  # If no app policy ids where specified, then return.
  if ( not app_pol_ids ): return

  err("Loading %d non-attached software policies...  ", len(app_pol_ids))

  # Filter out any app policy ids that are already listed.
  app_pol_ids = filter(lambda id, ids=app_pols.keys():id not in ids, app_pol_ids)

  # Load app policy names from spin.
  if ( len(app_pol_ids) > 0 ):
    app_pol_recs = spin.AppPolicy.getList(restrict={"app_policy_id":app_pol_ids}, fields=["app_policy_name"])
  else:
    app_pol_recs = []
  for app_pol_rec in app_pol_recs:
    app_pols[str_id(app_pol_rec[0])] = {"name":app_pol_rec[1], "via":["Command line"]}

  err("%d software policies found and loaded.\n" % len(app_pol_recs))

def load_unit_ids_on_app_pols(spin, app_pols, units):
  err("Loading unit ids on %d software policies...", (len(app_pols),))
  for apid in app_pols.keys():
    via = "AppPolicy:%s" % str_id(apid)
    uids = map(lambda i:str_id(i[1]), spin.AppPolicy.getChildList(id=apid, child_class="AppPolicyUnitItem", fields=["unit_id"]))
    err(" %d" % len(uids))
    for uid in uids:
      ur = dict_get(units, uid, {"avail":0, "id":uid})
      dict_get(ur, "via", []).append(via)
  err(" Done.\n")

# If unit is an RPM of the same platform and customer of <dvc>, then will load 
# up details about it.  Otherwise, will remove the record.
def load_rpm_details(spin, dvc, units):
  err("Filtering out unit IDs with incompatible platforms...\n")
  uids = units.keys()
  dvc_platform_id = dvc["platform_id"]
  dvc_acct_id = dvc["acct_id"]
  any_acct_id = str_id(spin.Account.get(name="ANY")["acct_id"])
  while ( len(uids) > 0 ):
    chunk_uids = shift_chunk(uids, CHUNK_SIZE)
    purs = spin._UnitPlatform.getList(restrict={"unit_id":chunk_uids}, fields=["unit_id", "platform_id"])
    pus = {}
    for pur in purs:
      uid = str_id(pur[1])
      platform_id = str_id(pur[2])
      dict_get(pus, uid, []).append(platform_id)
    for uid in chunk_uids:
      platform_ids = pus.get(uid, [])
      if ( dvc_platform_id in platform_ids ):
        units[uid]["platform_ids"] = platform_ids
      else:
        del units[uid]
  err("Done.\n")

  err("Loading RPM details for %d units...", (len(units),))
  uids = units.keys()
  while (len(uids) > 0):
    chunk_uids = shift_chunk(uids, CHUNK_SIZE)
    unit_recs = spin.Unit.getList(restrict={"unit_id":chunk_uids}, 
                                  fields=["file_type", "unit_name",
                                          "unit_file_name",
                                          "software_version",
                                          "software_release",
                                          "acct_id"])
    for unit_rec in unit_recs:
      uid = str_id(unit_rec[0])
      ur = units[uid]
      if ( unit_rec[1] == "RPM" ):
        ur["name"] = unit_rec[2]
        ur["file_name"] = unit_rec[3]
        ur["ver"] = unit_rec[4]
        ur["rel"] = unit_rec[5]
        ur["acct_id"] = str_id(unit_rec[6]) # replaced with acct_ids below
      else:
        if ( ur["avail"] == 1 ):
          err("\nWARNING: Unit record shows up as available yet isn't an RPM Type? :\n%s\n", (repr(ur),))
        del units[uid]
        chunk_uids.remove(uid)

    # gather folder path if unit is in folder and
    # delete unit if folder's accounts are incompatible with device's account
    fu_recs = spin._FolderUnit.getList(restrict={"unit_id":chunk_uids}, fields=["unit_id", "folder_id"])
    for fu_rec in fu_recs:
      uid = str_id(fu_rec[1])
      fid = str_id(fu_rec[2])
      ur = units[uid]
      f_acct_ids = get_folder_accts(spin, fid)
      if ( (dvc_acct_id in f_acct_ids) or
           (any_acct_id in f_acct_ids) ):
        del ur["acct_id"]
        ur["folder_path"] = get_folder_path(spin, fid)
        ur["acct_ids"] = f_acct_ids
      else:
        del units[uid]
    err(".")

  # Filter out units not in a folder that don't have compat acct with device.
  uids = units.keys()
  for uid in uids:
    ur = units[uid]
    if ( not ur.has_key("folder_path") ):
      if ( (ur["acct_id"] == dvc_acct_id) or 
           (ur["acct_id"] == any_acct_id) ):
        ur["acct_ids"] = [ur["acct_id"]]
        del ur["acct_id"]
      else:
        del units[uid]

  err("  Done.  %d RPM units found.\n" % (len(units),))

#------------------------------------------------------------------------------
# Returns the following data structure:
#   {"units":{<unit_id>:{"id":<unit_id>, "avail":<[0|1]>, 'name':<name>,
#                        "file_name":<file_name>, 'ver':<ver>, "rel":<rel>, 
#                         "via":[<via1>, ...], "folder_path":<folder_path>},
#                         "acct_ids":<acct_ids>,
#                         "platform_ids":<platform_ids>}, 
#    "app_pols":{<app_pol_id>:{'name':<name>, 'via':[<via1>, ...]}}, 
#    "dvc_grps":{<dvc_grp_id>:{'name':<name>}}, 
#    "dvc_cas":<dvc_cas>,
#    "dvc":{<dvc_record>, "acct_id":<acct_id>}
#------------------------------------------------------------------------------
# <app_pol_ids> - Application policies to be considered that are not currently
#    attached to the device given by <dvc_id>.
def load_data_for_dvc(dvc_id, app_pol_ids=None):
  data = {"units":{}, "app_pols":{}, "dvc_grps":{}}
  units = data["units"]
  app_pols = data["app_pols"]
  dvc_grps = data["dvc_grps"]

  # Load up spin wrapper.
  from coglib import spinwrapper
  spin = spinwrapper.SpinWrapper()

  # Load the device record and account.
  dvc = spin.Device.get(dvc_id).data
  for k in dvc.keys():
    v = dvc[k]
    if ( type(v).__name__ == "xmlrpcdateTime" ):
      dvc[k] = str(v)
  data["dvc"] = dvc
  dvc["acct_id"] = str_id(spin.Device.getAccount(dvc_id)["acct_id"])
  dvc["platform_id"] = str_id(dvc["platform_id"])

  # Load the CAs for this device.
  data["dvc_cas"] = load_cas(spin, dvc_id)

  # Load unit ids avialable to this device.
  load_avail_rpms(spin, dvc_id, units)

  # Load device groups the device is a member of.
  load_dvc_grps(spin, dvc_id, dvc_grps)

  # Load SW policies directly attached to device.
  load_app_pols_on_dvc(spin, dvc_id, app_pols)

  # Load SW policies attached to device groups.
  load_app_pols_on_dvc_grps(spin, dvc_grps, app_pols)

  # Load SW policies attached to SW policies.
  load_app_pols_on_app_pols(spin, app_pols)

  # Load SW policies not currently attached.
  load_app_pols_other(spin, app_pols, app_pol_ids)

  # Load RPM unit ids for all SW policies.
  load_unit_ids_on_app_pols(spin, app_pols, units)

  # Load details of currently loaded unit ids.
  load_rpm_details(spin, dvc, units)

  return data

def load_data_from_file(in_file):
  f = gzip.open(in_file, "rb")
  data = cPickle.load(f)
  f.close()
  return data

def dump_data_to_file(data, out_file):
  data["err"] = g_err
  f = gzip.open(out_file, "wb")
  cPickle.dump(data, f)
  f.close()

def fmt_ur(ur):
  return "\"%s/%s\"(%s)" % (ur.get("folder_path", "<NOT_IN_FOLDER>"), ur["file_name"], ur["id"])

# Analyze data and report results.
def process_data(data):
  dvc_cas = data["dvc_cas"]
  dvc_id = dvc_cas["dvc_id"]
  out("\nRPM attachment analysis for device ID %d:\n", (dvc_id,))

  out("\n(1) Member of the following device groups:\n")
  dvc_grps = data["dvc_grps"]
  c = 1
  for dvc_grp_id in dvc_grps.keys():
    out("  %d. \"%s\"(%s)\n", (c, dvc_grps[dvc_grp_id]["name"], dvc_grp_id))
    c = c + 1

  out("\n(2) Attached to the following software policies:\n")
  app_pols = data["app_pols"]
  c = 1
  for app_pol_id in app_pols.keys():
    apr = app_pols[app_pol_id]
    out("  %d. \"%s\"(%s)\n    via: %s\n", (c, apr["name"], app_pol_id, string.join(apr["via"], ", ")))
    c = c + 1

  out("\n(3) repo.restrict.* custom attribuets:\n")
  c = 1
  for key in dvc_cas["attrs"].keys():
    if ( key[:14] == 'repo.restrict.' ):
      ca = dvc_cas["attrs"][key][0]
      out("  %d. \"%s\"(scope=%s, id=%s):\n", (c, key, ca["scope"], ca["id"]))
      c = c + 1
      folders = re.split(r'\r|\n|\r\n', ca["value"])
      for folder in folders:
        out("    %s\n", (folder,))

  units = data["units"]
  uids = units.keys()
  unit_recs = units.values()

  urs = filter(lambda ur:ur["avail"]==0, unit_recs)
  out("\n(4) %d RPMs attached but not currently available to device:\n" % (len(urs),))
  c = 1
  for ur in urs:
    out("  %d. %s\n    via: %s\n", (c, fmt_ur(ur), string.join(ur["via"], ", ")))
    c = c + 1

#  # TEMP CODE:
#  # Filter out units that are not available.
#  for k in units.keys():
#    if ( units[k]['avail'] != 1 ):
#      del units[k]
#  uids = units.keys()
#  unit_recs = units.values()

  # Create a unit index by name.
  units_by_name = {}
  for uid in uids:
    ur = units[uid]
    dict_get(units_by_name, ur["name"], []).append(ur)

  # Get a list of unit ids attached to device via sw policy.
  swp_uids = map(lambda ur:ur["id"], filter(lambda ur:ur.has_key("via"), unit_recs))

  old_rpms = []

  # Itterate through each of the attached unit IDs.
  for uid in swp_uids:
    ur = units[uid]

    # Get the list of units of the same name.
    urs = units_by_name[ur["name"]]

    # Filter out unit records attached via a software policy.
    urs = filter(lambda ur:not ur.has_key("via"), urs)

    # Filter out all rpms that are not newer.
    urs = filter(lambda urt,ur=ur:rpmvercmp_ur(urt,ur)>0, urs)

    # If there are any unit records left, then report them.
    if ( len(urs) > 0 ):
      old_rpms.append((ur, urs))

  out("\n(5) %d RPMs attached to device with newer non-attached versions avialable:\n", (len(old_rpms),))
  c = 1
  for old_rpm in old_rpms:
    ur = old_rpm[0]
    out("  %d. %s\n    via: %s; is older than:\n", (c, fmt_ur(ur), string.join(ur["via"], ", ")))
    c = c + 1
    for nur in old_rpm[1]:
      out("      %s\n" % fmt_ur(nur))

  out("\n")

def out(s, args=None):
  if ( args is not None ): s = s % args
  sys.stdout.write(s)
  sys.stdout.flush()

g_err = ""
def err(s, args=None):
  if ( args is not None ): s = s % args
  global g_err
  g_err = g_err + s
  sys.stderr.write(s)
  sys.stderr.flush()

def usage():
  out("""Usage: %s [-h] [-p <app_pol_id_list>] [-o <out_file>] (<dvc_id> | -i <in_file>)

  [-p <app_pol_id_list>]
    Comma delemited list of application policies to consider that aren't 
    currently attached to the device in question.

Reports:

  (1) Device groups for which this device is a member

  (2) software policies that are attached to this device, and how.

  (3) The current <repo.restrict.*> custom attribute folders assigned to this
      device.

  (4) Any RPMs that are attached but not avialable to the device.

  (5) Any RPMs that are currently attached to the given device via a software
      policy for which there are newer versions avialable and _not_ attached to
      the device via a software policy.

Reported RPMs will include folder path, nevra, and software policies.

If <out_file> is provided, then the tool will dump the central data structures
used to make this calculation, for offline analysis.

If <in_file> is provided, then the tool will make use of previously dumped
data instead of loading it from the spin.

""",(sys.argv[0],))

def shift_chunk(l, len):
  r = l[0:len]
  del l[0:len]
  return r

def shift(l):
  r = l[0]
  del l[0]
  return r

def main(args):
  # If no arguments where given.
  if ( len(args) == 0 ):
    usage()
    sys.exit(1)

  dvc_id = None
  out_file = None
  in_file = None
  app_pol_ids = None

  # process arguments.
  while (len(args) > 0):
    cur_arg = shift(args)
    if ( cur_arg == "-o" ):
      out_file = shift(args)
    elif ( cur_arg == "-i" ):
      if ( dvc_id == None ):
        in_file = shift(args)
      else:
        err("%s: Device ID %s already specified, can't also specify an input file.  Ignoring...\n", (cur_arg, str(dvc_id)))
    elif ( cur_arg == "-p" ):
      app_pol_ids = map(str_id, string.split(shift(args), ","))
    elif ( cur_arg in ("-h", "--help") ):
      usage()
      sys.exit(0)
    else:
      if ( dvc_id == None ):
        if ( in_file == None ):
          dvc_id = cur_arg
        else:
          err("%s: <in_file> %s already specified, can't also specify a device ID.  Ignoring...\n", (cur_arg, in_file))
      else:
        err("%s: Device ID %s already specified.  Can't specify multiple device IDs.  Ignoring...\n", (cur_arg, str(dvc_id)))

  # If neither dvc_id nor in_file where specified:
  if ( dvc_id == None and in_file == None ):
    err("Must specify either a device ID or an input file.\n")
    usage()
    sys.exit(1)

  if (dvc_id != None):
    data = load_data_for_dvc(dvc_id, app_pol_ids)
  else:
    data = load_data_from_file(in_file)

  if ( out_file != None):
    dump_data_to_file(data, out_file)

  process_data(data)

if ( __name__ == "__main__" ):
  main(sys.argv[1:])
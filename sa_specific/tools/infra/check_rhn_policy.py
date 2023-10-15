# 

import sys,copy,time,string

def err(msg):
  sys.stdout.write("%s: %s\n" % (sys.argv[0], msg))

def info(msg):
  sys.stdout.write("%s\n" % msg)

def usage():
  info("""Will attempt to verify that all the RPMs in the given software policy are the 
newest RPMs among the RPMs avialable from either the specified folder or the
given device.

Usage: %s [-f <folder_id>|-d <dvc_id>] -sp <software_policy_id>
""" % sys.argv[0])

CHUNK_SIZE=500

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

def rpm_ver_cmp(a,b):
  return rpmvercmp("%s-%s" % (a['software_version'],a['software_release']),"%s-%s" % (b['software_version'],b['software_release']))

# Convert a dateTime.iso8601 object into seconds from epoch.
def d2s(d):
  return int(time.mktime(time.strptime(str(d),"%Y%m%dT%H:%M:%S")))

# This method figures out which rpm is newer than the other.  If the two rpms
# are different kinds of rpms, then returns 0.  The initial implementaion
# will make use of upload date to determine which is newer.
def rpm_dt_cmp(a,b):
  if (a['unit_name'] != b['unit_name'] ): return 0
  return cmp(d2s(a['create_dt']), d2s(b['create_dt']))

#rpm_cmp = rpm_dt_cmp
rpm_cmp = rpm_ver_cmp

def get_rpms_from_device(dvc_id):
  rpms = []
  rpm_ids = spin.Device.getAvailableRPMIDList(dvc_id)
  while rpm_ids:
    rpms.extend(spin.RPMUnit.getAll(restrict={'unit_id':rpm_ids[:CHUNK_SIZE]}))
    del rpm_ids[:CHUNK_SIZE]
  return rpms

def get_rpms_from_folder(folder_id):
  rpms = []
  rpm_ids = spin.Folder.getChildIDList(folder_id,child_class="RPMUnit")
  while rpm_ids:
    rpms.extend(spin.RPMUnit.getAll(restrict={'unit_id':rpm_ids[:CHUNK_SIZE]}))
    del rpm_ids[:CHUNK_SIZE]
  child_folder_ids = spin.Folder.getChildIDList(folder_id,child_class="Folder")
  for child_folder_id in child_folder_ids:
    rpms.extend(get_rpms_from_folder(child_folder_id))
  return rpms

def get_rpms_from_swp(swp_id):
  rpms = []
  uids = map(lambda r:r[1], spin.AppPolicyUnitItem.getList(restrict={'app_policy_id':swp_id},fields=['unit_id']))
  while uids:
    rpms.extend(spin.Unit.getAll(restrict={'unit_type':'RPM','unit_id':uids[:CHUNK_SIZE]}))
    del uids[:CHUNK_SIZE]
  child_swp_ids = map(lambda r:r[1], spin.AppPolicy.getChildList(swp_id,child_class='AppPolicyPolicyItem',fields=['child_app_policy_id']))
  for child_swp_id in child_swp_ids:
    rpms.extend(get_rpms_from_swp(child_swp_id))
  return rpms

from coglib import spinwrapper
spin = spinwrapper.SpinWrapper()

def main():
  args = copy.copy(sys.argv[1:])

  def shift(l):
    r = l[0]
    del l[0]
    return r

  pool_type = None
  pool_id = None
  swp_id = None

  while args:
    arg = shift(args)
    if ( arg == '-f' ):
      if ( pool_id ):
        err("RPM pool already specified: type:%s, id:%s" % (pool_type,pool_id))
        sys.exit(1)
      pool_type = "Folder"
      pool_id = shift(args)
    elif ( arg == '-d' ):
      if ( pool_id ):
        err("RPM pool already specified: type:%s, id:%s" % (pool_type,pool_id))
        sys.exit(1)
      pool_type = "Device"
      pool_id = shift(args)
    elif ( arg == '-sp' ):
      swp_id = shift(args)
  
  if ( not pool_id ):
    err("Must specify one of -d or -f")
    usage()
    sys.exit(1)
  
  # Gather rpms via given pool
  pool_name=pool_id
  if ( pool_type == "Folder" ):
    pool_rpms = get_rpms_from_folder(pool_id)
    f = spin.Folder.get(pool_id)
    pool_name = "%s(%s)" % (f['folder_name'],pool_id)
  elif ( pool_type == "Device" ):
    pool_rpms = get_rpms_from_device(pool_id)
    d = spin.Device.get(pool_id)
    pool_name = "%s(%s)" % (d['system_name'],pool_id)

  info("%d RPMs avialable via %s '%s'" % (len(pool_rpms), pool_type, pool_name))
  
  # Gather all rpms via given software policy.
  swp_rpms = get_rpms_from_swp(swp_id)

  swp = spin.AppPolicy.get(swp_id)
  info("Analyzing %d RPMs from software policy '%s(%s)'" % (len(swp_rpms), swp['app_policy_name'], swp_id))
  
  # (1) Make sure all swp_rpms are represented in the pool.
  for swp_rpm in swp_rpms:
    if ( not filter(lambda i,n=swp_rpm['unit_display_name']:i['unit_display_name']==n, pool_rpms) ):
      info("%s from given sw policy not found in RPMs via %s %s." % (swp_rpm['unit_display_name'], pool_type, pool_id))
  
  # (2) Make sure there are no rpms in the sw policy that have newer versions in the pool.
  
  # Filter out rpms from the pool, that already exist in the swp.
  pool_rpms = filter(lambda i,swp_rpms=map(lambda i:i['unit_display_name'],swp_rpms):i['unit_display_name'] not in swp_rpms, pool_rpms)
  
  for swp_rpm in swp_rpms:
    # Print the swp rpm we are currently analyzing.
    s = swp_rpm['unit_display_name']
    s = s + (79-len(s))*' '
    sys.stdout.write("\r%s" % s)
    sys.stdout.flush()

    # Get a list of like rpms from the given sw policy.
    swp_like_rpms = filter(lambda i,n=swp_rpm['unit_name']:i['unit_name']==n, swp_rpms)
  
    # If there are other rpms in the same sw policy that is newer, then continue.
    newer_rpms_in_swp = filter(lambda i,rpm_cmp=rpm_cmp,swp_rpm=swp_rpm:rpm_cmp(swp_rpm,i) < 0, swp_like_rpms)
    if ( newer_rpms_in_swp ):
#      info("In software policy: %s is succeeded by: %s" % (swp_rpm['unit_display_name'], repr(map(lambda i:i['unit_display_name'], newer_rpms_in_swp))))
      continue
  
    # Get a lit of like rpms from the pool.
    pool_like_rpms = filter(lambda i,n=swp_rpm['unit_name']:i['unit_name']==n, pool_rpms)
  
    # If there are newer rpms in the pool, then tell the user.
    newer_rpms_in_pool = filter(lambda i,rpm_cmp=rpm_cmp,swp_rpm=swp_rpm:rpm_cmp(swp_rpm,i) < 0, pool_like_rpms)
    if ( newer_rpms_in_pool ):
      info("\r%s is succeeded by: %s from %s %s" % (swp_rpm['unit_display_name'], repr(map(lambda i:i['unit_display_name'], newer_rpms_in_pool)), pool_type, pool_id))

  s = "Done."
  s = s + (79-len(s))*' ' + '\n'
  sys.stdout.write("\r%s" % s)

if ( __name__ == '__main__' ): main()
#!/opt/opsware/bin/python
#
# Read in all opsware service levels and the devices they're linked to
# so we can create a map of the core.
#
# Designed to provide troubleshooting context on a multibox core or a mesh of them.


SERVICE_LEVEL_STACK_ID = 4

import sys, string, math, os

sys.path.append("/opt/opsware/pylibs")

from coglib import spinwrapper
from coglib import certmaster

# @param spin:string hostname/ip for spin
def initSpin(spin="spin"):
    ctx = certmaster.getContextByName(spin,"spin.srv","opsware-ca.crt")
    s = spinwrapper.SpinWrapper(ctx=ctx)
    return s

# @param s:spinwrapper
def mapCore(s):
    # structure of core_map:
    # Dict core_map
    #              \____ Dict data_center              
    #                                    \____ Dict dvc_id
    #                                                     |____ List service_levels
    #                                                     |                        \____ String service_level
    #                                                     \____ Dict dvc_record
    #
    
    core_map = {}
    
    # get the service level roleclass stack
    service_levels = s.RoleClassStack.get(id=SERVICE_LEVEL_STACK_ID)

    # get the individual service level children from it
    service_level_rcs = service_levels.getChildren(child_class='RoleClass')

    # search service levels and categorize
    # exclude roleclasses cogbot and Windows-Cogbot - we don't care about agent attachments
    # include only devices owned by customer opsware - this will also rule out boxes being provisioned.
    
    for rc in service_level_rcs:
        rc_name = rc.get("role_class_full_name")
        if rc_name not in ["UNKNOWN","cogbot","Windows-Cogbot","ServiceLevel Opsware agent","ServiceLevel Opsware agent Windows"]:
            dvc_list = rc.getChildren(child_class='MegaDeviceRoleClassHardware')
            for dvc in dvc_list:
                if dvc["acct_name"] == 'OPSWARE':
                    dvc_id = dvc["dvc_id"]
                    dvc_info = {"service_levels":[],"device_record":""}
                    dc_id = dvc["data_center_name"]

                    # insert a service level record
                    try:
                        core_map[dc_id][dvc_id]["service_levels"].append(rc_name)
                    except:
                        # insert a device record and a service level record
                        try:
                            core_map[dc_id][dvc_id] = dvc_info
                            core_map[dc_id][dvc_id]["service_levels"].append(rc_name)
                            core_map[dc_id][dvc_id]["device_record"] = dvc
                        except:
                            # insert a datacenter record, a device record and a service level record
                            core_map[dc_id] = {dvc_id:dvc_info}
                            core_map[dc_id][dvc_id]["service_levels"].append(rc_name)
                            # the device record
                            core_map[dc_id][dvc_id]["device_record"] = dvc
    return core_map

def makeHumanReadable(size,unit='M'):
    try:
        size = float(size)
    except:
        return ''
    units = ['B', 'K', 'M', 'G', 'T', 'P', 'E']
    ui = units.index(string.upper(unit))

    while size > 1024:
        ui = ui + 1
        size = size / 1024
    size = float("%.1f" % size)

    if size % 1 == 0.0:
        return("%.0f%s" % (size, units[ui]))
    else:
        return("%.1f%s" % (size, units[ui]))

def longestStrLen(*strs):
    return int(reduce(lambda x, y: max(x, y), map(lambda x: len(x), strs)))

def stripSpaces(s):
    while string.find(s, '  ') != -1:
        s = string.replace(s, '  ', ' ')
    return s

def printMap(core_map):
    for dc in core_map.keys():
        print "Facility %s:\n" % dc
        for dvc in core_map[dc].keys():
            # map long names to shorter names for easier output formatting
            cpu_count = core_map[dc][dvc]["device_record"]["cpus"][0]["count"]
            cpu_type = core_map[dc][dvc]["device_record"]["cpus"][0]["cpu_model"]
            dev_name = core_map[dc][dvc]["device_record"]["dvc_desc"]
            dev_os = core_map[dc][dvc]["device_record"]["os_version"]
            dev_model = "%s / %s" % (core_map[dc][dvc]["device_record"]["dvc_mfg"], core_map[dc][dvc]["device_record"]["dvc_model"])
            dev_ip = core_map[dc][dvc]["device_record"]["management_ip"]
            dev_mem = core_map[dc][dvc]["device_record"]["ram_quantity"]
            dev_disks = ''
            dev_disk_tot = 0
            try:
                for stor in core_map[dc][dvc]["device_record"]["storage"]:
                    if stor["storage_media"][-4:] == "DISK" or stor["storage_media"][:4] == "RAID": 
                        dev_disk_tot = dev_disk_tot + (int(stor["storage_capacity"]) * int(stor["count"]))
                        if int(stor["count"]) > 1:
                            dev_disks = dev_disks + "/%s x %s " % (stor["count"], makeHumanReadable(stor["storage_capacity"], "M"))
                        else:
                            dev_disks = dev_disks + "/%s" % (makeHumanReadable(stor["storage_capacity"], "M"))
                dev_disks = dev_disks[1:] + " (%s)" % makeHumanReadable(dev_disk_tot, "M")
            except:
                dev_disks = 'None found'

            dev_cpu = "%s x %s / MEM: %s" % (cpu_count, stripSpaces(cpu_type), makeHumanReadable(dev_mem, "k"))
            print " | %s (%s) @ %s" % (dev_name, dev_os, dev_ip)
            print " |  - MODEL: %s" % (dev_model)
            print " |  - CPU/M: %s" % (dev_cpu)
            print " |  - DISKS: %s" % (dev_disks)
            print " `-" + "-" * (11 + longestStrLen(dev_model, dev_cpu, dev_disks))
            print "    %s\n" % (string.join(core_map[dc][dvc]["service_levels"],"\n    "))

def printTNSNames(tnsfile):
    try:
        print "tnsnames.ora:\n"
        for l in open(tnsfile, "r").readlines(): print l
        print "\n",
    except:
        print "ERROR: Couldn't read %s" % tnsfile

def printManagedHostCount(s):
    date = os.popen("date +%D").readline()
    print "\nManaged host count (as of %s): %s\n" % (string.strip(date), len(s.Device.getList()))

def printRealms(s):
    print "Realms:\n"
    for r in filter(lambda x: x != 'TRANSITIONAL', map(lambda x: x[1], s.Realm.getList())): print r
    print

if __name__ == '__main__':
    spin = initSpin("spin")
    core_map = mapCore(spin)
    printTNSNames("/var/opt/oracle/tnsnames.ora")
    printManagedHostCount(spin)
    printRealms(spin)
    printMap(core_map)

    ## TODO
    ## [x] Facilities & Realms
    ## [x] # of managed hosts
    ## truth=(DESCRIPTION=(ADDRESS=(HOST=arthur.fc.opsware.com)(PORT=1521)(PROTOCOL=tcp))(CONNECT_DATA=(SERVICE_NAME=truth)))
    ## [x] Oracle/truth (tnsnames.ora)
    ## [ ] Oracle/truth just like other components (ie, hw info (if under mgmt) etc)
    ## [ ] Oracle version
    ## [ ] SAS version (inventory)
    ## [ ] 7.0 architecture (slice,infrastructure,database,boot)

# tnsnames.ora
# facility / # of agents
#   core 1 (truth + others)
# fac 2 / # of agents
#   core 2 (truth, inf, slice, boot)
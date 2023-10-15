#!/opt/opsware/bin/python2
import sys
import time, os, string, re

sys.path.append("/opt/opsware/pylibs2")
import ConfigParser
import optparse
from optparse import OptionParser
import verify_dvc_rpms

from pytwist import *
from pytwist.com.opsware.server import *
from pytwist.com.opsware.search import Filter
from pytwist.com.opsware.swmgmt import SoftwarePolicyVO
from pytwist.com.opsware.swmgmt import SoftwarePolicyRef
from pytwist.com.opsware.swmgmt import SoftwarePolicyRPMItemData
from pytwist.com.opsware.swmgmt import SoftwarePolicyItemData
from pytwist.com.opsware.pkg import RPMService

#
# configurations
#
logf = None


def msg(s, args=None):
    if (args is not None): s = s % args
    sys.stdout.write(s)
    sys.stdout.flush()


def err(s, args=None):
    if (args is not None): s = s % args
    sys.stderr.write(s)
    sys.stderr.flush()


def log(s, args=None):
    if logf == None: return
    if (args is not None): s = s % args
    logf.write(s)
    logf.flush()


def getAllISoft_ByPlatform(plats, serversvc, archoption):
    fr = Filter()
    fr.expression = 'device_platform_name IN ["%s"]' % ('" "'.join(plats))
    srvrrefs = serversvc.findServerRefs(fr)
    log("Server Refs: %d\n" % len(srvrrefs))
    return getAllSoftwareForServers(srvrrefs, serversvc, archoption)


def getAllSoft_ByServerNameList(slist, plats, serversvc, archoption):
    count = 0
    sreflist = []
    while count < len(slist):
        snames = slist[count:count + 100]
        fr = Filter()
        fr.expression = '(device_display_name IN ["%s"]) & (device_platform_name IN ["%s"])' % (
        '" "'.join(snames), '" "'.join(plats))
        srvrrefs = serversvc.findServerRefs(fr)
        sreflist.extend(srvrrefs)
        count = count + 100
    log("Server List: %d\n" % len(sreflist))
    return getAllSoftwareForServers(sreflist, serversvc, archoption)


def getAllSoft_ByServerIdList(slist, plats, serversvc, archoption):
    count = 0
    sreflist = []
    while count < len(slist):
        snames = slist[count:count + 100]
        fr = Filter()
        fr.expression = '(dvc_id IN ["%s"]) & (device_platform_name IN ["%s"])' % (
        '" "'.join(snames), '" "'.join(plats))
        srvrrefs = serversvc.findServerRefs(fr)
        sreflist.extend(srvrrefs)
        count = count + 100
    log("Server List: %d" % len(sreflist))
    return getAllSoftwareForServers(sreflist, serversvc, archoption)


def getAllSoft_ByDeviceGroupNameList(glistnames, plats, dvcgrpsvc, serversvc, archoption):
    fr = Filter()
    fr.expression = '(device_group_rc_name IN ["%s"])' % ('" "'.join(glistnames))
    grprefs = dvcgrpsvc.findDeviceGroupRefs(fr)
    dvcs = dvcgrpsvc.getDevices(grprefs)
    snamelist = []
    for dvc in dvcs:
        snamelist.append(dvc.name)
    return getAllSoft_ByServerNameList(snamelist, plats, serversvc, archoption)


def getAllSoftwareForServers(srvrrefs, serversvc, archoption):
    epochmap = {}
    serversByRpm = {}  # Dictionary to map servers by rpm name and nvr tuple; serversByRPM = {rpmname:{nvr-1:[ser1,ser2],nvr-2:[ser3,ser4]}}
    for sref in srvrrefs:
        log("Getting Software List: for %s\n" % sref.name)
        isofts = serversvc.getInstalledSoftware(sref)
        log("Installed software list size: %d\n" % len(isofts))
        for s in isofts:
            #
            # print dir(s)
            # log("%s, %s, %s, %s, %s" % (s.getPackageName(), s.getName(), s.getDisplayName(), s.getRelease(), s.getVersion()))
            # format that is supposed to be saved as unit display name - <name>-[<epoch>:]<version>-<release>.<arch>
            dispname = s.getDisplayName()
            dispsplits = dispname.rsplit("-", 2)
            if len(dispsplits) < 3:
                # this occurs for zips and other types of packages, so log and continue
                # log("not a valid rpm : %s -- ignoring and continuing\n" % dispname)
                continue
            ep_ver_sps = dispsplits[1].split(":")
            if len(ep_ver_sps) > 1:
                epoch = ep_ver_sps[0]
                ver = ep_ver_sps[1]
            else:
                epoch = None
                ver = ep_ver_sps[0]

            rdispname = "%s-%s-%s" % (dispsplits[0], ver, dispsplits[2])
            nvr_tup = (epoch, ver, s.getRelease())
            arch = s.getDisplayName().split(".")[-1]
            dname = "%s.%s" % (s.getName(), arch)
            if archoption == 'strict':
                dnamelist = [dname]
            elif archoption == 'noarch':
                dnamelist = ["%s" % (s.getName())]
            else:
                if arch == 'noarch':
                    dnamelist = [dname, "%s.i386" % (s.getName()), "%s.x86_64" % (s.getName()),
                                 "%s.i686" % (s.getName())]
                else:
                    dnamelist = [dname, "%s.noarch" % (s.getName())]

            for dname in dnamelist:
                if serversByRpm.has_key(dname) == False:
                    serversByRpm[dname] = {nvr_tup: [sref.name]}
                    epochmap[rdispname] = epoch
                else:
                    # Update ServersByRpm Dictionary
                    serversByNvr = serversByRpm[dname]
                    if serversByNvr.has_key(nvr_tup) == False:
                        serversByNvr[nvr_tup] = [sref.name]
                    else:
                        serversByNvr.get(nvr_tup).append(sref.name)

    return serversByRpm, srvrrefs, epochmap


def getAllNeededRpms(chan_rpms, serversByRpm, epochmap, archoption, useepoch, skipServersWithRpmCountOption):
    needs = {}
    skips = {}
    serverMrcRpmsHm = {}  # Servers and the rpms contributed for MRC policy; {server1:[rpm1,rpm2],server2:[rpm1,rpm2,rpm3]}
    for rpmname in chan_rpms.keys():
        nvr_splits = rpmname.rsplit("-", 2)
        if len(nvr_splits) < 3:
            continue
        rel_splits = nvr_splits[2].rsplit(".", 1)
        if len(rel_splits) < 2:
            continue
        pkgname = nvr_splits[0]
        pkgver = nvr_splits[1]
        pkgrel = rel_splits[0]
        pkgarch = rel_splits[1]
        if useepoch == 1:
            epoch = chan_rpms.get(rpmname).getEpoch()
        else:
            epoch = None
        #
        # even though we know what epoch is for these rpm,
        # we wont use because the managed servers are not reporting epoch
        #
        nvr_tup = (None, pkgver, pkgrel)
        if archoption == "noarch":
            dname = "%s" % (pkgname)
        else:
            dname = "%s.%s" % (pkgname, pkgarch)
        # print "dname: %s" % dname
        if serversByRpm.has_key(dname):
            # print "Found dname: %s" % dname
            serversByNvr = serversByRpm.get(dname)
            allpkgnvrs = serversByNvr.keys()
            for nvr_t in allpkgnvrs:
                if verify_dvc_rpms.rpmvercmp_ur(tohash(nvr_tup), tohash(nvr_t)) != 0:
                    # if epoch is correct in packagenames that managed servers report
                    # then this would work. so leaving it here.
                    #
                    # if verify_dvc_rpms.rpmvercmp_ur(tohash(nvr_tup), tohash(nvr_t)) == 1:
                    # log("%s Need to be added to MRC\n" % (rpmname))
                    needs[rpmname] = chan_rpms.get(rpmname)
                    # Find all servers that have a different version of this channel rpm;
                    # Increment count for each of the servers to track number of rpms contributed toward mrc by each server.
                    serversList = serversByNvr[nvr_t]
                    for serverName in serversList:
                        if serverMrcRpmsHm.has_key(serverName):
                            serverMrcRpmsHm.get(serverName).append(rpmname)
                        else:
                            serverMrcRpmsHm[serverName] = [rpmname]
                else:
                    skips[rpmname] = chan_rpms.get(rpmname)

    log("Needed rpms dict size: %s \n" % len(needs.keys()))
    if skipServersWithRpmCountOption != -1:
        needs = filterRpmsBasedOnServerThreshold(needs, serverMrcRpmsHm, skipServersWithRpmCountOption)
        log("needed rpms dict size after filtering: %s \n" % len(needs.keys()))

    return needs


def tohash(nvr):
    return {"epoch": nvr[0], "ver": nvr[1], "rel": nvr[2]}


def findMRCSoftwarePolicy(swpname, folref, rpmvos, platformrefs, swpsvc, folsvc):
    # import pdb
    # pdb.set_trace()
    if folref == None:
        log("Cannot Find Folder: Please verify whether folderpath exisits and run again %s\n" % "/".join(folpathlist))
        raise Exception(
            "Cannot Find Folder: Please verify whether folderpath exisits and run again %s\n" % "/".join(folpathlist))

    swpf = Filter()
    swpf.expression = 'SoftwarePolicyVO.name IN ["%s"]' % swpname
    swprefs = swpsvc.findSoftwarePolicyRefs(swpf)

    swpvo = None
    for swpref in swprefs:
        swpvo = swpsvc.getSoftwarePolicyVO(swpref)
        if swpvo.folder.id == folref.id:
            break
        swpvo = None

    return swpvo


#
# getSoftwarePolicy, If its not there then it would create one
#
def getMRCSoftwarePolicy(swpname, folref, rpmvos, platformrefs, swpsvc, folsvc):
    # import pdb
    # pdb.set_trace()
    if folref == None:
        log("Cannot Find Folder: Please verify whether folderpath exisits and run again %s\n" % "/".join(folpathlist))
        raise Exception(
            "Cannot Find Folder: Please verify whether folderpath exisits and run again %s\n" % "/".join(folpathlist))

    swpf = Filter()
    swpf.expression = 'SoftwarePolicyVO.name IN ["%s"]' % swpname
    swprefs = swpsvc.findSoftwarePolicyRefs(swpf)

    swpvo = None
    for swpref in swprefs:
        swpvo = swpsvc.getSoftwarePolicyVO(swpref)
        if swpvo.folder.id == folref.id:
            break
        swpvo = None

    if swpvo == None:
        # create Software Policy VO
        swpvo = SoftwarePolicyVO()
        swpvo.folder = folref
        swpvo.name = swpname
        swpvo.platforms = platformrefs
        swpvo.lifecycle = "AVAILABLE"
        swpvo.setManualUninstall(True)
        swpvo = swpsvc.create(swpvo)

    if swpvo == None:
        raise Exception("Cannot Create Software Policy : %s" % swpname)

    rpmrefs = []
    for vo in rpmvos:
        rpmrefs.append(vo.ref)

    if len(rpmrefs) > 0:
        swpvo.platforms = platformrefs
        swpvo.setSoftwarePolicyItems(rpmrefs)
        swpvo.setManualUninstall(True)
        swpvo1 = swpsvc.update(swpvo.ref, swpvo, 0, 1)
        idatal = swpvo1.installableItemData
        idataln = []
        for idata in idatal:
            idata.remediateMode = "UPDATE_ONLY"
            idataln.append(idata)
        swpvo1.installableItemData = idataln
        swpvo1.uninstallableItemData = []
        swpvo = swpsvc.update(swpvo1.ref, swpvo1, 0, 1)
    return swpvo


def getPackageRefs(pkgnames, plat, folname, searchsvc):
    f = Filter()
    f.expression = '(software_display_name IN %s )&(software_platform_name IN ["%s"] )&(software_folder_name IN ["%s"] )' % (
    " ".join(pkgnames), plat, folname)
    f.objectType = 'software_unit'
    rpmrefs = searchsvc.findObjRefs(f)
    return rpmrefs


def load_config(conffile):
    config = ConfigParser.ConfigParser()
    result = config.read(conffile)
    if len(result) == 0:
        raise Exception("Cannot Read config File %s" % conffile)

    return config


def calcunfoundrpms(sou, dest):
    dmap = {}
    for rref in dest:
        dmap[rref.name] = None
    for s in sou:
        if dmap.has_key(s) == False:
            log(" RPM: %s unfound in HPSA \n" % s)


def getPlatformFromConfigBySwpName(swpname, swpsvc, rpmsvc):
    swpf = Filter()
    swpf.expression = 'SoftwarePolicyVO.name IN ["%s"]' % swpname
    swprefs = swpsvc.findSoftwarePolicyRefs(swpf)
    if len(swprefs) <= 0:
        raise Exception(
            "Cannot Find Any Policy with name: %s, Please corrent it in config file and execute it" % swpname)
    fref, platforms, refname, refid, rpmhm = getPlatformsAndFolder(swprefs[0], swpsvc, rpmsvc)
    # print len(rpmhm)
    return fref, platforms, refname, refid, rpmhm


def getPlatformFromConfigBySwpId(swpid, swpsvc, rpmsvc):
    swpref = SoftwarePolicyRef()
    swpref.id = long(swpid)
    fref, platforms, refname, refid, rpmhm = getPlatformsAndFolder(swpref, swpsvc, rpmsvc)
    # print len(d)
    return fref, platforms, refname, refid, rpmhm


def getPlatformsAndFolder(swpref, swpsvc, rpmsvc):
    rpmhm = {}
    swpvo = swpsvc.getSoftwarePolicyVO(swpref)
    fref = swpvo.folder
    platforms = swpvo.platforms
    getAllRpms(swpvo, rpmhm, swpsvc, rpmsvc)

    if len(platforms) <= 0:
        raise Exception(" Cannot Work on a software policy with Zero Platforms associated. ")

    return fref, platforms, swpvo.ref.name, swpvo.ref.id, rpmhm


def convertRefsToVos(rpmhm, rpmsvc):
    rpmrefs = []
    rpmvohm = {}
    for rpmname in rpmhm.keys():
        rpmrefs.append(rpmhm.get(rpmname))
        if len(rpmrefs) > 100:
            rpmvos = rpmsvc.getRPMVOs(rpmrefs)
            for vo in rpmvos:
                rpmvohm[vo.ref.name] = vo
            rpmrefs = []
    if len(rpmrefs) > 0:
        rpmvos = rpmsvc.getRPMVOs(rpmrefs)
        for vo in rpmvos:
            rpmvohm[vo.ref.name] = vo
    return rpmvohm


def filterRpmsByPlatform(rpmvohm, plats):
    plat_rpmvohm = {}
    for rpmvo_key in rpmvohm.keys():
        rpm_plats = rpmvohm[rpmvo_key].getPlatforms()
        plat_match = False
        for rpm_plat in rpm_plats:
            for plat in plats:
                if rpm_plat.id == plat.id:
                    plat_match = True
            if plat_match:
                plat_rpmvohm[rpmvo_key] = rpmvohm[rpmvo_key]
    return plat_rpmvohm


def getAllRpms(swpvo, rpmhm, swpsvc, rpmsvc):
    for idata in swpvo.installableItemData:
        if isinstance(idata, SoftwarePolicyRPMItemData):
            rpmref = idata.policyItem
            rpmhm[rpmref.name] = rpmref
        elif isinstance(idata, SoftwarePolicyItemData):
            if idata.policyItem:
                if not isinstance(idata.policyItem, SoftwarePolicyRef):
                    continue
            ivo = swpsvc.getSoftwarePolicyVO(idata.policyItem)
            getAllRpms(ivo, rpmhm, swpsvc, rpmsvc)


def keepOnlyLatestRpms(rpmhm):
    nvrhm = {}
    rpmrefhm = {}
    for rpmname in rpmhm.keys():
        # log("Working on %s %s %s\n" % (rpmname, len(nvrhm.keys()), len(rpmrefhm.keys())))
        nvr_splits = rpmname.rsplit("-", 2)
        if len(nvr_splits) < 3:
            continue
        rel_splits = nvr_splits[2].rsplit(".", 1)
        if len(rel_splits) < 2:
            continue
        pkgname = nvr_splits[0]
        pkgver = nvr_splits[1]
        pkgrel = rel_splits[0]
        pkgarch = rel_splits[1]
        epoch = rpmhm.get(rpmname).getEpoch()
        dname = "%s.%s" % (pkgname, pkgarch)
        # log("Dname: %s\n" % dname)
        nvr_tup = (epoch, pkgver, pkgrel)
        if nvrhm.has_key(dname):
            nvr_t = nvrhm.get(dname)
            # log("Comparing %s - %s with %s\n" % (dname, nvr_tup, nvr_t))
            if verify_dvc_rpms.rpmvercmp_ur(tohash(nvr_tup), tohash(nvr_t)) == 1:
                log("Found a latest rpm %s %s, so replacing\n" % (nvr_tup, nvr_t))
                nvrhm[dname] = nvr_tup
                rpmrefhm[dname] = rpmhm.get(rpmname)
        else:
            nvrhm[dname] = nvr_tup
            rpmrefhm[dname] = rpmhm.get(rpmname)

    rethm = {}
    for rpmvo in rpmrefhm.values():
        rethm[rpmvo.ref.name] = rpmvo
    return rethm


def deleteAllRIUsForDevicesByPolId(srvrrefs, swpolid):
    from coglib import spinwrapper
    from coglib import certmaster
    ctx = certmaster.getContextByName("spin", "spin.srv", "opsware-ca.crt")
    s = spinwrapper.SpinWrapper("https://spin:1004", ctx=ctx)

    for dvcref in srvrrefs:
        dvcid = dvcref.id
        d = s.Device.get(dvcid)
        children = d.getChildren(child_class="AppPolicyRIU", restrict={'app_policy_id': swpolid})

        for chld in children:
            try:
                log("* deleting RIU for unit %s on device %s in swpol %s:     %s\n" % (
                chld['unit_id'], dvcid, swpolid, chld.delete()))
                # log("* deleting RIU for unit %s on device %s in swpol %s    \n" % (chld['unit_id'],dvcid, swpolid))
            except Exception, e:
                if debug: print
                "! exception: %s" % e


def filterRpmsBasedOnServerThreshold(needrpms, serverMrcRpmsHm, skipServersWithRpmCountOption):
    log("RPM Threshold per server is enabled in Configuration file. Filtering servers contributing more than %s rpms \n" % skipServersWithRpmCountOption)
    serverMrcRpmsCt = {}
    for k, v in serverMrcRpmsHm.iteritems():
        serverMrcRpmsCt[k] = len(v)
    log("Servers contributing rpms for MRC policy %s\n" % serverMrcRpmsCt)
    skipServersList = []
    for k, v in serverMrcRpmsCt.iteritems():
        if v > skipServersWithRpmCountOption:
            skipServersList.append(k)
    log("Skipping servers %s from mrc policy creation because of rpm threshold \n" % skipServersList)
    if len(skipServersList) != 0:
        for serverRef in skipServersList:
            if serverMrcRpmsHm.has_key(serverRef):
                del serverMrcRpmsHm[serverRef]
        filteredRpms = set([])
        for v in serverMrcRpmsHm.values():
            filteredRpms.update(v)
        log("rpms list size after filtering %d \n" % len(filteredRpms))
        needrpmslist = needrpms.keys()
        for rpm in needrpmslist:
            if rpm not in filteredRpms:
                del needrpms[rpm]
    return needrpms


def main():
    global logf
    if len(sys.argv) < 2:
        log("Configuration File is not given as command arg so using mrc_rhn.conf as config file")
        conffile = "mrc_calc.conf"
    else:
        conffile = sys.argv[1]

    config = load_config(conffile)
    try:
        logfile = config.get("LOGGING", "logfile")
    except:
        logfile = "mrc_calc.log"
    logf = open(logfile, "a")
    log(" ******************************************************************* \n")
    log(" Started New MRC Session \n")

    ts = twistserver.TwistServer()
    swpservice = ts.swmgmt.SoftwarePolicyService
    serversvc = ts.server.ServerService
    pfsvc = ts.device.PlatformService
    folsvc = ts.folder.FolderService
    searchsvc = ts.search.SearchService
    platformsvc = ts.device.PlatformService
    dvcgrpsvc = ts.device.DeviceGroupService
    rpmsvc = ts.pkg.RPMService

    if config.has_section("softwarepolicy") == False:
        raise Exception("Please configure softwarepolicy section in config file and try it again")

    useepoch = 0
    if config.has_option("softwarepolicy", "useepoch"):
        useepoch = 1

    mrcpolname = None
    if config.has_option("softwarepolicy", "resultpolname"):
        mrcpolname = config.get("softwarepolicy", "resultpolname")

    if config.has_option("softwarepolicy", "name"):
        folref, plats, swpname, swpolid, rpmhm = getPlatformFromConfigBySwpName(config.get("softwarepolicy", "name"),
                                                                                swpservice, rpmsvc)
    elif config.has_option("softwarepolicy", "id"):
        folref, plats, swpname, swpolid, rpmhm = getPlatformFromConfigBySwpId(config.get("softwarepolicy", "id"),
                                                                              swpservice, rpmsvc)
    else:
        raise Exception("Please configure softwarepolicy section in config file and try it again")

    all_rpmvohm = convertRefsToVos(rpmhm, rpmsvc)
    log("Swp: %s Total Packges in Policy: %d\n" % (swpname, len(rpmhm)))
    rpmvohm = filterRpmsByPlatform(all_rpmvohm, plats)
    log("Swp: %s Total Platform matches Packges in Policy: %d\n" % (swpname, len(rpmvohm)))

    rethm = keepOnlyLatestRpms(rpmvohm)
    rpmhm = rethm
    log("Swp: %s Latest Packages in Policy: %d\n" % (swpname, len(rpmhm)))
    if len(rpmhm.keys()) <= 0:
        log("Nothing to Do. Swp Policy %s does not contain any packages\n" % swpname);
        sys.exit(1)

    srvrnamelist = []
    dvcgrpnamelist = []
    srvridlist = []
    if config.has_section("devices"):
        if config.has_option("devices", "names"):
            srvrnamelist = eval(config.get("devices", "names"))
        elif config.has_option("devices", "ids"):
            srvridlist = eval(config.get("devices", "ids"))
    elif config.has_section("devicegroups"):
        if config.has_option("devicegroups", "names"):
            dvcgrpnamelist = eval(config.get("devicegroups", "names"))

    # print "srvridlist; %s " % len(srvridlist)
    archoption = "allarchs"
    if config.has_section("architecture"):
        if config.has_option("architecture", "archoption"):
            archoption = config.get("architecture", "archoption")

    skipServersWithRpmCountOption = -1
    if config.has_section("exceptions"):
        if config.has_option("exceptions", "skipServersContributingRpms"):
            skipServersWithRpmCountOption = long(config.get("exceptions", "skipServersContributingRpms"))

    if mrcpolname == None:
        mrcpolname = "MRC_%s" % swpname
    epochcount = 0

    platformNames = []
    for platref in plats:
        platformNames.append(platref.name)

    if len(srvrnamelist) > 0:
        serversByRpm, srvrrefs, epochmap = getAllSoft_ByServerNameList(srvrnamelist, platformNames, serversvc,
                                                                       archoption)
    elif len(dvcgrpnamelist) > 0:
        # print dvcgrpnamelist
        serversByRpm, srvrrefs, epochmap = getAllSoft_ByDeviceGroupNameList(dvcgrpnamelist, platformNames, dvcgrpsvc,
                                                                            serversvc, archoption)
    elif len(srvridlist) > 0:
        serversByRpm, srvrrefs, epochmap = getAllSoft_ByServerIdList(srvridlist, platformNames, serversvc, archoption)
    else:
        serversByRpm, srvrrefs, epochmap = getAllISoft_ByPlatform(platformNames, serversvc, archoption)

    if len(serversByRpm.keys()) <= 0:
        print
        "No packages found for devices"
        sys.exit(1)

    log("Servers have %s unique packages\n" % len(serversByRpm.keys()))
    log("Calculating MRC for platforms %s\n" % (', '.join(platformNames)))
    chan_rpms = rpmhm.keys()
    log("policy %s has %d unique rpms in it.\ncalculating chan_nvr and chan_n...\n", (swpname, len(chan_rpms)))
    log("Calculating needed rpms for MRC policy: %s\n" % mrcpolname)

    needrpms = getAllNeededRpms(rpmhm, serversByRpm, epochmap, archoption, useepoch, skipServersWithRpmCountOption)

    log("List of Rpms for MRC policy: %s\n" % mrcpolname)
    for rpm in needrpms.keys():
        log("%s Need to be added to MRC\n" % (rpm))
    log("End of Rpms list \n")

    #
    # delete all RIUs for give devices and swpolicy
    #
    deleteAllRIUsForDevicesByPolId(srvrrefs, swpolid)
    swpvo = findMRCSoftwarePolicy(mrcpolname, folref, needrpms.values(), plats, swpservice, folsvc)
    if swpvo != None:
        deleteAllRIUsForDevicesByPolId(srvrrefs, swpvo.ref.id)

    swpvo = getMRCSoftwarePolicy(mrcpolname, folref, needrpms.values(), plats, swpservice, folsvc)
    log("Create Software Policy: %s\n" % swpvo.name)
    logf.close()


if __name__ == "__main__":
    main()



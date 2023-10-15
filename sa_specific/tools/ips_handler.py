import os
import time
import string
import shutil
import pickle
import logging

from coglib import pkg_handler
from coglib.unix import unix_common
from opsware_common import errors
from coglib import platform
from coglib.unix import ipsinfo
from coglib import wordclient

# initialize logging
IPS_TYPE = "IPS"
logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s')
logger = logging.getLogger("ips_handler.logger")
# set default log level
logger.setLevel(logging.ERROR)


# -----------------------------------------------------------------------------
# METHOD:  makeErrorText
# RETURN:  error text string
# NOTES:   An error_text is in the form of 'AGENT_ERROR_Xxx : some detail'
# -----------------------------------------------------------------------------
def makeErrorText(agent_error_code, error_details):
    return '%s : %s' % (agent_error_code, error_details)


# -----------------------------------------------------------------------------
# METHOD:  localFileNeedsRefresh
# RETURN:  0 if local file is current with word file; otherwise, non-zero
#          -DK Solaris 11 metadata is unique by file name, If it exists we don't need a new one.
# -----------------------------------------------------------------------------
def localFileNeedsRefresh(local_file_path):
    refresh = 1
    # Return now if local file does not exist or is zero length
    if not os.path.isfile(local_file_path):
        return refresh
    if os.path.getsize(local_file_path) == 0:
        logger.debug("Removing file with zero size %s " % local_file_path)
        os.unlink(local_file_path)
        return refresh

    # if the file is here then it is current.
    refresh = 0
    return refresh


# -----------------------------------------------------------------------------
# METHOD:  sol11MetaPrime - returns the current metadata filename
# NOTES:   This method can throw a cogbot.packageHandlerError exception
# -----------------------------------------------------------------------------
def sol11MetaPrime(metaFileDir, error_text=None):
    local_file_path = os.path.join(metaFileDir, 'sol11MetaFileNameFile')
    logger.debug("Called sol11metaPrime. tmp word file patch is %s" % local_file_path)

    found = createDirIfNotExists(metaFileDir)
    if not found:
        raise errors.OpswareError('cogbot.packageHandlerError',
                                  {'results': "DK - agent/metadata directory not found, or able to create!"})
    try:
        wordclient.urlRetrieve('https://theword:1003/wordbot.py?file=1&ips_metadata=repo', local_file_path)
    except:
        if error_text is None:
            error_text = makeErrorText('AGENT_ERROR_PATCH_IPS_SCAN_ERROR', 'error downloading %s' % local_file_path)
        raise errors.OpswareError('cogbot.packageHandlerError', {'results': error_text})

    fname = 'unfound'
    FILE = open(local_file_path, "r")
    try:
        while FILE:
            line = FILE.readline()
            if line.find('repository.zip'):
                fname = line.strip()
                break
        if fname == 'unfound':
            raise errors.OpswareError('cogbot.packageHandlerError',
                                      {'results': 'Failed to get Solaris meta-data file name.'})
    finally:
        FILE.close()

    return fname


def cleanOldMetaDataFiles(metaDataDir):
    logger.debug("called cleanOldMetaDataFiles on dir %s" % metaDataDir)
    dirList = os.listdir(metaDataDir)
    for fname in dirList:
        # print fname
        if fname.find("repository.zip") > -1:
            fpath = "%s/%s" % (metaDataDir, fname)
            if os.path.isfile(fpath):
                logger.debug("deleting old agent metadata %s" % fpath)
                os.unlink(fpath)


# -----------------------------------------------------------------------------
# METHOD:  downloadWordFileToLocalFile
# NOTES:   This method can throw a cogbot.packageHandlerError exception
#           Get the specificed solaris 11 metadata file,
# -----------------------------------------------------------------------------
def downloadWordFile(metadata_file_name, local_file_path, error_text=None):
    # downloadWordFile(metadata_file_name, local_file_path, tmp_error_text)
    try:
        urlstr = 'https://theword:1003/wordbot.py?file=1&ips_metadata=%s' % (metadata_file_name)
        logger.debug("attempting metadata download using url %s to local file %s" % (urlstr, local_file_path))
        wordclient.urlRetrieve(urlstr, local_file_path)
    except:
        if error_text is None:
            error_text = makeErrorText('AGENT_ERROR_PATCH_IPS_SCAN_ERROR', 'error downloading %s' % metadata_file_name)
        raise errors.OpswareError('cogbot.packageHandlerError', {'results': error_text})


# -----------------------------------------------------------------------------
# METHOD:  createDirIfNotExists
# RETURN:  1 if exists or is created successfully; otherwise, 0
# -----------------------------------------------------------------------------
def createDirIfNotExists(path):
    found = 0
    try:
        if not os.path.isdir(path):
            os.makedirs(path)
        found = 1
    except:
        pass
    return found


# class defining IPS unit representation.
# used both for upload and reporting of a package by bs_hardware.
class IPSUnit(pkg_handler.PackageUnit):
    ipsstr = IPS_TYPE

    def __init__(self, path="", name="", fmri="", status="", depend="", version="", branch="", build_release="",
                 software_release="", des="", manifest="", publisher=""):
        pkg_handler.PackageUnit.__init__(self, path, des)
        self.name = name
        self.unit_name = name
        self.fmri = fmri
        self.status = status
        self.publisher = ""
        self.manifest = []
        self.depend = depend
        self.version = version
        self.branch = branch
        self.build_release = build_release
        self.manifest = manifest
        self.publisher = publisher
        self.software_release = software_release

    def getType(self):
        return IPSUnit.ipsstr

    # this is used by bs_software
    def getUniqueName(self):
        # QC 145435 : Sometimes branch and build_release might be None.
        # 'ips info' also specify for branch 'None', so it is ok to display 'None'
        # return self.name + "@" + self.version + "," + str(self.build_release) + "-"  + str(self.branch)
        # return self.name + "@" + self.version + "," + str(self.build_release) + "-"  + str(self.branch)
        # QC 145749: Solaris 11 Agent code does not report FMRI timestamp
        # seems that solaris repo have republished packages in its repo, so we are returning all the data
        # including the timestamps
        pkg_index = ipsinfo.gen_indexes(self.fmri)
        return self.fmri[pkg_index[1]:]

    def getVersion(self):
        # QC 145435 : Sometimes branch and build_release might be None.
        # 'ips info' also specify for branch 'None', so it is ok to display 'None'
        # return self.version + "," + str(self.build_release) + "-"  + str(self.branch)
        # QC 145749: Solaris 11 Agent code does not report FMRI timestamp
        # seems that solaris repo have republished packages in its repo, so we are returning all the data
        # including the timestamps
        pkg_index = ipsinfo.gen_indexes(self.fmri)
        return self.fmri[pkg_index[0] + 1:]

    # QC 144844 : bs_software fails to report upgraded packages
    def getFileName(self):
        return self.getUniqueName()

    def getCommonName(self):
        return self.name

    def getRelease(self):
        return self.software_release

    def readDescription(self):
        return self.des

    # entry point for upload process. this method returns an IPSUnit object for the file passed.
    # the file has to be created with pkgrecv -a .
    #    @staticmethod
    def createFromFile(path):

        ipsdata = ipsinfo.ipsinfo(path)
        ipsinst = ipsdata[0]

        unit_name = ipsinst.get("unit_name")
        fmri = ipsinst.get("fmri")
        depend = ipsinst.get("depend")
        publisher = ipsinst.get("publisher")
        manifest = ipsinst.get("manifest")
        version, build_release, branch = ipsinfo.getVersionBranch(fmri)

        return IPSUnit(path=path, name=unit_name, fmri=fmri, depend=depend, version=version, branch=branch,
                       build_release=build_release, manifest=manifest, publisher=publisher)

    createFromFile = staticmethod(createFromFile)

    def install(self):
        ### TO ADD INSTALL
        if platform.os_type != platform.solaris:
            raise errors.OpswareError("cogbot.packageHandlerError", {"handler": "ips_handler",
                                                                     "results": "Cannot install IPS packages on non-solaris platforms"})

    def remove(self):
        ### TO ADD REMOVE
        if platform.os_type != platform.solaris:
            raise errors.OpswareError("cogbot.packageHandlerError", {"handler": "ips_handler",
                                                                     "results": "Cannot uninstall IPS packages on non-solaris platforms"})


# IPS package handler
class IPSHandler(pkg_handler.PackageHandler):
    handled_types = [IPS_TYPE]
    ## to add here the commands for cli
    pkg_cli = unix_common.findCommand(["/usr/bin/pkg"], "pkg")

    env_cmd_str = "unset PYTHONPATH; unset LD_LIBRARY_PATH;"

    def __init__(self):
        pkg_handler.PackageHandler.__init__(self)

    def claim(self, path, test=0):
        try:
            output = ipsinfo.ipsinfo(path)
            name = output.get("unit_name")
            fmri = output.get("fmri")
            depend = output.get("depend")
            publisher = output.get("publisher")
            return IPSUnit(name=name, fmri=fmri, depend=depend, publisher=publisher)
        except:
            pass

    # -----------------------------------------------------------------------------
    # METHOD:  checkScanEngineFiles
    # R
    #          Also, this method can throw a cogbot.packageHandlerError exception
    # -----------------------------------------------------------------------------
    # Check if patch database files are up to date.
    def checkSolMetaFiles(self):

        agent_var_lc_path = os.path.join('/opt', 'opsware')
        agent_lc_path = os.path.join(agent_var_lc_path, 'agent')
        metaFileDir = os.path.join(agent_lc_path, 'metadata')

        # Check if patch database files are up to date.
        try:

            metadata_file_name = sol11MetaPrime(metaFileDir)
            logger.debug("metadata file name is %s" % metadata_file_name)

        except:
            # print "DK - Patch Unit list  go boom "
            error_text = makeErrorText('AGENT_ERROR_PATCH_VERIFYING_PATCH_DATABASE',
                                       'error getting Solaris 11 metadata file name from word')
            raise errors.OpswareError('cogbot.packageHandlerError', {'results': error_text})

        error_text = None
        if metadata_file_name:

            local_file_path = os.path.join(agent_var_lc_path, 'agent/metadata', metadata_file_name)
            refresh = localFileNeedsRefresh(local_file_path)
            if refresh:
                tmp_error_text = makeErrorText('AGENT_ERROR_PATCH_VERIFYING_PATCH_DATABASE',
                                               'error downloading %s' % metadata_file_name)
                logger.debug("Metadata updated needed! Download file %s  to %s" % (metadata_file_name, local_file_path))
                cleanOldMetaDataFiles(metaFileDir)
                downloadWordFile(metadata_file_name, local_file_path, tmp_error_text)
                # Unzip newly downloaded repo so we can set it up as a repository
                unzip_cli = unix_common.findCommand([os.path.join(platform.Platform().lc_path, 'bin', 'unzip')],
                                                    'unzip')
                repoDir = os.path.join(metaFileDir, 'extr')
                if os.path.exists(repoDir):
                    logger.debug("delete old fake repo dir %s " % repoDir)
                    shutil.rmtree(repoDir)
                    logger.debug("old fake repo dir %s removed" % repoDir)
                cmd = '%s -oqd %s %s < /dev/null' % (unzip_cli, repoDir, '%s' % local_file_path)
                (output, result) = unix_common.cmdCapture(cmd)
                logger.debug("repo unzipped")
                logger.debug("REPODIR = %s" % repoDir)
                logger.debug("output = %s, result = %s" % (output, result))
            else:
                logger.debug("No download for %s, it is up to date!" % (local_file_path))

            found = 1
            if not found:
                error_text = makeErrorText('AGENT_ERROR_PATCH_VERIFYING_PATCH_DATABASE', 'IPS patch database not found')

        else:
            error_text = makeErrorText('AGENT_ERROR_PATCH_VERIFYING_PATCH_DATABASE', 'IPS patch database not found')
        if error_text:
            raise errors.OpswareError('cogbot.packageHandlerError', {'results': error_text})

        return refresh

    def backupIPSConfig(self):
        """
            Backup the existing config file /var/pkg/pkg5.image
        """
        logger.debug("backupIPSConfig")
        src_cfg = '/var/pkg/pkg5.image'
        dst_cfg = os.path.join('/var/pkg/', 'pkg5.image.%s' % str(time.time()))
        if os.path.exists(src_cfg):
            shutil.copy2(src_cfg, dst_cfg)
            logger.debug("%s copied to %s" % (src_cfg, dst_cfg))
            return dst_cfg
        else:
            raise Exception("%s not found, unable to do backup" % src_cfg)

    def restoreIPSConfig(self, backup_file):
        """
            Restores the given backup file as /var/pkg/pkg5.image
        """
        logger.debug("restoreIPSConfig backup_file = %s" % backup_file)
        if os.path.exists(backup_file):
            orig_file = '/var/pkg/pkg5.image'
            shutil.copy2(backup_file, orig_file)
            logger.debug("%s file restored successfulyy" % orig_file)
        else:
            raise Exception("%s doesn't exist, can't restore the pkg5.image file" % backup_file)

    def getExistingPublishers(self):
        """
            Returns the list of existing publishers on the Solaris11 machine
        """
        publishers = []
        logger.debug("getExistingPublishers")
        cmd = self.env_cmd_str + "pkg publisher"
        (output, result) = unix_common.cmdCapture(cmd)
        logger.debug("output = %s, result = %s" % (output, result))
        if not result:
            publishers = self.getPublishersFromOutput(output)
        logger.debug("publishers = %s" % publishers)
        return publishers

    def getPublishersFromOutput(self, output):
        """
            Parses the output of the 'pkg publisher' command and returns the list of publishers from this output
        """
        publishers = []
        if len(output) == 1:  # only the header "PUBLISHER  TYPE STATUS URI] was returned by the command
            return publishers
        for i in range(1, len(output)):
            words = string.split(output[i])
            if not words[0] in publishers:  # the first word on each line is the publisher
                publishers.append(words[0])
        return publishers

    def removePublishers(self, publishers):
        """
            Removes the given list of publishers from the Solaris11 machine
        """
        logger.debug("removePublishers")
        if publishers:
            cmd = self.env_cmd_str + "pkg unset-publisher %s" % string.join(publishers)
            logger.debug("cmd = %s" % cmd)
            (output, result) = unix_common.cmdCapture(cmd)
            logger.debug("output = %s, result = %s" % (output, result))
            return result

    def refreshSystemRepository(self):
        """
            Restore publisher for non-global zones
        """
        cmd = "svcadm refresh system-repository"
        logger.debug("cmd = %s" % cmd)
        (output, result) = unix_common.cmdCapture(cmd)
        logger.debug("output = %s, result = %s" % (output, result))

    def setupFakeRepo(self, fake_repo_dir, refresh):
        """
            Sets up the downloaded fake repository from the fake_repo_dir.
            The executed commands are :
                pkg rebuild -s `fake_repo_dir`
                pkgrepo info -s `fake_repo_dir`  to extract the list of publisher
                for each publisher execute pkg set-publisher -g `fake_repo_dir` `publisher`
        """
        if refresh:
            cmd = self.env_cmd_str + "pkgrepo rebuild --no-index -s %s" % fake_repo_dir
            o, r = unix_common.cmdCapture(cmd)
            if r:
                logger.debug("Unable to run command : %s " % cmd)
                return

        # get publishers from fake repo
        cmd = self.env_cmd_str + "pkgrepo info -s %s" % fake_repo_dir
        o, r = unix_common.cmdCapture(cmd)
        if r:
            logger.debug("Unable to run command : %s " % cmd)
            return
        publishers = self.getPublishersFromOutput(o)
        for p in publishers:
            cmd = self.env_cmd_str + "pkg set-publisher -g %s %s" % (fake_repo_dir, p)
            o, r = unix_common.cmdCapture(cmd)
            if r:
                logger.debug("unable to set publisher %s ; output = %s" % (p, o))

    def recommendedList(self, pkg_hash):
        p, status = unix_common.cmdCapture(self.env_cmd_str + "pkg version")

        # if this isn't an IPS compatible server, abort and return empty recommended_hash
        if status != 0:
            return

        repo_dir = "/opt/opsware/agent/metadata/extr"

        logger.debug("recommended list called with self %s" % self)
        refresh = self.checkSolMetaFiles()
        backup_file = None

        backup_file = self.backupIPSConfig()

        try:
            publishers = self.getExistingPublishers()
            self.removePublishers(publishers)
            self.setupFakeRepo(repo_dir, refresh)

            (l, status) = self.extractUpdateInfo()

            for u in l:
                unit = IPSUnit(u["Name"], u["Name"], fmri=u["FMRI"], status="recommended", \
                               branch=u['Branch'], version=u['Version'], build_release=u['Build Release'],
                               software_release=u['Software Release'])
                pkg_hash[unit.getUniqueName()] = unit

        finally:
            if backup_file:
                self.restoreIPSConfig(backup_file)
                self.refreshSystemRepository()

    def installedList(self, pkg_hash):

        (l, status) = self.extractPackageInfo()

        for u in l:
            unit = IPSUnit(name=u["Name"], path=u["Name"], fmri=u["FMRI"], status=u["Summary"], \
                           branch=u['Branch'], version=u['Version'], build_release=u['Build Release'])
            pkg_hash[u["FMRI"]] = unit

        # On Solaris 10 we have to be silent about IPS packages.
        # Given that IPS is standard on Solaris 11 we assume that pkg command is there.
        if ((status != 0) and (not platform.Platform().getOsVersion().startswith("SunOS 5.10"))):
            # raise the error
            raise errors.OpswareError("cogbot.PackageHandlerError",
                                      {"handler": "ips_handler",
                                       "command": IPSHandler.pkg_cli + " info",
                                       "results": "unable to extract installed package list: %s" % (status)})

    def extractPackageInfo(self):
        cmd = self.env_cmd_str + IPSHandler.pkg_cli + " info"
        #       These are all the attributes that cli gives for a package
        #       We don't need all of them since many are derived from FMRI. Still
        #       for parsing we will use all of them
        #        ['Name', 'Summary', 'Description', 'Category',
        #         'State', 'Publisher', 'Version','Build Release',
        #         'Branch','Packaging Date', 'Size','FMRI']
        #       This is sample of output:
        #                 Name: x11/library/toolkit/libxt
        #              Summary: libXt - X Toolkit Intrinsics library
        #          Description: The X Toolkit Intrinsics are a programming library tailored to
        #                       the special requirements of user interface construction within a
        #                       network window system, specifically the X Window System.  The X
        #                       Toolkit Intrinsics and a widget set such as the Athena Widgets
        #                       (Xaw) or Motif (Xm) make up an X Toolkit.
        #             Category: System/X11
        #                State: Installed
        #            Publisher: solaris
        #              Version: 1.0.9
        #        Build Release: 5.11
        #               Branch: 0.175.0.0.0.0.1215
        #       Packaging Date: September 27, 2011 12:43:51 PM
        #                 Size: 1.69 MB
        #                 FMRI: pkg://solaris/x11/library/toolkit/libxt@1.0.9,5.11-0.175.0.0.0.0.1215:20110927T124351Z

        ipsattr = ['Name', 'Summary', 'Description', 'Category',
                   'State', 'Publisher', 'Version', 'Build Release',
                   'Branch', 'Packaging Date', 'Size', 'FMRI']

        # get info for installed packages
        p, status = unix_common.cmdCapture(cmd)
        pkg_list = []
        if status == 0:
            d = {}

            for line in p:
                line = string.strip(line)
                line = string.split(line, ':', 1)
                if line[0] in ipsattr:
                    d[line[0]] = string.strip(line[1])
                elif line[0] == '':
                    pkg_list.append(d)
                    d = {}
            if d:
                pkg_list.append(d)
        # print "pkg list = %s" % pkg_list
        return (pkg_list, status)

    def extractUpdateInfo(self):
        """
        Run a sub process to get packages recommended for this server
        """

        # the sub process will need the path to the ips_recommended module,
        # which shares the same path as the current module, ips_handler
        local_python_path = os.path.dirname(os.path.abspath(__file__))
        recommended_script = "ips_recommended"
        recommended_script_path = os.path.join(local_python_path, recommended_script)

        # create output file location  for results
        results_file_name = "recommended_ips.pickle"
        results_file = os.path.join(platform.Platform.var_lc_path, "agent", results_file_name)

        # create command line options
        log_dir = platform.Platform.log_path
        log_file_name = "ips_recommended.log"
        recommended_input_params = "--logDir %s --logFile %s --outputFile %s" % \
                                   (log_dir, log_file_name, results_file)

        # execute ips_recommended as sub process against native python.  Native python libraries
        # are required to perform recommended update
        python_exe = '/usr/bin/python'
        recommended_cmd = "%s %s %s" % (python_exe, recommended_script_path, recommended_input_params)
        p, status = unix_common.cmdCapture("%s %s" % (self.env_cmd_str, recommended_cmd))

        logger.info("Finished executing %s" % recommended_cmd)

        # report status and any standard out from sub process
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("update command output = %s; with a status of %s" % (p, status))

        pkg_list = []

        if status == 0:
            # open the output file and retrieve the results
            if os.path.exists(results_file):
                try:
                    # open the pickle file containing recommended results
                    file_handler = open(results_file, 'r')
                    p = pickle.Unpickler(file_handler)
                    pkg_list = p.load()
                    file_handler.close()
                except Exception, e:
                    logger.error("Error opening recommended units results %s: Exception %s" % (results_file, e))

            if pkg_list:

                if logger.isEnabledFor(logging.DEBUG):
                    # report all recommended packages as debug
                    for pkg in pkg_list:
                        logger.debug("Recommended for %s : %s" % (pkg.get('FMRI', None), pkg.get('action', None)))

                # match recommended units with SA units
                id_map_file = '/opt/opsware/agent/metadata/extr/id_map'
                if os.path.exists(id_map_file):
                    f = file(id_map_file, 'r')
                    p = pickle.Unpickler(f)
                    data = p.load()
                    f.close()

                    # attempt to align recommended result with SA pkg inventory
                    for pkg in pkg_list:

                        # get package FMRI
                        fmri = pkg.get('FMRI', None)

                        # populate software release for recommended unit from unit in SA repo
                        for list in data:
                            if list[2] == fmri:
                                pkg["Software Release"] = list[0]

        else:
            # error occurred during check for recommended packages.  Report error and log file path
            recommended_log_file = os.path.join(log_dir, log_file_name)
            logger.error("Recommended units returned error exit code %d. See %s for more info. Error: %s" \
                         % (status, recommended_log_file, p))

        if not pkg_list:
            logger.info("No IPS packages recommended for upgrade")

        # report results
        return (pkg_list, status)


def register(handlers):
    handlers.append(IPSHandler())


#############################################################################

def main():
    a = IPSHandler()
    zz = {}
    a.installedList(zz)
    a.recommendedList(zz)
    print
    zz


if __name__ == "__main__":
    main()


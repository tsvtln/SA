#!/usr/bin/python
#
# Distributed RPM Builder
#

import os, sys, string, re, copy, time
from optparse import OptionParser, OptionGroup

class Config:
    ## rpm build & source paths
    ## these can either be a dict of osVersion -> paths, or just a string
    ##
    ## Dict Example:
    ## buildpath   = { "Linux 2.1AS"         : "/usr/src/redhat/BUILD/",
    ##                 "Linux 4AS"           : "/home/opsware/rpm/BUILD/",
    ##                 "Linux 4AS-X86_64"    : "/home/opsware/rpm/BUILD/",
    ##                 "Linux SLES-9"        : "/usr/src/packages/BUILD/",
    ##                 "Linux SLES-9-X86_64" : "/usr/src/packages/BUILD/" }

    buildpath = "/home/opsware/rpm/BUILD/"
    sourcepath = "/home/opsware/rpm/SOURCES"

    ## path to write specfiles on the managed host
    specpath   = "/home/opsware/specs/"

    ## name of the device group containing the buildservers (under /Public/.)
    buildgroup = "BuildSystem"

    ## opsware username & password for uploading to SAS
    username   = "autobuilder"
    password   = "0psw4r3"


class Replaceable:
    """Base class which provides a method for replacing tokens in strings with instance attribute values for easier formatting"""
    def autoToken(self, txt):
        def replaceTokens(matchobj):
            key = matchobj.group(3)
            mod = matchobj.group(2)
            if self.__dict__.has_key(key):
                if isinstance(self.__dict__[key], list):
                    if not mod or mod == "spaces":
                        return string.join(self.__dict__[key], ' ')
                    elif mod == "newlines":
                        return string.join(self.__dict__[key], '\n')
                    elif mod == "basenamespaces":
                        return string.join(filter(None, map(os.path.basename, self.__dict__[key])), ' ')
                    elif mod == "basenamenewlines":
                        return string.join(filter(None, map(os.path.basename, self.__dict__[key])), '\n')
                else:
                    return str(self.__dict__[key])
            else:
                return ""

        return re.compile(r"\@(([\w-]+):)?([\w-]+)\@", re.X).sub(replaceTokens, txt)

class SourceInputManager:
    supported_types = ('dir', 'ear', 'war', 'jar', 'tgz', 'tar', 'tbz', 'zip', 'tar.gz', 'tar.bz', 'file')
    needswork_types = {'dir': 'tar_from_dir()',
                       'ear': 'tar_from_jar()',
                       'war': 'tar_from_jar()',
                       'jar': 'tar_from_jar()'}
    exclude_list = ['.svn', '.cvs']
    
    def __init__(self, filename, tmpbasedir="/tmp", errors=True):
        self._error = errors
        self.tmp_basedir = tmpbasedir
        self.new_fullpath = ""
        self.tmp_path = ""
        self.filename = os.path.basename(filename)
        self.fullpath = os.path.abspath(filename)
        self.type = self.determine_type()
        if self.type in SourceInputManager.needswork_types.keys():
            eval("self." + SourceInputManager.needswork_types[self.type])
    
    def __del__(self):
        if self.tmp_path and os.path.exists(self.tmp_path):
            os.system("rm -rf %s" % self.tmp_path)
    
    def _run_command(self, cmd):
        fh = os.popen(cmd)
        outp = fh.readlines()
        if fh.close():
            return 0, outp
        else:
            return 1, outp
    
    def get_filename(self):
        if self.new_fullpath:
            return self.new_fullpath
        else:
            return self.fullpath
    
    def determine_type(self):
        if os.path.isdir(self.fullpath):
            return "dir"
        elif os.path.isfile(self.fullpath):
            try:
                return [ x for x in SourceInputManager.supported_types if self.fullpath.endswith(x) ][0]
            except:
                if self._error:
                    raise FiletypeNotSupported, "%s" % self.fullpath
                else:
                    return "file"
        else:
            raise IOError, "file '%s' doesn't exist" % self.fullpath
    
    def tar_from_dir(self):
        print "Converting %s/ to tarball format: \t" % (self.filename),
        #self.new_fullpath = self.tmp_basedir + "/%s.%s.tgz" % (self.filename, time.strftime('%Y%m%d%H%M%S', time.localtime()))
        self.new_fullpath = os.path.dirname(self.fullpath) + "/%s.%s.tgz" % (self.filename, time.strftime('%Y%m%d%H%M%S', time.localtime()))
        ## uncomment this to make sure this gets cleaned up when our SourceInputManager object is destroyed
        ## self.tmp_path = self.new_fullpath
        ## rebuild
        if os.path.exists(self.new_fullpath):
            raise IOError, "file '%s' exists - won't overwrite" % self.fullpath
        cmd = "cd %s && tar %s -czvf %s . 2>&1" % (self.fullpath, " ".join([ "--exclude " + x for x in SourceInputManager.exclude_list ]), self.new_fullpath)
        rv, outp = self._run_command(cmd)
        if rv and os.path.exists(self.new_fullpath):
            print "SUCCESS"
        else:
            print "FAILED"
            print "Command output:\n%s" % outp
            sys.exit(1)
    
    def tar_from_jar(self):
        print "Converting %s to tarball format: \t" % (self.filename),
        ## TODO: handle case for new_fullpath and tmp_dir existing
        self.new_fullpath = self.fullpath[:-len(self.type)] + "tgz"
        self.tmp_path = self.tmp_basedir + "/%s.%s" % (self.filename, time.strftime('%Y%m%d%H%M%S', time.localtime()))
        ## extract
        if os.path.exists(self.new_fullpath):
            raise IOError, "file '%s' exists - won't overwrite" % self.fullpath
        cmd = "mkdir %s && cd %s && jar xvf %s 2>&1" % (self.tmp_path, self.tmp_path, self.fullpath)
        rv, outp = self._run_command(cmd)
        
        if rv:
            ## rebuild
            cmd = "cd %s && tar czvf %s . 2>&1" % (self.tmp_path, self.new_fullpath)
            rv, outp = self._run_command(cmd)
            if rv and os.path.exists(self.new_fullpath):
                print "SUCCESS"
            else:
                print "FAILED"
                print "Command output:\n%s" % outp
                sys.exit(1)
        else:
            print "FAILED"
            print "Aborting - couldn't extract input file '%s' for conversion" % self.fullpath
            print "Command output:\n%s" % outp
            sys.exit(1)


class FiletypeNotSupported(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value


## specfile anatomy (http://www.rpm.org/RPM-HOWTO/build.html)
#############################################################
## header    - header
##               * Summary: one line description of the package
##               * Name: name string, e.g. MyPackage
##               * Version: version string, e.g. 1.0
##               * Release: release number, e.g. 1
##               * Copyright: copyright license, e.g. GPL, internal, etc
##               * Group: application group - e.g. "Applications/Utilities"
##               * Source: location of the "pristine source" (mult: SourceN)
##               * Patch: location of patches (mult: PatchN)
##               * BuildRoot: build root
##               * BuildRequires: list of packages required to build
##               * Requires: list of packages required to install
##               * Provides: list of provisions
##               * Prefix: ??
##               * Vendor: vendor information
##               * BuildArch: ??
##               * AutoReq: no - this will prevent rpmbuild from automatically seeking dependencies
##               * Obsoletes: packages this package obsoletes
##               * Conflicts: packages this package conflicts with
##             %description : multi-line description of the package
## prep      - %prep : get sources ready to build
##             %setup : unpack the source and cd to the source directory
##               * Options:
##               * -n <name> : set the name of the build directory (def: $NAME-$VERSION)
##               * -c : create and cd to the named dir before untarring
##               * -b # : untar Source# before cd'ing into directory
##               * -a # : untar Source# after cd'ing into directory
##               * -T : override default action of untarring the source
##               * -D : don't delete the directory before unpacking
##             %patch : automate process of applying patches
##               * can have multiple %patch - %patchN - %patch0, %patch1, etc (not implemented here)
##               * Options:
##               * -p # : number of directories to strip for patch cmd
##               * -b <ext>: save originals as filename.extension before patching
## build     - %build : build the package
## install   - %install : make install
## clean     - %clean : clean up
## pre/post  - %pre : pre-install scripts
##             %post : post-install scripts
##             %preun : pre-uninstall scripts
##             %postun : post-uninstall scripts
## files     - %files : files to include in the binary package
##               - %doc : mark documentation - goes in /usr/doc/$NAME-$VERSION-$RELEASE
##               - %config : mark configs - saves these post-upgrade
##               - %dir : mark dir for individual inclusion
##               - %defattr : (mode, owner, group) ; - = None
##               - %files -f <filename> : read filelist from filename
## changelog - %changelog : change log for the package
##               - format is:
##                     * `date +"%a %b %d %Y"` Author Name <author@email.com>
##                     - Comment goes here (can have multiple of these)

class SpecFile(Replaceable):
    """Python object representing an RPM specfile"""
    def __init__(self, specfile=""):
        self.specfile = specfile
        if self.specfile: return

        ## Standard Header Attributes
        self.summary = "Autogenerated RPM"
        self.name = ""
        self.version = "1.0"
        self.release = "1"
        self.license = "Internal"
        self.group = "Applications/SomeCompany"
        self.url = "http://somecompany.com"
        self.packager = "RPM AutoBuilder <autobuilder@somecompany.com>"
        self.vendor = "SomeCompany"
        self.prefix = "/usr/local"
        self.buildarch = ""

        ## Section Options (e.g. %setup -q)
        self.setupopts = "-c"
        self.patchopts = ""

        ## Standard Header Attributes (w/ multiple values)
        self.source = []
        self.patch = []
        self.requires = []
        self.provides = []
        self.buildrequires = []
        self.conflicts = []
        self.obsoletes = []
        self.autoreq = ""

        ## % Sections (e.g. %prep, %setup, etc) - text blobs
        self.macros = ""
        self.description = ""
        self.prep = ""
        self.setup = ""
        self.build = ""
        self.install = ""
        self.pre = ""
        self.post = ""
        self.preun = ""
        self.postun = ""
        self.clean = ""
        self.changelog = ""
        self.files = []

        ## Required attributes (for self.isValid())
        self._required = ('summary', 'name', 'version', 'release', 'packager', 'files')
        self._prefix = "/usr/local"

    def isValid():
        for r in self._required:
            if not r:
                return 0
        return 1

    def set(self, key, val):
        """set attributes on a class - usage: set(key, val) - if val is a file that exists on disk, we import that"""
        if key in ('source', 'patch', 'provides', 'requires', 'buildrequires'):
            raise Exception("can't set attribute %s using the set() method since these can have multiple values - use the add() method instead")

        if os.path.isfile(val) and key not in ('specfile'):
            self.__dict__[key] = open(val, "r").readlines()
        else:
            self.__dict__[key] = val
        return

    def add(self, key, val):
        """like set() but for list attributes"""
        ## for sources, strip everything after the last / - rpmbuild only honors the base filename and disregards the path
        if key == "source":
            index = string.rfind(val, "/") + 1
            if index: val = val[index:]

        ## make sure all files begin with / (except for % directives)
        if key == "files":
            if not val: return
            if val[0] not in ("%", "/"): val = "/" + val
            if not val.startswith(self.prefix) and val[0] != "%": val = os.path.abspath(self.prefix + "/" + val)

        self.__dict__[key].append(val)
        return

#    def addChangelog(self, date, author, email, text):
#        """addChangelog(date, author, email, text)"""
#        ## TODO: format validation for date (Sun Mar 21 1999), author (a-z only), email (blah@blah.com), text (no \n's)
#        if self.changelog: self.changelog = self.changelog + "\n"
#        self.changelog = self.changelog + "* %s %s <%s>\n- %s\n" % (date, author, email, text)

    def setFilesFromArchive(self, tar):
        def prefixer(x, prefix):
            if not prefix: prefix = "/"
            if prefix[-1] != "/": prefix = prefix + "/"
            if x[0] != "%" and not x.startswith(prefix):
                return prefix + x
            else:
                return x

        filename = os.path.basename(tar)
        if filename.lower().endswith('.tgz') or filename.lower().endswith('.tar.gz'):
            cmd = "/bin/tar tzf "
        elif filename.lower().endswith('.tar'):
            cmd = "/bin/tar tf "
        elif filename.lower().endswith('.tbz') or filename.lower().endswith('.tar.bz'):
            cmd = "/bin/tar tjf "
        elif filename.lower().endswith('.zip'):
            cmd = "/usr/bin/zipinfo -1 "
        else:
            return None

        fh = os.popen(cmd + tar)
        files = fh.readlines()
        files = map(lambda x: string.strip(x), files)
        files = filter(None, files)
        files = map(lambda x: prefixer(x, self.prefix), files)
        self.files.extend(files)

        if fh.close():
            return 0
        else:
            return 1

    def writeToFile(self, f):
        """writeToFile(file)"""
        fh = open(f, "w")
        if self.specfile:
            fh.write(string.join(open(self.specfile, "r").readlines()))
        else:
            fh.write(self.asText())
        fh.close()
        return

    def asText(self):
        """Return a text representation of the specfile"""
        if self.specfile: return string.join(open(self.specfile, "r").readlines())
        output = "## Do not edit - this file is dynamically generated by the RPM AutoBuilder\n"
        if self.macros: output = output + "@macros@\n\n"
        output = output + """
Summary: @summary@
Name: @name@
Version: @version@
Release: @release@
License: @license@
Group: @group@
Vendor: @vendor@
Packager: @packager@
BuildRoot: @buildroot@
Prefix: @prefix@
"""
        if self.buildarch: output = output + "BuildArch: @buildarch@\n"
        if self.obsoletes: output = output + "Obsoletes: @obsoletes@\n"
        if self.conflicts: output = output + "Conflicts: @conflicts@\n"

        if self.source:
            if len(self.source) > 1:
                count = 0
                for s in self.source:
                    output = output + "Source%s: %s\n" % (count, s)
                    count = count + 1
            else:
                output = output + "Source: %s\n" % (self.source[0])

        if self.patch:
            if len(self.patch) > 1:
                count = 0
                for s in self.patch:
                    output = output + "Patch%s: %s\n" % (count, s)
                    count = count + 1
            else:
                output = output + "Patch: %s\n" % (self.patch[0])

        if self.autoreq == "no": output = output + "AutoReqProv: no\n"
        if self.provides: output = output + "Provides: @spaces:provides@\n"
        if self.requires: output = output + "Requires: @spaces:requires@\n"
        if self.buildrequires: output = output + "BuildRequires: @spaces:buildrequires@\n"

        ###if self.source: output = output + "%setup @setupopts@\n@setup@\n"
        
        output = output + """
%description
@description@

%prep
@prep@

%setup @setupopts@
@setup@
"""

        if self.build: output = output + "%build\n@build\n"

        output = output + """
%install
@install@

%clean
@clean@

%files
@newlines:files@

%pre
@pre@

%post
@post@

%preun
@preun@

%postun
@postun@

"""

        if self.changelog:
            output = output + "%changelog\n"
            for c in self.changelog:
                output = output + "%s\n" % (c)

        return self.autoToken(self.autoToken(output))


class BuildServerCluster:
    def __init__(self, devgrp, buildpath, sourcepath):
        self.members = []
        self.buildpath = buildpath
        self.sourcepath = sourcepath
        self.ids = os.listdir("/opsw/Group/Public/" + devgrp + "/@/.Server.ID/")
        if not self.ids:
            raise Exception("Couldn't find specified device group: /Public/%s" % devgrp)
        for i in self.ids:
            self.members.append(BuildServer(i))

    def importSource(self, src):
        for m in self.members: m.importSource(src)
        return

    def build(self, spec):
        for m in self.members: m.build(spec)
        return

    def upload(self, user, pw, folder=""):
        for m in self.members:
            for r in m.builtrpms:
                m.uploadToSAS(r, user, pw, folder=folder)

    def setSpec(self, spec):
        for m in self.members:
            ## give a copy of our spec object to the buildserver object for local modifications
            m.spec = copy.copy(spec)

            ## append OS string to release
            if 'SLES' in m.osver:
                osv = string.strip(string.replace(m.osver, 'Linux', ''))
            elif 'AS' in m.osver or 'ES' in m.osver or 'Linux 5' in m.osver:
                osv = "RHEL" + string.strip(string.replace(m.osver, 'Linux', ''))
            else:
                osv = string.strip(string.replace(m.osver, 'Linux', ''))
            osv = osv.replace('-', '_')
            m.spec.release = m.spec.release + "." + osv

            if isinstance(self.buildpath, dict):
                m.buildpath = self.buildpath[m.osver]
                m.spec.buildroot = os.path.abspath("%s/%s-%s" % (m.buildpath, spec.name, spec.version))
            else:
                m.buildpath = self.buildpath
                m.spec.buildroot = os.path.abspath("%s/%s-%s" % (m.buildpath, spec.name, spec.version))

            if isinstance(self.sourcepath, dict):
                m.sourcepath = self.sourcepath[m.osver]
            else:
                m.sourcepath = self.sourcepath

    def writeSpec(self, specpath):
        for m in self.members: m.writeSpec(specpath)


class BuildServer:
    def __init__(self, mid):
        self.mid = mid
        self.name = open("/opsw/.Server.ID/%s/.self:n" % self.mid).readline()
        self.osver = open("/opsw/.Server.ID/%s/attr/osVersion" % self.mid).readline()
        self.platform = open("/opsw/.Server.ID/%s/attr/platform" % self.mid).readline()
        self.basepath = "/opsw/.Server.ID/%s/files/opsware" % self.mid
        self.buildpath = ""
        self.sourcepath = ""
        self.tmppath = "/tmp"
        self.rpmbuildpath = self.findRpmBuild() or "/usr/bin/rpmbuild"
        self.rpmbuildcmd = self.rpmbuildpath + " -bb"
        self.spec = ""
        self.builtrpms = []

    def md5sum(self, f):
        fh = os.popen("/usr/bin/md5sum %s/%s" % (self.basepath, f))
        if fh.close():
            return 0
        else:
            return 1

    def writeFile(self, f, txt):
        # full filename in the global shell
        fpath = os.path.abspath(self.basepath + "/" + f)
        # base directory in the global shell
        fpathbase = fpath[:string.rindex(fpath,'/')]

        # create the base directory if it doesn't exist
        if not os.path.exists(fpathbase):
            fh = os.popen("/bin/mkdir -p %s" % fpathbase)
            fh.close()

        # write the file
        fh = open(fpath, "w")
        fh.write(txt + "\n")
        if fh.close():
            return 0
        else:
            return 1

#    def copyFile(self, f, path=""):
#        rv, outp = self.getCommandOutput("/bin/cp -af %s %s/%s" % (f, self.basepath, path))
#        if rv:
#            return 0
#        else:
#            return 1

#    def runCommand(self, cmd):
#        fh = os.popen("/opsw/bin/rosh -l opsware -i %s \"%s\" 2>&1" % (self.mid, cmd))
#        if fh.close():
#            return 0
#        else:
#            return 1

    def getCommandOutputAsRoot(self, cmd):
        fh = os.popen("/opsw/bin/rosh -l root -i %s \"%s\" 2>&1" % (self.mid, cmd))
        outp = fh.readlines()
        if fh.close():
            return 0, outp
        else:
            return 1, outp

    def getCommandOutput(self, cmd):
        fh = os.popen("/opsw/bin/rosh -l opsware -i %s \"%s\" 2>&1" % (self.mid, cmd))
        outp = fh.readlines()
        if fh.close():
            return 0, outp
        else:
            return 1, outp

    def logErrors(self, title, body):
        date = time.strftime('%H:%M-%m-%d-%Y', time.localtime())
        logdir = "/tmp/errorlogs"
        logpath = logdir + "/" + self.name + "-" + date + "errors.log"
        if not os.path.exists(logdir): os.mkdir(logdir)
        fh = open(logpath, "w+")
        fh.write("\n\n================= %s @ %s =================\n\n" % (self.name, date))
        fh.write("an error occured during %s:\n\n" % title)
        fh.write(body)
        if title == "building":
            fh.write("\n\n")
            fh.write("******* specfile *******\n\n")
            fh.write(self.spec.asText())
        fh.close()
        return logpath

    def writeSpec(self, specpath):
        print "Writing specfile %27s:%s : \t" % (self.name, string.replace(specpath, '//', '/')),
        if self.spec.specfile:
            rv = self.writeFile(specpath, string.join(open(self.spec.specfile, "r").readlines(), ''))
        else:
            rv = self.writeFile(specpath, self.spec.asText())
        if rv:
            print "SUCCESS"
        else:
            print "FAILURE"

    def findRpmBuild(self, pathstr="/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin"):
        for path in pathstr.split(':'):
            if os.path.exists(self.basepath + path + "/rpmbuild"):
                return path + "/rpmbuild"
        return None

    def importSource(self, src):
        print "Distributing %s to build server %27s : \t" % (os.path.abspath(src), self.name),
        #print "\nDEBUG: /bin/cp -af %s %s/%s" % (os.path.abspath(src), self.basepath, self.sourcepath)
        
        fh = os.popen("/bin/cp -avf %s %s/%s 2>&1" % (os.path.abspath(src), self.basepath, self.sourcepath))
        output = fh.readlines()
        if not fh.close():
            print "SUCCESS"
        else:
            print "FAILURE"
            print "  - ErrorLog: %s" % self.logErrors("file copying", string.join(output, ''))

    def build(self, spec):
        print "Building %s on %27s : \t" % (os.path.abspath(spec), self.name),
        rv, output = self.getCommandOutput(self.rpmbuildcmd + " " + spec)
        for l in output:
            if l[:7] == "Wrote: ":
                self.builtrpms.append(string.strip(l[7:]))
        if rv and self.builtrpms:
            print "SUCCESS"
            print "  - RPMS: %s" % string.join(self.builtrpms, ",")
        else:
            print "FAILURE"
            print "  - ErrorLog: %s" % self.logErrors("building", string.join(output, ''))

    def uploadToSAS(self, rpm, user, pw, folder=""):
        env = "export OCLIPATH=/opt/opsware/ocli;  export PATH=/opt/opsware/agent/bin:$PATH; export ISMTOOLUSERNAME=%s; export ISMTOOLPASSWORD=%s; . /opt/opsware/ocli/ocli/login.sh;" % (user, pw)
        if folder:
            print "Uploading RPM %s to opsware:%s : \t" % (os.path.basename(rpm), folder),
            oupload = r'echo y | oupload -I -d \"%s\" -t \"RPM\" -O \"%s\" %s' % (folder, self.platform, rpm)
        else:
            print "Uploading RPM %s to opsware: \t" % (os.path.basename(rpm)),
            oupload = r'echo y | oupload -I --old --customer 0 --pkgtype \"RPM\" --os \"%s\" %s' % (self.platform, rpm)

        cmd = env + oupload
        #print "DEBUG: running \"%s\"" % cmd
        rv, output = self.getCommandOutputAsRoot(cmd)
        if rv:
            print "SUCCESS"
            try:
                for l in output:
                    m = re.match(r'.*?/([^:/]+):.*?COMPLETE.*?(\d+).*?', l)
                    if m:
                        try:
                            print "  - %s -> [ID:%s]" % (m.group(1), m.group(2))
                        except: pass
            except: pass
        else:
            print "FAILURE"
            print "  - ErrorLog: %s" % self.logErrors("uploading", string.join(output, ''))


def Optionator(spec):
    ## Option Parsing
    op = OptionParser(usage="%prog <[-n/-v/-r/-s] or [--spec/-s]> [options]")

    rgroup = OptionGroup(op, "Required Options", "You must either specify a name (-n), version (-v), release (-r) and source (-s) *or* a specfile (--spec) and source (-s).")
    ogroup = OptionGroup(op, "Other Options")
    hgroup = OptionGroup(op, "Header Options")
    bgroup = OptionGroup(op, "Body Options", "These can either be text blobs, or filenames (except for -f/--files)")

    ## Required header variables
    rgroup.add_option("-n", "--name", dest="name", help="RPM base name (e.g. 'JRockit')", action='store', default="")
    rgroup.add_option("-v", "--version", dest="version", help="RPM version (e.g. '1.0')", action='store', default="")
    rgroup.add_option("-r", "--release", dest="release", help="RPM release (e.g. '1')", action='store', default="")
    rgroup.add_option("--spec", dest="specfile", help="Build a package from specfile (mutually exclusive with other options e.g. -n)", action="store", default="")

    ## Other variables
    ogroup.add_option("-o", "--opswpath", dest="opswpath", help="Opsware folder path to upload this RPM to", action='store', default="")
    ogroup.add_option("-p", "--prefix", dest="prefix", help="Install prefix for the package", action='store', default="")
    ogroup.add_option("--buildgroup", dest="buildgroup", help="Opsware device group (relative to the main build group)", action='store', default="")
    ogroup.add_option("--autoreq", dest="autoreq", help="Turn automatic dependency analysis on/off (e.g. 'yes' or 'no')", action='store', default="yes")

    ## Optional header variables (override the default baseline)
    hgroup.add_option("-a", "--packager", dest="packager", help="RPM author/packager (e.g. 'Kris Wilson')", action='store', default="")
    hgroup.add_option("-e", "--email", dest="email", help="RPM packager email address (e.g. 'kris.wilson@.com')", action='store', default="")
    hgroup.add_option("-m", "--summary", dest="summary", help="RPM summary", action='store', default="")
    hgroup.add_option("-l", "--license", dest="license", help="RPM license/copyright info (e.g. 'GPL', 'Internal')", action='store', default="")
    hgroup.add_option("-u", "--url", dest="url", help="RPM/package information URL", action='store', default="")
    hgroup.add_option("-g", "--group", dest="group", help="RPM group (e.g. 'Applications/SomeCompany')", action='store', default="")
    hgroup.add_option("-b", "--buildarch", dest="buildarch", help="Build Architecture (e.g. 'noarch')", action='store', default="")
    #hgroup.add_option("-b", "--buildroot", dest="buildroot", help="Override default build root", action='store', default="")

    ## Appenders (accept multiple options)
    hgroup.add_option("-s", "--source", dest="source", help="Source packages to add to the RPM", action='append')
    hgroup.add_option("-t", "--patches", dest="patches", help="Patches to add to the RPM", action='append')
    hgroup.add_option("-d", "--buildrequires", dest="buildrequires", help="RPM build dependencies/requirements", action='append')
    hgroup.add_option("-q", "--requires", dest="requires", help="RPM dependencies/requirements", action='append')
    hgroup.add_option("-i", "--provides", dest="provides", help="packages this RPM provides", action='append')
    hgroup.add_option("--obsoletes", dest="obsoletes", help="packages this RPM obsoletes", action='append')
    hgroup.add_option("--conflicts", dest="conflicts", help="packages this RPM conflicts with", action='append')
    bgroup.add_option("-f", "--files", dest="files", help="Include only these files from the tarball (and exclude the rest)", action='append')

    ## Sections
    bgroup.add_option("--macros", dest="macros", help="specfile macros to include in the body", action='store', default="")
    bgroup.add_option("--description", dest="description", help="Body of the %description section", action='store', default="")
    bgroup.add_option("--prep", dest="prep", help="Body of the %prep section", action='store', default="")
    bgroup.add_option("--setup", dest="setup", help="Body of the %setup section", action='store', default="")
    bgroup.add_option("--setupopts", dest="setupopts", help="Options to pass to %setup (e.g. %setup -q)", action='store', default="")
    bgroup.add_option("--build", dest="build", help="Body of the %build section", action='store', default="")
    bgroup.add_option("--install", dest="install", help="Body of the %install section", action='store', default="")
    bgroup.add_option("--pre", dest="pre", help="Body of the %pre section", action='store', default="")
    bgroup.add_option("--post", dest="post", help="Body of the %post section", action='store', default="")
    bgroup.add_option("--preun", dest="preun", help="Body of the %preun section", action='store', default="")
    bgroup.add_option("--postun", dest="postun", help="Body of the %postun section", action='store', default="")
    bgroup.add_option("--clean", dest="clean", help="Body of the %clean section", action='store', default="")

    op.add_option_group(rgroup)
    op.add_option_group(ogroup)
    op.add_option_group(hgroup)
    op.add_option_group(bgroup)

    (oo, args) = op.parse_args()

    ## Required options
    if oo.specfile:
        if not oo.source: op.error("Missing required option: -s (use -h for help)")
        if not os.path.exists(oo.specfile): op.error("specfile %s can't be found" % oo.specfile)
    elif oo.name:
        missing = []
        if not oo.version: missing.append("-v")
        if not oo.release: missing.append("-r")
        if not oo.source: missing.append("-s")
        if missing: op.error("Missing required options: %s (use -h for help)" % string.join(missing, "/"))

        for s in oo.source:
            if not os.path.exists(s): op.error("source package %s can't be found" % s)
            #if os.path.isdir(s): op.error("source package %s is a directory" % s)

        if oo.name.find(" ") != -1: op.error("Invalid package name: %s" % oo.name)
    else:
        op.error("Missing required options: requires either -n or --spec (use -h for help)")

    if oo.opswpath:
        if not os.path.exists(os.path.abspath("/opsw/Library/%s" % oo.opswpath)): op.error("Invalid Opsware path: '%s' doesn't exist" % oo.opswpath)

    if oo.prefix:
        if oo.prefix[0] != "/": op.error("Invalid prefix (must begin with /)")
        ## we need to set this earlier than the bulk set so we can prefix all of the 'files' with this
        spec.prefix = oo.prefix

    for s in oo.source:
        if not os.path.exists(s): op.error("source path %s can't be found" % s)

    if oo.specfile:
        ## convert any ear/war/jar/dirs to tarballs here
        oo.source = [ SourceInputManager(x, errors=False).get_filename() for x in oo.source ]
    else:
        ## convert any ear/war/jar/dirs to tarballs here
        oo.source = [ SourceInputManager(x).get_filename() for x in oo.source ]

    for s in oo.source:
        if not os.path.exists(s): op.error("source package %s can't be found" % s)

    ## Bulk copy object attributes from the OptionParser object -> SpecFile object
    ## NOTE: this requires a 1:1 mapping of OptParser<->SpecFile attributes (list attributes must be set to the 'append' action so they map over appropriately)
    
    for v in oo.__dict__.keys():
        if isinstance(oo.__dict__[v], list):
            for x in oo.__dict__[v]:
                spec.add(v, string.strip(x))
        else:
            if oo.__dict__[v]:
                if spec.__dict__.has_key(v):
                    spec.set(v, string.strip(oo.__dict__[v]))

    ## if our source package contains a relative path, inject it with the prefix via the specfile
    if spec.prefix != "/":
        inject = """mkdir -p %%{_tmppath}/tmp-$$/%s/
cp -avf %%{buildroot}/* %%{_tmppath}/tmp-$$/%s/
rm -rvf %%{buildroot}/*
cp -avf %%{_tmppath}/tmp-$$/* %%{buildroot}/
rm -rvf %%{_tmppath}/tmp-$$
""" % (spec.prefix, spec.prefix)
        spec.setup = inject + spec.setup

    if not oo.files:
        for archive in oo.source:
            spec.setFilesFromArchive(archive)

    if oo.buildgroup:
        Config.oldbuildgroup = Config.buildgroup
        Config.buildgroup = Config.buildgroup + "/" + oo.buildgroup
        if not os.path.exists("/opsw/Group/Public/%s" % Config.buildgroup):
            validopts = filter(lambda x: x != "@", os.listdir("/opsw/Group/Public/%s" % Config.oldbuildgroup))
            op.error("Invalid sub-buildgroup '%s'; valid options are: %s" % (Config.buildgroup, string.join(validopts, ' ')))

    return op, oo


################################# main #################################

## Create a new SpecFile object
s = SpecFile()

## Populate it from cmdline args
optparser, options = Optionator(s)

## Create a new BuildServerCluster
bc = BuildServerCluster(Config.buildgroup, Config.buildpath, Config.sourcepath)
if s.specfile:
    specfilename = os.path.basename(s.specfile)
else:
    specfilename = "%s-%s-%s.spec" % (s.name, s.version, s.release)

## Set the specfile object and make local adjustments
bc.setSpec(s)

## Write the specfile(s) out
bc.writeSpec(Config.specpath + "/" + specfilename)

## Copy the source tarballs/etc to the buildservers
for src in options.source: bc.importSource(src)

## Build the RPM
bc.build(Config.specpath + "/" + specfilename)

## Upload the built RPMs to SAS
bc.upload(Config.username, Config.password, options.opswpath)

## ./rpmb2.py -n TestPkg -v 2.0 -r 1 -s ./test.tgz

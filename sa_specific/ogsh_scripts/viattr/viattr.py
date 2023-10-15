#!/usr/bin/python
# viattr (global shell attribute editor)


import os, sys, string, tempfile, difflib, re
from shutil import copyfile
from optparse import OptionParser, OptionGroup

sys.path.append("/opt/opsware/pylibs2")

from pytwist import *


class Attributes:
    def init(self):
        self.tmp_file = ""
        self.orig_file = ""
        self.diff = ""
        self.custattrs = {}

    def __del__(self):
        ## Cleanup tmp files
        for x in (self.tmp_file, self.orig_file):
            if os.path.exists(x):
                try:
                    os.unlink(x)
                except:
                    print "WARN: Couldn't clean up tmp file: %s" % x

    def uniq(self, seq):
        seen = {}
        dupes = []
        result = []
        for item in seq:
            if seen.has_key(item):
                dupes.append(item)
                continue
            seen[item] = 1
            result.append(item)
        return dupes, result

    def parse_file(self, f):
        entries = {}
        dupes = []
        bad = []
        seen = {}

        tmpstr = open(f, "r").read()
        while len(tmpstr) > 0:
            m = re.compile(r"(?:\s?([^:\n#\s]+):\s+\'(.*?)(?<!\\)\')|(?:.*?\n)", re.DOTALL).search(tmpstr)

            if not m:
                continue

            if m.group(1) and m.group(2):
                if not seen.has_key(m.group(1)):
                    seen[m.group(1)] = 1
                elif seen[m.group(1)] == 1:
                    dupes.append(m.group(1))
                    seen[m.group(1)] = 2
                entries[m.group(1)] = m.group(2)
            elif m.group(0)[0] != "#" and m.group(0) != "\n":
                bad.append(m.group(0))

            tmpstr = tmpstr[m.end():]

        return entries, dupes, bad

    def edit(self):
        finished = 0
        setkeys = {}
        delkeys = {}
    
        if not self.tmp_file or not os.path.exists(self.tmp_file):
            self.write_tmp()
            if not self.tmp_file or not os.path.exists(self.tmp_file):
                raise Exception("couldn't get tmp file")

        self.orig_file = self.tmp_file + ".orig"
        copyfile(self.tmp_file, self.orig_file)

        while finished != 1:
            os.system("TERM=xterm /bin/vi " + self.tmp_file)

            orig = self.parse_file(self.orig_file)[0]
            mod, moddupes, modbad = self.parse_file(self.tmp_file)

            if moddupes:
                print "ERROR: duplicate entries found for: %s" % string.join(self.uniq(moddupes)[1], ", ")
                print "\n** hit any key to re-edit or q to quit **"
                inp = raw_input()
                if inp == 'q':
                    sys.exit(1)
                else:
                    continue
            elif modbad:
                print "ERROR: one or more lines are invalid:\n"
                print string.join([ "\t> " + x for x in modbad])
                print "\n** hit any key to re-edit or q to quit **"
                inp = raw_input()
                if inp == 'q':
                    sys.exit(1)
                else:
                    continue
            else:
                finished = 1

                delkeys = {}
                ## look for key differences
                [ delkeys.setdefault(x,y) for x, y in orig.iteritems() if not mod.has_key(x) ]

                setkeys = {}
                ## look for key + value differences
                [ setkeys.setdefault(x,y) for x, y in mod.iteritems() if ( not orig.has_key(x) or orig[x] != mod[x] ) ]

        self._sets = setkeys
        self._dels = delkeys
        self._diff = [ "- %s: '%s'" % (x, y) for x, y in self._dels.iteritems() ] + \
                     [ "+ %s: '%s'" % (x, y) for x, y in self._sets.iteritems() ]

        return

    def write_to_sas(self):
        if self._diff:
            print "\n\nReady to update the following attributes for %s:\n\n" % self.ref.name
            for line in self._diff:
                print "\t%s" % line
            print "\n\nPlease enter 'y' to continue or any other key to exit: ",
            prompt = raw_input()
            print "\n"
            if prompt.lower() != "y":
                print "Exiting!"
                sys.exit(1)
    
            for key in self._dels.keys():
                if self._sets.has_key(key):
                    continue
                self.rm_custattr(self.ref, key)

            for key, val in self._sets.iteritems():
                self.set_custattr(self.ref, key, val)

        return

    def rm_custattr(self, ref, key):
        print "- Removing custattr '%s' on %s\t\t" % (key, self.ref.name),
        try:
            #print "self.service.removeCustAttr('%s', '%s')" % (ref.id, key)
            self.service.removeCustAttr(ref, key)
        except Exception, e:
            print "FAILED\n\t* %s" % e
            return

        print "SUCCESS"
        return

    def set_custattr(self, ref, key, val):
        print "- Setting custattr '%s' on %s\t\t" % (key, self.ref.name),
        try:
            #print "self.service.addCustAttr('%s', '%s', '%s')" % (ref.id, key, val)
            self.service.setCustAttr(ref, key, val)
        except Exception, e:
            print "FAILED\n\t* %s" % e
            return

        print "SUCCESS"
        return

    def write_tmp(self):
        fd_tmp_fd, fd_tmp_name = tempfile.mkstemp(suffix='.tmp')
        fh = os.fdopen(fd_tmp_fd, 'w+b')
        current = ""

        for attr in self.custattrs:
            if attr[0][:6] == '__OPSW':
                self.custattrs.remove(attr)

        self.custattrs.sort()

        for key, val, wfrom in self.custattrs:
            if current != wfrom:
                current = wfrom
                fh.write("## from: %s\n" % wfrom)
            if wfrom != "base" and wfrom != "server":
                fh.write("# ")
            fh.write("%s: '%s'\n" % (key, val.replace("'", "\\'")))
        fh.close()
        self.tmp_file = fd_tmp_name

        return


class ServerAttributes(Attributes):
    def __init__(self, ts, oid):
        self.init()
        self.twist = ts
        self.oid = oid
        try:
            self.ref = self.twist.search.SearchService.findObjRefs('dvc_id EQUAL_TO %s' % self.oid, 'device')[0]
        except:
            print "ERROR: couldn't find server with ID '%s'" % self.oid
            sys.exit(1)
        self.service = self.twist.server.ServerService
        self.custattrs = self.get_attrs()

    def get_attrs(self):
        """Gathers device custom attributes"""
        attrs = []  ## list of triples [(key, val, from)]
        # get device groups
        devgrps = self.twist.server.ServerService.getDeviceGroups(self.ref)
        ## get all attributes for device
        for x in ts.server.ServerService.getCustAttrDetailLists([self.ref], None, None, 1):
            for y in x.attrDetails:
                for z in y.values:
                    if y.key[:6] == "__OPSW": continue
                    ## append a triple (key, value, scope) to attrs
                    attrs.append((y.key, z.value, z.scope))

        return attrs


class GroupAttributes(Attributes):
    def __init__(self, ts, oid):
        self.init()
        self.twist = ts
        self.oid = oid
        try:
            self.ref = self.twist.search.SearchService.findObjRefs('DeviceGroupVO.pK EQUAL_TO %s' % self.oid, 'device_group')[0]
        except:
            print "ERROR: couldn't find device group with ID '%s'" % self.oid
            sys.exit(1)
        self.service = self.twist.device.DeviceGroupService
        self.custattrs = self.get_attrs()

    def get_attrs(self):
        """Gathers device group custom attributes"""
        attrs = []
        devgrpattrs = self.twist.device.DeviceGroupService.getCustAttrs(self.ref, None, 0)
        for key in devgrpattrs.keys():
            attrs.append((key, devgrpattrs[key], "base"))

        devgrpvo = self.twist.device.DeviceGroupService.getDeviceGroupVO(self.ref)

        return attrs


class PolicyAttributes(Attributes):
    def __init__(self, ts, oid):
        self.init()
        self.twist = ts
        self.oid = oid
        try:
            self.ref = self.twist.search.SearchService.findObjRefs('SoftwarePolicyVO.pK EQUAL_TO %s' % self.oid, 'software_policy')[0]
        except:
            print "ERROR: couldn't find swpolicy with ID '%s'" % self.oid
            sys.exit(1)
        self.service = self.twist.swmgmt.SoftwarePolicyService
        self.custattrs = self.get_attrs()

    def get_attrs(self):
        """Gathers policy custom attributes"""
        attrs = []
        policyattrs = self.twist.swmgmt.SoftwarePolicyService.getCustAttrs(self.ref, None, 1)
        for key in policyattrs.keys():
            attrs.append((key, policyattrs[key], "base"))

        return attrs


def getClosestRefByPath(p):
    found = 0
    while p != '/':
        if os.path.exists(p + "/.self:i"):
            found = 1
            break
        p = os.path.dirname(p)

    if found:
        return open(p + "/.self:i", "r").read()
    else:
        return None

if __name__ == '__main__':
    op = OptionParser(usage="%prog [-opts] <target>")
    maingroup = OptionGroup(op, "Modifiers Options")
    maingroup.add_option("-g", "--group", dest="group", help="Device Group", action="store_true", default=False)
    maingroup.add_option("-d", "--device", dest="server", help="Server", action="store_true", default=False)
    maingroup.add_option("-s", "--policy", dest="policy", help="Software Policy", action="store_true", default=False)
    modgroup = OptionGroup(op, "Main Options")
    modgroup.add_option("-n", dest="name", help="Name", action="store", default="")
    modgroup.add_option("-i", dest="id", help="ID", action="store", default="")
    modgroup.add_option("-p", dest="printonly", help="Print instead of editing", action="store_true", default=False)
    op.add_option_group(maingroup)
    op.add_option_group(modgroup)

    (options, args) = op.parse_args()

    ts = twistserver.TwistServer()

    ## global shell magic
    if not options.server and not options.group and not options.policy:
        ref = getClosestRefByPath(os.getcwd())
        if ref:
            reftype, refid = ref.split(":", 1)
            if reftype == "com.opsware.server.ServerRef":
                options.server = True
                options.id = refid
            if reftype == "com.opsware.device.DeviceGroupRef":
                options.group = True
                options.id = refid
            elif reftype == "com.opsware.swmgmt.SoftwarePolicyRef":
                options.policy = True
                options.id = refid

    if options.server:
        if options.name and not options.id:
            ## convert hostname to ID and set options.id
            try:
                options.id = string.split(open("/opsw/Server/@/%s/.self:i" % options.name, "r").read(), ':')[1]
            except Exception, e:
                print "ERROR: couldn't find a server named '%s' - %s" % (options.name, e)
                sys.exit(1)

        a = ServerAttributes(ts, options.id)

    elif options.group:
        if options.name and not options.id:
            ## convert pathname to ID and set options.id
            try:
                options.id = string.split(open("/opsw/Group/Public/%s/@/.self:i" % options.name, "r").read(), ':')[1]
            except Exception, e:
                print "ERROR: couldn't find a device group named '%s' - %s" % (options.name, e)
                sys.exit(1)

        a = GroupAttributes(ts, options.id)

    elif options.policy:
        if options.name and not options.id:
            ## convert pathname to ID and set options.id
            try:
                options.id = string.split(open("/opsw/Library/%s/@/.self:i" % options.name, "r").read(), ':')[1]
            except Exception, e:
                print "ERROR: couldn't find a policy named '%s' - %s" % (options.name, e)
                sys.exit(1)

        a = PolicyAttributes(ts, options.id)

    else:
        op.print_help()
        sys.exit()

    if options.printonly:
        a.write_tmp()
        print open(a.tmp_file, "r").read(),
    else:
        a.edit()
        a.write_to_sas()
        print "\n"
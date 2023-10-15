#!/usr/bin/python
# vidyngrp (edit dynamic group rules via vi)
#

import os, sys, string, tempfile, re
from shutil import copyfile
from optparse import OptionParser, OptionGroup

#sys.path.insert(0, "/home/opsware/public/gshlibs/stable")
sys.path.insert(0, "/opt/opsware/pylibs2")

from pytwist.com.opsware.search import Filter
from pytwist.com.opsware.common import NoChangeRequestedException
from pytwist import *

ts = twistserver.TwistServer()

class PathMagic:
  def __init__(self, path):
    path = re.sub(r'/$', '', path) # strip off a trailing slash
    path = re.sub(r'~', os.environ['HOME'], path)
    self.path = path
    self.self_i = self.findSelf_i()
    group,reftype,type,id = re.findall(r'^com\.opsware\.(\w+?)\.((\w+?)Ref):(\d+)$', self.self_i)[0]
    self.id = id
    self.reftype = reftype
    self.votype = type + 'VO'
    self.type = type
    self.service = group + '.' + type + 'Service'

  def getRef(self):
    methodcall = 'ts.' + self.service + '.find' + self.reftype + 's(f)[0]'
    f = Filter();
    searchvo = self.votype
    f.expression = '{ ' + searchvo + '.pK = ' + self.id + ' }'

    ref = eval(methodcall)
    return ref

  def getVO(self):
    ref = self.getRef()
    methodcall = 'ts.' + self.service + '.get' + self.votype + '(ref)'
    #print 'Calling: "' + methodcall + "'"
    vo = eval(methodcall)
    return vo

  def findSelf_i(self,path=''):
    if path == '':
      path = self.path
    if not os.path.isabs(path):
      path = os.path.abspath(path)
    if path == '/':
      raise Exception, "no .self:i was ever found for '" + self.path + "'"
    if os.path.exists(path):
      if os.path.isfile(path):
        if re.match(r'/\.self:i$',path):
          return self.slurp(path)
        else:
          return self.findSelf_i(os.path.dirname(path))
      elif os.path.isdir(path):
        if os.path.isfile(path + '/.self:i'):
          ref = self.slurp(path + '/.self:i')
          if re.match(r'^com\.opsware.*\d+$', ref):
            return ref
        if os.path.isfile(path + '/@/.self:i'):
          ref = self.slurp(path + '/@/.self:i')
          if re.match(r'^com\.opsware.*\d+$', ref):
            return ref
        return self.findSelf_i(os.path.dirname(path))
      else:
        raise Exception, "path '" + path + "' not a file or directory ( something else )"
    else:
      raise Exception, "path '" + path + "' not found on system"

  def slurp(self,file):
    p = open(file)
    txt = p.read()
    p.close()
    return txt

class DynamicDeviceGroup:
    def __init__(self, ref, vo):
        self.ref = ref
        self.vo = vo
        self._tmp_file = ""
        self.filter = ""

    def edit(self):
        valid = 0
        self.write_to_tmp()
        while not valid:
            os.system("TERM=xterm /bin/vi " + self._tmp_file)
            self.filter = string.strip(open(self._tmp_file).read())
            valid = self.test_filter()
        return

    def test_filter(self):
        if not self.filter: return 1
        f = Filter()
        f.expression = self.filter
        try:
            refs = ts.server.ServerService.findServerRefs(f)
        except Exception, e:
            print "e = %s" % e
            print "this looks like a bad filter - hit enter to re-edit or q to quit"
            yesno = raw_input()
            if yesno.lower().startswith("q"):
                sys.exit(0)
            else:
                return 0
        
        print "preview:\n"
        for r in refs:
            print "\t" + r.name
        print "enter 'y' to proceed, 'q' to quit, or enter to re-edit > ",
        yesno = raw_input()
        if yesno.lower().startswith("y"):
            return 1
        elif yesno.lower().startswith("q"):
            sys.exit(0)
        else:
            return 0

    def write_to_sas(self):
        if not self.filter:
            raise Exception, "can't write to SAS - no filter defined"
        f = Filter()
        f.expression = string.strip(self.filter)
        self.vo.dynamicRule = f
        print "\nSetting dynamic rule for %s to:" % vo.fullName
        print "\n" + self.filter
        try:
            ts.device.DeviceGroupService.update(self.ref, self.vo, 1, 1)
        except NoChangeRequestedException:
            pass
        return

    def write_to_tmp(self, ninput=""):
        fd_tmp_fd, fd_tmp_name = tempfile.mkstemp(suffix='.tmp')
        fh = os.fdopen(fd_tmp_fd, 'w+b')
        if ninput:
            fh.write(ninput)
        else:
            fh.write(vo.dynamicRule.expression)
        fh.close()
        self._tmp_file = fd_tmp_name
        return


if __name__ == '__main__':
    op = OptionParser(usage="%prog [-rp] /opsw/Group/some/dynamic/group")
    maingroup = OptionGroup(op, "Main Options")
    maingroup.add_option("--read", "-r", dest="readonly", help="Read from stdin instead of editing", action="store_true", default=False)
    maingroup.add_option("--print", "-p", dest="printonly", help="Print instead of editing", action="store_true", default=False)
    op.add_option_group(maingroup)

    (options, args) = op.parse_args()

    pm = None

    if len(args) == 0:
        try:
            pm = PathMagic(".")
        except:
            pass
    elif len(args) == 1:
        try:
            pm = PathMagic(args[0])
        except:
            pass

    if not pm:
        op.print_help()
        sys.exit()

    vo = pm.getVO()
    if not vo.dynamic:
        print "ERROR: %s is not a dynamic group" % pm.path
        sys.exit(1)

    if options.printonly:
        print vo.dynamicRule.expression + "\n"
    elif options.readonly:
        d = DynamicDeviceGroup(pm.getRef(), pm.getVO())
        d.filter = sys.stdin.read()
        d.write_to_sas()
    else:
        d = DynamicDeviceGroup(pm.getRef(), pm.getVO())
        d.edit()
        d.write_to_sas()

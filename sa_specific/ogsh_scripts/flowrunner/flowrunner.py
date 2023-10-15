#!/usr/bin/python
# flowrunner.py
# run PAS flows from the global shell w/ stored flows, auth and other cool stuff
#

import os, sys, socket, string, urllib, urllib2, base64
from optparse import OptionParser, OptionGroup
from ConfigParser import ConfigParser, NoOptionError, NoSectionError
from xml.dom import minidom
sys.path.append("/opt/opsware/pylibs2")
from opsware_common import obfuscator

justxml = 0

class FlowRunner:
    def __init__(self):
        self.host = ""
        self.port = "8443"
        self.proto = "https"
        self.flow = ""
        self.uuid = ""
        self.url = ""
        self.username = ""
        self.password = ""
        self.args = {}

    def set_url(self,url=""):
        if url:
            #self.url = urllib.quote(url, safe='''/;:?=+,!@#$%^&*()_-'"[]''')
            self.url = url.replace(' ', '%20')
        elif self.uuid:
            self.url = "%(proto)s://%(host)s:%(port)s/PAS/services/http/execute/%(uuid)s" % (self.__dict__)
        else:
            if not self.flow.startswith("/"):
                self.flow = "/" + self.flow
            self.url = "%(proto)s://%(host)s:%(port)s/PAS/services/http/execute/Library" % (self.__dict__)
            self.url += urllib.quote(self.flow)
        return

    def add_arg(self,key,val):
        self.args[key] = val
        return

    def update_args(self,args):
        self.args.update([ string.split(x,"=",1) for x in args ])
        return

    def run(self):
        if self.args:
            args = urllib.urlencode(self.args)
            full_url = self.url + "?" + args
        else:
            full_url = self.url
        if not justxml:
            print "Executing flow: %s" % full_url

        ## PAS requires pre-emptive auth, so this won't work - left here for reference
        #passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        #passman.add_password(None, self.url, self.username, self.password)
        #authhandler = urllib2.HTTPBasicAuthHandler(passman)
        #opener = urllib2.build_opener(authhandler)
        #urllib2.install_opener(opener)

        req = urllib2.Request(full_url)
        authheader = "Basic %s" % base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
        req.add_header("Authorization", authheader)

        fh = urllib2.urlopen(req)
        response = fh.read()
        fh.close()

        return response


class DataStore:
    def __init__(self):
        self.credentials = {}
        self.rcfile = os.path.expanduser("~/.flowrc")
        self.parser = ConfigParser()
        self.parser.read(self.rcfile)

    def get_flow(self, flow):
        try:
            return self.parser.get("flows", flow)
        except NoOptionError, e:
            return None
        except NoSectionError, e:
            return None

    def get_cred(self, cred):
        try:
            crypted = self.parser.get("creds", cred)
            saltstr = os.popen('whoami').readline()[:-1] * 4
            userstr = obfuscator.decrypt(crypted, saltstr)
            splits = userstr.split("+++", 1)
            if len(splits) != 2:
                return None, None
            else:
                return (splits[0], splits[1])
        except NoOptionError, e:
            return None, None
        except NoSectionError, e:
            return None, None

    def add_flow(self, flow, url):
        if "flows" not in self.parser.sections():
            self.parser.add_section("flows")
        self.parser.set("flows", flow, url)
        self.parser.write(open(self.rcfile, "w"))
        return 1

    def add_cred(self, cred, user, pw):
        if "creds" not in self.parser.sections():
            self.parser.add_section("creds")
        userstr = "%s+++%s" % (user, pw)
        saltstr = os.popen('whoami').readline()[:-1] * 4
        crypted = string.strip(obfuscator.encrypt(userstr, saltstr))
        self.parser.set("creds", cred, crypted)
        self.parser.write(open(self.rcfile, "w"))
        return 1

    def rm_flow(self, flow):
        if "flows" not in self.parser.sections():
            return 1
        if self.parser.remove_option("flows", flow):
            self.parser.write(open(self.rcfile, "w"))
            return 1
        else:
            return 0

    def rm_cred(self, cred):
        if "creds" not in self.parser.sections():
            return 1
        if self.parser.remove_option("creds", cred):
            self.parser.write(open(self.rcfile, "w"))
            return 1
        else:
            return 0

    def list_flows(self):
        if not self.parser.has_section("flows"):
            return None
        return self.parser.items("flows")

    def list_creds(self):
        creds = []
        if not self.parser.has_section("creds"):
            return None
        for x, y in self.parser.items("creds"):
            if x:
                u, p = self.get_cred(x)
                if u and p:
                    creds.append((x, u + "/" + "*" * len(p)))
        return creds


if __name__ == '__main__':
    op = OptionParser(usage="%prog [-supficrtx] arg1=val1 arg2=val2")
    maingroup = OptionGroup(op, "Main Options")
    credgroup = OptionGroup(op, "Credential Related Options")
    flowgroup = OptionGroup(op, "Flow Related Options")

    maingroup.add_option("-s", "--server", "--host", "--hostname", dest="host", help="OO Central Hostname", default="")
    maingroup.add_option("-u", "--user", "--username", dest="username", help="OO Username", default="")
    maingroup.add_option("-p", "--pass", "--password", dest="password", help="OO password", default="")
    maingroup.add_option("-f", "--flow", dest="flow", help="Path to flow (/Library is implied)", default="")
    maingroup.add_option("-i", "--uuid", dest="uuid", help="Run a flow by UUID", default="")
    maingroup.add_option("-c", "--cred", "--credentials", dest="creds", help="Use a stored credential (by keyword)", default="")
    maingroup.add_option("-r", "--url", dest="url", help="Call a flow by URL", default="")
    maingroup.add_option("-t", "--timeout", dest="timeout", help="Timeout", default="")
    maingroup.add_option("-x", "--justxml", dest="justxml", action='store_true', help="When specified, flowrunner will output the XML response from OO without parsing it.", default="")

    credgroup.add_option("--store-creds", dest="storecreds", help="Store credentials by keyword (store as 'default' for default use)", default="")
    credgroup.add_option("--list-creds", dest="listcreds", help="List credentials", action='store_true', default=False)
    credgroup.add_option("--remove-creds", dest="removecreds", help="Remove credentials", default="")

    flowgroup.add_option("--store-flow", dest="storeflow", help="Create a new keyword for a particular flow", default="")
    flowgroup.add_option("--list-flows", dest="listflows", help="List stored flows", action='store_true', default=False)
    flowgroup.add_option("--remove-flow", dest="removeflow", help="Remove stored flow", default="")

    op.add_option_group(maingroup)
    op.add_option_group(credgroup)
    op.add_option_group(flowgroup)

    (options, args) = op.parse_args()

    flow = FlowRunner()
    
    if options.timeout:
        socket.setdefaulttimeout(int(options.timeout))

    if options.justxml:
	justxml = 1

    if options.storecreds:
        ## storing creds
        if options.username and options.password:
            if DataStore().add_cred(options.storecreds, options.username, options.password):
                print "SUCCESS: stored new credentials keyword '%s' -> %s/%s" % (options.storecreds, options.username, "*" * len(options.password))
            else:
                print "ERROR: couldn't store new keyword '%s'" % options.storecreds
        else:
            op.error("Missing required options for --store-creds: --username & --password")

    elif options.listcreds:
        print "Stored credentials:\n"
        cl = DataStore().list_creds()
        if cl:
            print string.join([ "%20s -> %s" % (x[0], x[1]) for x in cl ], "\n")
        else:
            print "None found."

    elif options.removecreds:
        if DataStore().rm_cred(options.removecreds):
            print "SUCCESS: removed stored cred '%s'" % options.removecreds
        else:
            print "ERROR: couldn't find stored cred with keyword '%s'" % options.removecreds

    elif options.storeflow:
        ## storing flows
        if options.host and options.flow:
            flow.host = options.host
            flow.flow = options.flow
            flow.set_url()
        elif options.host and options.uuid:
            flow.host = options.host
            flow.uuid = options.uuid
            flow.set_url()
        elif options.url:
            flow.url = options.url
        else:
            op.error("Missing required options for --store-flow: --host + --flow, --host + --uuid, or --url")

        if DataStore().add_flow(options.storeflow, flow.url):
            print "SUCCESS: stored new flow keyword '%s' -> %s" % (options.storeflow, flow.url)
        else:
            print "ERROR: couldn't store new keyword '%s'" % options.storeflow

    elif options.listflows:
        print "Stored flows:\n"
        cl = DataStore().list_flows()
        if cl:
            print string.join([ "%20s -> %s" % (x[0], x[1]) for x in cl ], "\n")
        else:
            print "None found."

    elif options.removeflow:
        if DataStore().rm_flow(options.removeflow):
            print "SUCCESS: removed stored cred '%s'" % options.removeflow
        else:
            print "ERROR: couldn't find stored cred with keyword '%s'" % options.removeflow

    else:
        ## get flow info
        if options.host and options.flow:
            flow.host = options.host
            flow.flow = options.flow
            flow.set_url()
        elif options.host and options.uuid:
            flow.host = options.host
            flow.uuid = options.uuid
            flow.set_url()
        elif options.url:
            flow.set_url(options.url)
        elif not options.host and options.flow:
            ## stored flow
            url = DataStore().get_flow(options.flow)
            if url:
                flow.set_url(url)
            else:
                op.error("I can't find a stored flow named '%s'" % options.flow)                
        else:
            ## see if we're being called via a symlink, and if so try to find a keyword flow with the same name
            url = DataStore().get_flow(os.path.basename(sys.argv[0]))
            if url:
                flow.set_url(url)
            else:
                op.error("Need either a hostname + flow, a hostname + uuid, a url or a flow shortname to continue")

        ## get authentication info
        if options.username and options.password:
            flow.username = options.username
            flow.password = options.password
        elif options.creds:
            ## stored creds
            flow.username, flow.password = DataStore().get_cred(options.creds)
            if not flow.username or not flow.password:
                op.error("I can't find valid stored credentials named '%s'" % options.creds)
        else:
            ## try to get the default stored creds
            flow.username, flow.password = DataStore().get_cred("default")
            if not flow.username or not flow.password:
                op.error("Need either --username + --password, or --creds to continue")

        ## update flow args
        flow.update_args(args)

        ## run flow
        try:
            resp = flow.run()
            if resp:
                if justxml:
                    print resp
                    print
                    sys.exit(0)
                xmldom = minidom.parseString(resp)
                success = xmldom.firstChild.firstChild.getElementsByTagName("flow-response")[0].firstChild.data
                print "\nResponse: %s" % success
                returncode = xmldom.firstChild.firstChild.getElementsByTagName("flow-return-code")[0].firstChild.data
                print "\nReturn Code: %s" % returncode
                result = xmldom.firstChild.firstChild.getElementsByTagName("flow-result")[0].firstChild.data
                print "\nResult:\n%s\n" % result
                runid = xmldom.firstChild.firstChild.getElementsByTagName("run-id")[0].firstChild.data
                print "\nRun ID: %s" % runid
                runreportURL = xmldom.firstChild.firstChild.getElementsByTagName("run-report-url")[0].firstChild.data
                print "\nRun Report URL: %s" % runreportURL
        except urllib2.HTTPError, e:
            print "ERROR: server error:%s" % e
            sys.exit(1)
        except urllib2.URLError, e:
            print "ERROR: connection error: %s" % e
            sys.exit(1)

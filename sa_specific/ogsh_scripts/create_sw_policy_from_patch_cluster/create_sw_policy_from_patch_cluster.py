#!/usr/bin/python
# Since this runs within the OGSH, it will be written for Python 2.4.2

import sys
import string
import os
import time

from ocli_lib import common
from ocli_lib import policy

solaris={'10':30007,'10x86':10044,'8':150001,'9':920007}

def usage():
        print "usage: %s <os version> <patch_order filename> <patch cluster name>" % (sys.argv[0])
        print
        print "<os version> must be one of (10, 10x86, 8, 9)"
        print
        print
        sys.exit(1)

if len(sys.argv) != 4:
        usage()


def main(os_ver, patch_order_filename, patch_cluster_name):
        patch_order_file = open(patch_order_filename, "r")
        patches = patch_order_file.readlines()
        patches = map(string.strip, patches)
        bad_patches = []

	print "Checking that all patches are imported:",
        for patch_name in patches:
                cmd = "/opsw/api/com/opsware/pkg/solaris/SolPatchService/method/.findSolPatchRefs\:i filter='{name EQUAL_TO \"%s\"}'" % (patch_name)
                rv, output = common.runCommand(cmd)
                if output == '':
                        bad_patches.append(patch_name)
		sys.stdout.write('.')
		sys.stdout.flush()
	print ""

        if len(bad_patches):
                print "*** ERROR: The following patches are missing from the software repository. Please import the patches before continuing."
                for patch_name in bad_patches:
                        print patch_name
                sys.exit(1)

        policyname = "/Solaris Patch Clusters/%s" % patch_cluster_name

        print "Finding or creating policy %s." % (policyname)
	os_str = "SunOS 5.%s" % os_ver
        plcy = policy.Policy(policy_name=policyname, os_id=solaris[os_ver], os_str=os_str)

        print "Adding %s patches to policy %s." % (len(patches), policyname)

        plcy.setPatches(patches)
        print "Done."


if __name__ == "__main__":
        main(sys.argv[1], sys.argv[2], sys.argv[3])

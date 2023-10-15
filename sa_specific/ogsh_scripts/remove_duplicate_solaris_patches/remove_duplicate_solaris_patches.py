#!/usr/bin/python
#
# remove_duplicate_solaris_patches.py
#
# This is untested, but should work
import os, string

def getCmdAsList(cmd=None):
    child = os.popen(cmd)
    output = child.read()
    rv = child.close()
    if rv:
        raise RuntimeError, '%s failed with exit code %d' % (cmd, rv)
    lines = output.split('\n')
    lines = map(string.rstrip, lines)
    lines = filter(None, lines)
    return lines

def idFromRef(str=None):
    cpos = str.rfind(':')
    if cpos != -1:
        str = str[cpos+1:]
    return str

def getSolPatchFileType(rid=None):
    filetype = None
    rid = idFromRef(rid)
    cmd = "/opsw/api/com/opsware/pkg/solaris/SolPatchService/method/.findSolPatchRefs\:s filter='{id EQUAL_TO \"%s\" }'" % rid
    pdata = getCmdAsList(cmd)
    for p in pdata:
        if p[:9] == "fileType=":
            filetype = p[9:]
            filetype = filetype.strip('"')
            # it would be nice to jump out of the loop here, but if the patch info has ^fileType= anywhere in the info, this can break
    return filetype

def getSolPatchOSVersion(rid=None):
    ostype = None
    rid = idFromRef(rid)
    cmd = "/opsw/api/com/opsware/pkg/solaris/SolPatchService/method/.findSolPatchRefs\:s filter='{id EQUAL_TO \"%s\" }'" % rid
    pdata = getCmdAsList(cmd)
    for p in pdata:
        if p[:9] == "platform=":
            filetype = p[9:]
            filetype = filetype.strip('"')
            # it would be nice to jump out of the loop here, but if the patch info has ^platform= anywhere in the info, this can break
    return ostype

def removePatch(patch_ref=None):
    patch_ref = idFromRef(patch_ref)
    cmd = "/opsw/api/com/opsware/pkg/solaris/SolPatchService/method/remove self:i=%s" % patch_ref
    retcode = os.system(cmd)
    if (retcode >> 8) & 0xFF:
        return 1
    else:
        return 0

def getParentPolicies(patch_ref=None):
    cmd = "/opsw/api/com/opsware/pkg/solaris/SolPatchService/method/getSoftwarePolicies self:i=%s" % patch_ref
    try:
        parentlist = getCmdAsList(cmd)
    except:
        parentlist = []
    return parentlist


cmd = "/opsw/api/com/opsware/pkg/solaris/SolPatchService/method/.findSolPatchRefs\:n filter='{name LIKE \"%\" }'"

patches = getCmdAsList(cmd)

for patch in patches:
    cmd = "/opsw/api/com/opsware/pkg/solaris/SolPatchService/method/.findSolPatchRefs\:i filter='{name EQUAL_TO \"%s\" }'" % (patch)
    patchrefs = getCmdAsList(cmd)
    #print "%s: %s" % (patch, len(patchrefs))
    if len(patchrefs) > 1:
        ## TODO: dequalify this as a duplicate patch if the patches are for different OS's
        ## using getSolPatchOSVersion()
        print "* Multiple patch references found for name: %s" % patch
        for ref in patchrefs:
            ref_type = getSolPatchFileType(ref)
            parents = getParentPolicies(ref)
            pcount = len(parents)
            if pcount == 0:
                if ref_type == "JAR":
                    ## Criteria for removal: if filetype is JAR and doesn't exist in a policy (pcount == 0)
                    removePatch(ref)
                    print "  - %s (%s)  **removed**" % (ref, ref_type)
                else:
                     print "  - %s (%s)" % (ref, ref_type)
            else:
                print "  - %s (%s)" % (ref, ref_type)
                for p in parents:
                    print "    - AttachedToPolicy: %s " % p
#!/usr/bin/python
# Spinwrapper in OGSH approach for SA 7.5 and below

import sys, os
sys.path.insert(0,'/opt/opsware/pylibs2')

from coglib import spinwrapper, certmaster
from socket import gethostname

def get_spin(ts=None):
    if not ts:
        from pytwist import twistserver
        ts = twistserver.TwistServer()
    filterstr = 'ServerVO.hostName EQUAL_TO %s' % gethostname()
    core_ref = ts.search.SearchService.findObjRefs(filterstr, 'device')[0]
    certmaster.crypto_path = '/opsw/.Server.ID/%s/files/root/var/opt/opsware/crypto/' % core_ref.id
    certmaster.crypto_format = os.path.join(certmaster.crypto_path, "%s", "%s")
    ctx = certmaster.getContextByName("spin", "spin.srv", "opsware-ca.crt")
    return spinwrapper.SpinWrapper("https://localhost:1004", ctx=ctx)

s = get_spin()

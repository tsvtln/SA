#!/usr/bin/env python
#This script demonstrates how to run spinwrapper from the OGSH or an APX
#The basic trick is to get access to spin.srv and opsware-ca.crt from 
#the OGFS slice host where this code is running
import os
import sys

pylibsPath = "/opt/opsware/pylibs2"

if pylibsPath not in sys.path:
    sys.path.insert(0, pylibsPath)

from coglib import certmaster
from coglib import spinwrapper

def getSpin():
	certmaster.crypto_path = "/opsw/.Server.ID/.self/files/root/var/opt/opsware/crypto"
	certmaster.crypto_format = os.path.join(certmaster.crypto_path, "%s", "%s")
	ctx = certmaster.getContextByName("spin", "spin.srv", "opsware-ca.crt")
	return spinwrapper.SpinWrapper(ctx=ctx)
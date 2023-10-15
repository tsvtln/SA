import sys
import os

sys.path.append("/opt/opsware/pylibs")

import pytwist

import pytwist;from pytwist.com.opsware.locality import CustomerRef

ts = pytwist.twistserver.TwistServer()
ts.authenticate('detuser', sys.argv[1])

OPSWARE=CustomerRef(15)

# Get all ldap attributes
d= {}
for ns in ['com.hp.ldap.configuration','com.hp.ldap.configuration.credentials']:
	print "n====%s" % ns
	d[ns] = ts.locality.CustomerService.getCustAttrs(OPSWARE, ns, None, 0)
	 
print "ldap attributes ===%s" % d

# Delete all ldap attributes:
isDelete = False
try:
	value = sys.argv[2]
	isDelete = True
except:
	isDelete = False
if isDelete:
	for key in d:
		dict_obj = d[key]
		print "dict_obj==%s" % dict_obj
		for dict_key in dict_obj:
			print "removing dict_key==%s" % dict_key
			ts.locality.CustomerService.removeCustAttr(OPSWARE, key, dict_key)

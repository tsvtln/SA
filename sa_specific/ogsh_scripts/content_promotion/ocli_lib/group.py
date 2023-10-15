#!/usr/bin/python

import string
import os
import re

import common


class Group:

	id = None
	short_name = None

	def __init__(self, group_id=None, group_name=None):
		# if they gave us the name, we'll fetch the id
		if group_id:
			self.id = group_id

		elif group_name:
			cmd = "/opsw/api/com/opsware/device/DeviceGroupService/method/.findDeviceGroupRefs\:i filter='{ DeviceGroupVO.shortName = \"%s\" }'" % (group_name)

			# inferior:
			#cmd = "cat \"/opsw/Group/Public/%s/@/.id\"" % (group_name)

			rv, output = common.runCommand(cmd)
			if rv:
				msg = "Attempt to retrieve group \"%s\" failed:\n %s" % (group_name, output)
				raise Exception(msg)

			output = string.split(output,":",1)[-1]
			self.id = string.strip(output)
		else:
			raise
		

	def getServers(self):
		cmd = "/opsw/api/com/opsware/device/DeviceGroupService/method/getDevices self:i=%s" % self.id

		rv, output = common.runCommand(cmd)
		if rv:
			msg = "Attempt to retrieve servers for group failed:\n %s" % output
			raise Exception(msg)
	
		svr_list = string.split(output)
	
		return svr_list

	def getCustomAttribute(self, key):
		cmd =	"/opsw/api/com/opsware/device/DeviceGroupService/method/getCustAttr self:i=com.opsware.device.DeviceGroupRef:%s key=%s" % (self.id, key)

		rv, output = common.runCommand(cmd)
		if rv:
			output = ""
			#msg = "Attempt to retrieve servers for group failed:\n %s" % output
			#raise Exception(msg)

		return output
	

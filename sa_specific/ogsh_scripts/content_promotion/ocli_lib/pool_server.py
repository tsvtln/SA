#!/usr/bin/python

import string
import os
import re

import common

class PoolServer:
	
	id = None
	full_id = None
	name = None
	os = None
	os_type = None
	lifecycle = None

	def __init__(self, server_id=None, server_name=None):
		# if they gave us the name, we'll fetch the id and vice versa
		if server_id:
			server_id = string.strip(server_id)
			# get the server's hostname
			# the sed command in the next line strips out leading and trailing "s
			cmd = "%s/getServerVO self:i=%s 2>&1 |grep name | cut -d= -f2 | sed 's/^\"\(.*\)\"$/\\1/'" % (common.server_apis, server_id)
			rv, output = common.runCommand(cmd)
			if rv:
				msg = "Attempt to retrieve server name for \"%s\" failed:\n %s" % (server_id, output)
				raise Exception(msg)
			elif not output:
				msg = "Attempt to retrieve server name for server id \"%s\" failed, perhaps no server exists with this id?" % (server_id)
				raise Exception(msg)

			self.name = string.strip(output)

		elif server_name:
			self.name = server_name
			cmd = "%s/getServerVO self:n=%s 2>&1 |grep mid | cut -d= -f2 | sed 's/^\"\(.*\)\"$/\\1/'" % (common.server_apis, server_name)
			rv, output = common.runCommand(cmd)
			if rv:
				msg = "Attempt to retrieve server id for \"%s\" failed:\n %s" % (server_name, output)
				raise Exception(msg)
			elif not output:
				msg = "Attempt to retrieve server id for server name \"%s\" failed, perhaps no server exists with this id?" % (server_name)
				raise Exception(msg)
			self.id = string.strip(output)
			
		else:
			raise
		self.full_id = "com.opsware.server.ServerRef:%s" % self.id

	# CLI example: ./startOSSequence self:i=com.opsware.server.ServerRef:6530001 params='{oSSequence:i=com.opsware.osprov.OSSequenceRef:310001}';echo
	# os_sequence_id can be in full form (starting with "com.opsware.osprov.OSSequenceRef:", or just the id
	def provisionServer(self, os_sequence_id):
		if os_sequence_id[:4] != "com.":
			os_sequence_id = "com.opsware.osprov.OSSequenceRef:%s" % (os_sequence_id)
		cmd = "%s/startOSSequence self:i=%s params='{oSSequence:i=%s}'" % (common.server_apis, self.full_id, os_sequence_id)
		rv, output = common.runCommand(cmd)
		if rv:
			msg = "Attempt to invoke OS provisioning failed:\n %s" % (output)
			raise Exception(msg)
		return output

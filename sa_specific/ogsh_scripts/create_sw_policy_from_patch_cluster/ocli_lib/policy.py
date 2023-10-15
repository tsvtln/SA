#!/usr/bin/python

import string
import os
import common
import time
import re

import folder

OS_INDEPENDENT=1
slash_re = re.compile(r"\\")

class Policy:

	id = None
	os_string = None
	full_name = None
	short_name = None
	ogsh_path = None

	def __str__(self):
		return self.short_name

	# if you pass an os in, it needs to be the integer value representing the OS
	def __init__(self, policy_id=None, policy_name=None, os_id=None, os_str=None):
		self.os_string = os_str
		# if they gave us the name, we'll fetch the id and vice versa
		if policy_id:
			self.id = string.strip(policy_id)
			
			# the sed command in the next line strips out leading and trailing "s
			cmd = "%s/getSoftwarePolicyVO self:i=\"%s\" 2>&1 |grep ^name | cut -d= -f2 | sed 's/^\"\(.*\)\"$/\\1/'" % (common.policy_apis, self.id)

			rv, output = common.runCommand(cmd)
			#print rv, output
			if rv:
				msg = "Attempt to retrieve policy name for \"%s\" failed:\n %s" % (policy_id, output)
				raise Exception(msg)
			self.short_name = string.strip(output)

			# TODO: need to figure out how to get the full_name + ogsh_path

		elif policy_name:
			policy_name = slash_re.sub("/", policy_name)

			self.full_name = policy_name
			self.short_name = os.path.basename(policy_name)
	
			# look to see if it already exists
			self.ogsh_path = os.path.join("/opsw/Library", policy_name[1:], "@")

			if os.path.isdir(self.ogsh_path):
				self.id = open("%s/.self:i" % self.ogsh_path).read()
			else:
				# create it, since it doesn't already exist
				# should maybe separate this into its own method
				
				# first find the parent policy's id
				parent_path = os.path.dirname(self.full_name)

				if parent_path == "/":
					parent_id = 0
				else:
					# find or create the parent folder
					parent_folder = folder.Folder(folder_name=parent_path)
					parent_id = parent_folder.id

				#cmd = "%s/create softwarePolicyVO=\"{ name='%s' platforms:i=%s folder:i=%s }\"" % (common.policy_apis,self.short_name,OS_INDEPENDENT,parent_id)
				if not os_id:
					os_id = OS_INDEPENDENT

				cmd = "%s/create vo=\"{ name='%s' platforms:i=%s folder:i=%s }\"" % (common.policy_apis,self.short_name,os_id,parent_id)

				#print cmd
				rv, output = common.runCommand(cmd)
				if rv:
					msg = "Attempt to create policy %s failed:\n %s" % (policy_name, output)
					raise Exception(msg)

				# now we'll get the id of the policy we just created	
				idfilename = "%s/.self:i" % self.ogsh_path
				cnt = 0
				while not os.path.isfile(idfilename):
					# it sometimes takes a second for the id file to be created
					# retry a few times before giving up
					time.sleep(2)
					cnt = cnt + 1
					if cnt > 5:
						# this thing just isn't getting created, we'll try to 
						# continue (but probably error out on the next stmt
						break

				self.id = open("%s/.self:i" % self.ogsh_path).read()

	def attachServer(self, server_id):
		cmd = "%s/attachToPolicies selves:i=%s attachables:i=%s" % (common.policy_apis, self.id, server_id)
		rv, output = common.runCommand(cmd)
		if rv:
			msg = "Attempt to attach server %s to policy %s failed:\n %s" % (server_id, self.short_name, output)
			raise Exception(msg)

	def addPackage(self, package_id):
		cmd = "/opsw/api/com/opsware/swmgmt/SoftwarePolicyService/method/update self:i=3910001 vo='{softwarePolicyItems:i=com.opsware.pkg.solaris.SolPatchRef:54960001}';echo"
		pass

	# this will overwrite the current package list with the vo passed in
	# vo should be enclosed in {}'s when it is passed in
	def update(self, vo):
		cmd = "%s/update self:i=%s vo='%s' force=true" % (common.policy_apis, self.id, vo)
		rv, output = common.runCommand(cmd)
		if rv:
			msg = "Attempt to update policy %s failed:\n %s" % (self.short_name, output)
                        raise Exception(msg)

	def getPatchIDfromName(self, patch_name):
		# First, get a list of all patches with this name
		cmd = "/opsw/api/com/opsware/pkg/solaris/SolPatchService/method/.findSolPatchRefs\:i filter='{name EQUAL_TO \"%s\"}'" % (patch_name)
		rv, output = common.runCommand(cmd)
		if output == '':
			msg = "Attempt to retrieve id for patch %s failed:\n %s" % (patch_name, output)
			raise Exception(msg)
		patch_list = string.split(string.strip(output),'\n')
		# if we only see one patch, assume it's the right version
		if len(patch_list) == 1:
			return patch_list[0]
		for patch in patch_list:
			cmd = "/opsw/api/com/opsware/pkg/solaris/SolPatchService/method/getSolPatchVO self:i=%s | grep -c '^platform=\"%s\"'" % (patch,self.os_string)
			rv, output = common.runCommand(cmd)
			if output == '':
				msg = "Cannot find OS version for patch %s" % (patch)
				raise Exception(msg)
			if string.strip(output) != "0":
				return patch
		# Hmm, no matching patches found... just raise an exception
		msg = "Cannot find patch %s for OS %s" % (patch_name,self.os_string)
		raise Exception(msg)
			

	# patch list should be a python list of patch ids
	def setPatches(self, patch_list):
		#patches = map(lambda x: "softwarePolicyItems:i=com.opsware.pkg.solaris.SolPatchRef:%s" % x, patch_list)
		patch_list = map(lambda x: self.getPatchIDfromName(x), patch_list)
		patch_list = map(lambda x: "softwarePolicyItems:i=%s" % x, patch_list)
		vo = "{" + string.join(patch_list, " ") + "}"
		self.update(vo)



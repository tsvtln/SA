#!/usr/bin/python
#

import string
import os
import common
import time

class Folder:

	id = None
	full_name = None
	short_name = None
	ogsh_path = None

	def __init__(self, folder_id=None, folder_name=None):
		# if they gave us the name, we'll fetch the id and vice versa
		if folder_id:
			self.id = string.strip(folder_id)
			
			# the sed command in the next line strips out leading and trailing "s
			cmd = "%s/getFolderVO self:i=\"%s\" 2>&1 |grep ^name | cut -d= -f2 | sed 's/^\"\(.*\)\"$/\\1/'" % (common.folder_apis, self.id)

			rv, output = common.runCommand(cmd)
			print rv, output
			if rv:
				msg = "Attempt to retrieve folder name for \"%s\" failed:\n %s" % (folder_id, output)
				raise Exception(msg)
			self.short_name = string.strip(output)

			# TODO: need to figure out how to get the full_name + ogsh_path

		elif folder_name:
			self.full_name = folder_name
			self.short_name = os.path.basename(folder_name)
	
			# look to see if it already exists
			self.ogsh_path = os.path.join("/opsw/Library", folder_name[1:], "@")

			if os.path.isdir(self.ogsh_path):
				self.id = open("%s/.self:i" % self.ogsh_path).read()
			else:
				# create it, since it doesn't already exist
				
				# first find the parent folder's id
				parent_path = os.path.dirname(self.full_name)

				if parent_path == "/":
					parent_id = 0
				else:
					# recurse to find or create the parent folder
					parent_folder = Folder(folder_name=parent_path)
					parent_id = parent_folder.id

				cmd = "%s/create vo=\"{ name='%s' folder:i=%s }\"" % (common.folder_apis,self.short_name,parent_id)

				rv, output = common.runCommand(cmd)
				if rv:
					msg = "Attempt to create folder %s failed:\n %s" % (folder_name, output)
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

				# now we'll get the id of the folder we just created	
				self.id = open(idfilename).read()
				
	# this will overwrite the current package list with the vo passed in
	# vo should be enclosed in {}'s when it is passed in
	def update(self, vo):
		cmd = "%s/update self:i=%s vo='%s' force=true" % (common.folder_apis, self.id, vo)
		rv, output = common.runCommand(cmd)
		if rv:
			msg = "Attempt to update folder %s failed:\n %s" % (self.short_name, output)
			raise Exception(msg)

	def addACL(self, usergroup_name, access_level):
		usercmd = "/opsw/api/com/opsware/fido/UserRoleService/method/.findUserRoleRefs:i filter='{UserRoleVO.roleName CONTAINS \"%s\"}'" % (usergroup_name)

		rv, user_group_id = common.runCommand(usercmd)

		cmd = "%s/addFolderACLs acls='{accessLevel=\"%s\" folder:i=%s role:i=%s}'" % (common.folder_apis, access_level, self.id, user_group_id)

		print "cmd = %s" % cmd

		rv, out = common.runCommand(cmd)
		if rv:
			msg = "Attempt to add ACL to folder %s failed:\n %s" % (self.short_name, out)
			raise Exception(msg)
		return

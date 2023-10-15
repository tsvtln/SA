#!/usr/bin/python
#

import string
import os
import common
import time
import re

class Folder:

	id = None
	full_name = None
	short_name = None
	ogsh_path = None
	quote_re = re.compile('^\\"')

	def __init__(self, folder_id=None, folder_name=None, folder_desc=""):
		# if they gave us the name, we'll fetch the id and vice versa
		if folder_id:
			self.id = string.strip(folder_id)
			
			# the sed command in the next line strips out leading and trailing "s
			cmd = "%s/getFolderVO self:i=\"%s\" 2>&1 |grep ^name | cut -d= -f2 | sed 's/^\"\(.*\)\"$/\\1/'" % (common.folder_apis, self.id)

			rv, output = common.runCommand(cmd)
			#print rv, output
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

			#print "path = %s" % self.ogsh_path
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

				# now we'll get the id of the folder we just created
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

				# now we'll set the id of the folder we just created	
				self.id = open(idfilename).read()

				if folder_desc:
					self.setDescription(desc=folder_desc)
				
	# this will overwrite the current package list with the vo passed in
	# vo should be enclosed in {}'s when it is passed in
	def update(self, vo):
		cmd = "%s/update self:i=%s vo='%s' force=true" % (common.folder_apis, self.id, vo)
		rv, output = common.runCommand(cmd)
		if rv:
			msg = "Attempt to update folder %s failed:\n %s" % (self.short_name, output)
			raise Exception(msg)

	def setDescription(self, desc):
		descfile = open("%s/attr/description" % self.ogsh_path, "w")
		descfile.write(desc)
		descfile.close()
		#vo = "{description=\"%s\"}" % (desc)
		#self.update(vo)

	def getDescription(self):
		desc = open("%s/attr/description" % self.ogsh_path).read()
		return string.strip(desc)

	def addACL(self, usergroup_name, access_level):
		usercmd = "/opsw/api/com/opsware/fido/UserRoleService/method/.findUserRoleRefs:i filter='{UserRoleVO.roleName = \"%s\"}'" % (usergroup_name)

		rv, user_group_id = common.runCommand(usercmd)

		if not user_group_id:
			msg = "Couldn't find user group id for user group %s." % (usergroup_name)
			raise Exception(msg)

		cmd = "%s/addFolderACLs recursive=\"true\" acls='{accessLevel=\"%s\" folder:i=%s role:i=%s}'" % (common.folder_apis, access_level, self.id, user_group_id)

		rv, out = common.runCommand(cmd)
		if rv:
			msg = "Attempt to add %s ACL to folder %s for user group % failed:\n %s" % (access_level, self.short_name, usergroup_name, out)
			raise Exception(msg)
		return

	def removeACL(self, usergroup_name, access_level):
		usercmd = "/opsw/api/com/opsware/fido/UserRoleService/method/.findUserRoleRefs:i filter='{UserRoleVO.roleName = \"%s\"}'" % (usergroup_name)

		rv, user_group_id = common.runCommand(usercmd)

		if not user_group_id:
			msg = "Couldn't find user group id for user group %s." % (usergroup_name)
			raise Exception(msg)

		cmd = "%s/removeFolderACLs recursive=\"true\" acls='{accessLevel=\"%s\" folder:i=%s role:i=%s}'" % (common.folder_apis, access_level, self.id, user_group_id)

		rv, out = common.runCommand(cmd)
		if rv:
			msg = "Attempt to remove %s ACL from folder %s for user group % failed:\n %s" % (access_level, self.short_name, usergroup_name, out)
			raise Exception(msg)
		return

	def getOSSequences(self):
		seq_dir_path = os.path.join(self.ogsh_path, "OSSequence")
		seqs = os.listdir(seq_dir_path)
		seq_ids = []
		for seq in seqs:
			idfile_path = os.path.join(seq_dir_path, seq, ".self:i")
			id = open(idfile_path).read()
			seq_ids.append(id)
		return seq_ids

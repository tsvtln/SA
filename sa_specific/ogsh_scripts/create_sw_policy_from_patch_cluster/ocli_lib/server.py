#!/usr/bin/python

import string
import os
import re

import common

class Server:
	
	id = None
	full_id = None
	name = None
	os = None
	os_type = None
	dir = None
	method_dir = None
	temp_dir = None
	swd_dir = None
	user = None
	python = None

	# the next 2 REs are for converting windows paths to unix ones
	drive_re = None
	slash_re = None

	def __init__(self, server_id=None, server_name=None):
		# if they gave us the name, we'll fetch the id and vice versa
		if server_id:
			server_id = string.strip(server_id)
			# the sed command in the next line strips out leading and trailing "s
			cmd = "%s/getServerVO self:i=%s 2>&1 |grep name | cut -d= -f2 | sed 's/^\"\(.*\)\"$/\\1/'" % (common.server_apis, server_id)
			rv, output = common.runCommand(cmd)
			if rv:
				msg = "Attempt to retrieve server name for \"%s\" failed:\n %s" % (server_id, output)
				raise Exception(msg)
			self.name = string.strip(output)

		elif server_name:
			self.name = server_name

		else:
			raise

		# set the directory in OGSH for this server
		self.dir = "/opsw/Server/@/%s/" % (self.name)
		self.method_dir = "/opsw/Server/@/%s/method" % (self.name)

		self.full_id = open("%s/.self:i" % self.dir).read()
		self.id = string.split(self.full_id, ":")[-1]

		self.getState()

		# set the OS for this server object
		self.os = open(os.path.join(self.dir, "attr/osVersion")).read()

		# set the OS type (Windows or Unix) for this server
		if string.find(self.os, "Windows") != -1:
			self.os_type = "Windows"
			self.user = "LocalSystem"
			# determine the %ProgramFiles% dir TODO: test this
			# This is gonna take more work on windows, may have to store the 
			# local version of dirs, and what it looks like in ogsh
			if self.state != "OK":
				return
			rv, progfiles = self.runCommand("echo %ProgramFiles%")
			progfiles = string.strip(progfiles)
			self.temp_dir = r"%s\Common Files\opsware\agent" % progfiles
			self.swd_dir = r"%s\swd" % self.temp_dir
			self.python = r"%s\Opsware\agent\lcpython15\python.exe" % progfiles
		else:
			self.os_type = "Unix"
			self.user = "root"
			self.temp_dir = "/var/opt/opsware/agent"
			self.swd_dir = "%s/swd" % self.temp_dir
			self.python = "/opt/opsware/agent/bin/python"


	def getGroups(self):
		cmd = "%s/getDeviceGroups self:i=%s" % (common.server_apis, self.id)
	
		rv, output = common.runCommand(cmd)
		if rv:
			msg = "Attempt to retrieve groups for server failed:\n %s" % output
			raise Exception(msg)
	
		group_list = string.split(output, "\n")
		group_list.remove('')
	
		return group_list

	def isPolicyAttached(self, policy_name):
		cmd = "%s/getSoftwarePolicyAssociations |grep policy=\\\"%s\\\"" % (self.method_dir, policy_name)
		rv, output = common.runCommand(cmd)
		if rv:
			# the grep failed, meaning we didn't find a policy of that name attached
			return None
		else:
			return 1


	def runCommand(self, cmd):

		# Rules for running commands on windows servers:
		# - double quotes must surround each argument that has a space in it
		# ex. this will work:  rosh -l LocalSystem -i 20001 "\"C:\Program Files\Opsware\agent\lcpython15\python.exe\" -c \"print 'hello'\""
		cmd = "/opsw/bin/rosh -l %s -i %s \"%s\"" % (self.user, self.id, cmd)
		rv, output = common.runCommand(cmd)
		return rv, output

	# using rosh's script pushing feature (-s) to run a script on the remote
	# box
	def runScript(self, script):
		cmd = ""
		if script[-4:] == ".vbs" and self.os_type == "Windows":
			# it's a visual basic script, we'll copy the script over and run it 
			# with "cscript"
			self.copyFileToServer(script, self.temp_dir)
			script_path = r"\"%s/%s\"" % (self.temp_dir, os.path.basename(script))
			cmd = "/opsw/bin/rosh -l %s -i %s \"cscript /nologo %s\"" % (self.user, self.id, script_path)
			# TODO: should delete the script after we run it, but 
		else:
			cmd = "/opsw/bin/rosh -l %s -i %s -s %s" % (self.user, self.id, script)

		rv, output = common.runCommand(cmd)
		return rv, output

	def convPathToUnix(self, path):
		# the first time this method runs, we'll compile the REs
		if not self.drive_re:
			self.drive_re = re.compile("([a-zA-Z]):")
	
		if not self.slash_re:
			self.slash_re = re.compile(r"\\")

		path = self.drive_re.sub(r'\1',path)
		path = self.slash_re.sub("/", path)
		return path

	def getOGSHPath(self, local_path):
		ogsh_filename = local_path
		if self.os_type == "Windows":
			ogsh_filename = self.convPathToUnix(ogsh_filename)
		else:
			if ogsh_filename[0] == "/":
				ogsh_filename = ogsh_filename[1:]
		ogsh_filename = os.path.join(self.dir, "files", self.user, ogsh_filename)
		return ogsh_filename
		
	# src filename should be a path within the OGFS, dst_filename should be 
	# relative to the root directory on the server
	# For windows, the dst_filename can be in windows filename format or unix, 
	# we'll convert it to unix format before copying the file.
	def copyFileToServer(self, src_filename, dst_filename):
		dst_filename = self.getOGSHPath(dst_filename)

		dst_dir = os.path.dirname(dst_filename)
		if not os.path.isdir(dst_dir):
			common.debug("Directory %s doesn't exist yet, creating it." % dst_dir)
			os.makedirs(dst_dir)

		cmd = "/bin/cp -f \"%s\" \"%s\"" % (src_filename, dst_filename)
		common.debug("Copying file %s to %s." % (src_filename, dst_filename))
		rv, output = common.runCommand(cmd)
		if rv:
			msg = "Copy of %s to %s returned %s.  Output: \n%s" % (src_filename, dst_filename, rv, output)
			raise Exception(msg)
		return 1

	# src dirname should be a path within the OGFS, dst_dirname should be 
	# relative to the root directory on the server
	# For windows, the dst_dirname can be in windows dirname format or unix, 
	# we'll convert it to unix format before copying the dir.
	def copyDirToServer(self, src_dirname, dst_dirname):
		dst_dirname = self.getOGSHPath(dst_dirname)

		# if you have problems w/ this during development because it copies
		# RO files, then can't write over them, chmod -R ogu+x the directory
		# you're copying (ex. .svn/)
		cmd = "/bin/cp -rf \"%s\" \"%s\"" % (src_dirname, dst_dirname)
		common.debug("Copying dir %s to %s." % (src_dirname, dst_dirname))
		rv, output = common.runCommand(cmd)
		if rv:
			msg = "Copy of %s to %s returned %s.  Output: \n%s" % (src_dirname, dst_dirname, rv, output)
			raise Exception(msg)
		return 1

	# takes a string and a destination filename (relative to root of the server)
	# and writes a new file out in that location with the contents passed in
	def writeFileToServer(self, contents, dst_filename):
		dst_filename = self.getOGSHPath(dst_filename)
		common.debug("Writing out file %s" % dst_filename)
		dst_file = open(dst_filename, "w")
		dst_file.write(contents)
		dst_file.close()
		return 1
	
	def setCustomAttribute(self, key, value):
		key = string.strip(key)
		custattrfilename = os.path.join(self.dir, "CustAttr", key)
		custattrfile = open(custattrfilename, "w")
		custattrfile.write(value)
		custattrfile.close()

	def delCustomAttribute(self, key):
		key = string.strip(key)
		custattrfilename = os.path.join(self.dir, "CustAttr", key)
		if os.path.isfile(custattrfilename):
			os.unlink(custattrfilename)

	def setCustomField(self, field_name, str_value="", long_value="", date_value=""):
		if not str_value:
			print "Only string custom fields implemented at this point"
			return
		
		cmd = "%s/setCustomField fieldName=%s strValue=\"%s\"" % (self.method_dir, field_name, str_value)
	
		rv, output = common.runCommand(cmd)
		if rv:
			msg = "Attempt to set custom field for server failed:\n %s" % output
			raise Exception(msg)
		
	def getCustomField(self, field_name):
		cmd = "%s/getCustomField fieldName=%s" % (self.method_dir, field_name)
		rv, output = common.runCommand(cmd)
		if rv:
			msg = "Attempt to get custom field for server failed:\n %s" % output
			raise Exception(msg)
		return output
		


	def getState(self):
		self.state = open(os.path.join(self.dir, "attr/state")).read()
		return self.state

	# returns the contents of the server's "info" file
	def getInfo(self):
		info = open(os.path.join(self.dir, "info")).read()
		return info

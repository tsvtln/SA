#!/usr/bin/env python

import sys
import string
import re
import exceptions
import os.path
from xmllib import *
from opsware_common.errors import OpswareError

# Config values
tempLocation = "C:\\temp" 
auditLocation = "C:\\temp\\audit" 
rootLocation = "C:\\temp\\audit\\dotnet_xml_config" 

#
# Possible exceptions that can be raised by the parser.
#
class DotNetConfigInfoSyntaxError (exceptions.Exception):
	def __init__(self, args=None):
		if( args is None ):
			self.args = "DotNetConfigInfoSyntaxError"
		else:
			self.args = args

class Directory:
	def __init__( self, parentDirName, cwdName, parent):
		if parentDirName == None:
			self.parentDirName = cwdName
		else:
			self.parentDirName = parentDirName
		self.cwdName = cwdName
		self.parent = parent
		self.subDirs = {}
		self.files = {}

	def addSubDir( self, subDirName ):
		newdir = Directory( os.path.join( self.parentDirName, self.cwdName ), subDirName, self )
		self.subDirs[subDirName] = newdir
		return newdir

	def getParent( self ):

		return self.parent
		
	def addFile( self, name, value ):
		self.files[name] = value
		
	def createFileStructure( self ):
		if self.subDirs is not None:
			for d in self.subDirs.keys():
				try:					
					aresolved_dir_path = os.path.join( self.parentDirName, self.cwdName, d )
					os.mkdir( aresolved_dir_path )
				except OSError, (errno,strerror):
					# check for file exists, if so, continue
					if( errno == 17):
						pass
					else:
						raise
				except:
					raise
				self.subDirs[d].createFileStructure()
			
		if self.files is not None:
			for v in self.files.keys():
				path = os.path.join( self.parentDirName, self.cwdName, v )
				f = open( path, "wb" )
				f.write("%s=%s" % (v,self.files[v]) )
				f.close()
		
class DotNetConfigParser(XMLParser) :

	def filter_multiple_entries( self, x ):
		ret_value = []
		temp = ""
		for c in x:
			if c == temp:
				continue
			else:
				temp = c
				ret_value.append( c )
		return ret_value

	def __init__(self, rootDirectory ):

		self.__initElemLists()
		self.__elemLists = []
		self.__accumData = 0
		self.__curData = None
		self.__curAttrs = None
		self.debug_parser = 0
		self.elements = self.__topLevelElems
		self.error = None
		self.rootDirectory = Directory( None, rootDirectory, None )
		self.cwd = self.rootDirectory
		
		XMLParser.__init__(self)

	def __initElemLists(self) :
		self.__topLevelElems = {
			"configuration" : (self.start_configuration, None),
			}
		self.__configurationElems = {
			"mscorlib" : (self.start_mscorlib, None),
			"configSections" : (self.start_configsections, None),
			"configuration" : (None, self.end_configuration),
			}
		self.__mscorlibElems = {
			"security" : (self.start_security, None),
			"mscorlib" : (None, self.end_mscorlib),
			}
#		self.__configSectionsElems = {
#			"section" : (self.start_section, None),
#			"sectionGroup" : (self.start_sectiongroup, None),
#			"configSections" : (None, self.end_configsections),
#			}
		self.__securityElems = {
			"policy" : (self.start_policy, None),
			"security" : (None, self.end_security),
			}
		self.__policyElems = {
			"PolicyLevel" : (self.start_policylevel, None),
			"policy" : (None, self.end_policy),
			}
		self.__policyLevelElems = {
			"NamedPermissionSets" : (self.start_namedpermissionsets, None),
			"SecurityClasses" : (self.start_securityclasses, None),
			"CodeGroup" : (self.start_codegroup, None),
			"FullTrustAssemblies" : (self.start_fulltrustassemblies, None),
			"PolicyLevel" : (None, self.end_policylevel),
			}
		self.__securityClassesElems = {
			"SecurityClass" : (self.start_securityclass, self.end_securityclass),
			"SecurityClasses" : (None, self.end_securityclasses ),
			}
		self.__namedPermissionSetsElems = {
			"PermissionSet" : (self.start_permissionset, None),
			"NamedPermissionSets" : (None, self.end_namedpermissionsets),
			}
		self.__permissionSetElems = {
			"IPermission" : (self.start_ipermission, None),
			"PermissionSet" : (None, self.end_permissionset),
			}
		self.__ipermissionElems = {
			"Machine" : (self.start_machine, self.end_machine),
			"IPermission" : (None, self.end_permissionset),
			}
		self.__codeGroupElems = {
			"CodeGroup" : (self.start_codegroup, self.end_codegroup),
			"IMembershipCondition" : (self.start_imembershipcondition, self.end_imembershipcondition),
			}
		self.__fullTrustAssembliesElems = {
			"IMembershipCondition" : (self.start_imembershipcondition, self.end_imembershipcondition),
			"FullTrustAssemblies" : (None, self.end_fulltrustassemblies),
			}

	def __setError(self, error, override = 0) :
		if override or self.error is None :
			self.error = error
			
	def __initData(self, init = "") :
		self.__curData = init
		self.__accumData = 1
		
	def __clearData(self) :
		str = self.__curData
		self.__curData = None
		self.__accumData = 0
		self.__currAttrs = None
		return str
	
	def syntax_error(self, message):
		if self.debug_parser :
			print "Recoverable syntax error, line number: '%d', xmllib message: '%s'" % (self.lineno, message)
		return

	def unknown_starttag(self, tag, attrs):
		self.__setError("Unknown tag: '%s' at line %d" % ( tag, self.lineno ))
		raise DotNetConfigInfoSyntaxError, self.error				 

	def handle_data(self, data):
		if self.__accumData :
			data = string.strip(data)
			if len(self.__curData) > 0 and len(data) > 0 :
				spacer = " "
			else :
				spacer = ""
			self.__curData = self.__curData + spacer + data

	def close(self):
		self.__elemLists = None
		self.__curData = None
		self.__curAttrs = None
		self.elements = None
		self.error = None
		XMLParser.close(self)
		
	# ----------------------------------------------------------------------
	# Top level elements
	# ----------------------------------------------------------------------
	
	def start_configuration(self, attrs) :
		if self.debug_parser :
			print "START CONFIGURATION"
		self.__elemLists.append(self.elements)
		self.elements = self.__configurationElems
		
		# Add a directory to the root level directory		
		self.cwd = self.cwd.addSubDir( "configuration" )
		
	def end_configuration(self) :
		if self.debug_parser :
			print "END CONFIGURATION"
		self.elements = self.__elemLists.pop()
		self.cwd = self.cwd.getParent()
		
	# ----------------------------------------------------------------------
	# Elements under <configuration>
	# ----------------------------------------------------------------------

	def start_mscorlib(self, attrs) :
		if self.debug_parser :
			print " START MSCORLIB"

		# Prepare the elements stack for the incoming XML data
		self.__elemLists.append(self.elements)
		self.elements = self.__mscorlibElems

		self.cwd = self.cwd.addSubDir( "mscorlib" )
		
	def end_mscorlib(self) :
		if self.debug_parser :
			print " END MSCORLIB"
		self.elements = self.__elemLists.pop()
		self.cwd = self.cwd.getParent()

	def start_configsections(self, attrs) :
		if self.debug_parser :
			print " START CONFIGSECTIONS"

		self.__elemLists.append(self.elements)
		self.elements = self.__configSectionsElems
		self.cwd = self.cwd.addSubDir( "configSections" )

	def end_configsections(self) :
		if self.debug_parser :
			print " END CONFIGSECTIONS"
		self.elements = self.__elemLists.pop()
		self.cwd = self.cwd.getParent()
		
	# ----------------------------------------------------------------------
	# Elements under <mscorlib>
	# ----------------------------------------------------------------------

	def start_security(self, attrs) :
		if self.debug_parser :
			print "  START SECURITY"

		# Prepare the elements stack for the incoming XML data
		self.__elemLists.append(self.elements)
		self.elements = self.__securityElems
		self.cwd = self.cwd.addSubDir( "security" )

	def end_security(self) :
		if self.debug_parser :
			print "  END SECURITY"
		self.elements = self.__elemLists.pop()
		self.cwd = self.cwd.getParent()

	# ----------------------------------------------------------------------
	# Elements under <security>
	# ----------------------------------------------------------------------

	def start_policy(self, attrs) :
		if self.debug_parser :
			print "   START POLICY"
		self.__elemLists.append(self.elements)
		self.elements = self.__policyElems
		self.cwd = self.cwd.addSubDir( "policy" )

	def end_policy(self) :
		if self.debug_parser :
			print "   END POLICY"
		self.elements = self.__elemLists.pop()
		self.cwd = self.cwd.getParent()

	# ----------------------------------------------------------------------
	# Elements under <policy>
	# ----------------------------------------------------------------------

	def start_policylevel(self, attrs) :
		if self.debug_parser :
			print "    START POLICYLEVEL"
		self.__elemLists.append(self.elements)
		self.elements = self.__policyLevelElems
		self.cwd = self.cwd.addSubDir( "PolicyLevel" )

		# Harvest the attributes from the start tag
		keys = attrs.keys()
		for key in keys:
			self.cwd.addFile( key, attrs[key] )
				
	def end_policylevel(self) :
		if self.debug_parser :
			print "    END POLICYLEVEL"
		self.elements = self.__elemLists.pop()
		self.cwd = self.cwd.getParent()

	# ----------------------------------------------------------------------
	# Elements under <policylevel>
	# ----------------------------------------------------------------------

	def start_securityclasses(self, attrs) :
		if self.debug_parser :
			print "     START SECURITYCLASSES"
		self.__elemLists.append(self.elements)
		self.elements = self.__securityClassesElems

		self.cwd = self.cwd.addSubDir( "SecurityClasses" )

		# Harvest the attributes from the start tag
		keys = attrs.keys()
		for key in keys:
			self.cwd.addFile( key, attrs[key] )

	def end_securityclasses(self) :
		if self.debug_parser :
			print "     END SECURITYCLASSES"
		self.elements = self.__elemLists.pop()
		self.cwd = self.cwd.getParent()

	def start_namedpermissionsets(self, attrs) :
		if self.debug_parser :
			print "     START NAMEDPERMISSIONSETS"
		self.__elemLists.append(self.elements)
		self.elements = self.__namedPermissionSetsElems
		self.cwd = self.cwd.addSubDir( "NamedPermissionSets" )

		# Harvest the attributes from the start tag
		keys = attrs.keys()
		for key in keys:
			self.cwd.addFile( key, attrs[key] )

	def end_namedpermissionsets(self) :
		if self.debug_parser :
			print "     END NAMEDPERMISSIONSETS"
		self.elements = self.__elemLists.pop()
		self.cwd = self.cwd.getParent()

	def start_codegroup(self, attrs) :
		if self.debug_parser :
			print "     START CODEGROUP"
		self.__elemLists.append(self.elements)
		self.elements = self.__codeGroupElems
		
		keys = attrs.keys()
		for key in keys:
			if string.lower(key) == "class":
				n1 = attrs[key]
			if string.lower(key) == "name":
				n2 = attrs[key]

		fname = "CodedGroup-%s-%s" % (n1,n2)
		self.cwd = self.cwd.addSubDir( fname )

		# Harvest the attributes from the start tag
		keys = attrs.keys()
		for key in keys:
			self.cwd.addFile( key, attrs[key] )

	def end_codegroup(self) :
		if self.debug_parser :
			print "     END CODEGROUP"
		self.elements = self.__elemLists.pop()
		self.cwd = self.cwd.getParent()

	def start_fulltrustassemblies(self, attrs) :
		if self.debug_parser :
			print "     START FULLTRUSTASSEMBLIES"
		self.__elemLists.append(self.elements)
		self.elements = self.__fullTrustAssembliesElems
		self.cwd = self.cwd.addSubDir( "FullTrustAssemblies" )

		# Harvest the attributes from the start tag
		keys = attrs.keys()
		for key in keys:
			self.cwd.addFile( key, attrs[key] )

	def end_fulltrustassemblies(self) :
		if self.debug_parser :
			print "     END FULLTRUSTASSEMBLIES"
		self.elements = self.__elemLists.pop()
		self.cwd = self.cwd.getParent()

	# ----------------------------------------------------------------------
	# Elements under <securityclasses>
	# ----------------------------------------------------------------------

	def start_securityclass(self, attrs) :
		if self.debug_parser :
			print "      START SECURITYCLASS"

		keys = attrs.keys()
		for key in keys:
			if string.lower(key) == "name":
				name_value = attrs[key]

		fname = "SecurityClass-%s" % (name_value)
		self.cwd = self.cwd.addSubDir( fname )

		# Harvest the attributes from the start tag
		keys = attrs.keys()
		for key in keys:
			self.cwd.addFile( key, attrs[key] )

	def end_securityclass(self) :
		if self.debug_parser :
			print "      END SECURITYCLASS"
		self.cwd = self.cwd.getParent()

	# ----------------------------------------------------------------------
	# Elements under <namedpermissionsets>
	# ----------------------------------------------------------------------

	def start_permissionset(self, attrs) :
		if self.debug_parser :
			print "      START PERMISSIONSET"

		# Prepare the elements stack for the incoming XML data
		self.__elemLists.append(self.elements)
		self.elements = self.__permissionSetElems

		keys = attrs.keys()
		for key in keys:
			if string.lower(key) == "class":
				name_value = attrs[key]

		fname = "PermissionSet-%s" % (name_value)
		self.cwd = self.cwd.addSubDir( fname )

		# Harvest the attributes from the start tag
		keys = attrs.keys()
		for key in keys:
			self.cwd.addFile( key, attrs[key] )

	def end_permissionset(self) :
		if self.debug_parser :
			print "      END PERMISSIONSET"
		self.elements = self.__elemLists.pop()
		self.cwd = self.cwd.getParent()

	# ----------------------------------------------------------------------
	# Elements under <permissionset>
	# ----------------------------------------------------------------------

	def start_ipermission(self, attrs) :
		if self.debug_parser :
			print "       START IPERMISSION"
		self.__elemLists.append(self.elements)
		self.elements = self.__ipermissionElems

		keys = attrs.keys()
		for key in keys:
			if string.lower(key) == "class":
				name_value = attrs[key]

		fname = "IPermission-%s" % (name_value)
		self.cwd = self.cwd.addSubDir( fname )

		# Harvest the attributes from the start tag
		keys = attrs.keys()
		for key in keys:
			self.cwd.addFile( key, attrs[key] )

	def end_ipermission(self) :
		if self.debug_parser :
			print "       END IPERMISSION"
		self.elements = self.__elemLists.pop()
		self.cwd = self.cwd.getParent()

	# ----------------------------------------------------------------------
	# Elements under <ipermission>
	# ----------------------------------------------------------------------
	
	def start_machine(self, attrs) :
		if self.debug_parser :
			print "        START MACHINE"
		self.__initData()
		self.cwd = self.cwd.addSubDir( "Machine"  )

	def end_machine(self) :
		if self.debug_parser :
			print "        END MACHINE"
		self.cwd = self.cwd.getParent()

	# ----------------------------------------------------------------------
	# Elements under <fulltrustassemblies>
	# ----------------------------------------------------------------------

	def start_imembershipcondition(self, attrs) :
		if self.debug_parser :
			print "      START IMEMBERSHIPCONDITION"
		self.__initData()
		
		keys = attrs.keys()
		for key in keys:
			if string.lower(key) == "class":
				name_value = attrs[key]

		fname = "IMC-%s" % (name_value)
		self.cwd = self.cwd.addSubDir( fname )

		# Harvest the attributes from the start tag
		keys = attrs.keys()
		for key in keys:
			self.cwd.addFile( key, attrs[key] )

	def end_imembershipcondition(self) :
		if self.debug_parser :
			print "      END IMEMBERSHIPCONDITION"
		self.cwd = self.cwd.getParent()


	# ----------------------------------------------------------------------
	# Elements to be ignored
	# ----------------------------------------------------------------------
	def start_start(self, attrs) :
		if self.debug_parser :
			print "START START"
		self.__initData()

	def end_start(self) :
		if self.debug_parser :
			print "END START"
		new_start = int(self.__clearData())

	def start_end(self, attrs) :
		if self.debug_parser :
			print "START END"
		self.__initData()

	def end_end(self) :
		if self.debug_parser :
			print "END END"
		new_end = int(self.__clearData())



def testLoadFromFile(file):
	f = open(file, "r")
	try :
		data = f.read()
	finally :
		f.close()
	loadFromBuffer(data)


def parseConfig( xml_file, home ):
	f = open(xml_file, "r")
	try :
		data = f.read()
	finally :
		f.close()

	parser = DotNetConfigParser( home )
	parser.debug_parser = 0
	parser.feed( data )
	parser.close()

	if home is not None:
		try:
			os.mkdir( home )
		except OSError, (errno,strerror):
			# check for file exists, if so, continue
			if( errno == 17):
				pass
			else:
				raise
		except:
			raise	
		parser.rootDirectory.createFileStructure()

try:					
	os.mkdir( tempLocation )
except OSError, (errno,strerror):
	# check for file exists, if so, continue
	if( errno == 17):
		pass
	else:
		raise

try:					
	os.mkdir( auditLocation )
except OSError, (errno,strerror):
	# check for file exists, if so, continue
	if( errno == 17):
		pass
	else:
		raise

try:					
	os.mkdir( rootLocation )
except OSError, (errno,strerror):
	# check for file exists, if so, continue
	if( errno == 17):
		pass
	else:
		raise

# Locate security.config
dotnetconfig = 'Microsoft.NET\\Framework\\v1.1.4322\\CONFIG'
windowsdir = os.environ['SystemRoot']
securityConfig = os.path.join( windowsdir, dotnetconfig, 'security.config' ) 

parseConfig( securityConfig, rootLocation )

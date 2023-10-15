# Originonally written by Tsai.
# Modified by me to:
#   Accept passwords securely vai tty instead of on command line.
#

# -----------------------------------------------------------------------------
# SPECIFY THE DEVICE, USERID, AND PASSWORD
# -----------------------------------------------------------------------------
# main will look for dvc_id, if none, it will look for dvc with specified
# dvc_management_ip, if dvc_management_ip is None, it will look for dvc with
# dvc_desc.
#
# userid/password is used to authenticate with the twist, this is your OCCC
# userid/password.
# -----------------------------------------------------------------------------
dvc_id = None                          # this should be an int or long
dvc_management_ip = '192.168.225.17'   # this should be a string
dvc_desc = 'testserver.opsware.com'    # this should be a string

userid = None                    # this should be a string
password = None                  # this should be a string
# -----------------------------------------------------------------------------



import os
import sys
import time
import types
import string
import pprint
import traceback
#if os.path.isdir('/opt/opsware/pylibs2/shadowbot'):
#	sys.path.append('/opt/opsware/pylibs2')
#else:
#	sys.path.append('/opt/opsware/pylibs')
sys.path.append('/opt/opsware/spin')
if not os.environ.has_key( "SPIN_DIR" ):
	os.environ["SPIN_DIR"] = "/opt/opsware/spin"


import truthdb
from coglib import spinwrapper
from coglib import certmaster
ctx = certmaster.getContextByName("spin","spin.srv","opsware-ca.crt")
spin = spinwrapper.SpinWrapper(ctx=ctx)


from pytwist import *
from pytwist.com.opsware.pkg import DevicePatch
from pytwist.com.opsware.pkg import PatchVO
from pytwist.com.opsware.server import ServerRef
from pytwist.com.opsware.swmgmt import WindowsPatchPolicyRef
from pytwist.com.opsware.fido import AuthenticationException
from pytwist.com.opsware.fido import AuthorizationDeniedException
twistServer = None



COMPLIANCE_STATE_NON_COMPLIANT = 'NON-COMPLIANT'
COMPLIANCE_STATE_PARTIAL_COMPLIANT = 'PARTIAL-COMPLIANT'
COMPLIANCE_STATE_COMPLIANT = 'COMPLIANT'
COMPLIANCE_STATE_BLANK = ''
complianceCodeToLabelMap = {}
complianceCodeToLabelMap['R'] = COMPLIANCE_STATE_NON_COMPLIANT
complianceCodeToLabelMap['Y'] = COMPLIANCE_STATE_PARTIAL_COMPLIANT
complianceCodeToLabelMap['G'] = COMPLIANCE_STATE_COMPLIANT
complianceCodeToLabelMap['B'] = COMPLIANCE_STATE_BLANK
complianceLevelToCodeMap = {'1':'B',  '2':'R',  '3':'G',  '4':'R',  '5':'G', '6':'B',  '7':'Y',  '8':'R',  '9':'G',  '10':'R', '11':'R', '12':'R', '13':'Y', '14':'R', '15':'G', '16':'G', '17':'G', '18':'R', '19':'G', '20':'R'}



# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# SQL to fetch platform patches
# -----------------------------------------------------------------------------
sql_patformPatches = """
SELECT
u.unit_display_name,
u.unit_type,
u.software_release,
u.unit_id,
u.unit_file_name,
patch_locale.label,
u.unit_loc

FROM
units u,
(SELECT units.unit_id AS unit_id, virtual_column_values.text_value AS label FROM truth.unit_virtual_column_values, truth.virtual_column_values, truth.virtual_columns, truth.units WHERE units.unit_id=unit_virtual_column_values.unit_id AND unit_virtual_column_values.virtual_column_value_id=virtual_column_values.virtual_column_value_id AND virtual_column_values.virtual_column_id=virtual_columns.virtual_column_id AND virtual_columns.virtual_column_name='patch_locale') patch_locale

WHERE
u.platform_id=%s AND
u.unit_type in ('HOTFIX', 'SERVICE_PACK', 'UPDATE_ROLLUP') AND
u.unit_id=patch_locale.unit_id(+)

ORDER BY
u.unit_display_name,
u.unit_id
"""

sql_policyPatches = """
SELECT
u.unit_display_name,
u.unit_type,
u.software_release,
u.unit_id

FROM
role_class_wads rcw,
rc_template_elements rcte,
role_classes rc,
units u,

(SELECT rc.role_class_id AS role_class_id, u.unit_id AS unit_id FROM role_classes rc, role_class_wads rcw, rc_wad_elements rcwe, units u WHERE rc.stack_id = 15 AND rc.role_class_id = rcw.role_class_id AND rcw.rc_wad_id = rcwe.rc_wad_id AND rcwe.rc_element_id = u.unit_id AND u.unit_type in ('HOTFIX', 'SERVICE_PACK', 'UPDATE_ROLLUP')) rcu

WHERE
rcw.role_class_id = %s AND
rcw.rc_wad_id = rcte.rc_wad_id AND
rcte.role_class_id = rc.role_class_id AND
rc.role_class_id = rcu.role_class_id AND
rcu.unit_id = u.unit_id
"""





# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# authenticateWithTwist
# -----------------------------------------------------------------------------
def authenticateWithTwist(userid, password):
	global twistServer
	twistServer = twistserver.TwistServer()
	try:
		twistServer.authenticate(userid, password)
	except AuthenticationException:
		sys.stderr.write('error:  authentication error, please specify a valid userid and password\n')
		sys.exit(1)
	except:
		sys.stderr.write('error:  unable to authenticate\n')
		err = apply( traceback.format_exception_only, sys.exc_info()[0:2] )
		err = string.strip( string.join( err, "" ) )
		print err
		sys.exit(1)



# -----------------------------------------------------------------------------
# doQuery
# -----------------------------------------------------------------------------
def doQuery(db, sql):
    cur = db.getCursor()
    cur.execute(sql)
    return cur.fetchall()



# -----------------------------------------------------------------------------
# getComplianceLevelLabel
# -----------------------------------------------------------------------------
def getComplianceLevelLabel(level):
	result = ''
	level = str(level)
	if level[-1] == 'L':
		level = level[:-1]
	if complianceLevelToCodeMap.has_key(level):
		code = complianceLevelToCodeMap[level]
		if complianceCodeToLabelMap.has_key(code):
			result = complianceCodeToLabelMap[code]
	return result



# -----------------------------------------------------------------------------
# findDeviceIdByManagementIpOrDvcDesc
# -----------------------------------------------------------------------------
def findDeviceIdByManagementIpOrDvcDesc(management_ip=None, desc=None):
	result = None
	# User dvc_id if specified
	if dvc_id:
		result = dvc_id
	else:
		# Look for device matching specified management_ip
		if management_ip:
			dvcs = spin.Device.getAll(restrict={'management_ip':management_ip})
			for dvc in dvcs:
				result = dvc['dvc_id']
				break
		# If we still haven't found the device, look for device
		# matching specified desc
		if not result and desc:
			dvcs = spin.Device.getAll(restrict={'dvc_desc':desc})
			for dvc in dvcs:
				result = dvc['dvc_id']
	return result



# -----------------------------------------------------------------------------
# getUnitDetails
# -----------------------------------------------------------------------------
def getUnitDetails(unit_loc):
	print ''
	head, tail = os.path.split(unit_loc)
	units = spin.Unit.getAll(restrict={'unit_loc':unit_loc})
	if units:
		unit = units[0]
		print '* %s' % tail
		print '  - checksum:         %s %s' % (unit['checksum_hash_type'], unit['checksum'])
		print '  - filesize:         %s' % unit['file_size']
		if unit.get('software_version'):
			print '  - software_version: %s' % unit['software_version']
	else:
		print '* %s not found' % tail
		


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# outputWindowsPatchConfiguration
# -----------------------------------------------------------------------------
def outputWindowsPatchConfiguration():
	global complianceLevelToCodeMap
	print '\n\n\n'
	print '---------------------------'
	print 'Windows.Patch.Configuration'
	print '---------------------------'
	unit = spin.PatchMetaDataUnit.get(name='wsusscn2.cab')
	if unit:
		dict = unit.getMetaInfo()
		print 'last database upload:                            %s' % unit['modified_dt']
		print 'last database update:                            %s' % dict.get('last_data_update')

		roleClassPath = ['ServiceLevel', 'Opsware', 'word']
		rc = spin.RoleClass.getByPath(path=roleClassPath)
		lst = spin.RoleClass.getChildren(id=rc['id'], child_class='AppConfigWad')
		if lst and len(lst) > 0:
			dict = {}
			appConfigWad = lst[0]
			outerlist = appConfigWad.getLocalDictItems()
			for list in outerlist:
				key = list[0]
				val = list[1]
				if key == 'patchman.http_url_mbsa20_location':
					dict['patchman.http_url_mbsa20_location'] = val
				elif key == 'patchman.compliance_level_theme':
					dict['patchman.compliance_level_theme'] = val
				elif key == 'patchman.custom_policy_compliance_levels':
					dict['patchman.custom_policy_compliance_levels'] = val
				elif key == 'patchman.strict_policy_compliance_levels':
					dict['patchman.strict_policy_compliance_levels'] = val
				elif key == 'patchman.wrt_policy_compliance_levels':
					dict['patchman.wrt_policy_compliance_levels'] = val

				elif key == 'patchman.ms_mbsa20_selected_localelist':
					dict['patchman.ms_mbsa20_selected_localelist'] = val
				elif key == 'patchman.agent_locale_legacy_value_map':
					dict['patchman.agent_locale_legacy_value_map'] = val
				elif key == 'patchman.all_server_patches_additional_locales':
					dict['patchman.all_server_patches_additional_locales'] = val

				elif key == 'patchman.ms_mbsa20_products':
					dict['patchman.ms_mbsa20_products'] = val
				elif key == 'patchman.ms_mbsa20_selected_products':
					dict['patchman.ms_mbsa20_selected_products'] = val

			print 'patchman.http_url_mbsa20_location:               %s' % dict.get('patchman.http_url_mbsa20_location')
			print 'patchman.compliance_level_theme:                 %s' % dict.get('patchman.compliance_level_theme')
			if dict.get('patchman.compliance_level_theme') == 'WITH_RESPECT_TO_CUSTOMIZATIONS':
				print 'patchman.wrt_policy_compliance_levels:           %s' % dict.get('patchman.wrt_policy_compliance_levels')
				complianceLevelToCodeMap = eval(dict.get('patchman.wrt_policy_compliance_levels'))
			elif dict.get('patchman.compliance_level_theme') == 'STRICT':
				print 'patchman.strict_policy_compliance_levels:        %s' % dict.get('patchman.strict_policy_compliance_levels')
				complianceLevelToCodeMap = eval(dict.get('patchman.strict_policy_compliance_levels'))
			elif dict.get('patchman.compliance_level_theme') == 'CUSTOM':
				print 'patchman.custom_policy_compliance_levels:        %s' % dict.get('patchman.custom_policy_compliance_levels')
				complianceLevelToCodeMap = eval(dict.get('patchman.custom_policy_compliance_levels'))
			print 'patchman.ms_mbsa20_selected_localelist:          %s' % dict.get('patchman.ms_mbsa20_selected_localelist')
			print 'patchman.agent_locale_legacy_value_map:          %s' % dict.get('patchman.agent_locale_legacy_value_map')
			print 'patchman.all_server_patches_additional_locales:  %s' % dict.get('patchman.all_server_patches_additional_locales')

			selected = ''
			productdict = eval(dict.get('patchman.ms_mbsa20_products'))
			if productdict:
				selectedlist = eval(dict.get('patchman.ms_mbsa20_selected_products'))
				if selectedlist:
					try:
						for item in selectedlist:
							if len(selected):
								selected = '%s,   %s' % (selected, productdict.get(item))
							else:
								selected = productdict.get(item)
					except:
						selected = selectedlist
			print 'patchman.ms_mbsa20_selected_products:            %s' % selected

		getUnitDetails('/packages/any/nt/5.2/WindowsUpdateAgent20-x86.exe')
		getUnitDetails('/packages/any/nt/5.2/WindowsUpdateAgent20-x64.exe')
		getUnitDetails('/packages/any/nt/5.2/mbsacli20.exe')
		getUnitDetails('/packages/any/nt/5.2/wusscan.dll')
		getUnitDetails('/packages/any/nt/5.2/parsembsacli20.exe')
		getUnitDetails('/packages/any/nt/5.0/opswpatchlib.zip')

		print ''
		print '* indicators'
		print '  - unit_type:        ()'
		print '  - unit_id/rc_id:    ()'
		print '  - unit_locale       {}'
		print '  - unit_loc          <>'
		print '  - software_release  []'


# -----------------------------------------------------------------------------
# outputDeviceInfo
# -----------------------------------------------------------------------------
def outputDeviceInfo(dvc_id):
	print '\n\n\n'
	print '---------------'
	print 'spin.Device.get'
	print '---------------'
	dvc = spin.Device.get(id=dvc_id)
	print 'dvc_desc:          %s' % dvc.get('dvc_desc')
	print 'os_version:        %s' % dvc.get('os_version')
	print 'os_sp_version:     %s' % dvc.get('os_sp_version')
	print 'agent_version:     %s' % dvc.get('agent_version')
	print 'agent_locale:      %s' % dvc.get('agent_locale')
	print 'prev_sw_reg_date:  %s' % dvc.get('prev_sw_reg_date')




# -----------------------------------------------------------------------------
# outputComplianceVirtualColumns
# -----------------------------------------------------------------------------
def outputComplianceVirtualColumns(dvc_id):
	print '\n\n\n'
	print '---------------------------'
	print 'Device.Patch.VirtualColumns'
	print '---------------------------'
	resultdict = spin.Device.getVirtualColumnValues(id=dvc_id)
	print '%-48s: %s' % ('OPSWARE.patch.aggregate.code', resultdict.get('OPSWARE.patch.aggregate.code'))
	print '%-48s: %s' % ('OPSWARE.patch.aggregate.last_check_date', resultdict.get('OPSWARE.patch.aggregate.last_check_date'))
	print '%-48s: %s' % ('OPSWARE.patch.aggregate.out_of_compliance_count', resultdict.get('OPSWARE.patch.aggregate.out_of_compliance_count'))
	print '%-48s: %s' % ('OPSWARE.patch.aggregate.reason', resultdict.get('OPSWARE.patch.aggregate.reason'))



# -----------------------------------------------------------------------------
# outputDevicePatches
# -----------------------------------------------------------------------------
def outputDevicePatches(dvc_id):
	print '\n\n\n'
	print '-----------------------------'
	print 'patchService.getDevicePatches'
	print '-----------------------------'
	overrideRefs = []
	patchService = twistServer.pkg.PatchService
	serverRef = ServerRef(dvc_id)
	try:
		devicePatches = patchService.getDevicePatches(serverRef)
	except AuthorizationDeniedException:
		sys.stderr.write('error:  authorization error when attempting to view server patches\n')
		sys.exit(1)
	listNonCompliant = []
	listPartialCompliant = []
	listCompliant = []
	listOther = []
	for devicePatch in devicePatches:
		patchResult = ''
		appendList = listOther
		installedText = ''
		recommededText = ''
		if devicePatch.installed: installedText = ' is installed'
		if devicePatch.recommended: recommededText = ' is recommended'
		complianceLevelText = ''
		temp = getComplianceLevelLabel(devicePatch.aggregateComplianceLevel)
		if temp:
			complianceLevelText = ' "%s"' % temp
			if temp == COMPLIANCE_STATE_NON_COMPLIANT:
				appendList = listNonCompliant
			elif temp == COMPLIANCE_STATE_PARTIAL_COMPLIANT:
				appendList = listPartialCompliant
			elif temp == COMPLIANCE_STATE_COMPLIANT:
				appendList = listCompliant
		if devicePatch.patch:
			softwareRelease = devicePatch.softwareRelease
			patchResult = '%s (%s): %s%s [%s] %s (%s)%s' % (devicePatch.patch.name, devicePatch.unitType, installedText, recommededText, softwareRelease, devicePatch.aggregateComplianceLevel, devicePatch.policyOverride, complianceLevelText)
		else:
			patchResult = '%s (%s): %s%s [%s] %s (%s)%s' % (devicePatch.unitDisplayName, devicePatch.unitType, installedText, recommededText, 'None', devicePatch.aggregateComplianceLevel, devicePatch.policyOverride, complianceLevelText)
		appendList.append(patchResult)
		if devicePatch.policyOverride:
			overrideRefs.append(devicePatch.policyOverride)
	for list in [listNonCompliant, listPartialCompliant, listCompliant, listOther]:
		for item in list:
			print item
		if len(list) and list != listOther:
			print
	if len(overrideRefs):
		print '\n\n\n'
		print '---------------------------------'
		print 'patchService.getPolicyOverrideVOs'
		print '---------------------------------'

		vos = patchService.getPolicyOverrideVOs(overrideRefs)
		for vo in vos:
			print '%s (%s)' % (vo.name, vo.ref.id)
			print '- patch:   %s' % vo.patch
			print '- type:    %s' % vo.type
			print '- reason:  %s' % vo.reason
			print '- attach:  %s' % vo.policyAttachable
			print ''



# -----------------------------------------------------------------------------
# outputInstalledUnit
# -----------------------------------------------------------------------------
def outputInstalledUnit(dvc_id):
	print '\n\n\n'
	print '--------------------'
	print 'Device.InstalledUnit'
	print '--------------------'
	ius = spin.Device.getChildren(id=dvc_id, child_class='InstalledUnit')
	for iu in ius:
		softwareRelease = iu.get('software_release')
		print '%s (%s): [%s]' % (iu['unit_display_name'], iu['unit_type'], softwareRelease)



# -----------------------------------------------------------------------------
# outputRecommendedPatch
# -----------------------------------------------------------------------------
def outputRecommendedPatch(dvc_id):
	print '\n\n\n'
	print '-----------------------'
	print 'Device.RecommendedPatch'
	print '-----------------------'
	rps = spin.Device.getChildren(id=dvc_id, child_class='RecommendedPatch')
	for rp in rps:
		softwareRelease = rp.get('software_release')
		print '%s (%s): [%s]' % (rp['unit_display_name'], rp['unit_type'], softwareRelease)



# -----------------------------------------------------------------------------
# outputAttachedPolicies
# -----------------------------------------------------------------------------
def outputAttachedPolicies(dvc_id, db):
	print '\n\n\n'
	print '--------------------'
	print 'Device.PatchPolicies'
	print '--------------------'
	dvc_id_str = str(dvc_id)
	if dvc_id_str[-1] == 'L':
		dvc_id_str = dvc_id_str[:-1]
	policyIdToPolicyNameDict = {}
	searchService = twistServer.search.SearchService
	refs = searchService.findObjRefs('(patch_policy_dvc_id_direct = %s)' % dvc_id_str, 'patch_policy')
	for ref in refs:
		policyIdToPolicyNameDict[ref.id] = ref.name
		print 'directly attached policy:   %s (%s)' % (ref.name, ref.id)
	refs = searchService.findObjRefs('(patch_policy_dvc_id = %s)' % dvc_id_str, 'patch_policy')
	for ref in refs:
		if not policyIdToPolicyNameDict.has_key(ref.id):
			policyIdToPolicyNameDict[ref.id] = ref.name
			print 'indirectly attached policy: %s (%s)' % (ref.name, ref.id)

	policyService = twistServer.swmgmt.WindowsPatchPolicyService
	patchService = twistServer.pkg.PatchService
	policyIds = policyIdToPolicyNameDict.keys()
	for policyId in policyIds:
		policyRef = WindowsPatchPolicyRef(policyId)
		policyVO = policyService.getWindowsPatchPolicyVO(policyRef)
		if policyVO.type == 'DYNAMIC':
			continue
		print '\npatches for policy: %s' % policyVO.name
		policyIdStr = str(policyId)
		if policyIdStr and policyIdStr[-1] == 'L':
			policyIdStr = policyIdStr[:-1]
		results = doQuery(db, sql_policyPatches % policyIdStr)
		for result in results:
			print '%s (%s): [%s] (%s)' % (result[0], result[1], result[2], result[3])



# -----------------------------------------------------------------------------
# outputPlatformPatches
# -----------------------------------------------------------------------------
def outputPlatformPatches(dvc_id, db):
	print '\n\n\n'
	print '-----------------------'
	print 'Device.Platform.Patches'
	print '-----------------------'
	platform_id_str = None
	platforms = spin.Device.getChildren(id=dvc_id, child_class='Platform')
	for platform in platforms:
		platform_id_str = '%s' % platform['platform_id']
		if platform_id_str and platform_id_str[-1] == 'L':
			platform_id_str = platform_id_str[:-1]
		break
	if platform_id_str:
		results = doQuery(db, sql_patformPatches % platform_id_str)
		for result in results:
			print '%s (%s): [%s] (%s) %s {%s} <%s>' % (result[0], result[1], result[2], result[3], result[4], result[5], result[6])



# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def main():
	db = truthdb.DB()
	# Authenticate with Twist
	authenticateWithTwist(userid, password)
	# Find the user specified device
	dvc_id = findDeviceIdByManagementIpOrDvcDesc(dvc_management_ip, dvc_desc)
	if not dvc_id:
		sys.stderr.write('error:  invalid dvc_id specified\n')
		sys.exit(1)
	print 'Patch details for dvc_id:  %s' % dvc_id

	# Get spin version info
	result_dict = spin.sys.getAllConf()
	print 'spin.version:              %s' % result_dict.get('spin.version')

	# outputWindowsPatchConfiguration
	st = time.time()
	outputWindowsPatchConfiguration()
	print '%s:  %.02f' % ('', (time.time() - st))
	# outputDeviceInfo
	st = time.time()
	outputDeviceInfo(dvc_id)
	print '%s:  %.02f' % ('', (time.time() - st))
	# outputComplianceVirtualColumns
	st = time.time()
	outputComplianceVirtualColumns(dvc_id)
	print '%s:  %.02f' % ('', (time.time() - st))
	# outputDevicePatches
	st = time.time()
	outputDevicePatches(dvc_id)
	print '%s:  %.02f' % ('', (time.time() - st))
	# outputInstalledUnit
	st = time.time()
	outputInstalledUnit(dvc_id)
	print '%s:  %.02f' % ('', (time.time() - st))
	# outputRecommendedPatch
	st = time.time()
	outputRecommendedPatch(dvc_id)
	print '%s:  %.02f' % ('', (time.time() - st))
	# outputAttachedPolicies
	st = time.time()
	outputAttachedPolicies(dvc_id, db)
	print '%s:  %.02f' % ('', (time.time() - st))
	# outputPlatformPatches
	st = time.time()
	outputPlatformPatches(dvc_id, db)
	print '%s:  %.02f' % ('', (time.time() - st))



# -----------------------------------------------------------------------------
# usage
# -----------------------------------------------------------------------------
def usage():
	sys.stderr.write('error:  usage error\n')
	sys.stderr.write('\n')
	sys.stderr.write('usage:  /opt/opsware/bin/python  %s <dvc_id> <user_id> [<password>]\n' % sys.argv[0])
	sys.stderr.write('            dvc_id     : Opsware ID of server to report on\n')
	sys.stderr.write('            user_id    : OCC user name to authenticate with\n')
	sys.stderr.write('            password   : password of OCC user name\n')
	sys.stderr.write('                         (will prompt if not present.)\n')
	sys.stderr.write('\n')
	sys.stderr.write('example:\n')
	sys.stderr.write('    /opt/opsware/bin/python %s 880001 johns\n' % sys.argv[0])
	sys.stderr.write('\n')
	sys.exit(1)


import tty,termios,signal
def get_password():
  old_attrs = None
  stdin_fd = sys.stdin.fileno()
  sec_stdout_fd = stdin_fd
  try:
    old_attrs = tty.tcgetattr(stdin_fd)
    new_attrs = tty.tcgetattr(stdin_fd)
    new_attrs[3] = new_attrs[3] ^ tty.ECHO
    def sig_int(n, frame, stdin_fd=stdin_fd, sec_stdout_fd=sec_stdout_fd, old_attrs=old_attrs):
      tty.tcsetattr(stdin_fd, tty.TCSADRAIN, old_attrs)
      os.write(sec_stdout_fd, '\n')
      sys.exit(1)
    signal.signal(signal.SIGINT,sig_int)
    tty.tcsetattr(stdin_fd, tty.TCSADRAIN, new_attrs)
  except termios.error, e:
    sys.stderr.write("WARNING: stdin is not a tty, therefore password echoing cannot be disabled!\n")
    sec_stdout_fd = sys.stderr.fileno()

  # Actually read the password.
  os.write(sec_stdout_fd, "password: ")
  password = string.strip(sys.stdin.readline())
  os.write(sec_stdout_fd, "\n")

  if ( old_attrs ):
    tty.tcsetattr(stdin_fd, tty.TCSADRAIN, old_attrs)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

  # Return the read in password.
  return password


if __name__ == '__main__':
	if len(sys.argv) > 2:
		try:
			dvc_id = sys.argv[1]
			if dvc_id[-1] == 'L':
				dvc_id = dvc_id[:-1]
			dvc_id = long(dvc_id)
		except:
			usage()
		userid = sys.argv[2]
		if ( len(sys.argv) > 3 ):
			password = sys.argv[3]
		else:
			password = get_password()

		try:
			dvc = spin.Device.get(id=dvc_id)
		except:
			sys.stderr.write('error:  invalid dvc_id specified: %s\n' % dvc_id)
			sys.exit(1)
	if (dvc_id is None) or (userid is None) or (password is None):
		usage()
	main()


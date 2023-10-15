import sys
import whrandom

if "/lc/blackshadow" not in sys.path: sys.path.append("/lc/blackshadow")
sys.path.append("/cust/usr/blackshadow")

from coglib import spinwrapper
from coglib import certmaster

created_by = 'Create Fake Servers'
notes = 'generated by %s' % created_by

mfg_models = {
	'AIX'		: [ 'IBM', "7028-6C1" ],
	'HP-UX'		: [ 'HP', "9000/800/A400-6X" ],
	'LINUX'		: [ 'DELL COMPUTER CORPORATION', 'POWEREDGE 650' ],
	'SUNOS'		: [ 'SUN MICROSYSTEMS', "NETRA X1" ],
	'NT'	    : [ 'DELL COMPUTER CORPORATION', 'POWEREDGE 650' ],
}

def create_fake_device( spin, params ):

	platform_id	= long( params.get( "platform_id", "120000" ) )
	dc_id		= long( params.get( "dc_id", "1" ) )
	account_id	= long( params.get( "account_id", "15" ) )
	count		= long( params.get( "count", "1" ) )
	index		= long( params.get( "index", "0" ) )
	prefix		= params.get( "prefix", "fake" )
	postfix		= params.get( "postfix", ".opsware.com" )
	state		= params.get( "state", "OK" )
	stage		= params.get( "stage", "LIVE" )
	use		= params.get( "use", "PRODUCTION" )
	lifecycle	= params.get( "lifecycle", "MANAGED" )
	version		= params.get( "version", "" )

	# get an account cloud for the customer
	acs = spin.AccountCloud.getAll( restrict={'acct_id':account_id, 'data_center_id':dc_id} )
	if acs == None or len(acs) == 0:
		sys.stdout.write( "Error: Account cloud does not exist for customer %d and facility %d\n" % (account_id, dc_id) )
		return 1
	else:
		ac = acs[0]

		p = spin.Platform.get( platform_id )
		if p["os_version"]:
			os_version = p["os_version"]
		else:
			os_version = p["platform_name"]

		[mfg, model] = mfg_models.get( p["platform_short_name"], [None, None] )

		# set up the device and device role
		idx = 0
		randomIdx = long(round(whrandom.whrandom().random() * 255 * 255 * 255 * 255))
		for l in range( index, index + count ):

			name = '%s%04d%s' % (prefix, l, postfix)

			idx = idx + 1

			oct1 = ((randomIdx + l) & 0xFF)
			oct2 = ((randomIdx + l) & 0xFF00) >> 8
			oct3 = ((randomIdx + l) & 0xFF0000L) >> 16
			oct4 = ((randomIdx + l) & 0xFF000000L) >> 24
			oct5 = ((randomIdx + l) & 0xFF00000000L) >> 32
			oct6 = ((randomIdx + l) & 0xFF0000000000L) >> 40
			hexOct1 = hex(int(oct1))[2:]
			hexOct2 = hex(int(oct2))[2:]
			hexOct3 = hex(int(oct3))[2:]
			hexOct4 = hex(int(oct4))[2:]
			hexOct5 = hex(int(oct5))[2:]
			hexOct6 = hex(int(oct6))[2:]
			primary_ip = '%d.%d.%d.%d' % (oct1, oct2, oct3, oct4)
			hw_addr = '%s:%s:%s:%s:%s:%s' % (hexOct1, hexOct2, hexOct3, hexOct4, hexOct5, hexOct6)

			dvc_struct = {
				"chassis_id" : hw_addr,
				"dvc_type" : "SERVER",
				"agent_version" : version,
				"system_name" : name,
				"os_version" : os_version,
				"dvc_mfg" : mfg,
				"dvc_model" : model,
				"peer_ip" : primary_ip,
				"management_ip" : primary_ip,
				"interfaces" :
				[
					{
						"hw_addr" : hw_addr,
						"ip_address" : primary_ip,
						"slot" : "eth0",
						"interface_type" : "ethernet",
						},
					],
				}

			if lifecycle in ["UNPROVISIONED", "PROVISIONING", "PROVISION FAILED"]:
				dvc_id = apply( spin.Device.updateMiniAgentHW, (), dvc_struct )
				d = spin.Device.get( dvc_id )
				if lifecycle in ["PROVISIONING", "PROVISION FAILED"]:
					d.beginOSProvision()
					if (lifecycle == "PROVISION FAILED" ):
						d.failOSProvision()
					else:
						# Provisioning
						d.update( state=state )
			else:
				mid = apply( spin.Device.updateHW, (), dvc_struct )
				d = spin.Device.get( name=mid )
				if (lifecycle == "DEACTIVATED" ):
					d.decomission()
				else:
					# Managed
					d.update( state=state )

			# Set the user-settable fields
			d.update( stage=stage, use=use, notes=notes )

			# Move it to the correct Account
			d.moveAccount( new_acct_id=account_id )

			# Move it to the correct DC.  This has to be hacked because the Spin assumes all devices
			# that reg with it are in its DC.
			dr = d.getChildren( child_class="DeviceRole" )[0]
			dr.update( cust_cld_id=ac["id"] )
			old_dc_rc = d.getChildren( child_class="RoleClass", restrict={"stack_id":2} )[0]
			new_dc_rc = spin.DataCenter.getRoleClass( dc_id )
			if (old_dc_rc["id"] != new_dc_rc["id"]):
				d.removeRoleClasses( child_ids=[old_dc_rc["id"]] )
				d.addRoleClasses( child_ids=[new_dc_rc["id"]] )


	return 0

spin = spinwrapper.SpinWrapper(
        ctx = certmaster.getContextByName("spin", "spin.srv", ""),
)

create_fake_device( spin, {} )

def UsageError(msg):
	raise "external_spinmethods.UsageError: <Error(external_spinmethods.usage): %s>" % msg

def realm_deleteEntire(spin,id,t_id=None,mm_replicate=1):
	try:
		if t_id==None:
			tran_id=spin.tran.start()
			autocommit=1
		else:
			tran_id=t_id
			autocommit=0

		realm=spin.Realm.get(id)

		if realm['id'] == 0:
			UsageError("Attempt to delete TRANSITIONAL realm.")

		if not realm.isRealmReachable():
			realmunits=realm.getChildren(child_class='RealmUnit')
			for ru in realmunits: ru.delete(t_id=tran_id,mm_replicate=mm_replicate)
			realm.delete(t_id=tran_id,mm_replicate=mm_replicate)
			if autocommit: spin.tran.commit(t_id=tran_id)
		else:
			UsageError("Cannot delete a realm that is reachable. Uninstall any gateways servicing this realm before attempting to delete.")
	except:
		try:
			if autocommit:
				spin.tran.rollback(t_id=tran_id)
		finally:
			raise

def datacenter_deleteEntire(spin,id,t_id=None,mm_replicate=1,force=0):
	try:
		if t_id==None:
			tran_id=spin.tran.start()
			autocommit=1
		else:
			tran_id=t_id
			autocommit=0

		dc=spin.DataCenter.get(id)
		dvcs=dc.getChildren(child_class='Device',omit={'opsw_lifecycle':'DELETED'})
		if len(dvcs) > 0:
			UsageError("Cannot delete a Facility that has devices attached. Delete or re-assign any devices belonging to this facility.")

		deleted_dvcs=dc.getChildren(child_class='Device',restrict={'opsw_lifecycle':'DELETED'})
		if len(dvcs) > 0:
			UsageError("Cannot delete a Facility with pending device deletes; make sure the primary spin is running and wait 10 minutes for the garbage collection thread to remove the data.")

		realms = dc.getChildren(child_class='Realm',omit={'realm_id':0})
		deleted_realm_ids = []
		for r in realms:
			if r['realm_name'] == dc['display_name'] + '-agents' or r['realm_name'] == dc['display_name']:
				realm_deleteEntire(spin, r['id'],t_id=tran_id)
				deleted_realm_ids.append(r['id'])

		deleted_realm_ids.append(0)

		realms = dc.getChildren(child_class='Realm',omit={'realm_id':deleted_realm_ids})
		if len(realms) > 0:
			UsageError("Cannot delete a Facility that has extra satellite realms, those realms must be removed manually beforehand.")

		# delete all non-system account clouds (those are deleted within datacenter.delete())

		dummyVLAN = dc.getDummyVLAN()
		dummyVLANacID = spin.VLANCompartment.get(dummyVLAN['vlan_comp_id'])['cust_cld_id']
		acctclds = dc.getChildren(child_class='AccountCloud')
		for ac in acctclds:
			vlans = ac.getChildren(child_class='vlan',omit={'vlan_pool_id':dummyVLAN['vlan_pool_id']})
			for vlan in vlans:
				IPAddrs=vlan.getChildren(child_class='IPAddress')
				for IP in IPAddrs:
					dvcs = IP.getChildren(child_class='Device')
					# if in use, re-assign to the dummy vlan, otherwise delete the IP from the pool
					if len(dvcs) != 0: IP.update(vlan_pool_id=dummyVLAN['vlan_pool_id'],t_id=tran_id,mm_replicate=mm_replicate,force=force)
					else: IP.delete(t_id=tran_id,mm_replicate=mm_replicate,force=force)
				vlan.delete(t_id=tran_id,mm_replicate=mm_replicate,force=force)
			vlancs = ac.getChildren(child_class='VlanCompartment',omit={'vlan_comp_id':dummyVLAN['vlan_comp_id']})
			for vlanc in vlancs: vlanc.delete(t_id=tran_id,mm_replicate=mm_replicate,force=force)
			if ac['cust_cld_id'] != dummyVLANacID:
				ac.delete(t_id=tran_id,mm_replicate=mm_replicate,force=force)

		dc.delete(t_id=tran_id,mm_replicate=mm_replicate,force=force)
		if autocommit: spin.tran.commit(t_id=tran_id)
	except:
		try:
			if autocommit:
				spin.tran.rollback(t_id=tran_id)
		finally:
			raise
	

def session_deleteEntire(spin,id,t_id=None,mm_replicate=1):
	try:
		if t_id==None:
			tran_id=spin.tran.start()
			autocommit=1
		else:
			tran_id=t_id
			autocommit=0

		drcs=spin.DeviceRoleClass.getAll(restrict={'reconcile_session_id':id})
		for drc in drcs:
			drc.update(reconcile_session_id='',t_id=tran_id, mm_replicate=mm_replicate)
		
		locks=spin._SessionLock.getAll(restrict={'session_id':id})
		for lock in locks:
			lock.delete(t_id=tran_id, mm_replicate=mm_replicate)

		session=spin.Session.get(id)
		cmds=session.getChildren(child_class='SessionCommand')
		for cmd in cmds:
			cmd_params=cmd.getChildren(child_class='_SessionCommandParam')
			cmd_results=cmd.getChildren(child_class='_SessionCommandResult')
			for cmd_param in cmd_params:
				cpvs=cmd_param.getChildren(child_class='_SessionCommandParamValue')
				for cpv in cpvs:
					cpv.delete(t_id=tran_id, mm_replicate=mm_replicate)
				cmd_param.delete(t_id=tran_id, mm_replicate=mm_replicate)
			for cmd_result in cmd_results:
				crvs=cmd_result.getChildren(child_class='_SessionCommandResultValue')
				for crv in crvs:
					crv.delete(t_id=tran_id, mm_replicate=mm_replicate)
				cmd_result.delete(t_id=tran_id, mm_replicate=mm_replicate)
			cmd.delete(t_id=tran_id, mm_replicate=mm_replicate)
		
		params=session.getChildren(child_class='_SessionParam')
		for param in params:
			spvs=param.getChildren(child_class='_SessionParamValue')
			for spv in spvs:
				spv.delete(t_id=tran_id, mm_replicate=mm_replicate)
			param.delete(t_id=tran_id, mm_replicate=mm_replicate)

		results=session.getChildren(child_class='_SessionResult')
		for result in results:
			srvs=result.getChildren(child_class='_SessionResultValue')
			for srv in srvs:
				srv.delete(t_id=tran_id, mm_replicate=mm_replicate)
			result.delete(t_id=tran_id, mm_replicate=mm_replicate)

		ssis=session.getChildren(child_class='SessionServiceInstance')
		for ssi in ssis:
			ssirs=ssi.getChildren(child_class='_SessSrvcInstReport')
			for ssir in ssirs:
				ssirds=ssir.getChildren(child_class='_SessSrvcInstReportData')
				for ssird in ssirds:
					ssird.delete(t_id=tran_id, mm_replicate=mm_replicate)
				ssir.delete(t_id=tran_id, mm_replicate=mm_replicate)
			ssi.delete(t_id=tran_id, mm_replicate=mm_replicate)

		perms=session.getChildren(child_class='SessionPermission')
		for perm in perms:
			perm.delete(t_id=tran_id, mm_replicate=mm_replicate)

		session.delete(t_id=tran_id, mm_replicate=mm_replicate)
		if autocommit:
			spin.tran.commit(t_id=tran_id)
	except:
		try:
			if autocommit:
				spin.tran.rollback(t_id=tran_id)
		finally:
			raise

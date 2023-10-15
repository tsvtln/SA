// export CLASSPATH=.:/opt/opsware/occ/deploy/occ-runtime-service.sar/occ-runtime.jar:/opt/opsware/occ/occ/lib/javax.servlet.jar:/var/opt/opsware/occ/tmp/deploy/tmp6137654033298254266com.loudcloud.owm.usrmgr.ear-contents/com.loudcloud.owm.usrmgr.war/WEB-INF/classes/:/opt/opsware/occ/occ/lib/commons-logging.jar:/opt/opsware/occ/deploy/occ-runtime-service.sar/common-latest.jar

package com.opsware.owm.ch.usrmgr.bean;

import java.util.*;

import javax.servlet.http.*;
import javax.servlet.*;

import com.opsware.occ.auth.intf.*;
import com.opsware.occ.auth.impl.*;
import com.opsware.occ.auth.*;

public class ExternalUsersBean extends PermBaseBean {

    int totalNumUsers = 0;
    int pageNumUsers = 0;
    Collection usrList = null;
    String filter = "";     // "*";  10/20/2006 rwong BZ138153

    protected void init() throws Exception {
        super.init();
        setStartAt(request);
	    setLimit(request);
        String filterParam = request.getParameter("filter");
        if (null != filterParam && ! filterParam.equals("")) {
            setFilter(filterParam);
        }
	    //setOrderBy(request);
	    //setSortOrder(request);
    }

    public boolean getIsOpswareAdmin() throws AuthException {
        boolean isOpswareAdmin =  false;

        try {
            isOpswareAdmin = user.isAdmin();
        } catch (Exception e) {
            log.error("DomainUsersBean check User isAdmin error ", e);
        }

        return isOpswareAdmin;
    }


    public boolean getIsCustomerAdmin() throws AuthException {
        boolean isCustomerAdmin =  false;

        try {
            isCustomerAdmin = user.isCustomerAdmin();
        } catch (Exception e) {
            log.error("Check User isCustomerAdmin error ", e);
        }

        return isCustomerAdmin;
    }

    public boolean getIsAnyAdmin() throws AuthException {
        return (getIsOpswareAdmin() || getIsCustomerAdmin());
    }

    public boolean getIsCreateUserOK() {
        String umVal = env.getProperty("usermgr.ui.create_user");
        boolean bCreateOK = false;

	if (umVal != null && umVal.equalsIgnoreCase("true")) {
            bCreateOK = true;
	}

        return bCreateOK;
    }

    public boolean getIsImportUsersOK() throws Exception {
        System.out.println("DEBUG: getIsImportUsersOK() called!!!");
        IExternalUserManager usrMgr = AdminManagerFactory.getExternalUserManager(user,session);
        return usrMgr.isEnabled();
    }

    public boolean getIsDeleteUserOK() {

        boolean bDeleteOK = false;
        String umVal = env.getProperty("usermgr.ui.delete_user");
        if (umVal != null && umVal.equalsIgnoreCase("true")) {
            bDeleteOK = true;
        }

        return bDeleteOK;
    }

    public void setFilter(String f) {
    	filter = f;
    }

    public String getFilter() {
    	return (filter == null || filter.equals("")) ? "*": filter;
    }

    public Collection getExternalUsers() throws Exception  {

        if ( usrList == null) {
            IExternalUserManager usrMgr = AdminManagerFactory.getExternalUserManager(user,session);

            // 10/20/2006 rwong BZ138153 do NOT list all users if filter is not initially specified.
            if (filter != null && ! filter.equals("")) {
                usrList =  usrMgr.listUsers(filter);
            } else {
                usrList = new LinkedList();
            }
        }

        return usrList;
    }


    public int getTotalNumUsers()  throws Exception{
        // 10/20/2006 rwong BZ138153 Wonderful!  Why does this need to be computed TWICE?
        // getExternalUsers makes this call already!!!!

        // IExternalUserManager usrMgr = AdminManagerFactory.getExternalUserManager(user,session);
        // usrList = usrMgr.listUsers(filter);
        // totalNumUsers  = usrList.size();
        Collection list = getExternalUsers();
        totalNumUsers = list != null? list.size(): 0;

	return totalNumUsers;
    }

    public void setTotalNumUsers(int num) {
	this.totalNumUsers = num;
    }

    public int getPageNumUsers() {
	return this.pageNumUsers;
    }

    public void setPageNumUsers(int num) {
	this.pageNumUsers = num;
    }

}

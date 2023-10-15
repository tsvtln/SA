//package com.opsware.fido.impl.externaluser;

//import java.util.regex.*;
import java.sql.Timestamp;
import javax.ejb.*;
import java.util.*;
import java.math.*;
import java.io.*;
import java.net.URI;
import java.net.URISyntaxException;
    
import javax.naming.Context;
import javax.naming.NamingEnumeration;
import javax.naming.NamingException;
import javax.naming.directory.DirContext;
import javax.naming.directory.InitialDirContext;
import javax.naming.directory.SearchControls;
import javax.naming.directory.SearchResult;
import javax.naming.directory.Attributes;
import javax.naming.directory.Attribute;
import javax.naming.ldap.Control;
import javax.naming.ldap.LdapContext;
import javax.naming.ldap.InitialLdapContext;
import com.sun.jndi.ldap.ctl.PagedResultsControl;
import com.sun.jndi.ldap.ctl.PagedResultsResponseControl;

import com.opsware.twist.event.*;
import com.opsware.twist.utils.Configurator;
import com.opsware.ldap.LdapSslClientConfig;
import com.opsware.fido.ejb.entity.*;
import  com.opsware.fido.impl.user.LdapCallbackHandler;
import com.opsware.fido.util.*;
import com.opsware.fido.vo.*;
import com.opsware.fido.list.filter.impl.*;
import com.opsware.exception.*;
import com.opsware.fido.exception.*;
import com.opsware.fido.event.audit.*;
import com.opsware.fido.ejb.session.*;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

/**
 *
 * @author dboreham
 **/
public class ExternalUserUtil
{
    final Log log = LogFactory.getLog(this.getClass());
    protected static ExternalUserUtil INSTANCE=null;

    private String ldapUrl;
    private String ldapFilterTemplate;
    private String ldapSearchBase;
    private String ldapBindDn;
    private String ldapBindPw;
    private String namingAttribute;
    private String displayNameAttribute;
    private LdapSslClientConfig sslConf;
    private boolean useSsl = false;
    private boolean useStartTls = false;
    private String clientCertFilename;
    private String clientCertCaFilename;
    private String serverCertCaFilename;
    private boolean useClientCert;
    private boolean configured = false;
    private int pageSize = 0;
    private String[] returningAttributes;
    
    private Hashtable env;

    private static Properties m_oLdapConfig = new Properties();

    public static synchronized ExternalUserUtil getInstance() {
	if (INSTANCE == null)
	    INSTANCE = new ExternalUserUtil(); 
	return INSTANCE;
    }

    protected ExternalUserUtil() {
    
    	env = new Hashtable();
	
    	String serverHostname = m_oLdapConfig.getProperty("aaa.ldap.hostname");
        if (serverHostname != null) {
	    String serverPort = m_oLdapConfig.getProperty("aaa.ldap.port","389");
	    useSsl = m_oLdapConfig.getProperty("aaa.ldap.ssl","false").equals("true");
	    String serverSecureport = m_oLdapConfig.getProperty("aaa.ldap.secureport","636");
	    useStartTls = m_oLdapConfig.getProperty("aaa.ldap.usestarttls","false").equals("true");
	    useClientCert = m_oLdapConfig.getProperty("aaa.ldap.clientcert","false").equals("true");
	    clientCertFilename = m_oLdapConfig.getProperty("aaa.ldap.clientcert.fname","");
	    clientCertCaFilename = m_oLdapConfig.getProperty("aaa.ldap.clientcert.ca.fname","");
	    serverCertCaFilename = m_oLdapConfig.getProperty("aaa.ldap.servercert.ca.fname","");
	    String searchFilter_Template = m_oLdapConfig.getProperty("aaa.ldap.search.filter.template","uid=$");
	    String searchBaseTemplate = m_oLdapConfig.getProperty("aaa.ldap.search.base.template","");
	    namingAttribute = m_oLdapConfig.getProperty("aaa.ldap.search.naming.attribute","uid"); // samAccountName for AD
	    displayNameAttribute = m_oLdapConfig.getProperty("aaa.ldap.search.display.name.attribute","cn"); // also cn on AD
	    String searchBindDn = m_oLdapConfig.getProperty("aaa.ldap.search.binddn","");
	    String searchBindPw = m_oLdapConfig.getProperty("aaa.ldap.search.pw","");
	    pageSize = Integer.parseInt(m_oLdapConfig.getProperty("aaa.ldap.search.pagesize", "0"));
	    returningAttributes = new String[]{namingAttribute, displayNameAttribute, "c", "givenName", "l", "mail", "postalAddress", "postalCode", "sn", "st", "streetAddress", "telephoneNumber"};
	    
	    ldapSearchBase = searchBaseTemplate;
	    ldapFilterTemplate = searchFilter_Template;
	    if (useSsl) {
		String[] certPaths;
                sslConf = new LdapSslClientConfig();
                if (useClientCert) {
                    certPaths = new String[] {clientCertFilename, clientCertCaFilename, serverCertCaFilename};
                } else {
                    certPaths = new String[] {serverCertCaFilename};
                }
                // Add the cert paths to the ssl config object
                try {
                    sslConf.init(certPaths);
                } catch (Exception e) {
                    // Need to log errors here
                }
                ldapUrl = "ldaps://" + serverHostname + ":" + serverSecureport;
            } else {
                ldapUrl = "ldap://" + serverHostname + ":" + serverPort;
            }
	    
            ldapBindDn = searchBindDn;
            ldapBindPw = searchBindPw;
	    
            //setupLdapConnection();
            configured = true;
        }
    }

    private String verifyPassword(String binddn, String bindpw) {
        String retval = "";

        Hashtable env = new Hashtable();

        env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
        // Set the LDAP URL for the connection.
        env.put(Context.PROVIDER_URL, ldapUrl);
        // Provide the bind credentials.
        env.put(Context.SECURITY_PRINCIPAL, binddn);
        env.put(Context.SECURITY_CREDENTIALS, bindpw);

        // Set referral property to "follow" referrals automatically
        env.put(Context.REFERRAL, "follow");

        // Setup SSL if required
        if (useSsl) {
            sslConf.configureJndiContext(env);
        }

        try {
            DirContext ctx = new InitialDirContext(env);  // BIND
            ctx.close();  // UNBIND
            retval = "SUCCESS";
        } catch (NamingException e) {
            retval = "FAIL: " + e;
        }

        return retval;
    }
    
    private static void PrintUsage() {
        System.out.println( "Usage: ExternalUserUtil.java [-u <sas_username>] -b <binddn> [-toc <twist_overrides_conf>]" );
    }
    
    public static void main( String[] asArgs ) {
        try {
            String sUsername = null;
            String sPassword = null;
            String sBindDN = null;
            String sTocFile = "/etc/opt/opsware/twist/twistOverrides.conf";
            boolean bDebug = false;

            try {
                for( int iCurArg = 0; iCurArg < asArgs.length; iCurArg++ ) {
                    String sCurArg = asArgs[iCurArg];
                    if ( sCurArg.equals( "-u" ) ) {
                        iCurArg++;
                        sUsername = asArgs[iCurArg];
                    } else if ( sCurArg.equals( "-b" ) ) {
                        iCurArg++;
                        sBindDN = asArgs[iCurArg];
                    } else if ( sCurArg.equals( "-toc" ) ) {
                        iCurArg++;
                        sTocFile = asArgs[iCurArg];
                    } else if ( sCurArg.equals( "-d" ) ) {
                        bDebug = true;
                    }
                }
            } catch ( Exception e ) {
                // If any error occurs while parsing arguments, then print usage and exit.
                PrintUsage();
                System.exit(1);
            }

            // Read password from stdin:
            Properties oProps = new Properties();
            oProps.load(System.in);
            sPassword = oProps.getProperty("password");

            // If no binddn or password was supplied,
            if ( sBindDN == null || sPassword == null ) {
                // Then exit with error.
                PrintUsage();
                System.exit(1);
            }

            if ( bDebug ) {
                System.out.println( "DEBUG: sUsername = '" + sUsername + "'\n" +
                    "DEBUG: sPassword.toCharArray().length = " + sPassword.toCharArray().length + "\n" +
                    "DEBUG: sBindDN = '" + sBindDN + "'\n" +
                    "DEBUG: sTocFile = '" + sTocFile + "'\n" );
            }

            File oTocFile = new File( sTocFile );
            if ( !oTocFile.exists() ) {
                System.out.println( oTocFile + ": Not found" );
                System.exit(1);
            }

            m_oLdapConfig.load(new FileInputStream(oTocFile));

            // Instantiate a new ExternalUserUtil using these loaded props.
            ExternalUserUtil util = ExternalUserUtil.getInstance();

            if ( sUsername != null ) System.out.println( "Username: '" + sUsername + "'" );
            System.out.println("Bind DN: '" + sBindDN + "'");
            System.out.println("Authentication Result: " + util.verifyPassword( sBindDN, sPassword ) );
        } catch ( Exception e ) {
            System.out.println( "Caught Exception: " + e );
            e.printStackTrace();
        }
    }
}

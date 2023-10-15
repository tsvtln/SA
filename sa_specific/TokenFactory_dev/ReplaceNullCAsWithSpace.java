// export CLASSPATH=.:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/bea/weblogic81/server/lib/wlclient.jar:/opt/opsware/twist/lib/opsware_common-latest.jar:/opt/opsware/twist/lib/spinclient-latest.jar:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/twist/lib/twist.jar:/opt/opsware/twist/lib/common-latest.jar
// export CLASSPATH=`find /home/dwest/jlib/ -name "*.jar" | perl -pe 's/\n/:/g'`.

import java.io.InputStream;
import java.lang.reflect.*;
import java.util.*;

import com.opsware.client.*;
import com.opsware.search.Filter;
import com.opsware.common.ObjRef;
import com.opsware.custattr.CustomAttributeReference;
import com.opsware.common.ModifiableMap;
import com.opsware.fido.ejb.session.UserFacade;

import com.opsware.server.ServerService;

public class ReplaceNullCAsWithSpace {
    private static Twist s_tw = null;
    private static Map s_mapValidScopes = new HashMap();

    private static void ProcessCAs( String sCurScope, boolean bReplaceNullsWithSpace ) {
        try {
            System.out.print("Scope " + sCurScope + ": ");

            // Grab the service stub corresponding to this scope.
            Object Service = s_tw.getService( (String)s_mapValidScopes.get(sCurScope) );

            // Grab the findXXXRefs method for this service.
            Method mthdFindRefs = Service.getClass().getMethod( "find" + sCurScope + "Refs", new Class[] { Filter.class } );

            // Invoke the findXXXRefs method to get a list of all objects at this scope.
            ObjRef[] aoRefs = (ObjRef[])mthdFindRefs.invoke( Service, new Object[] { new Filter() } );

            // Grab the getCustAttrs method off the service stub.
            Method mthdGetCustAttrs = Service.getClass().getMethod( "getCustAttrs", new Class[] { CustomAttributeReference.class, String.class, boolean.class } );

            // Grab the setCustAttrs method from the service.
            Method mthdSetCustAttrs = Service.getClass().getMethod( "setCustAttrs", new Class[] { CustomAttributeReference.class, ModifiableMap.class } );

            System.out.println("Processing " + aoRefs.length + " records...");

            // Itterate through all the object references.
            for ( int i = 0; i < aoRefs.length; i++ ) {
//System.out.println("DEBUG: getCustAttrs(" + aoRefs[i] + ")");
                // Invoke the getCustAttrs method against this object with no scope.
                ModifiableMap mapCAs = (ModifiableMap)mthdGetCustAttrs.invoke( Service, new Object[] { aoRefs[i], null, new java.lang.Boolean(false) } );

//System.out.println("DEBUG: mapCAs.size() == " + mapCAs.size());
                // Indicate no change made.
                boolean bChangeMade = false;

                // If this set of CAs doesn't have a null value, then continue.
                if ( !mapCAs.containsValue(null) ) continue;

                // Itterate through all the custom attributes for this object.
                Iterator itrCAKey = mapCAs.keySet().iterator();
                while( itrCAKey.hasNext() ) {
                    // Grab current CA key.
                    String sCurCAKey = (String)itrCAKey.next();
//System.out.println("DEBUG: " + sCurCAKey + ": " + mapCAs.get(sCurCAKey));
                    // If the current custom attribute is <null>.
                    if ( mapCAs.get(sCurCAKey) == null ) {
                        // Let user know we found a null CA.
                        System.out.print( "  " + sCurScope + "(" + aoRefs[i].getId() + "): \"" + sCurCAKey + "\": CA <null> value detected" );

                        // If we are to replace nulls with a space.
                        if ( bReplaceNullsWithSpace ) {
                            // Set value to a single space, indicate a change made, and let user know we are fixing.
                            mapCAs.put( sCurCAKey, " " );
                            bChangeMade = true;
                            System.out.println(" fixing...");
                        } else {
                            System.out.println("");
                        }
                    }
                }

                // If any changes where made.
                if ( bChangeMade ) {
                    // Invoke the setCustAttrs using the modified map of CAs.
                    mthdSetCustAttrs.invoke( Service, new Object[] { aoRefs[i], mapCAs } );
                }
            }
        } catch (Exception e) {
            System.out.println( "Caught Exception: " + e );
            java.io.ByteArrayOutputStream baos = new java.io.ByteArrayOutputStream();
            e.printStackTrace(new java.io.PrintStream(baos));
            System.out.println( "Stacktrace:\n" + baos );
        }
    }

    public static void main( String[] asArgs ) {
        try {
            if ( asArgs.length < 2 ) {
                System.out.println( "Internal Usage: ReplaceNullCAsWithSpace <username> <userid> [<other_args>]" );
                System.exit(1);
            }

            s_tw = Twist.getInstance();
            s_tw.setProvider("http", "localhost", (short)1026, null);
            //tw.setVerbose(true);

            // Generate token for user/userid passed in.
            final String sToken = TokenFactory.getInstance( ).generateToken( asArgs[0], asArgs[1], null, -1, -1, UserFacade.IDENTITY_TOKEN );
            Twist.registerUserTokenFinder(new ITwistUserTokenFinder() {
                    public String getCurrentUserToken() {
                        return sToken;
                    }
                });

            // Valid scopes and corresponding service class.
            s_mapValidScopes.put( "Server", "com/opsware/server/ServerService" );
            s_mapValidScopes.put( "DeviceGroup", "com/opsware/device/DeviceGroupService" );
            s_mapValidScopes.put( "Customer", "com/opsware/locality/CustomerService" );
            //s_mapValidScopes.put( "Realm", "com/opsware/locality/RealmService" );
            s_mapValidScopes.put( "Facility", "com/opsware/locality/FacilityService" );
            s_mapValidScopes.put( "SoftwarePolicy", "com/opsware/swmgmt/SoftwarePolicyService" );
            String[] asAllScopes = new String[] { "Server", "DeviceGroup", "Customer", /*"Realm",*/ "Facility", "SoftwarePolicy" };
            String sAllScopes = "[";
            for ( int i = 0; i < asAllScopes.length; i++ ) {
                if ( i > 0 ) sAllScopes += ",";
                sAllScopes += asAllScopes[i];
            }
            sAllScopes += "]";

            // Process external arguments.
            int nScopeStartIndex = 0;
            String[] asScopes = asAllScopes;
            boolean bReplaceNullsWithSpace = false;
            if ( asArgs.length > 2 ) {
                if ( asArgs[2].equals("-f") ) {
                    bReplaceNullsWithSpace = true;
                    if ( asArgs.length > 3 ) {
                        asScopes = asArgs;
                        nScopeStartIndex = 3;
                    }
                } else if ( asArgs[2].equals("-h") ) {
                    System.out.println( "Usage: ReplaceNullCAsWithSpace -f|-h [<scope1> <scope2> ...]" );
                    System.out.println( "Where <scopeX> is one of " + sAllScopes );
                    System.exit(0);
                } else {
                    asScopes = asArgs;
                    nScopeStartIndex = 2;
                }
            }

            // Iterate through all the scopes we are to search.
            for ( int i = nScopeStartIndex; i < asScopes.length; i++ ) {
                // Get currect scope.
                String sCurScope = asScopes[i];

                // Make sure current scope is valid.
                if ( -1 == sAllScopes.indexOf( sCurScope ) ) {
                    // Warn user that the scope is not valid.
                    System.out.println("WARNING: " + sCurScope + ": Not one of the following valid scopes:\n" + sAllScopes);
                    continue;
                }

                // Process the CAs at the current scope.
                ProcessCAs( sCurScope, bReplaceNullsWithSpace );
            }

        } catch (Exception e) {
            System.out.println( "Caught Exception: " + e );
            java.io.ByteArrayOutputStream baos = new java.io.ByteArrayOutputStream();
            e.printStackTrace(new java.io.PrintStream(baos));
            System.out.println( "Stacktrace:\n" + baos );
        }
    }
}


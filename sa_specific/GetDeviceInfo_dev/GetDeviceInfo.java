// export CLASSPATH=.:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/bea/weblogic81/server/lib/wlclient.jar:/opt/opsware/twist/lib/opsware_common-latest.jar:/opt/opsware/twist/lib/spinclient-latest.jar:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/twist/lib/twist.jar:/opt/opsware/twist/lib/common-latest.jar

import com.opsware.client.*;
import com.opsware.server.*;
import com.opsware.swmgmt.*;
import com.opsware.search.Filter;
import com.opsware.pkg.*;
import com.opsware.fido.ejb.session.UserFacade;

public class GetDeviceInfo {
    // Returns a string representation of an arbitrary java object.
    private static String repObj( Object o ) { return repObj( o, null ); }
    private static String repObj( Object o, java.util.Collection oSeenObjects ) {
        // If the object is null.
        if ( o == null ) { return "<null>"; }

        // If the collection of seen options is empty, then instantiate one.
        if ( oSeenObjects == null ) {
            oSeenObjects = new java.util.ArrayList();
        }

        // If the object is a java.lang.String.
        if ( o.getClass() == String.class ) return "\"" + (String)o + "\"";

        // If the object is a java.util.Date.
        if ( o.getClass() == java.util.Date.class ) return "/" + o.toString() + "/";

        if ( o.getClass().isArray() ) {
            String sArRep = "[";
            for ( int i = 0; i < java.lang.reflect.Array.getLength(o); i++ ) {
                sArRep = sArRep + repObj( java.lang.reflect.Array.get(o, i), oSeenObjects ) + ", ";
            }
            if ( sArRep.endsWith(", ") ) { sArRep = sArRep.substring(0,sArRep.length() - 2); }
            return sArRep + "]";
        }

        // if we have seen this object before
        if ( oSeenObjects.contains(o) ) {
            return "/sb: " + o + "/";
        }

        // Return representation.
        String r = "";

        // Get the array of methods for the object.
        java.lang.reflect.Method[] aMethods = o.getClass( ).getMethods( );

        // Itterate through each method.
        int nCurMethod;
        for ( nCurMethod = 0; nCurMethod < aMethods.length; nCurMethod++ ) {
            // Get the current method.
            java.lang.reflect.Method CurMethod = aMethods[nCurMethod];

            //System.out.println( CurMethod.getName( ) + " | " + CurMethod.getReturnType( ) + " | " + CurMethod.getParameterTypes().length );
            // If this method starts with the substring "get" and
            // has no parameters.
            if ( CurMethod.getName( ).substring( 0, 3 ).equals( "get" ) &&
                 (CurMethod.getParameterTypes() == null || CurMethod.getParameterTypes().length == 0 ) &&
                 CurMethod.getDeclaringClass() != Object.class) {
                // Invoke the method.
                Object oVal = null;
                try {
                    oVal = CurMethod.invoke( o, new Object[] {} );
                } catch( Exception e ) {
                    oVal = "Exception occured during Invoke: " + e;
                }

                // Print out the value.
                r += CurMethod.getName( ).substring( 3 ) + ": " + repObj(oVal, oSeenObjects) + ", ";
            }
        }

        // Chop of trailing ", " if there.
        if ( r.endsWith(", ") ) {
            r = r.substring(0,r.length() - 2);
        }

        // If we got an empty rep, try to invoke the object's toString functionality.
        if ( r == "" ) r = "/" + o.toString() + "/"; else {
            // Add to the collection of seen objects.
            oSeenObjects.add(o);
            r = "{" + r + "}";
        }

        return r;
    }

    public static void main( String[] asArgs ) {
        if ( asArgs.length != 4 ) {
            System.err.println( "Usage: GetDeviceInfo <dvc_id> <username> <userid> <twist_key>" );
            System.exit( 1 );
        }

        String sDvcId = asArgs[0];
        String sUserName = asArgs[1];
        String sUserID = asArgs[2];
        TokenFactory.PRIVATE_KEY_PATH = asArgs[3];

        try {
            final String sUserToken = TokenFactory.getInstance().generateToken( sUserName, sUserID, null, -1, -1, UserFacade.IDENTITY_TOKEN );

            Twist tw = Twist.getInstance();
            tw.setProvider("http://localhost:1026","weblogic.jndi.WLInitialContextFactory");

            Twist.registerUserTokenFinder(new ITwistUserTokenFinder() {
                public String getCurrentUserToken() {
                    return sUserToken;
                }
            });

            ServerService ss = (ServerService)tw.getService(ServerService.class);
            ServerRef sr = new ServerRef(java.lang.Long.parseLong(sDvcId));
            ServerVO svo = ss.getServerVO( sr );
            System.out.println( "Device: " + svo.getName() + "(" + svo.getMid() + "): " + repObj(svo) );

            System.out.println( "Application Policies:" );
            SoftwarePolicyService sps = (SoftwarePolicyService)tw.getService(SoftwarePolicyService.class);
            SoftwarePolicyRef[] asprs = ss.getSoftwarePolicies( new ServerRef[] { sr } );
            for ( int i = 0; i < asprs.length; i++ ) {
                SoftwarePolicyVO spvo = sps.getSoftwarePolicyVO(asprs[i]);
                System.out.println( "  App Policy: " + spvo.getName() + "(" + asprs[i].getId() + "): " + repObj(spvo) );
            }

            System.out.println( "Patch Policies:" );
            PatchPolicyService pps = (PatchPolicyService)tw.getService(PatchPolicyService.class);
            PatchService ps = (PatchService)tw.getService(PatchService.class);
            PatchPolicyRef[] apprs = pps.findPatchPolicyRefs( new Filter("patch_policy", "patch_policy_dvc_id = " + sDvcId) );
            for ( int i = 0; i < apprs.length; i++ ) {
                PatchPolicyVO ppvo = pps.getPatchPolicyVO(apprs[i]);
                System.out.println( "  Patch Policy: " + ppvo.getName() + "(" + apprs[i].getId() + "): " + repObj(ppvo) );
                PatchReference[] aprs = pps.getPatches(new PatchPolicyReference[] { apprs[i] });
                for ( int x = 0; x < aprs.length; x++ ) {
                    PatchVO pvo = ps.getPatchVO(aprs[x]);
                    System.out.println( "    Patch: " + pvo.getName() + "(" + aprs[x].getId() + "): " + repObj(pvo) );
                }
            }

            System.out.println( "Installed Software: " );
            InstalledSoftware[] aiss = ss.getInstalledSoftware( sr );
            for ( int i = 0; i < aiss.length; i++ ) {
                System.out.println( "  o " + repObj(aiss[i]) );
            }
        } catch ( Exception e ) {
            System.err.println( "Caught Exception: " + e );
            e.printStackTrace();
        }
    }
}

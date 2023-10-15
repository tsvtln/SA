//jars=`printf "twistclient.jar\nopsware_common-latest.jar\nspinclient-latest.jar\ntwistclient.jar\nwlclient.jar" | xargs -n 1 -iREPL sh -c "locate REPL | head -1"`
//export CLASSPATH=.:`echo $jars|perl -pe 's/ /:/g'`
//export CLASSPATH=.:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/bea/weblogic81/server/lib/wlclient.jar:/opt/opsware/twist/lib/opsware_common-latest.jar

import java.lang.reflect.*;
import java.util.Hashtable;
import java.util.Set;
import java.util.Iterator;

import javax.ejb.*;

import com.opsware.client.*;
import com.opsware.folder.*;

import com.opsware.custattr.CustomAttribute;
import com.opsware.custattr.CustomAttributeReference;
import com.opsware.common.ModifiableMap;
import com.opsware.locality.CustomerRef;
import com.opsware.fido.FolderACL;

public class DumpFolders {
    static java.lang.String s_sIndent = "";
    static FolderService s_fs = null;
    static Hashtable s_hashServices = new Hashtable( );

    static boolean s_bDumpCustAttrs = true;
    static boolean s_bDumpVOs = true;
    static boolean s_bDumpPerms = false;

    public static void main( String[] asArgs ) throws Exception {
        if ( asArgs.length < 2 ) {
            System.out.println( "Usage: DumpFolders.class <SAS_Username> <Password> [-perms] [-ca_only]" );
            System.exit( 1 );
        }

        for( int iCurArg = 2; iCurArg < asArgs.length; iCurArg++ ) {
            if ( asArgs[iCurArg].equals( "-ca_only" ) ) {
                s_bDumpVOs = false;
            }
            if ( asArgs[iCurArg].equals( "-perms" ) ) {
                s_bDumpPerms = true;
            }
        }

        Twist tw = Twist.getInstance( );

        tw.setProvider("http://localhost:1026","weblogic.jndi.WLInitialContextFactory");
        tw.setTwistUser( new TwistUser( asArgs[0], asArgs[1] ) );

        s_fs = (FolderService)tw.getFacade( FolderService.class );

        FNodeReference fnrRoot = s_fs.getFNode( new String[] { "/" } );

        DumpFolder( fnrRoot );
    }

    private static void DumpFolder( FNodeReference fnrCurNode ) throws Exception {
        // If the FNodRef is a folder ref.
        if ( fnrCurNode.getClass( ).getName( ) == "com.opsware.folder.FolderRef" ) {
            // Print out the current node.
            System.out.print( s_sIndent + "-" + fnrCurNode );

            // Print out the folder permissions
            if ( s_bDumpPerms ) {
                // Print out associated customers. (Customers tab)
                System.out.print( ", Customers: {" );
                CustomerRef[] aCusts = s_fs.getCustomers( (FolderRef)fnrCurNode );
                for ( int nCurCust = 0; nCurCust < aCusts.length; nCurCust++ ) {
                    if ( nCurCust > 0 ) System.out.print( ", " );
                    CustomerRef oCurCust = aCusts[nCurCust];
                    System.out.print( oCurCust.getName() );
                }
                System.out.print( "}" );

                // Print out ACLs.  (Permissions tab)
                System.out.print( ", ACLs: {" );
                FolderACL[] aACLs = s_fs.getFolderACLs( new FolderRef[] {(FolderRef)fnrCurNode} );
                for ( int nCurACL = 0; nCurACL < aACLs.length; nCurACL++ ) {
                    if ( nCurACL > 0 ) System.out.print( ", " );
                    FolderACL oCurACL = aACLs[nCurACL];
                    System.out.print( oCurACL.getRole().getName() + ":" + oCurACL.getAccessLevel() );
                }
                System.out.print( "}" );
            }

            // Go to next line of output.
            System.out.println( "" );

            // Get the FolderVO.
            FolderVO fvoCurNode = s_fs.getFolderVO( (FolderRef)fnrCurNode );

            // Get all the children of this folder.
            FNodeReference[] afnrChildren = fvoCurNode.getMembers( );

            // For each child folder node reference.
            int nCurIndex;
            for ( nCurIndex = 0; nCurIndex < afnrChildren.length; nCurIndex++ ) {
                s_sIndent = s_sIndent + "  ";
                DumpFolder( afnrChildren[nCurIndex] );
                s_sIndent = s_sIndent.substring( 2 );
            }
        } else {
            DumpItem( fnrCurNode );
        }
    }

    private static void DumpItem( FNodeReference fnrItem ) throws Exception {
        // String rep for this item.
        String sRep = "";

        // Get the specific reference class name.
        String sRefClassName = fnrItem.getClass( ).getName( );

        // Calculate a service class name.
        String sServiceClassName = sRefClassName.replaceAll( "Ref", "Service" );

        // Attempt to grab the class for this service class name.
        Class clsService = null;
        try {
            clsService = Class.forName( sServiceClassName );
        } catch ( Exception e ) {
            System.out.println( s_sIndent + "  Couldn't load class '" + sServiceClassName + "'" );
            return;
        }

        // Grab a ref to the twist object.
        Twist tw = Twist.getInstance( );

        // Attempt to load the corresponding service object.
        Object svc = null;
        try {
            // Attempt to pull the service out of the cache.
            if ( ( svc = s_hashServices.get( clsService ) ) == null ) {
                // Get the facade again.
                svc = tw.getFacade( clsService );

                // Cache a reference to the service for future use.
                s_hashServices.put( clsService, svc );
            }
        } catch( Exception e ) {
            System.out.println( s_sIndent + "  Couldn't load service '" + sServiceClassName + "'" );
            return;
        }

        // If we are to dump the VO for the reference:
        if ( s_bDumpVOs ) {
            // Calculate the get command to get the VO from the service.
            String sGetVOMethodName = sRefClassName.replaceAll( "Ref", "VO" ).replaceAll( "^.+\\.", "get" );

            // Get the "get vo" method from the service class.
            Method mdGetVO = null;
            try {
                mdGetVO = clsService.getMethod( sGetVOMethodName, new Class[] { fnrItem.getClass( ) } );
            } catch( Exception e ) {
                System.out.println( s_sIndent + "  Couldn't get method: '" + sGetVOMethodName );
                return;
            }

            // Attempt to invoke the GetVO method.
            Object VO = null;
            try {
                VO = mdGetVO.invoke( svc, new Object[] { fnrItem } );
            } catch( Exception e ) {
                System.out.println( s_sIndent + "  Failed to invoke method: '" + sGetVOMethodName + "' on '" + svc );
                e.printStackTrace( );
                return;
            }

            // Get the array of methods for the VO.
            Method[] aMethods = VO.getClass( ).getMethods( );

            // Itterate through each method.
            int nCurMethod;
            for ( nCurMethod = 0; nCurMethod < aMethods.length; nCurMethod++ ) {
                // Get the current method.
                Method CurMethod = aMethods[nCurMethod];

                // If this method starts with the substring "get" and
                // has no parameters.
                if ( CurMethod.getName( ).substring( 0, 3 ).equals( "get" ) && (
                     CurMethod.getParameterTypes() == null ||
                     CurMethod.getParameterTypes().length == 0 ) ) {
                    //System.out.println( s_sIndent + "  " + CurMethod.getName( ) + " | " + CurMethod.getName( ).substring( 0, 3 ) + " | " + CurMethod.getParameterTypes().length );
                    // Invoke the method.
                    Object oVal = CurMethod.invoke( VO, new Object[] {} );

                    // Print out the value.
                    sRep += s_sIndent + "   " + CurMethod.getName( ).substring( 3 ) + ": " + oVal + "\n";
                }
            }
        }

        // If we are to dump the custom attributes for this reference.
        if ( s_bDumpCustAttrs ) {
            // If the service object is an instance of CustomAttribute.
            if ( svc instanceof com.opsware.custattr.CustomAttribute ) {
                // Grab the custom attributes for this reference.
                ModifiableMap mapCustAttrs = ((CustomAttribute)svc).getCustAttrs( (CustomAttributeReference)fnrItem, null, false );

                // If there is at least one custom attributes on this node.
                if ( mapCustAttrs.size() > 0 ) {
                    // Output a section heading.
                    sRep += s_sIndent + "   Custom Attributes:\n";

                    // Get an itterator for all the keys in the map.
                    Iterator itKeys = mapCustAttrs.keySet( ).iterator( );

                    // Itterate through all the keys in the map.
                    while ( itKeys.hasNext( ) ) {
                        // Get current key.
                        Object oCurKey = itKeys.next( );

                        // Get the current value.
                        Object oValue = mapCustAttrs.get( oCurKey );

                        // If the value is <null>, then set it to "<null>"
                        if ( oValue == null ) oValue = "<null>";

                        // Print out the current key/value.
                        sRep += s_sIndent + "     " + oCurKey + ": " + oValue + "\n";
                    }
                }
            }
        }

        // If any rep was collected.
        if ( !sRep.equals("") ) {
          System.out.println( s_sIndent + "o " + fnrItem + "\n" + sRep );
        }
    }
}

// setenv CLASSPATH `ls /home/bdaddy/.java/.deployment/javaws/cache/http/Dsas65.nccs/P80/DMwebstart/RM*.jar | perl -pe 's/\n/:/g'`.
// java -Dngui.debug=true DumpNguiCache dwest sas65.nccs.opsware.com mypassword com.opsware.ngui.cache.ServerCacheUpdater.dat

import javax.swing.*;
import java.io.*;
import java.util.logging.*;
import java.lang.reflect.*;
import java.util.*;
import java.lang.*;
import java.net.*;

//import com.opsware.ngui.cache.DesEncrypter;

class DumpNguiCache {
    // Returns a string representation of an arbitrary java object.
    private static String repObj( Object o ) { return repObj( o, null ); }
    private static String repObj( Object o, java.util.Collection oSeenObjects ) {
        // Return representation.
        String r = "";

        // If the object is null.
        if ( o == null ) { return "<null>"; }

        // If the collection of seen options is empty, then instantiate one.
        if ( oSeenObjects == null ) { oSeenObjects = new java.util.ArrayList(); }

        // If the object is a java.lang.String.
        if ( o.getClass() == String.class ) {
            r = "\"" + (String)o + "\"";
            //for( char i = 0; i < 32; i++ ) {
            //    r = r.replaceAll(new String(new char[]{i}), "\\\\x" + (i < 16 ? "0" : "") + java.lang.Integer.toHexString(i).toUpperCase());
            //}
            return r;
        }

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
        if ( oSeenObjects.contains(o) ) { return "sb: " + o; }

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
        if ( r.endsWith(", ") ) { r = r.substring(0,r.length() - 2); }

        // If we got an empty rep, try to invoke the object's toString functionality.
        if ( r == "" ) r = "/" + o.toString() + "/"; else {
            // Add to the collection of seen objects.
            oSeenObjects.add(o);
            r = "{" + r + "}";
        }

        return r;
    }

    public static String getApplicationDirectory() {
        File appdataDir = new File(System.getProperty("user.home"), "Application Data");
        if (appdataDir.exists() && appdataDir.isDirectory() && System.getProperty("os.name").startsWith("Windows")) {
            return System.getProperty("user.home") + File.separator + "Application Data" + File.separator + "Opsware" + File.separator;
        }
        return System.getProperty("user.home") + File.separator + ".opsware" + File.separator;
    }

    static void DumpCacheFile(String sCacheFile, Object encrypter) {
        System.out.println("Cache File: " + sCacheFile);

        try {
            Method mthd_readEncryptedObject = encrypter.getClass().getMethod( "readEncryptedObject", new Class[]{String.class} );
            Object o = mthd_readEncryptedObject.invoke( encrypter, new Object[]{sCacheFile} );

            if ( sCacheFile.indexOf("index.dat") > -1 || o == null ) {
                System.out.println("value: " + o);
            } else {
                Field fld_data;
                fld_data = o.getClass().getDeclaredField("data");
                fld_data.setAccessible(true);

                if ( fld_data == null ) {
                    System.out.println( "Object has no <data> member.  o: " + o );
                    return;
                }

                Map data = (Map)fld_data.get(o);
                Set oKeys = data.keySet();
                for ( Iterator oKeyIter = oKeys.iterator(); oKeyIter.hasNext(); ) {
                    Object oKey = oKeyIter.next();
                    System.out.println("  key: " + repObj(oKey) + "\n  value: " + repObj(data.get(oKey)));
                }
            }
        } catch ( Exception e ) {
            System.out.println("Exception caught: " + e);
            e.printStackTrace();
        }
    }

    public static void main( String[] asArgs ) {
        if ( asArgs.length < 4 ) {
            System.out.println( "Usage: DumpNguiCache <occ_hostname> <username> <password> <cachefile1> [<cachefile2> ...]" );
            System.out.println( "(Use \"prompt\" for the <password> arg and a secure prompt will be displayed.)" );
            System.exit(1);
        }

        String sOccHostname = asArgs[0];
        String sUsername = asArgs[1];
        String sPassword = asArgs[2];

        if ( sPassword.equals("prompt") ) {
            JLabel pw_label = new JLabel("Please enter password:");
            JPasswordField pw_field = new JPasswordField();
            int res = JOptionPane.showConfirmDialog(null,
                                                new Object[]{pw_label, pw_field}, "Password",
                                                JOptionPane.OK_CANCEL_OPTION);

            if ( res == JOptionPane.CANCEL_OPTION || res == JOptionPane.CLOSED_OPTION ) {
                System.out.println( "Cancled cache dump, exiting..." );
                System.exit(1);
            }

            sPassword = new String(pw_field.getPassword());
        }

        // Not sure a reliable way to figure this out:
        //String sCacheFileDir = getApplicationDirectory() + sUsername + File.separator + "cache" + File.separator + sOccHostname + File.separator;

        try {
            ClassLoader ucl = new URLClassLoader( new URL[] {new URL("http://" + sOccHostname + "/webstart/ngui.jar"),
                new URL("http://" + sOccHostname + "/webstart/twistclient.jar")}, ClassLoader.getSystemClassLoader() );

            // Construct a new DesEncrypter
            Class clsDesEncrypter = Class.forName( "com.opsware.ngui.cache.DesEncrypter", true, ucl );
            Constructor cstrDesEncrypter = clsDesEncrypter.getConstructor( new Class[] {String.class} );
            Object encrypter = cstrDesEncrypter.newInstance( new Object[]{sPassword} );

            // Setup debug logging to stderr.
            System.setProperty("ngui.debug", "true");
            Class clsLog = Class.forName( "com.opsware.ngui.util.Log", true, ucl );
            Method mthd_getLogger = clsLog.getMethod( "getLogger", new Class[]{} );
            Logger l = (Logger)mthd_getLogger.invoke(null, new Object[]{});
            l.addHandler(new ConsoleHandler());
            l.setLevel(Level.ALL);

            for ( int i = 3; i < asArgs.length; i++ ) {
                String sCurFile = asArgs[i];
                File oCurFile = new File(sCurFile);

                if ( oCurFile.isDirectory() ) {
                    File[] afs = (new File(sCurFile)).listFiles(new FilenameFilter() {
                            public boolean accept(File dir, String name) {
                                return name.endsWith(".dat");
                            }
                        });

                    for( int j = 0; j < afs.length; j++ ) {
                        DumpCacheFile(afs[j].getAbsolutePath(), encrypter);
                    }
                } else {
                    DumpCacheFile(sCurFile, encrypter);
                }
            }
        } catch ( Exception e ) {
            System.out.println("Exception caught: " + e);
            e.printStackTrace();
        }

        System.exit(0);
    }
}

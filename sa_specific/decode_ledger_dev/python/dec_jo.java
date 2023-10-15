import java.io.*;
import java.util.*;
import java.io.ObjectInputStream;

public class dec_jo {

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

    public static void main(String[] asArgs) {
        for ( int iCurArg = 0; iCurArg < asArgs.length; iCurArg++ ) {
            try {
                String sCurFile = asArgs[iCurArg];
                ObjectInputStream ois = null;
                if ( sCurFile.equals("-") ) {
                    ois = new ObjectInputStream(System.in);
                } else {
                    ois = new ObjectInputStream(new FileInputStream(sCurFile));
                }

                Object obj = null;

                while ( (obj = ois.readObject()) != null ) {
                    System.out.println(repObj(obj));
                }
            } catch (IOException e) {
                /*means we are done, silently ignore.*/
                //System.out.println("Exception: " + e);
                //e.printStackTrace(System.out);
            } catch (ClassNotFoundException e) {
                System.out.println("Class Not Found: " + e);
                System.out.println("(Change the $CLASSPATH env variable to include this missing class.)");
                e.printStackTrace(System.out);
            }
        }
    }
}




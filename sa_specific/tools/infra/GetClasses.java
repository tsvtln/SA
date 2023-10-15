import java.util.ArrayList;
import java.io.File;
import java.net.URL;
import java.io.InputStream;
import java.lang.Package;

public class GetClasses {
    public static Class[] getClasses(String pckgname)
        throws ClassNotFoundException {
        ArrayList classes = new ArrayList();
        // Get a File object for the package
        File directory = null;
        try {
            ClassLoader cld = Thread.currentThread().getContextClassLoader();
            if (cld == null) {
                throw new ClassNotFoundException("Can't get class loader.");
            }
            //String path = pckgname.replace('.', '/');
            String path = pckgname;
            URL resource = cld.getSystemResource(path);
            //URL resource = System.class.getResource(path);
            if (resource == null) {
                throw new ClassNotFoundException("No resource for " + path);
            }
            //System.out.println( resource.openStream().read() );
            directory = new File(resource.getFile());
        } catch (Exception x) {
            x.printStackTrace();
            throw new ClassNotFoundException(pckgname + " (" + directory
                                             + ") does not appear to be a valid package");
        }
        if (directory.exists()) {
            // Get the list of the files contained in the package
            String[] files = directory.list();
            for (int i = 0; i < files.length; i++) {
                // we are only interested in .class files
                if (files[i].endsWith(".class")) {
                    // removes the .class extension
                    classes.add(Class.forName(pckgname + '.'
                                              + files[i].substring(0, files[i].length() - 6)));
                }
            }
        } else {
            throw new ClassNotFoundException(pckgname
                                             + " does not appear to be a valid package");
        }
        Class[] classesA = new Class[classes.size()];
        classes.toArray(classesA);
        return classesA;
    }

    public static void main( String[] asArgs ) {
        Package[] a = Package.getPackages();
        int i;
        for ( i = 0; i < a.length; i++ ) {
            System.out.println( a[i].getName() );
        }
        try {
            System.out.println( getClasses( asArgs[0] ) );
        } catch ( Exception e ) {
            System.out.println( "Execption occured:" );
            e.printStackTrace( );
        }
    }
}

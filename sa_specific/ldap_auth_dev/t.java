import java.util.Properties;

public class t {
    public static void main( String[] asArgs ) {
        try {
            Properties p = new Properties();
            p.load(System.in);
            System.out.println("DEBUG: " + p);
        } catch ( Exception e ) {
            System.out.println( "Caught Exception: " + e );
            e.printStackTrace();
        }
    }
}

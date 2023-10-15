// export CLASSPATH=/root/rendition/client/truecontrol-client.jar:.

import com.rendition.tools.DatabaseInfo;

class dump_a_da {
    public static void main( String asArgs[] ) {
        if ( asArgs.length < 1 ) {
            System.out.println( "Usage: dump_a_da <nas_install_home>" );
            System.exit( 1 );
        }

        DatabaseInfo dbi = new DatabaseInfo( asArgs[0], asArgs[0] + "/server/ext/jboss" );
        dbi.load();
        System.out.println( "Database Server: " + dbi.getServer( ) );
        System.out.println( "Database Name: " + dbi.getName() );
        System.out.println( "Database Username: " + dbi.getUser( ) );
        System.out.println( "Database Password: " + dbi.getPassword( ) );
    }
}

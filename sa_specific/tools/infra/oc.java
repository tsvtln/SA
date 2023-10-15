import com.opsware.client.*;
import com.opsware.server.*;

class oc {
    public static void main( String[] asArgs ) {
        if ( asArgs.length < 4 ) {
            System.out.println("Usage: t <twist_host> <username> <password> <dvc_id>");
            System.exit(1);
        }

        try {
            OpswareClient.connect(asArgs[0], asArgs[1], asArgs[2]);
            final ServerService ss = (ServerService)OpswareClient.getService(ServerService.class);
            final ServerRef sr = new ServerRef(java.lang.Long.parseLong(asArgs[3]));
            System.out.println( ss.getServerHardwareVO( sr ) );
        } catch ( Exception e ) {
            System.out.println( "Caught Exception: " + e );
            e.printStackTrace();
        }
    }
}

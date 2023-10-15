// export CLASSPATH="`ls /opt/opsware/occclient/*.jar | perl -pe 's/\n/:/g'`."

import java.io.InputStream;

import com.opsware.client.*;
import com.opsware.ejb.session.*;
import com.opsware.vo.*;
import com.opsware.ngui.util.LoginContext;

import com.opsware.ngui.adt.model.WindowsDeploymentHelper;

public class t1 {
    public static void main( String[] asArgs ) {
        try {
            if ( asArgs.length != 3 ) {
                System.out.println( "Usage: t1 <occ_host> <dvc_id> <token>" );
                System.exit(1);
            }
            System.out.println(asArgs[0] + " | " + asArgs[1] + " | " + asArgs[2]);

            // Initialize CA:
            InputStream[] inputStreams = new InputStream[1];
            inputStreams[0] = t1.class.getResourceAsStream("/opsware-ca.crt");
            com.opsware.security.SSLConfig.init(inputStreams);

            Twist tw = Twist.getInstance();
            tw.setProvider("https", asArgs[0], (short)443, null);
            //tw.setProvider("http", asArgs[0], (short)1026, "weblogic.jndi.WLInitialContextFactory");
            //tw.setVerbose(true);

            final String sToken = asArgs[2];
            Twist.registerUserTokenFinder(new ITwistUserTokenFinder() {
                    public String getCurrentUserToken() {
                        return sToken;
                    }
                });
            //com.opsware.ngui.util.LoginContext.setUserToken(sToken);

            // Initialize the modelcache:
            com.opsware.ngui.manager.LoginDialog.initCache();

            //            DeviceFacade df = (DeviceFacade)tw.getFacade(DeviceFacade.class);

            //            DeviceSummaryVO dsvo = df.getDeviceSummaryVO(new java.lang.Long(asArgs[1]));

            WindowsDeploymentHelper wdh;
            //wdh = new WindowsDeploymentHelper( dsvo );
            wdh = WindowsDeploymentHelper.locateDeploymentHelper();

            System.out.println("hello: " + wdh);
        } catch (Exception e) {
            System.out.println( "Caught Exception: " + e );
            java.io.ByteArrayOutputStream baos = new java.io.ByteArrayOutputStream();
            e.printStackTrace(new java.io.PrintStream(baos));
            System.out.println( "Stacktrace:\n" + baos );
        }
    }
}

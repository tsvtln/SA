// export CLASSPATH=.:/root/dw/cbt/lib/activation.jar:/root/dw/cbt/lib/antlr.jar:/root/dw/cbt/lib/cbt.jar:/root/dw/cbt/lib/common-1.2.0.jar:/root/dw/cbt/lib/commons-codec-1.3.jar:/root/dw/cbt/lib/commons-lang-2.0.jar:/root/dw/cbt/lib/commons-logging.jar:/root/dw/cbt/lib/compliance-handlers.jar:/root/dw/cbt/lib/concurrent.jar:/root/dw/cbt/lib/ejb-2.0.jar:/root/dw/cbt/lib/HTTPClient-hacked.jar:/root/dw/cbt/lib/icu4j.jar:/root/dw/cbt/lib/jakarta-oro-2.0.5.jar:/root/dw/cbt/lib/jena_0604.jar:/root/dw/cbt/lib/jsafeFIPS.jar:/root/dw/cbt/lib/junit.jar:/root/dw/cbt/lib/mail.jar:/root/dw/cbt/lib/opsware_common-latest.jar:/root/dw/cbt/lib/rdf-api-2001-01-19.jar:/root/dw/cbt/lib/spinclient-latest.jar:/root/dw/cbt/lib/twistclient-latest.jar:/root/dw/cbt/lib/weblogic.jar:/root/dw/cbt/lib/wlcipher.jar:/root/dw/cbt/lib/xercesImpl.jar:/root/dw/cbt/lib/xml-apis.jar
// /opt/opsware/j2sdk1.4/bin/java -Dbea.home=/root/dw/cbt/cfg t3

import java.util.Properties;

import javax.naming.Context;

import com.opsware.client.*;
import com.opsware.ejb.session.*;
import com.opsware.vo.*;

public class t3 {
    public static void main( String[] asArgs ) {
        try {
            Twist tw = Twist.getInstance();
            tw.setProvider("t3s", "twist", (short)1032, null, new String[] {"/var/opt/opsware/crypto/twist/opsware-ca.crt"}, null);
            //tw.setProvider("t3", "localhost", (short)1026, null, new String[] {"/var/opt/opsware/crypto/twist/opsware-ca.crt"}, null);
            tw.setTwistUser( new ITwistUser () {
                    private Context context = null;
                    public String getName() { return "dwest"; }
                    public Context getContext() { return this.context; }
                    public void setContext(Context context) { this.context = context; }
                    public String getPassword() {
                        return "mypassword";
                    }
                });

            TwistServer ts = (TwistServer)tw.getFacade(TwistServer.class);
            System.out.println("DEBUG: " + ts.getVersion());
        } catch (Exception e) {
            System.out.println( "Caught Exception: " + e );
            java.io.ByteArrayOutputStream baos = new java.io.ByteArrayOutputStream();
            e.printStackTrace(new java.io.PrintStream(baos));
            System.out.println( "Stacktrace:\n" + baos );
        }
    }
}

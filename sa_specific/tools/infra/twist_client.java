// export CLASSPATH=.:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/bea/weblogic81/server/lib/wlclient.jar:/opt/opsware/twist/lib/opsware_common-latest.jar:/opt/opsware/twist/lib/spinclient-latest.jar:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/twist/lib/twist.jar:/opt/opsware/twist/lib/common-latest.jar
// export CLASSPATH=`find /home/dwest/jlib/ -name "*.jar" | perl -pe 's/\n/:/g'`.

import java.io.InputStream;

import java.security.*;
import java.security.cert.*;
import javax.net.ssl.*;

import com.opsware.client.*;
import com.opsware.ejb.session.*;
import com.opsware.vo.*;

public class t1 {
    public static void main( String[] asArgs ) {
        try {
            if ( asArgs.length != 3 ) {
                System.out.println( "Usage: t1 <occ_host> <dvc_id> <token>" );
                System.exit(1);
            }
            System.out.println(asArgs[0] + " | " + asArgs[1] + " | " + asArgs[2]);

            // Initialize CA:
            InputStream inputStream = System.class.getResourceAsStream("/opsware-ca.crt");
            Security.addProvider(new com.sun.net.ssl.internal.ssl.Provider());
            Security.addProvider(new com.sun.crypto.provider.SunJCE());
            KeyStore ks = KeyStore.getInstance("JKS");
            ks.load(null, "foobar".toCharArray());
            CertificateFactory cf = CertificateFactory.getInstance("X509");
            X509Certificate cert = (X509Certificate)cf.generateCertificate(inputStream);
            ks.setCertificateEntry("trustcert", cert);
            KeyManagerFactory kmFactory = KeyManagerFactory.getInstance("SunX509");
            kmFactory.init(ks, "foobar".toCharArray());
            KeyManager[] kms = kmFactory.getKeyManagers();
            TrustManagerFactory tmFactory = TrustManagerFactory.getInstance("SunX509");
            tmFactory.init(ks);
            TrustManager[] tms = tmFactory.getTrustManagers();
            SSLContext ctx = SSLContext.getInstance("SSL");
            ctx.init(kms, tms, SecureRandom.getInstance("SHA1PRNG"));
            SSLSocketFactory ssfc = ctx.getSocketFactory();
            javax.net.ssl.HttpsURLConnection.setDefaultSSLSocketFactory(ssfc);
            javax.net.ssl.HttpsURLConnection.setDefaultHostnameVerifier(
                new HostnameVerifier() {
                    public boolean verify(String hostname, SSLSession session) {
                        return true;
                    }
                });

            Twist tw = Twist.getInstance();
            tw.setProvider("https", asArgs[0], (short)443, null);
            //tw.setProvider("http", asArgs[0], (short)1026, null);
            //tw.setVerbose(true);

            final String sToken = asArgs[2];
            Twist.registerUserTokenFinder(new ITwistUserTokenFinder() {
                    public String getCurrentUserToken() {
                        return sToken;
                    }
                });

            DeviceFacade df = (DeviceFacade)tw.getFacade(DeviceFacade.class);

            DeviceSummaryVO dsvo = df.getDeviceSummaryVO(new java.lang.Long(asArgs[1]));

            System.out.println("hello: " + dsvo);
        } catch (Exception e) {
            System.out.println( "Caught Exception: " + e );
            java.io.ByteArrayOutputStream baos = new java.io.ByteArrayOutputStream();
            e.printStackTrace(new java.io.PrintStream(baos));
            System.out.println( "Stacktrace:\n" + baos );
        }
    }
}

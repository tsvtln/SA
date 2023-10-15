// export CLASSPATH=/opt/opsware/twist/lib/client/opswclient.jar:

import com.opsware.client.OpswClientEndpoint;
import com.opsware.client.security.SSLSetup;
import com.opsware.server.*;

public class opsw_client_endpoint {
  public static void main(String[] asArgs) throws Exception {
    if ( asArgs.length != 3 ) {
      System.out.println("Usage: opsw_client_endpoint <proto> <host> <port>");
      return;
    }

    OpswClientEndpoint oce = OpswClientEndpoint.getInst();

    SSLSetup.setupHTTPS();

//    oce.setJNDIProvider("https","10.126.154.10",(short)1032, null);
    oce.setJNDIProvider(asArgs[0],asArgs[1],java.lang.Short.parseShort(asArgs[2]), null);

    oce.getContext(true);

    System.out.println("oce: " + oce);

/*
    ServerService ss = (ServerService)OpswareClient.getService(ServerService.class);

    ServerRef sr = new ServerRef(10001);

    ServerVO svo = ss.getServerVO(sr);

    System.out.println("svo.getName(): " + svo.getName());
*/
  }
}

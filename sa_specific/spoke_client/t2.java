// /opt/opsware/j2sdk1.4/bin/java -classpath /opt/opsware/occclient/ngui.jar:/var/opt/opsware/twist/twist/stage/_appsdir_main_ear/libref/spoke_client.jar:/opt/opsware/twist/lib/opsware_rmi.jar:/opt/opsware/occclient/jnlp.jar:/opt/opsware/occclient/jide-common.jar:/opt/opsware/occclient/jsch-latest.jar:. t2

// C:\Opsware\javaws_cache\http\Dsas65.nccs.opsware.com\P80\DMwebstart>\Opsware\jre\bin\java.exe -classpath RMbatik-all.jar;RMcmdb-catalog.jar;RMcmlp.jar;RMcommon.jarRMcommons-lang.jar;RMcooper.jar;RMcrypto.jar;RMgui-commands-1.1.42.jar;RMjbossall-client.jar;RMjgoodies-binding.jar;RMjgoodies-forms.jar;RMjgoodies-looks.jar;RMjgoodies-uif-extras.jar;RMjgoodies-uif.jar;RMjgoodies-validation.jar;RMjide-common.jar;RMjide-dock.jar;RMjnlp.jar;RMjrex.jar;RMjsch-latest.jar;RMl2fprod-common-buttonbar.jar;RMl2fprod-common-outlookbar.jar;RMl2fprod-common-tasks.jar;RMlicenses.jar;RMngui.jar;RMomdb-scheduler-client.jar;RMomdb-scheduler.jar;RMomdb-security-client.jar;RMopsware_common-latest.jar;RMopsware_rmi.jar;RMoro.jar;RMrowset.jar;RMrsrc_en.jar;RMspinclient-latest.jar;RMspoke_client.jar;RMswingx.jar;RMtwistclient.jar;RMwlclient.jar;RMwww_en.jar;RMxercesImpl.jar;RMy.jar;\work\cases\00209249 -Dcom.opsware.gwproxy.host=sas65.nccs.opsware.com t2

import com.opsware.ngui.client.SpokeClient;
import com.opsware.rt.intf.IRuntime;
import com.opsware.ngui.util.LoginContext;

import java.security.Policy;
import java.security.AllPermission;
import java.security.Permissions;
import java.security.CodeSource;
import java.security.PermissionCollection;

public class t2 {
    final static void setupSecurityPolicy() {
        // This overcomes a Java Web Start bug where classes
        // loaded from custom class loaders does not inherit
        // the policy described in the jnlp file.  This affects
        // our Weblogic client.
        Policy.setPolicy( new Policy() {
            public PermissionCollection getPermissions(CodeSource codesource) {
                Permissions perms = new Permissions();
                perms.add(new AllPermission());
                return(perms);
            }
            public void refresh() {} });
    }

  public static void main( String[] asArgs ) {
    try {
      setupSecurityPolicy();
      LoginContext.setUsername( "detuser" );
LoginContext.setUserToken("gNTeXmpL0KIetKCLh+dO/vcLbeILEp+UXgaXpQMcgHuJj2MaVw9nKWvDK5WtOpcmhRmLs2FwBoe/KSkYVLieZf9QvptL+Zo54iri3m/RttZcPK4lSSjsPgXCB6JguA0J+ryzdKFCPbd3QTwwGF5mQCssi8u3YHYVFCiErHK0CvPLeQNjn5O58eqIoSFgRQLcxhEsxyzc7M+fgcxtvcr1vmMZz8b+f6FfT/BJZlRlqeJ0N2aS8RzNjCr55nxi9ArA");
      SpokeClient sc = SpokeClient.getInstance();
      sc.initialize();
      IRuntime rt = sc.getRuntime();
      System.out.println( "DEBUG: " + rt );
    } catch ( Exception e ) {
      System.out.println( "Exceptino: " + e );
      e.printStackTrace();
    }
  }
}

// /opt/opsware/j2sdk1.4/bin/java -classpath /opt/opsware/spoke/www/spoke_client.jar:/var/opt/opsware/twist/twist/stage/_appsdir_main_ear/session/shared-session.jar:/var/opt/opsware/twist/twist/stage/_appsdir_main_ear/libref/opsware_unified_api.jar:/opt/opsware/twist/lib/opsware_rmi.jar:/opt/opsware/twist/lib/twist.jar:/opt/opsware/twist/lib/common-latest.jar:/opt/opsware/twist/lib/jsch-latest.jar:. t

import com.opsware.compliance.sco.rmi.IComplianceService;
import com.opsware.shared.helper.SpokeServices;
import com.opsware.twist.TwistSpoke;

import java.util.Properties;
import java.security.Policy;
import java.security.AllPermission;
import java.security.Permissions;
import java.security.CodeSource;
import java.security.PermissionCollection;

public class t {
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
      Properties p = System.getProperties();
      Properties props = new Properties();
      props.setProperty("spoke.wwwroot", "rsrc:/www");
      props.setProperty("spoke.cpath", "/twist_spoke_stubs.jar");
      props.setProperty("spoke.local", "false");
      props.setProperty("gwproxy.host", "localhost");
      props.setProperty("gwproxy.port", "8080");
      TwistSpoke.init(props);
      SpokeServices.init();
      IComplianceService cs = SpokeServices.getInstance().getComplianceService();
      System.out.println( "DEBUG: " + cs );
    } catch (Exception e ) {
      System.out.println( "Exceptino: " + e );
      e.printStackTrace();
    }
  }
}

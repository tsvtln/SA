import com.sun.tools.attach.*;

import java.io.*;
import java.util.Properties;

public class jpatch {
  public static void main( String[] asArgs ) throws Exception {
    if ( (asArgs.length < 4) ||
         ((((float)asArgs.length)/2.0) != (asArgs.length/2)) ) {
      System.out.println("Usage: jpatch <jvm_pid> <class_name> <new_class_file>\n");
      System.exit(1);
    }

    String s_agent_jar = (new File(asArgs[0])).getAbsolutePath();
    String s_jvm_pid = asArgs[1];

    // Attach to the target JVM.
    VirtualMachine vm = null;
    try {
      vm = VirtualMachine.attach( s_jvm_pid );
    } catch (IOException e) {
      if ( e.getMessage().equals("well-known file is not secure") ) {
        throw new Exception("This usually means you are running jpatch as a different user than the target JVM.", e);
      }
      throw e;
    } catch (AttachNotSupportedException e) {
      if ( e.getMessage().equals("Unable to open socket file: target process not responding or HotSpot VM not loaded") ) {
        throw new Exception("This usually means you are running jpatch as a different user than the target JVM.", e);
      }
      throw e;
    }

    // Package up the class to be patched into a java properties string.
    Properties p = new Properties();
    for ( int i=2; i < asArgs.length; i = i + 2 ) {
      p.setProperty(asArgs[i], (new File(asArgs[i+1])).getAbsolutePath());
    }
    StringWriter sw = new StringWriter();
    p.store(sw, null);

    // Load the agent into the target JVM and pass the arguments.
    vm.loadAgent(s_agent_jar, sw.toString());
  }
}

import java.lang.instrument.*;

import java.io.*;
import java.util.*;
import java.lang.Class;

public class jpatch_agent {
  public static void agentmain( String args, Instrumentation inst ) {
    System.out.println("Number of classes loaded into this JVM: " + inst.getAllLoadedClasses().length);

    Properties p = new Properties();
    // Deserialize the properties from the args string.
    try {
      p.load(new StringReader(args));
    } catch (Exception e) {
      System.out.println("Caught Exception: " + e);
      e.printStackTrace();
    }

    // System.out.println("p: " + p);

    Class[] aClasses = inst.getAllLoadedClasses();
    for ( int i=0; i < aClasses.length; i++ ) {
      Class cls = aClasses[i];
      String sClsName = cls.getName();
      String sClsFile = p.getProperty(sClsName, null);
      if ( sClsFile == null ) continue;

      File f = new File(sClsFile);
      if ( !f.exists() ) {
        System.out.println("'" + f.getAbsolutePath() + "': Class file not found");
        // Remove this class file entry so we don't run into it again.
        p.remove(sClsName);
        continue;
      }

      System.out.println("Redefining class '" + sClsName + "' (#" + i + ") with the class in file '" + f.getAbsolutePath() + "'.");

      // We could cache the loaded bytes pack into the <p> property bag. -dw
      try {
        byte[] abNewCls = new byte[(int) f.length()];
        DataInputStream in = new DataInputStream(new FileInputStream(f));
        in.readFully(abNewCls);
        in.close();
        ClassDefinition oClsDef = new ClassDefinition(cls, abNewCls);
        inst.redefineClasses(oClsDef);
      } catch (Exception e) {
        System.out.println("Caught Exception: " + e);
        e.printStackTrace();
      }
    }
  }
}

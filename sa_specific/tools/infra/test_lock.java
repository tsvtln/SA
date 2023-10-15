import java.io.*;
import java.nio.channels.FileLock;

public class test_lock {
    public static void main( String[] asArgs ) throws Exception {
        FileLock fl = (new FileOutputStream(new File(asArgs[0]))).getChannel().tryLock(0,Long.MAX_VALUE,false);
        System.out.println("fl: " + fl);
    }
}

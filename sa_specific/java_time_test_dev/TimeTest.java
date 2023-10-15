import java.io.InputStream;
import java.io.IOException;
import java.sql.Timestamp;
import java.util.Date;
import java.util.Properties;
import java.text.SimpleDateFormat;

public class TimeTest {
    public static void main(String[] args) {
        final SimpleDateFormat DATE = new SimpleDateFormat("EEE MMM dd kk:mm:ss zzz yyyy");

        // change time zone setting 
        //System.out.println("old: " + System.setProperty("user.timezone", "US/Pacific"));

        // print out current timezone.
        System.out.println("user.timezone: " + System.getProperty("user.timezone"));

        // output from 'date'
        System.out.print("shell:    ");
        try {
            Process child = Runtime.getRuntime().exec("date");
            InputStream in = child.getInputStream();
            int c;
            while ((c = in.read()) != -1) {
                System.out.print((char)c);
            }
        } catch (IOException e) {}

        // output from vm
        System.out.println("normal:   " + DATE.format(new Date()));

        // dirty hack!
        //Timestamp ts = new Timestamp(System.currentTimeMillis() - 25200000);
        //System.out.println("adjusted: " + DATE.format(ts));
    }
}


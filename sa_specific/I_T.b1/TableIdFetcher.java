import java.io.*;
import java.sql.*;
import java.util.*;
import java.text.*;

public class TableIdFetcher {
  public static void main(String args[]) throws SQLException {
    if (args.length < 4) {
      System.err.println("Usage: spin_obj table_name column_name jdbc_url [jdbc_url]");
      System.exit(1);
    }
    String spin_obj = args[0];
    String table_name = args[1];
    String column_name = args[2];
    String sele_string = "select ";
    String from_string = " from ";
    sele_string = sele_string + column_name + from_string + table_name;
    SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd_hh:mm:ss");
    String timestamp;
    int i = 3;
    int num_rows = 0;

    DriverManager.registerDriver (new oracle.jdbc.driver.OracleDriver());
    while (i < args.length) {
	timestamp = sdf.format(new java.util.Date());
	System.err.println(timestamp+" "+args[i]);
	Connection conn = DriverManager.getConnection(args[i],"spin","spin");
	Statement stmt = conn.createStatement();
	stmt.setFetchSize(1000);
	ResultSet rset = stmt.executeQuery(sele_string);
	boolean have_results = rset.next();
	while (have_results) {
	    num_rows++;
	    if (0 == num_rows%1000) {
		timestamp = sdf.format(new java.util.Date());
		System.err.println(timestamp+" "+num_rows);
	    }
	    System.out.println(rset.getString(1));
	    try {
		have_results = rset.next();
	    } catch (SQLException e) {
		timestamp = sdf.format(new java.util.Date());
		System.err.println(timestamp+" "+args[i]+" "+e.toString());
	    }
	}
	stmt.close();
	i++;
    }
  }
}

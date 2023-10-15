public class t1 {
  public static void foo() {
    System.out.println("foo");
  }

  public static void main(String[] asArgs) {
    System.out.println("hello");
    while (true) {
      System.out.println("info");
      foo();
      try {
        java.lang.Thread.sleep(1000);
      } catch( Exception e ) {
        e.printStackTrace();
      }
    }
  }
}

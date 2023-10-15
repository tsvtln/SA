public class t {
    static String newString(int len, char c) {
        char[] ac = new char[len];
        java.util.Arrays.fill(ac, c);
        return new String(ac);
    }

    public static void main(String[] asArgs) {
        //String[][] o = new String[][] {new String[] {"one", "two"}, new String[] {"three", "four"}};
        //System.out.println("hello: " + o[0].length);

        for ( int i = 0; i < asArgs.length; i++ ) {
            System.out.println("asArgs[" + i + "]: " + asArgs[i]);
        }

        System.out.println("test: " + newString(10, 'z'));
    }
}

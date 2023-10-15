package com.dw.tibco;

public class Util {
    /* Returns a string of length <len> where every character is <c>.
     */
    private static String newString(int len, char c) {
        char[] ac = new char[len];
        java.util.Arrays.fill(ac, c);
        return new String(ac);
    }

    /* Produces a printable string based on the characters in <ab>.  If <ab>
     * contains non printable characters, these are escaped out in a human
     * readable way.
     */
    public static String byteArrayToPrintableString(byte[] ab) {
        return String(ab);
    }

    /* Inserts <iSpaces> number of space characters at the front of every line
     * of text in <str>.
     */
    public static String indent(String str, int iSpaces) {
        return str;
    }

    /* Inserts <iSpaces> number of space characters at the front of every line
     * except the first line.
     */
    public static String indentValue(String sVal, int iSpaces) {
        return str;
    }
}

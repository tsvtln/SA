// /opt/opsware/jdk1.6/bin/javac -cp /opt/opsware/twist/lib/commons-codec-1.3.jar twist_token_crypto.java

import java.util.regex.*;
import java.util.Arrays;
import java.io.BufferedReader;
import java.io.FileReader;
import java.security.SecureRandom;
import java.security.MessageDigest;
import javax.crypto.spec.SecretKeySpec;
import javax.crypto.KeyGenerator;
import javax.crypto.Cipher;
import org.apache.commons.codec.binary.Base64;

class twist_token_crypto {
  private final static int KEYSIZE = 128;
  private final static String RANDOM_ALGO = "SHA1PRNG";
  private final static String HASH_ALGORITHM = "SHA1";
  private final static int HASH_LENGTH = 20;
  private final static String SYMMETRIC_ENC = "AES";
  private final static String TWIST_KEY_FILE = "/var/opt/opsware/crypto/twist/twist-key.pem";
  private final static String CHAR_ENC = "US-ASCII";

  static void usage() {
    System.out.println("Usage: twist_token_crypto (dec|enc) <tok>");
  }

  static String _toHex(byte[] bytes) {
    if ( bytes == null ) return "<null>";
    String digits = "0123456789abcdef";
    StringBuilder sb = new StringBuilder(bytes.length * 2);
    for (byte b : bytes) {
      int bi = b & 0xff;
      sb.append(digits.charAt(bi >> 4));
      sb.append(digits.charAt(bi & 0xf));
      sb.append(" ");
    }
    return sb.toString();
  }

  static String _toHex(String s) {
    return _toHex(s.getBytes());
  }

  static SecretKeySpec getKey() throws Exception {
    // Load the twist key as is done in "com.opsware.security.CryptoImporter.readPEM()":
    FileReader frTwistKey = new FileReader(TWIST_KEY_FILE);
    StringBuilder sbTwistKey = new StringBuilder();
    char[] cBuf = new char[4096];
    while (frTwistKey.read(cBuf, 0, cBuf.length) > 0) {
      sbTwistKey.append(new String(cBuf));
    }
    Matcher m =  Pattern.compile("-----BEGIN RSA PRIVATE KEY-----(\r|\n|\r\n)(.*?)-----END RSA PRIVATE KEY-----(\r|\n|\r\n)", Pattern.DOTALL).matcher(sbTwistKey.toString());
    m.find();
    byte[] byteTwistKey = m.group(2).getBytes();

    // Use this twist-key.pem contents as a seed to generate a random key.
    SecureRandom sr = SecureRandom.getInstance(RANDOM_ALGO);
    sr.setSeed(byteTwistKey);
    KeyGenerator kgen = KeyGenerator.getInstance(SYMMETRIC_ENC);
    kgen.init(KEYSIZE, sr);
    byte[] byteKey = kgen.generateKey().getEncoded();
    System.out.println("DEBUG: byteKey: " + _toHex(byteKey));
    return new SecretKeySpec(byteKey, SYMMETRIC_ENC);
  }

  static String decryptToken( String sEncB64Tok ) throws Exception {
    // Convert the base64 encrypted token string into a encoded bytes.
    byte[] byteEncTok = (new Base64()).decode(sEncB64Tok.getBytes());

    // Decrypt the token using the key.
    Cipher cipher = Cipher.getInstance(SYMMETRIC_ENC);
    cipher.init(Cipher.DECRYPT_MODE, getKey());
    byte[] byteTokAndHash = cipher.doFinal(byteEncTok);

    // Sepearte the token and the token hash.
    byte[] byteHash = new byte[HASH_LENGTH];
    System.arraycopy(byteTokAndHash, byteTokAndHash.length-HASH_LENGTH, byteHash, 0, HASH_LENGTH);
    byte[] byteTok = new byte[byteTokAndHash.length-HASH_LENGTH];
    System.arraycopy(byteTokAndHash, 0, byteTok, 0, byteTokAndHash.length-HASH_LENGTH);

    // Verify the token hash.
    byte[] byteExpectedHash = MessageDigest.getInstance(HASH_ALGORITHM).digest(byteTok);
    if ( Arrays.equals(byteHash, byteExpectedHash) ) {
      return new String(byteTok, CHAR_ENC);
    } else {
      throw new Exception("Decrypt failure for token \"" + sEncB64Tok + "\".");
    }
  }

  static String encryptToken( String sTok ) throws Exception {
    byte[] byteTok = sTok.getBytes();

    // Calculate the token hash.
    byte[] byteHash = MessageDigest.getInstance(HASH_ALGORITHM).digest(byteTok);

    // Combine the token and hash together.
    byte[] byteTokAndHash = new byte[byteTok.length + HASH_LENGTH];
    System.arraycopy(byteTok, 0, byteTokAndHash, 0, byteTok.length);
    System.arraycopy(byteHash, 0, byteTokAndHash, byteTokAndHash.length-HASH_LENGTH, HASH_LENGTH);

    // Encrypt token and hash.
    Cipher cipher = Cipher.getInstance(SYMMETRIC_ENC);
    cipher.init(Cipher.ENCRYPT_MODE, getKey());
    System.out.println("DEBUG: cipher.getIV(): " + _toHex(cipher.getIV()));
    byte[] byteEncTokAndHash = cipher.doFinal(byteTokAndHash);

    // Convert encrypted token/hash to base64 and return.
    return new String((new Base64()).encode(byteEncTokAndHash), CHAR_ENC);
  }

  public static void main( String[] asArgs ) throws Exception {
    if ( asArgs.length != 2 ) {
      usage();
      return;
    }

    String sCmd = asArgs[0];
    String sTok = asArgs[1];

    if ( sCmd.equals("dec") ) {
      System.out.println(decryptToken(sTok));
    } else if ( sCmd.equals("enc") ) {
      System.out.println(encryptToken(sTok));
    } else {
      System.out.println(asArgs[0] + ": Unexpected command.");
      usage();
      return;
    }
  }
}

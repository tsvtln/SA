//package com.opsware.fido.impl.user;

import java.io.*;
import org.apache.commons.codec.binary.Base64;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.security.NoSuchAlgorithmException;
import javax.crypto.SecretKey;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import javax.crypto.KeyGenerator;
import org.w3c.dom.*;
import org.xml.sax.*;
import javax.xml.parsers.*;
import javax.xml.transform.*;
import javax.xml.transform.stream.*;
import javax.xml.transform.dom.*; 

import java.util.HashMap;

import com.opsware.security.CryptoImporter;
//import com.opsware.fido.vo.*;
import com.opsware.twist.authentication.ITokenDecoder;
import com.opsware.twist.authentication.ISecurityToken;
import com.opsware.fido.ejb.session.UserFacade;

import java.lang.Long;

/**
 * Generates security tokens
 *
 *
 *
 * @author Mit Shah
 */
public class TokenFactory {

    final static String HASH_ALGORITHM = "SHA1";
    final static String SYMMETRIC_ENC = "AES";
    // only used for Base64 characters hence i18n friendly
    final static String CHAR_ENC = "US-ASCII";
 
    protected static TokenFactory INSTANCE;
    protected SecretKeySpec secretKeySpec;
    protected Base64 base64Encoder;
    // token fields
    public final static String TOKEN = "tok";
    public final static String USERNAME = "un";
    public final static String USERID = "uid";
    public final static String OPAQUE = "o";
    public final static String VERSION = "v";
    public final static String TOKENTYPE = "t";
    public final static String VALID_FROM = "vf";
    public final static String VALID_UNTIL = "vu";
    // token values
    final static String _VERSION = "1.0";
    // hidden value prefix (only settable from the twist)
//    final String _HIDDEN = Configurator.getInstance().getProperty("opsware.hiddenAttrPrefix").toLowerCase();
    

    //////////////////////////////////////////////////////////

    private final static String RANDOM = "SHA1PRNG";
    private static final String MAC_FUNCTION = "HMacSHA1";
    //final static String PRIVATE_KEY_PATH = "/var/opt/opsware/crypto/twist/twist-key.pem";
    public static String PRIVATE_KEY_PATH = "/var/opt/opsware/crypto/twist/twist-key.pem";
    // only used for Base64 characters hence i18n friendly

    private static int KEYSIZE = 128;
    private static SecretKey _secretKey = null;

    /**
     * Call this function to retrieve the secret, encrypted key
     * TokenFactory uses this as well as HMac....
     */
    public static SecretKey getSecretKey() {
	if ( _secretKey == null ) {
	    renewKeyState();
	}
	return _secretKey;
    }

    /**
     * Call this function to reset whether the override file exists, and what the
     * privateKey is.  It is called once, the first time the system needs this state,
     * but can be called by the user as often as needed.
     */
    public static void renewKeyState() {

	File f = new File(PRIVATE_KEY_PATH);

	byte [] keyBytes;

	//if ( !f.exists() ) {
	//    f = new File("/soft/lco/twist/twist/certs/twist-key.pem");
	//}

	if ( !f.exists() ) {
	    f = new File("certs/twist-key.pem");
	}

	if (f.exists()) {
	    try {
		FileReader fr = new FileReader(f.getPath());
		String privateKey = CryptoImporter.readPEM(fr, false);

		keyBytes = privateKey.getBytes();
	    } catch (Exception e) {
		System.err.println("could not read twist private key>: " + e);
		keyBytes = "DefaultKeyBrokenHorkHorkHork".getBytes();
	    }
	} else {
	    System.err.println("Could not find twist private key '" + PRIVATE_KEY_PATH + "', \nhence unable to seed the hashing function");
            System.exit( 1 );
	    keyBytes = "DefaultKeyBrokenHorkHorkHork".getBytes();
	}

        KEYSIZE = 128;

	// generate the signing key
	try {
	    SecureRandom random = SecureRandom.getInstance(RANDOM);
	    random.setSeed(keyBytes);

	    javax.crypto.KeyGenerator kgen;
	    kgen = javax.crypto.KeyGenerator.getInstance(SYMMETRIC_ENC);
	    kgen.init(KEYSIZE, random);
	    _secretKey = kgen.generateKey();
	} catch (NoSuchAlgorithmException e) {
	    System.err.println("Signing and Tokenization is handicapped: " + e);
            e.printStackTrace( );
	}
    }

    /////////////////////////////////////////////////////////////

    public static TokenFactory getInstance( ) {
	if (INSTANCE == null) {
	    INSTANCE = new TokenFactory( );
	}
	return INSTANCE;
    }
    
    protected TokenFactory( ) {
	try {
	    
	    base64Encoder = new Base64();
	    
	    // generate the signing key
	    generateSigningKey( );
	} catch (Exception e) {
	    System.err.println("Caught Excetpion: " + e);
            e.printStackTrace( );
	}	
    }
    
    
    // regenerate the signing key, should be the same on each run
    // since the source crypto material is the same    
    protected void generateSigningKey() {
	secretKeySpec = new SecretKeySpec(getSecretKey().getEncoded(),
					  SYMMETRIC_ENC);
    }
    
    /**
     * This method must not be exposed to the outside world; only from within the Twist's 
     * TwistContext class can it be called. The outside world will call a variant of this method
     * which will set the variable to false.
     */
    public String generateToken(String sUsername, String sUserId, String[] opaqueFields, long firstValidTime, long duration, String type, boolean allowHiddenParameters) throws Exception {
	    if (!type.equals(UserFacade.IDENTITY_TOKEN) &&
		!type.equals(UserFacade.SERVICE_TOKEN)) {
		System.err.println("A token type must be set to UserFacade.IDENTITY_TOKEN or UserFacade.SERVICE_TOKEN");
                System.exit( 1 );
	    }
	    DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
	    DocumentBuilder builder = factory.newDocumentBuilder();
	    Document doc = builder.newDocument();
	    Element root = doc.createElement(TOKEN);
	    doc.appendChild(root);
	    // version
	    Node version = doc.createElement(VERSION);
	    version.appendChild(doc.createTextNode(_VERSION));
	    root.appendChild(version);
	    // token type
	    Node typeN = doc.createElement(TOKENTYPE);
	    typeN.appendChild(doc.createTextNode(type));
	    root.appendChild(typeN);
	    // user element
	    Node userid = doc.createElement(USERID);
	    userid.appendChild(doc.createTextNode(sUserId));
	    root.appendChild(userid);
	    Node username = doc.createElement(USERNAME);
	    username.appendChild(doc.createTextNode(sUsername));
	    root.appendChild(username);
	    // opaque fields
            // Removed.
	    // first valid epoch time
	    if (firstValidTime <= 0) {
		firstValidTime = System.currentTimeMillis();
	    }
	    Element validFrom = doc.createElement(VALID_FROM);
	    validFrom.appendChild(doc.createTextNode(String.valueOf(firstValidTime)));
	    root.appendChild(validFrom);
	    // expiry time
	    long expiryTime = System.currentTimeMillis();
	    if (duration == -1) {
		expiryTime = -1;
	    } else {
		expiryTime += duration;
	    }
	    Element validUntil = doc.createElement(VALID_UNTIL);
	    validUntil.appendChild(doc.createTextNode(String.valueOf(expiryTime)));
	    root.appendChild(validUntil);
	    
	    // convert to string
	    StringWriter sw = new StringWriter();
	    transform(doc, new StreamResult(sw));
	    
	    String rawToken = sw.getBuffer().toString();
	    
	    String token = encryptTokenWithMAC(rawToken);
	    return token;
    }

    public String generateToken(String sUsername, String sUserId, String[] opaqueFields, long firstValidTime, long duration, String type) throws Exception {
	return generateToken(sUsername, sUserId, opaqueFields, firstValidTime, duration, type, false);
    }

    protected String encryptTokenWithMAC(String rawToken) {
	try {
	    // generate MAC for raw token
	    byte[] rawTokenBytes = rawToken.getBytes();
	    MessageDigest md = MessageDigest.getInstance(HASH_ALGORITHM);
	    byte[] digest = md.digest(rawTokenBytes);
	   

	    // combine MAC + raw Token bytes
	    byte[] combined = new byte[rawTokenBytes.length + digest.length];
	    System.arraycopy(rawTokenBytes, 0, combined, 0, rawTokenBytes.length);
	    System.arraycopy(digest, 0, combined, rawTokenBytes.length, digest.length);
	   
	    
	    // encrypt this with AES
	    Cipher cipher = Cipher.getInstance(SYMMETRIC_ENC);
	    cipher.init(Cipher.ENCRYPT_MODE, secretKeySpec);
	    byte[] tokenBytes = cipher.doFinal(combined);

	    // base 64 encode the token
	    byte[] base64 = base64Encoder.encode(tokenBytes);
	   
            return new String(base64, CHAR_ENC);
	} catch (Exception e) {
	    System.err.println("Caught Exception: " + e);
            e.printStackTrace( );
            System.exit( 1 );
            return null;
	}
    }

    // debugging method
    protected void transform(Document doc, StreamResult s) {
	try {
	    TransformerFactory transFactory = TransformerFactory.newInstance();
	    Transformer transformer = transFactory.newTransformer();	    
	    transformer.setOutputProperty(OutputKeys.INDENT, "yes");
	    transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
	    DOMSource source = new DOMSource(doc);
	    transformer.transform(source, s);
	} catch (Exception e) {
	    System.err.println("Caught Exception: " + e);
            e.printStackTrace( );
            System.exit( 1 );
	}
    }
   
    public static void main( String[] asArgs ) throws Exception {
        if ( asArgs.length != 3 ) {
            System.err.println( "Usage: TokenFactory <username> <userid> <twist_key>" );
            System.exit( 1 );
        }
        PRIVATE_KEY_PATH = asArgs[2];
        /*
        UserVO uvo = new UserVO( );
        uvo.setUsername( asArgs[0] );
        uvo.setUserId( new Long(asArgs[1]) );
        */
        String s = TokenFactory.getInstance( ).generateToken( asArgs[0], asArgs[1], null, -1, -1, UserFacade.IDENTITY_TOKEN );
        System.out.print( s );
    }    

}

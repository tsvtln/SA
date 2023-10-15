
/**
 * Program Overview:
 *
 * This java program is part of a SAS command line utility that allows a SAS
 * user to change their password, or a SAS administrator to change the password
 * of a given SAS user.  This program prompts the user for passwords as
 * as neccessary and assumes that the tty has already been put into a secure
 * no echo mode.  It then proceeds to establish a weblogic RMI connection with
 * the twist in order to effect the password modification.
 */

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.Long;

import com.opsware.client.*;
import com.opsware.fido.ejb.session.UserFacade;
import com.opsware.fido.vo.UserVO;

class sas_passwd_rmi {
    // Whether or not we are in debug mode.
    static boolean s_bDebug = false;

    /**
     * Requires: Assumes tty is already in no echo mode.
     * Effects: Does nothing if no arguments are supplied.  If one argument is 
     *   supplied then, this is expected to be the username whose password is
     *   to be changed.  If two arguments are given, then the second one is
     *   expected to be an administrator username that has the authority to 
     *   set the password of the given user.  If more than two arguments are
     *   given, then they are ignored.
     */
    public static void main( String[] asArgs ) {
        try {
            // Create a buffered reader for standard input.
            BufferedReader StdIn = new BufferedReader( new InputStreamReader( System.in ) );

            // Username to be changed.
            String sUsername = "";

            // New password.
            String sNewPassword;

            // Username to be used to change password.
            String sAdminUN = "";

            // Password to be used to change password.
            String sAdminPW = "";

            // Usage: $0 [-d] [-a <admin_username>] <username>
            int nIndex = 0;
            for ( nIndex = 0; nIndex < asArgs.length; nIndex++ ) {
                // Get the current argument.
                String sCurArg = asArgs[nIndex];

                // If the current argument doesn't start with a "-".
                if ( !sCurArg.startsWith( "-" ) ) {
                    // Use this argument as the username.
                    sUsername = sCurArg;

                    // If no admin username has been obtained yet.
                    if ( sAdminUN.equals( "" ) ) {
                        // Use the username as the admin username too.
                        sAdminUN = sUsername;
                    }

                    // Finally break from the arg parse loop.
                    break;
                }

                // If the current argument is "-d".
                if ( sCurArg.equals( "-d" ) ) {
                    // Indicate debug mode.
                    s_bDebug = true;
                }

                // If the current argument is "-a" and we aren't at the end.
                if ( sCurArg.equals( "-a" ) && nIndex != (asArgs.length-1) ) {
                    // Use the next arg as the admin username.
                    nIndex++;
                    sAdminUN = asArgs[nIndex];
                }
            }

            // If no arguments where given.
            if ( asArgs.length == 0 ) {
                // Do nothing and exit.
                System.exit( 0 );
            }

            // If the same username was given twice.
            if ( sUsername.equals( sAdminUN ) ) {
                // Read in the user's current password.
                System.out.println( "Old Password:" );
                sAdminPW = StdIn.readLine();
            // Otherwise perform a password set.
            } else {
                // Read om the admin user's password.
                System.out.println( sAdminUN + "'s password:" );
                sAdminPW = StdIn.readLine();
            }

            // Create a twist object and login.
            Twist tw = Twist.getInstance( );
            tw.setProvider("http://localhost:1026","weblogic.jndi.WLInitialContextFactory");
            try {
                tw.setTwistUser( new TwistUser( sAdminUN, sAdminPW ) );
            } catch( java.lang.RuntimeException e ) {
                if ( e.toString().matches( ".*Unable to authenticate user name.*" ) ) {
                    // Let user know we couldn't authenticate.
                    if ( sAdminUN.equals( sUsername ) ) {
                        System.out.println( "Invalid Old Password." );
                    } else {
                        System.out.println( "Invalid Password for user '" + 
                            sAdminUN + "'" );
                    }

                    // If we are in debug mode.
                    if ( s_bDebug ) {
                        // Rethrow so that user sees full stacktrace.
                        throw e;
                    }
                } else {
                    // Must be some other error, so rethrow it.
                    throw e;
                }

                // Go ahead and exit.
                System.exit(1);
            }

            // Second new password for testing accuracy.
            String sNewPassword2 = "";

            // Repeat until we get matching new passwords.
            do {
                // Read in the new password.
                System.out.println( sUsername + "'s New Password:" );
                sNewPassword = StdIn.readLine();

                // Read in the password a second time for accuracy.
                System.out.println( "Retype " + sUsername + "'s New Password:" );
                sNewPassword2 = StdIn.readLine();

                // If the two new passwords do not match.
                if ( !sNewPassword.equals( sNewPassword2 ) ) {
                    // Let user knoew the passwords didn't match and exit.
                    System.out.println( "Mismatch; try again, ^C to quit." );
                }
            } while ( !sNewPassword.equals( sNewPassword2 ) );

            // Obtain a reference to com.opsware.fido.ejb.session.UserFacade.
            UserFacade uf = (UserFacade)tw.getFacade( UserFacade.class );

            // If we the admin and the user are the same.
            if ( sAdminUN.equals( sUsername ) ) {
                // Then only change the password of the currently authenticated
                // user.
                uf.changePassword( sNewPassword );

                // Let the user know what we did.
                System.out.println( "Successfully changed the password for " +
                    "user '" + sUsername + "'." );
            } else {
                // Obtain the userid for the given user.
                UserVO uvo = uf.getUserVOForUser( sUsername, null );
                Long uid = uvo.getUserId();

                // Attempt to change the password of the given user using the 
                // admin creds.
                uf.changePasswordForUser( uid, sNewPassword );

                // Let the user know what we did.
                System.out.println( "Successfully changed the password for " +
                    "user '" + sUsername + "', using " + sAdminUN + "'s " + 
                    "credentials." );
            }
        } catch ( Exception e ) {
            System.out.println( "Exception caught: " + e );
            e.printStackTrace();
        }
    }
}

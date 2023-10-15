#!/lc/bin/python
##
# Opsware Agent Shell v2 goals:
#
#  [ ] Impelment a custom asyncore layer that supports non-selectable streams
#      using a multithreading.  These threaded streams should be tightly
#      synchronized with the core select loop in order to provide the exact
#      same client semantics that a fully selectable asyncore would provide.
#
#  [ ] Come up with a usage paradigm to better abstract client objects in an
#      asyncore world.  At the moment I'm thinking of some kind of state
#      machine based mechanism.  Ideally these objects would encapsulate 
#      knowledge about how specific communication exchanges worked in such a
#      that they could be layered and reused.
#
#  [ ] Come up with a regular way to embed dependent python modules into a
#      single python source file.
#------------------------------------------------------------------------------
#

##
# Program Overview:
#
# This program can be used to instantiate a direct shell connection to an agent
# using only a certificate signed by "opsware".
#
# The implementation is very premative.  For example, the local tty is not put 
# into "raw" mode.  Also, the initial request is hard-coded, whereas a more
# general purpose implementation would allow these to be set on the command 
# line.
#
# In windows, the backspace appears not to work.  I'm guessing some kind of 
# key mapping needs to take place here.
#
# TODO:
#
# [X] Add opswgw option.
#
# [X] Automatically query the agent for platform and version.
#
# [X] Add an option to run a specified command on the target agent.
#     (This would allow for a scp style file transfer.)
#     (-e <cmdline>)
#
# [X] Add an option to evaluate an arbitrary python string.  This will allow 
#     for a consistant cross-platform, and cross-version, injection point for 
#     the execution of remote code.  (-y <python_string>)
#
# [ ] Make username specificaition optional.  Default to "root" for non-win32
#     and "LocalSystem" for win32.
#
# [X] Convert this program to use the asyncore library.
#
# [ ] Add an option to fork into the background. ([-f])
#
# [ ] Add an option to forward communications to a listening socket instead 
#     of stdio, and optionally spawn a telnet client to the speicified 
#     listener port.  ([-l host:port [-t]])
#     (I think this would actually be a mostly useless feature.  Unless we 
#     went to the trouble of creating an entire telnet compatible server.
#     Otherwise, the telnet/nc client would either end up getting the raw 
#     OGSH encoded output, or some arbitrarily filtered fixed window-size
#     type terminal.  So I'm not sure this feature would be all that 
#     usefull.)
#
# [ ] Create an integrate arbitrary TCP socket forwarding and multiplexing.
#     ([-L [lhost:]lport:rhost:rport] [-R [rhost:]rport:lhost:lport])
#
# [X] Remove dependence on "coglib.certmaster".
#
# [X] Add code to handle SAS escape codes:
#     #define ESC_CHAR        ((char) 0xEE)
#     #define WINCH_CHAR      'W'
#     #define STDOUT_CHAR     'O'
#     #define STDERR_CHAR     'E'
#     #define EXIT_CHAR       '?'
#     #define EOF_IN_CHAR     'i'
#     #define EOF_OUT_CHAR    'o'
#     #define EOF_ERR_CHAR    'e'
#     #define PTY_YES_CHAR    't'
#     #define PTY_NO_CHAR     'T'
#
# [X] Add cleaner getopt parameter parsing.
#
# [X] Have various properties of XML RPC request filled in more intellegently.
#     For example, terminal properties, etc.
#
#------------------------------------------------------------------------------

class Options:
    def PrintUsage( self ):
        _Debug( """Direct shell login to opsware agents via "ogsh.jump" xmlrpc.

Usage: %s [-p <password>] [-c <client_cert_path] [-e <command>] 
       [-g [realm@]gwhost[:gwport]] [-h] [-L [lhost:]lport:[rhost]:rport] [-T] 
       [-y <python_expression>] [-R [rhost:]rport:[lhost]:lport]
       user@agent_host[:agent_port]

Options:
 -c  Supply an optional client certificate.  (Expected to be in PEM format and
     contain both certificate and private key.)
 -d  Enable debug printouts.
 -e  Execute given command remotely.
 -g  Connect through an opswgw proxy port.  Realm is optional.  If no port is
     specified, then defaults to 3001.
 -h  Prints this help text.
 -L  Specifies a local listener on host <lhost> port <lport> to be forwarded 
     through the tunnel connection to remote host <rhost> on port <rport>.  If
     either of <lhost> or <rhost> are not specified, then "localhost" is
     assumed.
 -p  Supply an optional password.  (In the future this will be neccessary when
     authing as a win32 AD account.)
 -R  Specifies a remote listener on host <rhost> port <rport> to be forwarded 
     through the tunnel connection to local host <lhost> on port <lport>.  If
     either of <lhost> or <rhost> are not specified, then "localhost" is
     assumed.
 -T  Suppress pty allocation request.
 -y  Execute given python expression remotely.

Notes:
    o If [:agent_port] is not specified, '1002' is assumed.
    o If [:gwport] port is not specified, then '3002' is assumed.

Discussion:
    This utility is still in heavy development.
""" % g_sName )
        sys.exit( 1 )


def main( lstArgs ):
  # Process arguments.

  # Create a local tty terminal session object if requested.

  # Create a listener terminal session object if requested.

  # If any stream mux options where specified.
    # Start remote stream mux instance bound to stdio stream.

    # Pass along stream mux options and create local instance.

  # Go into async select loop.

  
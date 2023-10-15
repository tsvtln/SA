#!/lc/bin/python

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

import sys
import time
import select
import tty
import os
import getopt
import string
import socket
import asyncore
import types
import signal
import gzip
import base64
import md5
import re
import fcntl, termios, struct
import imp
import errno

from errno import ECONNRESET

# Global tunnel object.
g_oTunnel = None

if "/opt/opsware/pylibs" not in sys.path: sys.path.append("/opt/opsware/pylibs")
if "/lc/blackshadow" not in sys.path: sys.path.append("/lc/blackshadow")

from M2Crypto import SSL
from M2Crypto import M2Crypto

# Global debug level.
g_nDebug = 0

# Figure out a name.
if ( __name__=='__main__' ):
    g_sName = sys.argv[0]
else:
    g_sName = __name__

# Global OnExit object.  This object should be chained and contain a function 
# named OnExit().  It is to allow various objects to insert code that needs to
# execute when the program exits, no matter what exit conditions are.  For
# example, tty reset code.
g_oOnExit = None

# Global asyncore loop select error callback object. ;)  When a signal is
# handled without exiting the process, any pending select statement will throw
# an exception.  In that case, this object's "OnSelectError()" method will be 
# called.  For example, this allows a window size change signal to be propertly
# handled and serviced.
g_oAsyncCb = None

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

    def __init__( self, lstArgs ):
        # Initialize input parameters to default values.
        self.sUsername = ""
        self.sCertPath = ""
        self.sCmd = ""
        self.bFork = 0
        self.bUseGW = 0
        self.sGWHost = ""
        self.nGWPort = -1
        self.sGWRealm = ""
        self.sPassword = ""
        self.bNoPty = 0
        self.sPythonExp = ""
        self.sAgentHost = ""
        self.sAgentPort = ""
        self.nAgentPort = -1
        self.lstTcpmuxOpts = []
        self.sArgs = ""

        # Parse arguments.
        (lstOpts, lstArgs) = getopt.getopt(lstArgs, "c:de:fg:hL:p:R:Ty:")
        if ( len(lstArgs) > 0 ): sArgs = lstArgs[0]
        if ( len(lstArgs) != 1 or len(string.split(sArgs, "@")) !=2 ):
            # Print usage and exit with error.
            self.PrintUsage( )

        global g_nDebug
        # Itterate through all the options.
        for aCurOpt in lstOpts:
            if( aCurOpt[0] == "-c" ):
                self.sCertPath = aCurOpt[1]
            elif( aCurOpt[0] == "-d" ):
                g_nDebug = g_nDebug + 1
            elif( aCurOpt[0] == "-e" ):
                self.sCmd = aCurOpt[1]
            elif( aCurOpt[0] == "-f" ):
                self.bFork = 1
            elif( aCurOpt[0] == "-T" ):
                self.bNoPty = 1
            elif( aCurOpt[0] == "-g" ):
                self.bUseGW = 1
                self.sGWHost = aCurOpt[1]
                sGWPort = "3002"
                if ( string.find( self.sGWHost, "@" ) > -1 ): ( self.sGWRealm, self.sGWHost ) = string.split( self.sGWHost, "@" )
                if ( string.find( self.sGWHost, ":" ) > -1 ): ( self.sGWHost, sGWPort ) = string.split( self.sGWHost, ":" )
                if ( sGWPort ): self.nGWPort = int( sGWPort )
            elif( aCurOpt[0] == "-p" ):
                self.sPassword = aCurOpt[1]
            elif( aCurOpt[0] == "-R" ):
               self.lstTcpmuxOpts = self.lstTcpmuxOpts + [aCurOpt[0], aCurOpt[1]] 
            elif( aCurOpt[0] == "-y" ):
                self.sPythonExp = aCurOpt[1]
            elif( aCurOpt[0] == "-h" ):
                # Print usage and exit.
                self.PrintUsage( )
            elif( aCurOpt[0] == "-L" ):
               self.lstTcpmuxOpts = self.lstTcpmuxOpts + [aCurOpt[0], aCurOpt[1]] 

        # Grab the first non-parsed argument as the "target" and parse it.
        sTarg = lstArgs[0]
        (self.sUsername, sTarg) = string.split(sTarg, "@")
        if ( string.find( sTarg, ":" ) > -1 ): (self.sAgentHost, self.sAgentPort) = string.split(sTarg, ":")
        else: (self.sAgentHost, self.sAgentPort) = (sTarg, "1002")
        try:
            self.nAgentPort = int( self.sAgentPort )
        except:
            _Debug( "%s: Agent port, <agent_port> must be an integer.\n\n" % g_sName )
            self.PrintUsage( )

        if ( self.sCertPath == "" ):
            DARWIN_CERT_PATH='/var/lc/crypto/spin/spin.srv'
            EINSTEIN_CERT_PATH='/var/opt/opsware/crypto/spin/spin.srv'

            if ( os.path.exists( EINSTEIN_CERT_PATH ) ): self.sCertPath=EINSTEIN_CERT_PATH
            elif ( os.path.exists( DARWIN_CERT_PATH ) ): self.sCertPath=DARWIN_CERT_PATH
            else:
                _Debug( "%s: Could not find a default cert and no cert specified!\n\n" % g_sName )
                sys.exit(1)
        elif ( not os.path.exists( self.sCertPath ) ):
            _Debug( "%s: %s: Cert does not exist!\n\n" % (g_sName, self.sCertPath) )
            sys.exit(1)


HTTPRespHdrRE = re.compile("^HTTP[^ ]+ (\d+).*\r\n\r\n", re.S)
def ProcessHTTPResp( oSslSock, sHttpReq, anAllowedRespCodes, sBuf="" ):
    # Send the HTTP request:
    oSslSock.send( sHttpReq )

    # Wait for the response.
    while 1:
        aSel = select.select( [oSslSock], [], [], 30 )

        if ( oSslSock in aSel[0] ):
            sBlock = oSslSock.recv(4096)
            if ( g_nDebug > 0 ): _Debug( "HTTP Response block: -%s-\n" % sBlock )
            sBuf = sBuf + sBlock

            match = HTTPRespHdrRE.search( sBuf )

            if ( match ):
                # Return any part of the buffer left over after processing the HTTP headers.
                sBuf = sBuf[match.regs[0][1]:]
                # Grab the HTTP response code.
                nRespCode = int(match.group(1))
                # If the HTTP response code is not one of the allowed.
                if ( not ( nRespCode in anAllowedRespCodes ) ):
                    # Extract the HTTP Headers and print an error message.
                    sHTTPRespHdrs = match.string[:match.regs[0][1]]
                    _Debug( "Recieved error HTTP response code %d\nHeaders recieved:\n%s\n" % (nRespCode, sHTTPRespHdrs) )
                    _Exit( 1 )
                # Indicate that we are done processing HTTP response headers.
                break
        else:
           _Debug( "%s: Tiemout while sending HTTP request!\n" % g_sName )
           _Exit( 1 )

    # Return the results.
    return sBuf


OGSHRespHdrRE = re.compile("^([^\r\n]+)\r?\n")
def ProcessOGSHResp( oSslSock, sBuf, asExpectedResp ):
    bTimedOut = 0
    sRespCode = 0
    while 1:
        aSel = select.select( [oSslSock], [], [], 30 )

        if ( oSslSock in aSel[0] ):
            sCurBuf = oSslSock.recv(4096)
            if ( not sCurBuf ): continue
            if ( g_nDebug > 0 ): _Debug( "OGSH response message: -%s-\n" % sCurBuf )
            sBuf = sBuf + sCurBuf

            match = OGSHRespHdrRE.search( sBuf )

            if ( match ):
                # Return any part of the buffer left over after processing the OGSH response.
                sBuf = sBuf[match.regs[0][1]:]
                # Return OGSH response message.
                sRespMsg = match.group(1)

                # If we recieved the expected response.
                if ( sRespMsg in asExpectedResp ):
                    break
                else:
                    _Debug( "%s: Recieved unexpected OGSH response message -%s-\n" % (g_sName, sRespMsg) )
                    _Debug( "%s: Expecting %s\n" % (g_sName, str(asExpectedResp)) )
                    _Exit( 1 )
        else:
            # Indicate that we timed out.
            _Debug( "%s: Tiemout while waiting for OGSH response!\n" % g_sName )
            _Exit( 1 )

    # Return the results.
    return sBuf


def ConnectViaGW( sock, sGWHost, nGWPort, sGWRealm, sTargetHost, nTargetPort ):
    # Connect to the given gateway proxy port.
    sock.connect((sGWHost, nGWPort))

    # Construct the GW HTTP connect request.
    sGWConnectReq = "CONNECT %s:%d HTTP/1.0\r\n" % ( sTargetHost, nTargetPort )
    if ( sGWRealm ):
        sGWConnectReq = sGWConnectReq + "X-OPSW-REALM: %s\r\n" % sGWRealm
    sGWConnectReq = sGWConnectReq + "\r\n"

    if ( g_nDebug > 0 ): _Debug( "GW Req: -%s-\n" % sGWConnectReq )

    # Process the response.
    sBuf = ProcessHTTPResp( sock, sGWConnectReq, [200] )

    # Return the socket.
    return sock


# Debug method
def hexstr(s):
    lst = []
    for ch in s:
        hv = string.replace(hex(ord(ch)), '0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    
    return reduce(lambda x,y:x+y, lst)

# Debug method
def DumpObj(o):
    _Debug( "Object: [%s]:\n" % str(o) )
    for sCurAttr in dir(o):
        _Debug( "  %s:[%s]\n" % (sCurAttr, getattr( o, sCurAttr ) ) )

#def toStr(s):
#    return s and chr(atoi(s[:2], base=16)) + toStr(s[2:]) or ''


# Class to decode OGSH escape sequencies.
OGSH_ESC_CHAR = "\356"
OGSH_WINCH_CHAR = "W"
class OGSHDecoder:
    def __init__( self, sBuf="" ):
        self.bStdOut = 1
        self.sBufStdOut = ""
        self.sBufStdErr = ""
        self.sBuf = sBuf

    def Process( self, sBuf ):
        self.sBuf = self.sBuf + sBuf

        while (OGSH_ESC_CHAR in self.sBuf):
           nEscPos = string.find( self.sBuf, OGSH_ESC_CHAR )
           if ( self.bStdOut ):
               self.sBufStdOut = self.sBufStdOut + self.sBuf[:nEscPos]
           else:
               self.sBufStdErr = self.sBufStdErr + self.sBuf[:nEscPos]
           self.sBuf = self.sBuf[nEscPos:]
           if ( len(self.sBuf) > 1 ):
               if ( self.sBuf[1] == "O" ):
                   self.bStdOut = 1
               elif ( self.sBuf[1] == "E" ): 
                   self.bStdOut = 0
               elif ( self.sBuf[1] == OGSH_ESC_CHAR ):
                   if ( self.bStdOut ):
                       self.sBufStdOut = self.sBufStdOut + OGSH_ESC_CHAR
                   else:
                       self.sBufStdErr = self.sBufStdErr + OGSH_ESC_CHAR

               if ( g_nDebug > 0 ): _Debug( "%" + self.sBuf[1] )

               if ( self.sBuf[1] == OGSH_WINCH_CHAR ):
                   if ( len(self.sBuf) > 5 ):
                       self.sBuf = self.sBuf[6:]
                   else:
                       break
               else:
                   self.sBuf = self.sBuf[2:]

        if ( string.find( self.sBuf, OGSH_ESC_CHAR ) < 0 ):
            if ( self.bStdOut ):
                self.sBufStdOut = self.sBufStdOut + self.sBuf
            else:
                self.sBufStdErr = self.sBufStdErr + self.sBuf

            self.sBuf = ""

    def GetStdOut( self ):
        sBuf = self.sBufStdOut
        self.sBufStdOut = ""
        return sBuf

    def GetStdErr( self ):
        sBuf = self.sBufStdErr
        self.sBufStdErr = ""
        return sBuf


class OgshSocket( OGSHDecoder ):
    def __init__( self, oSocket, sBuf ):
        OGSHDecoder.__init__( self, sBuf )
        self.oSocket = oSocket

    def fileno( self ):
        return self.oSocket.fileno( )

    def recv( self, nBuf ):
        sData = self.oSocket.recv( nBuf )
        self.Process( sData )
        sErrBuf = self.GetStdErr( )
        if ( sErrBuf and g_nDebug > 0 ): _Debug( sErrBuf )
        sStdOut = self.GetStdOut( )
        return sStdOut

    def send( self, sBuf ):
        return self.oSocket.send( sBuf )

    def setblocking( self, *aArgs ):
        apply( self.oSocket.setblocking, aArgs )

    def close( self ):
        return self.oSocket.close( )


##
# Obtains an ssl socket to the given agent, optionally through an opswgw proxy 
# port.
def GetAgentSslSock( oOpts ):
    ctx = SSL.Context( "sslv23" )
    ctx.load_cert( oOpts.sCertPath )
    ctx.set_cipher_list( 'RC4-MD5:RC4-SHA:DES-CBC3-SHA:DES-CBC3-MD5' )

    ssl_sock = SSL.Connection( ctx )

    if ( oOpts.bUseGW ):
        ConnectViaGW( ssl_sock.socket, oOpts.sGWHost, oOpts.nGWPort, oOpts.sGWRealm, oOpts.sAgentHost, oOpts.nAgentPort )
        ssl_sock._setup_ssl((oOpts.sGWHost, oOpts.nGWPort))
        ssl_sock._check_ssl_return(M2Crypto.ssl_connect(ssl_sock.ssl))
    else:
        ssl_sock.connect((oOpts.sAgentHost,oOpts.nAgentPort))

    return ssl_sock


XMLRPCReturnValueRE = re.compile(".*methodResponse.+params.+param.+value.+string>([^<>]+)<", re.S)
sHttpGetOsType = "GET /rpc.py?method=platform.getOsType HTTP/1.0\r\n\r\n"
g_sAgentOsType = ""
def GetAgentOsType( oOpts ):
    # If we already know the agent os type.
    global g_sAgentOsType
    if ( g_sAgentOsType ): return g_sAgentOsType

    # Open a ssl socket to the agent.
    oSslSock = GetAgentSslSock( oOpts )

    # Execute the platform.getOsType XMLRPC call and Wait for the HTTP response.
    sBuf = ProcessHTTPResp( oSslSock, sHttpGetOsType, [200] )

    # Read in the HTTP response body.
    sResp = sBuf
    try:
        sBuf = oSslSock.recv( 4096 )
        while ( len(sBuf) > 0 ):
            sResp = sResp + sBuf
    except:
        pass

    # Close the ssl socket.
    oSslSock.close()

    # Grep the response for the platform identifier
    oMatch = XMLRPCReturnValueRE.search(sResp)
    g_sAgentOsType = sOsType = sResp[oMatch.regs[1][0]:oMatch.regs[1][1]]

    if ( g_nDebug > 0 ): _Debug( "%s: Detected OS type: '%s'\n" % ( g_sName, g_sAgentOsType ) )

    # Return the OS type.
    return g_sAgentOsType
    

sHttpGetVersion = "GET /rpc.py?method=cogbot.getVersion HTTP/1.0\r\n\r\n"
g_sAgentVersion = ""
def GetAgentVersion( oOpts ):
    # If we already know the agent version.
    global g_sAgentVersion
    if ( g_sAgentVersion ): return g_sAgentVersion

    # Open a ssl socket to the agent.
    oSslSock = GetAgentSslSock( oOpts )

    # Execute the cogbot.getVersion XMLRPC call and wait for the HTTP response.
    sBuf = ProcessHTTPResp( oSslSock, sHttpGetVersion, [200] )

    # Read in the HTTP response body.
    sResp = sBuf
    try:
        sBuf = oSslSock.recv( 4096 )
        while ( len(sBuf) > 0 ):
            sResp = sResp + sBuf
    except:
        pass

    # Close the ssl socket.
    oSslSock.close()

    # Grep the response for the cogbot version
    oMatch = XMLRPCReturnValueRE.search(sResp)
    g_sAgentVersion=sResp[oMatch.regs[1][0]:oMatch.regs[1][1]]

    if ( g_nDebug > 0 ): _Debug( "%s: Detected agent version: '%s'\n" % ( g_sName, g_sAgentVersion ) )

    # return the results.
    return g_sAgentVersion
    

def compact_traceback():
    t, v, tb = sys.exc_info()
    tbinfo = []
    assert tb # Must have a traceback
    while tb:
        tbinfo.append((
            tb.tb_frame.f_code.co_filename,
            tb.tb_frame.f_code.co_name,
            str(tb.tb_lineno)
            ))
        tb = tb.tb_next

    # just to be safe
    del tb

    file, function, line = tbinfo[-1]
#    info = string.join(['[%s|%s|%s]' % x for x in tbinfo])
    info = '[' + string.join (
        map (
            lambda x: string.join (x, '|'),
            tbinfo
            ),
        '] ['
        ) + ']'
    return (file, function, line), t, v, info


class MyDispatcher( asyncore.dispatcher ):
    def __init__( *args ):
        apply (asyncore.dispatcher.__init__, args)

    def log( self, sMesg ):
        if ( g_nDebug > 0 ): _Debug( "%s: asyncore: %s\n" % ( g_sName, sMesg ) )

    def handle_error(self):
        nil, t, v, tbinfo = compact_traceback()

        # sometimes a user repr method will crash.
        try:
            self_repr = repr(self)
        except:
            self_repr = '<__repr__(self) failed for object at %0x>' % id(self)

        sys.stderr.write( 'uncaptured python exception, closing channel %s (%s:%s %s)' % (self_repr, t, v, tbinfo) )
        self.close()

    def handle_error_old (self, *info):
        (t,v,tb) = info
        if ( g_nDebug > 0 ):
            (file,fun,line), tbinfo = asyncore.compact_traceback (t,v,tb)

            # sometimes a user repr method will crash.
            try:
                self_repr = repr (self)
            except:
                self_repr = '<__repr__ (self) failed for object at %0x>' % id(self)

            _Debug (
                '%s: uncaptured python exception, closing channel %s (%s:%s %s)\n' % (
                    g_sName,
                    self_repr,
                    str(t),
                    str(v),
                    tbinfo
                    )
                )
        del t,v,tb
        self.close()


class MyFileDispatcher( asyncore.file_dispatcher ):
    def __init__( self, nFD ):
        asyncore.file_dispatcher.__init__( self, nFD )

        # If this FD is stdin, stdout, or stderr, then hijack file_wrapper's close.
        if ( nFD in [0, 1, 2]):
            self.socket.close = lambda : 0

        # Hack to make file_wrapper class work right.
        self.socket.send = self.socket.write

    def log( self, sMesg ):
        if ( g_nDebug > 0 ): _Debug( "%s: asyncore: %s\n" % ( g_sName, sMesg ) )

    def handle_error(self):
        nil, t, v, tbinfo = compact_traceback()

        # sometimes a user repr method will crash.
        try:
            self_repr = repr(self)
        except:
            self_repr = '<__repr__(self) failed for object at %0x>' % id(self)

        sys.stderr.write( 'uncaptured python exception, closing channel %s (%s:%s %s)' % (self_repr, t, v, tbinfo) )
        self.close()

    def handle_error_old (self, *info):
        (t,v,tb) = info
        (file,fun,line), tbinfo = compact_traceback (t,v,tb)

        # sometimes a user repr method will crash.
        try:
            self_repr = repr (self)
        except:
            self_repr = '<__repr__ (self) failed for object at %0x>' % id(self)

        if ( g_nDebug > 0 ): _Debug (
            '%s: uncaptured python exception, closing channel %s (%s:%s %s)' % (
                g_sName,
                self_repr,
                str(t),
                str(v),
                tbinfo
                )
            )
        del t,v,tb
        self.close()

def OgshJump( oOpts, oStdIoeConn ):
    # HTTP/XMLRPC related string constants for ogsh.jump method.
    sPostBody = "<?xml version='1.0'?>\n<methodCall>\n<methodName>ogsh.jump</methodName>\n<params>\n<param>\n<value><struct>\n<member>\n<name>term_rows</name>\n<value><int>%d</int></value>\n</member>\n<member>\n<name>cwd</name>\n<value><string></string></value>\n</member>\n<member>\n<name>term_type</name>\n<value><string>%s</string></value>\n</member>\n<member>\n<name>password</name>\n<value><string>%s</string></value>\n</member>\n<member>\n<name>run_as_superuser</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>pty</name>\n<value><int>%d</int></value>\n</member>\n<member>\n<name>term_cols</name>\n<value><int>%d</int></value>\n</member>\n<member>\n<name>term_ios</name>\n<value><string>38400:38400:3.1C.8.15.4.0.0.11.13.1A.100.12.17.16.100.100.100.F:B40:1E3B:544505:8</string></value>\n</member>\n<member>\n<name>username</name>\n<value><string>%s</string></value>\n</member>\n</struct></value>\n</param>\n</params>\n</methodCall>\n" % (oStdIoeConn.aWinSize[0], os.environ['TERM'], oOpts.sPassword, not oOpts.bNoPty, oStdIoeConn.aWinSize[1], oOpts.sUsername)
    sHttpPostReq = 'POST /ops/shell/shell_init.py HTTP/1.0\r\nHOST: %s:%s\r\nUpgrade: OGSH/1.0\r\nUser-Agent: xmlrpclib.py/0.9.8 (Using SSL by Loudcloud)\r\nContent-Type: text/xml\r\nContent-Length: %d\r\n\r\n' % (oOpts.sAgentHost, oOpts.sAgentPort, len(sPostBody)) + sPostBody

    # Open a ssl socket to the agent.
    oSslSock = GetAgentSslSock( oOpts )

    # Execute the ogsh.jump XMLRPC call and wait for the HTTP response.
    sBuf = ProcessHTTPResp( oSslSock, sHttpPostReq, [101] )

    # Wait for the OGSH "OK" response.
    sBuf = ProcessOGSHResp( oSslSock, sBuf, ["OK"] )

    if ( g_nDebug > 0 ): _Debug( "%s: Connected to %s as %s\n" % (g_sName, oOpts.sAgentHost, oOpts.sUsername) )

    # Return the socket and any left over buffer:
    return (oSslSock, sBuf)


class OgshSocketDisp( MyDispatcher ):
    def __init__( self, oSslSock, sBuf, oStdIoeConn ):
        # Call the parent's initializer.
        MyDispatcher.__init__( self, oSslSock )

        # Initialze some member variables.
        self.oStdIoeConn = oStdIoeConn
        self.sRawReadBuf = sBuf
        self.ogsh_decoder = OGSHDecoder( )

    def handle_connect(self):
        pass

    def handle_read(self):
        try:
            sRead = self.recv(4096)
            if ( type(sRead) == types.StringType ): 
                self.sRawReadBuf = self.sRawReadBuf + sRead
                self.ogsh_decoder.Process( self.sRawReadBuf )
                self.sRawReadBuf = ""
                self.oStdIoeConn.WriteStdOut( self.ogsh_decoder.GetStdOut() )
                self.oStdIoeConn.WriteStdErr( self.ogsh_decoder.GetStdErr( ) )
            else:
                if ( g_nDebug > 0 ): _Debug( "Warning: non string type read from agent socket: -%s-, %s\n" % (sRead, type(sRead)))
        except:
            self.handle_close()

    def writable(self):
        return (self.oStdIoeConn.HasStdIn( ))

    def handle_write(self):
        sent = self.send(self.oStdIoeConn.ReadStdIn( ))

    def handle_close(self):
        _Debug( "Connection to %s closed.\r\n" % self.socket.addr[0] )
        self.close()
        self.oStdIoeConn.Close()


def OgshPush( oOpts, oStdIoeConn, sCmd ):
    # Figure out the script content
    if ( GetAgentOsType( oOpts ) == "win32" ):
        sScriptCode = "%s" % sCmd
    else:
        sScriptCode = "#!/bin/sh\n%s" % sCmd

    # Calculate the script hash.
    sScriptHash = base64.encodestring(md5.md5(sScriptCode).digest())[:-1]

    # If a stdioe object was supplied.
    if ( oStdIoeConn ):
        nRows = oStdIoeConn.aWinSize[0]
        nCols = oStdIoeConn.aWinSize[1]
        bNoPty = oOpts.bNoPty
    else:
        nRows = 25
        nCols = 80
        bNoPty = 1

    # HTTP/XMLRPC related string constants for ogsh.jump method.
    sPostBody = "<?xml version='1.0'?>\n<methodCall>\n<methodName>ogsh.push</methodName>\n<params>\n<param>\n<value><struct>\n<member>\n<name>cwd</name>\n<value><string></string></value>\n</member>\n<member>\n<name>term_type</name>\n<value><string>%s</string></value>\n</member>\n<member>\n<name>password</name>\n<value><string>%s</string></value>\n</member>\n<member>\n<name>exempt_script</name>\n<value><int>1</int></value>\n</member>\n<member>\n<name>run_as_superuser</name>\n<value><int>0</int></value>\n</member>\n<member>\n<name>pty</name>\n<value><int>%d</int></value>\n</member>\n<member>\n<name>term_cols</name>\n<value><int>%d</int></value>\n</member>\n<member>\n<name>term_ios</name>\n<value><string>38400:38400:3.1C.7F.15.4.0.0.11.13.1A.100.12.17.16.100.100.100.F:140:E3B:544505:8</string></value>\n</member>\n<member>\n<name>term_rows</name>\n<value><int>%d</int></value>\n</member>\n<member>\n<name>script_name</name>\n<value><string>ogsh_script.bat</string></value>\n</member>\n<member>\n<name>script_hash</name>\n<value><string>%s\n</string></value>\n</member>\n<member>\n<name>script_version</name>\n<value><string>32.0.1</string></value>\n</member>\n<member>\n<name>username</name>\n<value><string>%s</string></value>\n</member>\n</struct></value>\n</param>\n</params>\n\n</methodCall>\n" % (os.environ['TERM'], oOpts.sPassword, not bNoPty, nCols, nRows, sScriptHash, oOpts.sUsername)
    sHttpPostReq = "POST /ops/shell/shell_init.py HTTP/1.0\r\nHOST: %s:%s\r\nUpgrade: OGSH/1.0\r\nUser-Agent: xmlrpclib.py/0.9.8 (Using SSL by Loudcloud)\r\nContent-Type: text/xml\r\nContent-Length: %d\r\n\r\n" % (oOpts.sAgentHost, oOpts.sAgentPort, len(sPostBody)) + sPostBody

    # Open a ssl socket to the agent.
    oSslSock = GetAgentSslSock( oOpts )

    # Execute the ogsh.jump XMLRPC call and wait for the HTTP response.
    sBuf = ProcessHTTPResp( oSslSock, sHttpPostReq, [101] )

    # Wait for the OGSH "CODE" response.
    sBuf = ProcessOGSHResp( oSslSock, sBuf, ["CODE"] )

    # Send the length of the script code.
    oSslSock.send( "%d\r\n" % len(sScriptCode) )

    # Send the code itself.
    oSslSock.send( sScriptCode )

    # Send an empty line.
    oSslSock.send( "\r\n" )

    # Wait for the OGSH "ARGS" or "UARGS" response.
    sBuf = ProcessOGSHResp( oSslSock, sBuf, ["UARGS","ARGS"] )

    # Send empty args.
    oSslSock.send( "0\r\n" )

    # Wait for the OGSH "OK" response.
    sBuf = ProcessOGSHResp( oSslSock, sBuf, ["OK"] )

    if ( g_nDebug > 0 ): _Debug( "%s: Connected to %s as %s\n" % (g_sName, oOpts.sAgentHost, oOpts.sUsername) )

    # Return the socket and any left over buffer:
    return (oSslSock, sBuf)


def OgshExecPythonExp( oOpts, oStdIoeConn, sPythonExp ):
    if ( GetAgentOsType( oOpts ) == "win32" ):
        if ( GetAgentVersion( oOpts ) >= "32" ):
            sCmd = '"%%%%PROGRAMFILES%%%%\\Opsware\\agent\\lcpython15\\python.exe" -c "%s"'
        else:
            sCmd = '"%%%%PROGRAMFILES%%%%\\LoudCloud\\lcpython15\\python.exe" -c "%s"'
    else:
        if ( GetAgentVersion( oOpts ) >= "32" ):
            sCmd = '/opt/opsware/bin/python -c "%s"'
        else:
            sCmd = '/lc/bin/python -c "%s"'

    # Add in the framework loader.
    sCmd = sCmd % "import base64;eval(compile(base64.decodestring('%s'), 'bs1', 'exec'))"

    return OgshPush( oOpts, oStdIoeConn, sCmd % string.replace(base64.encodestring(sPythonExp),"\n","") )


# Opens a ogsh.push channel with agent and marshes the python module 
# <sPythonMod> to the remote python interpreter.  <sPythonMod> is expected to
# to be a base64 gzip compressed string.
def OgshExecPythonMod( oOpts, sPythonModName, sPythonEval, oStdIoeConn, sPythonMod ):
    # Remote python module boot loader code.
    sPythonExp = 'import base64; import gzip; eval(compile(gzip.zlib.decompress(base64.decodestring("eNptT0GKAjEQvOcVQ04JjkFB9iDmtLsnDz5glaCTxm1IOkM6Mq6vd+LgguCturqrugpjn3JpMPYCJ8h//ITpH52ODB+r53S+YS8SmyFjAbVs5efu63tPUguyo9xw8Ugmw9EHJFCVpp91AFKk58uDgPdXwSIV9W6lBVspxfCLAVT1Yb0Jes2WZ2OMeqcWbZhPG/0Sbbd9BIt2zG4IBheTv4wupAVcoWu6FPvqWjuZW8CT8VC5DMxqqv1gPHDJSOf6oKVWVrHUDVITjXMeu+Lc5Aiv5B2WNnfD")),"bs2","exec"));'

    # Open up a python expression connection to the agent.
    (oSocket, sBuf) = OgshExecPythonExp( oOpts, oStdIoeConn, sPythonExp )
 
    # Wrap this socket and buffer inside of an OGSH decoder wrapper.
    oOgshSock = OgshSocket( oSocket, sBuf )

    # Wait for the "CODE" response.
    sBuf = ProcessOGSHResp( oOgshSock, sBuf, ["CODE"] )

    # Send the name of the python module, and eval statement, and the length 
    # of the compressed module.
    oOgshSock.send( "%s\n%s\n%s\n" % (sPythonModName, sPythonEval, len(sPythonMod) ) )

    # Send the python module.
    while ( len( sPythonMod ) > 0 ):
        sPythonMod = sPythonMod[oOgshSock.send( sPythonMod[:4096]):]

    # Wait for the "OK" response.
    sBuf = ProcessOGSHResp( oOgshSock, sBuf, ["OK"] )

    # Return the socket and buffer.
    return oOgshSock


class StdIoeConn:
    def __init__( self, nStdIn, nStdOut, nStdErr, oOpts ):
        self.oStdInDisp = StdInDisp( nStdIn, self )
        self.oStdOutDisp = StdOutDisp( nStdOut, self )
        self.oStdErrDisp = StdErrDisp( nStdErr, self )
        self.bWinSizeCh = 0
        self.sOldTty = ""

        # If a pty was requested.
        if ( not oOpts.bNoPty ):
            # Set the local pty to raw.
            self.TtySetRaw( oOpts )

            # Install this object into the global OnExit handler.
            # (TODO: make this a hook.)
            g_oOnExit = self

            # Install a handler for the terminal window size change signal.
            StdIoeConn.oSigWinChHandler = self
            def sigwinch_handler( n, frame ):
                StdIoeConn.oSigWinChHandler.bWinSizeCh = 1
            signal.signal( signal.SIGWINCH, sigwinch_handler )

            # Install an OnSelectError handler to check for window size changes.
            # (We don't want to do this in the middle of the actual SIGNWINCH
            # handler for concurency reasons.)
            global g_oAsyncCb
            g_oAsyncCb = self

        # Detect the current width and height of the terminal.
        self.aWinSize = self.GetPtyWinSize( )

    def HasStdIn( self ):
        return ( len(self.oStdInDisp.sReadBuf) > 0 )

    def ReadStdIn( self ):
        sData = self.oStdInDisp.sReadBuf
        self.oStdInDisp.sReadBuf = ""
        return sData

    def WriteStdOut( self, sData ):
        self.oStdOutDisp.WriteBuffered( sData )

    def WriteStdErr( self, sData ):
        self.oStdErrDisp.WriteBuffered( sData )

    # hack for python 1.5.x version of termios that seems to lack TIOCGWINSZ.
    if ( not hasattr(termios,"TIOCGWINSZ") ):
        if ( string.find( sys.platform, "linux" ) > -1 ): termios.TIOCGWINSZ=21523
        elif ( string.find( sys.platform, "freebsd" ) > -1 ): termios.TIOCGWINSZ=1074295912

    def ioctl_GWINSZ( self, fd ):
        try:
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, 'abcd'))
        except:
            return None
        return cr

    def GetPtyWinSize( self ):
        cr = self.ioctl_GWINSZ(0) or self.ioctl_GWINSZ(1) or self.ioctl_GWINSZ(2)

        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
            if not cr:
                try:
                    cr = (env['LINES'], env['COLUMNS'])
                except:
                    cr = (25, 80)
        return cr

    # OnSlectError handler.
    def OnSelectError( self ):
        # If a window size change was detected.
        if ( self.bWinSizeCh ):
            # Indicate we have handled the window size change event.
            self.bWinSizeChSig = 0

            # Get the current window size.
            self.aWinSize = self.GetPtyWinSize( )

            # Construct an OGSH message to communicate this change to the agent.
            sWinChMsg = OGSH_ESC_CHAR + OGSH_WINCH_CHAR + struct.pack( ">HH", self.aWinSize[0], self.aWinSize[1] )

            # Optional debug statement explaining what is going on.
            if ( g_nDebug > 1 ): _Debug( "%s: Window change detected to %s.  Sent OGSH msg: %d[%s]\n" % ( g_sName, self.aWinSize, len(sWinChMsg), hexstr(sWinChMsg) ) )

            # Push this message into the stdin dispatcher's read buffer.
            self.oStdInDisp.sReadBuf = self.oStdInDisp.sReadBuf + sWinChMsg

    # OnExit handler.
    def OnExit( self ):
        # Restore the tty.
        self.TtyRestore( )

        # If there is a global tunnel object.
        global g_oTunnel
        if ( g_oTunnel ):
            # Tell the tunnel to shut down when all flows expire.
            # If there are currently any flows open...
            if ( g_oTunnel.CloseWhenNoFlows( ) ):
                _Debug( "Waiting for existing flows to expire.\n" )

    def Close( self ):
        # Close the std in, out, and error dispatchers.
        self.oStdInDisp.close()
        self.oStdOutDisp.close()
        self.oStdErrDisp.close()

        # Invoke our OnExit handler.
        self.OnExit( )

    # Set the local tty to raw and preserve current settings.
    def TtySetRaw( self, oOpts ):
        # Setup local tty.
        self.sOldTty = tty.tcgetattr(0)
        new = tty.tcgetattr(0)
        if ( GetAgentOsType( oOpts ) == 'win32' ): 
            new[0] = tty.ICRNL | tty.IXON
            new[1] = tty.OPOST | tty.ONLCR | tty.NL0 | tty.CR0 | tty.TAB0 | tty.BS0 | tty.VT0 | tty.FF0
            new[2] = tty.CS8 | tty.CREAD
            new[3] = tty.ISIG | tty.ICANON | tty.IEXTEN | tty.ECHO | tty.ECHOE | tty.ECHOK | tty.ECHOCTL | tty.ECHOKE
        else:
            new[0] = tty.IGNPAR
            new[1] = 0
            new[2] = (new[2] & ~(tty.CSIZE | tty.PARENB)) | tty.CS8
            new[3] = 0
            new[6][tty.VMIN] = 1
            new[6][tty.VTIME] = 0
        tty.tcsetattr(0, tty.TCSADRAIN, new)

    def TtyRestore( self ):
        # If there is an old tty setting.
        if ( self.sOldTty ):
            # Restore previous tty settings, if there are any.
            tty.tcsetattr( 0, tty.TCSAFLUSH, self.sOldTty )


class StdInDisp( MyFileDispatcher ):
    def __init__( self, nFD, oStdIoeConn ):
        MyFileDispatcher.__init__( self, nFD )
        self.oStdIoeConn = oStdIoeConn
        self.sReadBuf = ""

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(4096)
        self.sReadBuf = self.sReadBuf + read

    def writable(self):
        return 0

    def handle_write(self):
        pass

    def handle_close(self):
        self.close()
        self.oStdIoeConn.Close( )


class StdOutDisp( MyFileDispatcher ):
    def __init__( self, nFD, oStdIoeConn ):
        MyFileDispatcher.__init__( self, nFD )
        self.oStdIoeConn = oStdIoeConn
        self.sWriteBuf = ""

    def handle_connect(self):
        pass

    def handle_read(self):
        pass

    def writable(self):
        return (len(self.sWriteBuf) > 0)

    def handle_write(self):
        nSent = self.send( self.sWriteBuf )
        self.sWriteBuf = self.sWriteBuf[nSent:]

    def handle_close(self):
        self.close( )
        self.oStdIoeConn.Close( )

    def WriteBuffered( self, sData ):
        self.sWriteBuf = self.sWriteBuf + sData


class StdErrDisp( MyFileDispatcher ):
    def __init__( self, nFD, oStdIoeConn ):
        MyFileDispatcher.__init__( self, nFD )
        self.oStdIoeConn = oStdIoeConn
        self.sWriteBuf = ""

    def handle_connect(self):
        pass

    def handle_read(self):
        pass

    def writable(self):
        return (len(self.sWriteBuf) > 0)

    def handle_write(self):
        nSent = self.send( self.sWriteBuf )
        self.sWriteBuf = self.sWriteBuf[nSent:]

    def handle_close(self):
        self.close( )
        self.oStdIoeConn.Close( )

    def WriteBuffered( self, sData ):
        self.sWriteBuf = self.sWriteBuf + sData


# Install a default SIGINT handler.
def sigint_handler( n, frame ):
    # Close all open file descriptors in the asyncore map.
    for oCurKey in asyncore.socket_map.keys( ):
        if ( type(oCurKey) == types.IntType ):
            nFD = oCurKey
            os.close( oCurKey )
        else:
            nFD = oCurKey.fileno( )
        try:
            os.close( nFD )
        except IOError, sWhy:
            if ( g_nDebug > 1 ): _Debug("%s: %s: IOError while closing fd: %s\n" % (g_sName, str(nFD), sWhy))
            pass
        except OSError, sWhy:
            if ( g_nDebug > 1 ): _Debug("%s: %s: OSError while closing fd: %s\n" % (g_sName, str(nFD), sWhy))
            pass
    _Debug( "Killed by signal %d.\n" % signal.SIGINT )
    _Exit( 1 )
signal.signal( signal.SIGINT, sigint_handler )

def siginfo_handler( n, frame ):
    _Debug( "DEBUG: [%s]\n" % asyncore.socket_map )
signal.signal( signal.SIGTSTP, siginfo_handler )

def Main( lstArgs ):
    # Parse the options.
    oOpts = Options( lstArgs[1:] )

    # If any port forwarding options where given.
    if ( oOpts.lstTcpmuxOpts ):
        # If the platform is not windows.
        if ( GetAgentOsType( oOpts ) != "win32" ):
            # Execute tcpmux on the remote end.
            oOgshSock = OgshExecPythonMod( oOpts, "tcpmuxr", "Main( ['tcpmuxr', '-s'%s] )" % (", '-d'" * g_nDebug), None, g_sTcpmuxGzB64 )

            # Create a module space for the local execution of the tcpmux blob.
            global tcpmuxl
            tcpmuxl = imp.new_module( "tcpmuxl" )

            # Load the tcpmux blob into the locally create module.
            exec compile( gzip.zlib.decompress( base64.decodestring( g_sTcpmuxGzB64 ) ), "tcpmuxl", "exec" ) in tcpmuxl.__dict__

            # Execute tcpmux locally in the newly create module.
            tcpmuxl.Main( ["tcpmuxl"] + (['-d'] * g_nDebug) + oOpts.lstTcpmuxOpts + ['-S', oOgshSock] )

            # If a tunnel object was created.
            if ( hasattr( tcpmuxl, "g_oTunnel" ) ):
                global g_oTunnel
                g_oTunnel = tcpmuxl.g_oTunnel
        else:
            # Indicate that port forwarding is disabled against win32 agents.
            _Debug( "%s: Port forwarding is not currently supported against windows agents.\n" % g_sName )

    # If the fork option was not given.
    if ( not oOpts.bFork ):
        # Create a stdioe dispatcher.
        oStdIoeConn = StdIoeConn( sys.stdin.fileno(), sys.stdout.fileno(), sys.stderr.fileno(), oOpts )

        # If a command was specified.
        if ( oOpts.sCmd ):
            (oSocket, sBuf) = OgshPush( oOpts, oStdIoeConn, oOpts.sCmd )
        # Else, if a python expression was specified
        elif ( oOpts.sPythonExp ):
            (oSocket, sBuf) = OgshExecPythonExp( oOpts, oStdIoeConn, oOpts.sPythonExp )
        # Else, just open up a ogsh.jump.
        else:
            (oSocket, sBuf) = OgshJump( oOpts, oStdIoeConn )

        # Create a OGSH socket dispatcher.
        oOgshSockDisp = OgshSocketDisp( oSocket, sBuf, oStdIoeConn )
    else:
        # Just do nothing for now.
        _Debug( "%s: Forking isn't currently implemented, so we will just sit here and do nothing...\n" % g_sName );

def _Debug( sMsg ):
    sys.stderr.write( sMsg + "\r" )

def _Exit( nErr=0 ):
    # If there is an OnExit object, and it has a cleanup method.
    if ( hasattr( g_oOnExit, "OnExit" ) and 
        type(g_oOnExit.OnExit) == types.MethodType ):
        # Call the cleanup method.
        g_oOnExit.OnExit( )

    sys.exit( nErr )

# Embedded tcpmux source code.  Encoded gzipped and base64ed python source code
# tcpmux is a generic tcp forwarding program implemented in python.  The 
# Opsware agent doesn't posses an API to support arbitrary port porwards.  We
# use the following tcpmux code blob by uploading it to a python instance 
# running on the remote agent.  All agents have a python inpreter.  We then
# execute this code blob locally.  In both places the bloc is executed in side
# of its own module space.
#
g_sTcpmuxGzB64 = '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'

if __name__=='__main__':
    try:
        Main( sys.argv )

        # Infinate while loop to keep going back into the asyncore loop if
        # certain allowable exceptions occur.
        while 1:
            try:
                # Enter the asyncore loop.
                asyncore.loop()

                # If we get here, then we must be done due to normal user 
                # interaction, so break out of the while loop.
                break
            # If we get a select error..
            except select.error, sWhy:
                # And if the error is due to an interrupted system call...
                if ( string.find(string.lower(str(sWhy)),"interrupted system call") > -1 ):
                    # If there is an async callback object and method.
                    if ( hasattr( g_oAsyncCb, "OnSelectError" ) and
                        type(g_oAsyncCb.OnSelectError) == types.MethodType ):
                        # Invoke the callback method.
                        g_oAsyncCb.OnSelectError( )
                else: raise
    finally:
        _Exit( )

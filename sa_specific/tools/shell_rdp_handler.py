#!/usr/bin/env python
# shell_rdp_handler.py -- gfvt
# PURPOSE
#   RDP Handler for Opsware Global Shell
#

import sys
import os
import socket
import select
import types
import traceback
import string
from coglib import authentication_cache
from cogbot.base.ops.shell import shell_base_handler
from coglib import lcthreading
from opsware_common.logging import Logger
from opsware_common import conf
from coglib import platform
if sys.platform == "win32":
   from coglib.nt import registry

cogbot_agent_ogsh_logging = "cogbot.agent_ogsh_logging"
# Read the ogsh logging config value
# 0 = off
# 1 = some
# 2 = verbose
ogsh_logging = 0
try:
    if conf.__conf__.has_key(cogbot_agent_ogsh_logging):
        ogsh_logging = conf.__conf__.get(cogbot_agent_ogsh_logging)
except:
    pass

RDP_LISTEN_PORT = "RDPListenPort"
RDP_BOUND_IP = "RDPBoundToIPAddress"

DEFAULT_RDP_PORT = 3389
DEFAULT_LOOPBACK_IP_ADDRESS = '127.0.0.1'

def send_to_socket( source_socket, target_socket, direction, oplock ):
    while 1:
        if select.select( [source_socket], [], [], 10 )[0] != []:
            oplock.acquire()
            try:
                try:
                    data = source_socket.recv( 4095 )
                except socket.error:
                    Logger.info("RDP handler thread exiting")
                    return
                except:
                    Logger.error("Error during socket recv")
                    raise
            finally:
                oplock.release()
            if not data:
                if direction == 0:
                    Logger.info("No data returned by recv() from TTLG. RDP handler thread exiting" )
                else:
                    Logger.info("No data returned by recv() from RDP server. RDP handler thread exiting" )
                return
            elif type( data ) == types.StringType:
                if ogsh_logging == 2:
                    if direction == 0:
                        Logger.trace("%s bytes received from TTLG" % len(data))
                    else:
                        Logger.trace("%s bytes received from RDP server" % len(data))
                num_bytes_sent = total_bytes_sent = 0
                while (total_bytes_sent < len(data) ):
                    try:
                        while not select.select( [], [target_socket], [], 10 )[1]: 
                            Logger.trace("Write blocked for 10 seconds waiting for SSL connection")
                        oplock.acquire()
                        try:
                            num_bytes_sent = target_socket.send( data[total_bytes_sent:] )
                        finally:
                            oplock.release()
                        if ogsh_logging == 2:
                            if direction == 0 :
                                Logger.trace("%s bytes sent to RDP server" % num_bytes_sent)
                            else:
                                if num_bytes_sent > 0:
                                    Logger.trace("%s bytes sent to TTLG" % num_bytes_sent)
                                else:
                                    Logger.trace("%s returned by send() to TTLG" % num_bytes_sent)
                        if num_bytes_sent < 0:
                            num_bytes_sent = 0
                    except socket.error: 
                        Logger.trace("RDP handler thread exiting")
                        return
                    except:
                        Logger.error("Error during socket send")
                        raise
                    total_bytes_sent = total_bytes_sent + num_bytes_sent
            elif type( data ) != types.StringType and data == -2:
                if ogsh_logging == 2:
                    if direction == 0:
                        Logger.trace("-2 returned by recv() from TTLG" )


def send_to_socket_wrapper( source_socket, target_socket, direction, oplock ):
    # If anything at all bad happens, we want to catch it and log it.  And
    # then we want the thread to die a quiet death, rather than forcing
    # something upstream to deal with it.
    try:
        send_to_socket(source_socket, target_socket, direction, oplock)
    except:
        l = apply( traceback.format_exception, sys.exc_info() )
        Logger.error("Error during send_to_socket: %s" % l)


class OGSHRDP( shell_base_handler.ShellCommandHandler ):
    def __init__( self, params ):
        shell_base_handler.ShellCommandHandler.__init__( self, params )
        
        # Work around a really idiotic bug in m2crypto, which doesn't
        # account for the possibility that more than one thread might
        # use the same SSL context.  Doing that screws up the thread
        # state pointer save/restore logic and eventually causes
        # Python to throw a "tstate mix-up" error.  See bug 161880.
        #
        # I refuse to call this a "fix" to that bug, even though it
        # eliminates the symptoms.  The only proper fix is to modify
        # m2crypto to eliminate the above assumption entirely or, better
        # yet, eliminate the need for Python C extension code to manage
        # the Python thread state pointer at all (extension code should
        # never have to remember Python internal state).
        self.oplock = lcthreading.RLock()


    def preCheck( self ):
        rdp_tcp_key = "System\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp"
        lanatable_key = "System\\CurrentControlSet\\Control\\Terminal Server\\lanatable"
        interfaces_key = "System\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces"
        port_number_value_name  = "PortNumber"
        lan_adapter_value_name  = "LanAdapter"
        port = DEFAULT_RDP_PORT
        host = DEFAULT_LOOPBACK_IP_ADDRESS

        # Determine if agent config has a hard-coded value, the IP address to which RDP
        # is bound. This can be used as a fallback in the field if our logic to determine the 
        # IP to which RDP is bound yields an incorrect value.
        rdp_bound_to = conf.__conf__.get(RDP_BOUND_IP)
        if rdp_bound_to != None:
            Logger.info( "Override of RDP bind address value found in agent config - %s: %s" % (RDP_BOUND_IP, rdp_bound_to) )
            host = string.strip(rdp_bound_to)
        else:
            # Fix for BZ137276 - 'RDP needs to be listening on localhost for the agent to connect'
            # If RDP is bound to a specific interface, here's how we determine that.
            default_loopback_chosen = 0
            try:
                lan_adapter_id = registry.regGetInt( rdp_tcp_key, lan_adapter_value_name )   
            except: 
                Logger.error("RDP handler failed to read LanAdapter id from registry" + \
                      ", defaulting to LanAdapter 0")
                lan_adapter_id = 0
                pass

            if( lan_adapter_id != 0):
                try:
                    # From the LanAdapter id, iterate over the children, obtaining the LanAdapter GUID
                    lanatable_entries = registry.regKeyChildren( lanatable_key )
                    for lte in lanatable_entries:
                        # Get the LanAdapter id for each alan tabl entry and compare
                        lanatable_entry_key = lanatable_key + "\\" + lte
                        this_lan_adapter_id = registry.regGetInt( lanatable_entry_key, "LanaId")
                        if this_lan_adapter_id == lan_adapter_id:
                            # The correct LanAdapter has been identified, now get the IP address
                            # to which this adapter is bound
                            interfaces_table_entries = registry.regKeyChildren( interfaces_key )
                            for ite in interfaces_table_entries:
                                if( ite == lte ):
                                    # Matching GUID found in the Interfaces list, get the corresponding
                                    # IP address.
                                    ite_key = interfaces_key + "\\" + ite
                                    ip_address_list = registry.regGetStringList( ite_key, "IPAddress")
                                    if( len(ip_address_list) == 1 ):
                                        if( ip_address_list[0] == "0.0.0.0" ):
                                            # Look at DHCP
                                            dhcp_ip_address_list = registry.regGetStringList( ite_key, "DhcpIPAddress")
                                            if( len(dhcp_ip_address_list) == 1 ):
                                                if( dhcp_ip_address_list[0] == "0.0.0.0" ):
                                                    # Neither of the two known address lists have 
                                                    # a valid IP so write a message to the logfile,
                                                    # assume 127.0.0.1 and carry on.
                                                    default_loopback_chosen = 1
                                                else:
                                                    host = dhcp_ip_address_list[0]
                                            else:
                                                host = dhcp_ip_address_list[0]
                                        else:
                                            host = ip_address_list[0]
                                    else:
                                        host = ip_address_list[0]
                                    break
                            break
                except:
                    default_loopback_chosen = 1

                if default_loopback_chosen == 1:
                    host = DEFAULT_LOOPBACK_IP_ADDRESS
            else:
                host = DEFAULT_LOOPBACK_IP_ADDRESS

            if( host != DEFAULT_LOOPBACK_IP_ADDRESS or default_loopback_chosen == 1 ):
                Logger.info( "The IP address to which RDP is bound is assumed to be %s" % host)
                Logger.info( "To override this assumption, add this name-value pair to the agent configuration file: %s: <IP address>, e.g. %s: 192.168.9.201" % (RDP_BOUND_IP,RDP_BOUND_IP))
                Logger.info( "then restart the Opsware Agent")

        # Determine if agent config has a hard-coded port number value, the port number 
        # on which RDP acceepts connections. This can be used as a fallback in the field 
        # if our logic to determine the port numbe ron which RDP is listening 
        # yields an incorrect value.
        rdp_listen_port = conf.__conf__.get(RDP_LISTEN_PORT)
        if rdp_listen_port != None:
            Logger.info( "Override of RDP port number value found in agent config - %s: %s" % (RDP_LISTEN_PORT,rdp_listen_port))
            port = rdp_listen_port
        else:
            try:
                port = registry.regGetInt( rdp_tcp_key, port_number_value_name )   
            except: 
                Logger.trace("RDP handler failed to read PortNumber from registry, " + \
                      ", defaulting to PortNumber %s" % port)
                pass

            if( port != DEFAULT_RDP_PORT ):
                Logger.info( "The PortNumber on which RDP is assumed to be listening is %s" % port)
                Logger.info( "To override this assumption, add this name-value pair to the agent configuration file: %s: <PortNumber>, e.g. %s: 3390" % (RDP_LISTEN_PORT,RDP_LISTEN_PORT))
                Logger.info( "then restart the Opsware Agent")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            Logger.info("Connecting to RDP server %s:%s" % (host,port))
            self.sock.connect( (host, port) )
            Logger.flush()
        except socket.error: 
            Logger.error("Failed to connect to RDP server on port %s" % port)
            Logger.flush()
            pass

    def run( self, conn ):
        self.conn = conn

        Logger.trace( "Creating thread to send from TTLG to RDP" )
        Logger.flush()
        t1 = lcthreading.Thread(target=send_to_socket_wrapper,args=( conn,self.sock,0,self.oplock))

        Logger.trace( "Creating thread to send from RDP to TTLG" )
        Logger.flush()
        t2 = lcthreading.Thread(target=send_to_socket_wrapper,args=( self.sock,conn,1,self.oplock))

        t1.start()
        t2.start()

        t1.join()
        t2.join()
        Logger.trace( "Both threads joined" )
        Logger.flush()

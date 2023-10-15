# This library facilitates the execution of arbitary commands against
# an Opsware Agent using the TTLG multiplexing protocol on top of the
# agentexec binary handshaking protocol.

MSG_CLOSED = -1
MSG_STDIN  = 0
MSG_STDOUT = 1
MSG_STDERR = 2

##
# Represents an exec session against a target agent.
#
class AgentExec:
  def __init__( self, gw_proxy_host, gw_proxy_port, target_realm, target_host,
                target_port, cmd, argv, btty=0, cert=None ):

  def __del__( self ):

  def recvmsgs( self ):
    """Returns a list of recieved messages: [(type, msg), ...]
Might block.  Empty list does not emply the session is closed."""

  def sendmsg( self, type, msg ):

  def fileno( self ):
    """Returns the file descriptor number for the socket for this agent exec session."""

  def close( self ):
    """Closes this agentexec session."""


#!/bin/sh

##
# Program Overview:
#
# This program attempts to replicate the process used by the NGUI to bring up a
# OGSH session.  This includes roughly (1) opening an ssh execution channel 
# opswsshd, (2) executing a remote "ogsh" command, and (3) setting up a local
# single-use listening socket forwarded to the ssh execution channel and (3)
# invoking a local telnet client against this socket.  The one item that this 
# script doesn't currentl perform is to access opswssh via the lb-gw (port 
# 8080).  The purpose of this script is to disect the end-to-end process in an 
# relatively straight-forward way to facilitate the understanding and debugging
# issues in the field.  This utility uses ssh, netcat, twinpipe, and gcc.  The
# script uses gcc to build the twinpipe utility.
#
# This script attempts to detect the particular version of SAS being worked
# with.  It caches this detected version along with a twist token for the 
# particular hostname and username you are using.  It doesn't currently 
# contain any logic to invalidate this cached data, so if you have trouble
# logging in, you might want to try clearing out these cache files.
#
# TODO: 
#
# [ ] See about adding the lb-gw step for completeness.
#

# Grab arguments:
sHostname=$1
sUsername=$2
sTelnetPort=$3
TOKEN=$4

# If arguments wheren't given.
if ( [ ! \( -n "$sHostname" -a -n "$sUsername" \) ]; ) then {
  echo "Usage: $0 <hostname> <username> [telnet_port=8888]"
  exit 1
} fi

# If no telnet port was given.
if ( [ ! "$sTelnetPort" ]; ) then {
  sTelnetPort=8888
} fi

# Insure that we have netcat on the system.
if ( [ ! "`which nc`" ]; ) then {
  echo $0: netcat not found!!
  exit 1
} fi

# Calculate a unique name for the ssh ask pass env var.
export SSH_ASKPASS="./.${sUsername}@${sHostname}.token"
SAS_VERSION_FILE="./.${sUsername}@${sHostname}.sas_version"

# If there is no ssh ask pass file.
if ( [ ! -f "$SSH_ASKPASS" -o ! -f "$SAS_VERSION_FILE" ]; ) then {
  # If a token was provided on the command line.
  if ( [ ! "$TOKEN" ]; ) then {
    # Obtain a token for the user.
    echo $0: Querying hub for a token for user ${sUsername}
    TOKEN_AND_SAS_VERSION="`ssh -p 2222 ${sUsername}@${sHostname} 'cat /opsw/.token && echo  && /opsw/api/com/opsware/shared/TwistConsoleService/method/getVersion 2>/dev/null'`"
    TOKEN=`echo $TOKEN_AND_SAS_VERSION | awk '{print $1}'`
    SAS_VERSION=`echo $TOKEN_AND_SAS_VERSION | awk '{print $2}'`
  } fi

  # If there is not token.
  if ( [ \! "$TOKEN" ]; ) then {
    exit 1
  } fi

  # Create an ask pass for the user.
  echo $0: Caching token to '"'$SSH_ASKPASS'"'
  printf "#!/bin/sh\necho '$TOKEN'" > "$SSH_ASKPASS"
  chmod u+x "$SSH_ASKPASS"

  # Cache the SAS version:
  echo $SAS_VERSION > "$SAS_VERSION_FILE"
} else {
  # Pull out the cached token.
  echo $0: Using cached token '"'$SSH_ASKPASS'"'
  TOKEN="`$SSH_ASKPASS`"

  # Pull out the cached SAS version.
  SAS_VERSION="`cat $SAS_VERSION_FILE`"
} fi

# If no version string is given, assume darwin.
if ( [ ! -n "$SAS_VERSION" ]; ) then {
  sOUser=opswtunnel
  sOGSH_CMD="/opt/OPSWogfs/bin/ogsh"
# If the version is less than 32f..
} elif ( [ `echo $SAS_VERSION | perl -pe 'if ( /^32[abcde]/ ) { $_="true" };'` = "true" ]; ) then {
  sOUser=opswtun
  sOGSH_CMD="/opt/opsware/ogfs/bin/ogsh"
# Assume SAS version > 6.1
} else {
  sOUser=$sUsername
  sOGSH_CMD="/opt/opsware/ogfs/bin/ogsh"
} fi

# If the twinpipe program doesn't exist in the cwd.
if ( [ ! -x ./twinpipe ]; ) then {
  echo $0: 'Compiling "twinpipe.c"... (Only done the first time.)'
  gcc -o twinpipe twinpipe.c
} fi

# Execute the twinpipe in the background.
#./twinpipe "ssh -T -p 2222 ${sOUser}@${sHostname} ${sOGSH_CMD} -y -z -u ${sUsername} -t $TOKEN -e UTF-8" "nc -l $sTelnetPort" &
./twinpipe "ssh -T -p 2222 ${sOUser}@${sHostname} ${sOGSH_CMD} -y -z -u ${sUsername} -t $TOKEN" "nc -l $sTelnetPort" &

# Open up an xterm
xterm -geometry +10+10 -T "OGSH: ${sUsername}@${sHostname}" -e telnet 127.0.0.1 $sTelnetPort

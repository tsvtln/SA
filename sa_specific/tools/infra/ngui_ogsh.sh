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

# Locate the openssl binary.
sOpenSslCmd="`which openssl`"
if ( [ \! -f "$sOpenSslCmd" ]; ) then {
  echo "$0: Could not locate openssl.  (Needed to extract twinpipe.)"
  exit 1
} fi

# If the twinpipe source code doesn't exit.
sTwinpipeSrc="/tmp/twinpipe.c"
if ( [ \! -f "$sTwinpipeSrcd" ]; ) then {
  perl -pe 'while( $_ ne "" ) { print substr($_,0,64) . "\n";$_=substr($_,64); }' <<EOF | $sOpenSslCmd base64 -d | gzip -d -c > $sTwinpipeSrc
H4sIAPQGEEYAA51VUW/bNhB+Dn/FTcUSKrAji8UeGtcF2mAdihn2Q1PsYSsChqItNgypiVTcIs1++46krTl2vAUzYOH08buPx7vj6YUyQneVhNfOV8qe1W/Ii21Iq+vHWGcUwjs8tTRc72DfXLHiyj9GZduanU0WwvjoS4pTQj7MPl6+nU7fXn6Yz84JWQoBw9+41viEYSMrbrxCaM5gaMGvlGlUI3vjTBDRIO+flaJzbaGt4Lq4VqYg2sBwsYseYndOS9kQclqE4ODCNt9ataw90Iscylev2ICNRiN4p9yfK4Vo7X1zXhTqRp0tFCpEuMgh+DvPQ+TKeAhblb+zz4NoMbTGm+U7qypwnf4iaTBzck+OhLZO0kQdfc7HsA2UCGxTyl1KmSgPOxFUZdi9YmPyaOtKSRoIJu58o7SmiWvCNpt3lt5RM3BvuTLRibdLMQBhjfMgat7CabJPceEuCvZ7JxGnqhD8lsOCKz3JMkSRvKBBEX6YwMucHKF7D00mwBCKWBRVMAHurQrLd+ukRLrK4R5SHdEeQyt91xoYjQELmnAsDzwgPfwXTYtyC4otjq06CCLZJ8eX8nxDvlWixdxi0JX7w2TbjL6NToS9veWmKk96k51syJe1hDXoYIUZhWsJ/FpjF1sMj1cguajB+lq2Dmznm86foXM80jr8YYkvDyFJ6epRrBCWLlDWANsFyj1K+XIP+alHYvopFggT66RHg+Y5vIZRnrCl9M2ybehjLq7D8THQUEYkZYhleU4g/L5/h9iQqSvzPW6En2azp9kM2Yl+T4TVmjdOVuf7VYRs3ol6AJhRWNlWV/ClCx23cQH6o8tDigcQ5GOiG3S0LU2t+2Tm49zq79wA3l99/Pny/RQ19hZ+CQs5HMNf86vZfPZuOr/4NYhuM8tDEuUzJdihKNizo2CHomD/EUXqgHCzsTYL295smmVpsan7RI8TMfDC7XWhh7Cx0oTBXglSUjuZLnvVNWwrjaNYhh5MIZURTAMzmvKrFJpmcXy7GiuapedQ4HM9HAYw+zSdRvqV/Ko8jdI4zTanYM88Bds5Bfu3U7CnTlH+31Owg6cIQ6FXIkerWmlJw5eYRj68maQgyFE/C3GS/w2M3JXhCAgAAA==
EOF
} fi

# If the twinpipe program doesn't exist.
sTwinpipeCmd="/tmp/twinpipe"
if ( [ ! -x "$sTwinpipeCmd" ]; ) then {
  echo $0: 'Compiling "twinpipe.c"... (Only done the first time.)'
  gcc -o "$sTwinpipeCmd" "$sTwinpipeSrc"
} fi

# Execute the twinpipe in the background.
#"$sTwinpipeCmd" "ssh -T -p 2222 ${sOUser}@${sHostname} ${sOGSH_CMD} -y -z -u ${sUsername} -t $TOKEN -e UTF-8" "nc -l $sTelnetPort" &
"$sTwinpipeCmd" "ssh -T -p 2222 ${sOUser}@${sHostname} ${sOGSH_CMD} -y -z -u ${sUsername} -t $TOKEN" "nc -l $sTelnetPort" &

# Open up an xterm
xterm -geometry +10+10 -T "OGSH: ${sUsername}@${sHostname}" -e telnet 127.0.0.1 $sTelnetPort

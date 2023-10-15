#!/bin/sh
# This program provides access to the OGSH under any SAS user with only a
# username.  It does this by generating a twist token for the user and using
# it to manually authenticate to the hub via the ".authenticate" special file.
# It then leverages the "ttlg" command to initiate the "normal" OGSH session.
# A twist token is an encrypted string of XML that contains a username, 
# userid, and other timing and type related information.  The token is 
# encrypted with a key that is generated from a deterministic psuedo random 
# number generator that is seeded with the twist's private key, 
# "twist-key.pem".  This RNG is implemented in java, so this script has an 
# embedded token generation  class that is emitted at runtime to "/tmp" and 
# executed with the local java interpreter.
#
# Currently, this script depends on the spin, via local spinwrapper libraries,
# to lookup the userid of the given username.  This dependency could be 
# removed by having this script accept the userid on the command line.
#
# Also, at the end of this script there is a note about how to obtain an OGSH
# session for a user despite the user lacking the "launchGlobalShell"
# permission.  This mechanism also bypasses OGSH auditing.
#

if ( [ "$2" ]; ) then {
  sUserName="$1"
  sDvcId="$2"
} elif ( [ "$1" ]; ) then {
  sUserName="detuser"
  sDvcId="$1"
} else {
  echo Usage: $0 '[<username>] <dvc_id>'
  exit 1
} fi

# Extract all arguments past the first as the command.
sCmd="`echo "$@"\  | perl -pe 's/^[^\s]+ //'`"

# Locate twist private key.
EINSTEIN_KEY_PATH="/var/opt/opsware/crypto/twist/twist-key.pem"
DARWIN_KEY_PATH="/var/lc/crypto/twist/twist-key.pem"
if ( [ -f "$EINSTEIN_KEY_PATH" ]; ) then {
  sKeyPath="$EINSTEIN_KEY_PATH"
} elif ( [ -f "$DARWIN_KEY_PATH" ]; ) then {
  sKeyPath="$DARWIN_KEY_PATH"
} else {
  echo $0: Could not locate twist private key on this system.
  exit 1
} fi

# Locate the python interpreter.
EINSTEIN_PYTHON_BIN="/opt/opsware/bin/python"
DARWIN_PYTHON_BIN="/lc/bin/python"
if ( [ -f "$EINSTEIN_PYTHON_BIN" ]; ) then {
  sPythonCmd="env PYTHONPATH=/opt/opsware/pylibs $EINSTEIN_PYTHON_BIN"
  sOgshEnvPath="/bin:/usr/bin:/usr/local/bin:/usr/sbin:/opt/opsware/ogfs/bin"
  sTtlgCmd="/opt/opsware/ogfs/bin/ttlg"
} elif ( [ -f "$DARWIN_PYTHON_BIN" ]; ) then {
  sPythonCmd="env PYTHONPATH=/lc/blackshadow $DARWIN_PYTHON_BIN"
  sOgshEnvPath="/bin:/usr/bin:/usr/local/bin:/usr/sbin:/opt/OPSWogfs/bin"
  sTtlgCmd="/opt/OPSWogfs/bin/ttlg"
} else {
  echo $0: Could not locate the opsware python interpreter on this system.
  exit 1
} fi

# Locate the java interpreter and required libraries.
# Locate the java interpreter and required libraries.
if ( [ -f "/opt/opsware/twist/lib/client/twistclient.jar" ]; ) then {
  sJavaCmd="/opt/opsware/j2sdk1.4/bin/java -classpath $0:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/twist/lib/twist.jar:/opt/opsware/twist/lib/common-latest.jar"
} elif ( [ -f "/cust/twist/lib/client/twistclient.jar" ]; ) then {
  sJavaCmd="/opt/opsware/j2sdk1.4/bin/java -classpath $0:/cust/twist/lib/client/twistclient.jar:/cust/twist/lib/twist.jar:/cust/twist/lib/common-latest.jar:/cust/twist/lib/commons-codec-1.3.jar"
} else {
  echo $0: Could not locate dependent twist jar libraries for the token generation step.
  exit 1
} fi

# Locate the openssl binary.
EINSTEIN_OPENSSL_BIN="/opt/opsware/bin/openssl"
DARWIN_OPENSSL_BIN="/lc/bin/openssl"
if ( [ -f "$EINSTEIN_OPENSSL_BIN" ]; ) then {
  sOpenSslCmd="$EINSTEIN_OPENSSL_BIN"
} elif ( [ -f "$DARWIN_OPENSSL_BIN" ]; ) then {
  sOpenSslCmd="$DARWIN_OPENSSL_BIN"
} elif ( [ -f "`which openssl`" ]; ) then {
  sOpenSslCmd="`which openssl`"
} else {
  echo $0: Could not locate an openssl binary on this system.
  exit 1
} fi

# Attempt to locate the user id of this user from the spin.
nUserID=`$sPythonCmd -c "from coglib import spinwrapper;import string;import sys;sys.stdout.write(string.replace(str(spinwrapper.SpinWrapper()._AAAAaaUser.getList(name='$sUserName')[0][0]),'L',''))"`

# If no user id was found.
if ( [ \! "$nUserID" ]; ) then {
  echo $0: "'"$sUserName"'": Could not locate the userid of this user from the spin.
  exit 1
} fi

# Attempt to generate a token for this user/userid.
sToken=`$sJavaCmd TokenFactory $sUserName $nUserID $sKeyPath`

# If token failed to be generated.
if ( [ \! "$sToken" ]; ) then {
  echo $0: Failed to generate token for username="'"$sUserName"'"/userid="'"$nUserID"'".
  exit 1
} fi

/opt/opsware/bin/python -c 'import sys,time;sys.path.append("/opt/opsware/pylibs");sys.path.append("/opt/opsware");from waybot.base import twistaccess;ta=twistaccess.getTwistServiceForIp("twist");print ta.auditPatchPolicyComplianceWithReturn(token=sys.argv[2], device=sys.argv[1], lastcheckdate=str(long(time.time())*1000), reason="{}")' $sDvcId $sToken

exit 0

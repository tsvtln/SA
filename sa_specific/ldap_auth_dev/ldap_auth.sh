#!/bin/sh

# Calculate classpath.
export CLASSPATH=$0:/opt/opsware/twist/lib/ldapbp.jar:/opt/opsware/twist/lib/ldapssl.jar:/opt/opsware/bea/weblogic81/server/lib/weblogic.jar:/var/opt/opsware/twist/twist/stage/_appsdir_main_ear/libref/TwistCommon.jar:/var/opt/opsware/twist/twist/stage/_appsdir_fido_ear/entity/fido-entity.jar:/var/opt/opsware/twist/twist/stage/_appsdir_fido_ear/session/fido-session.jar:/opt/opsware/twist/lib/commons-logging.jar:/opt/opsware/twist/lib/opsware_common-latest.jar:/opt/opsware/twist/lib/spinclient-latest.jar:/opt/opsware/twist/lib/common-latest.jar:.

# Calculate java binary
JAVA_BIN="`ls /opt/opsware/j*/bin/java | head -1`"
if ( [ \! -f "$JAVA_BIN" ]; ) then {
  echo $0: 'Unable to locate java interpreter. (Is this a SAS 6.x+ box with a twist on it?)'
  exit 1
} fi

PrintUsage() {
  echo "Usage: $0 <sas_username> | -b <binddn> [-toc <twist_overrides_conf>]"
}

# If user specified no arguments.
if ( [ "$1" = "" ]; ) then {
  PrintUsage
  exit 1
} fi

# Insure that we are talking with a tty.
if ( [ \! -e "`tty`" ]; ) then {
  echo "$0: Not connected to a tty, therefore can't aquare password securely."
  exit 1
} fi

# Grab the password from the user securely.
if ( stty -echo; ) then {
  printf "password: "
  read sPassword
  stty sane
  printf "\n"
} else {
  echo "$0: Failed to put tty into raw mode."
  exit 1
} fi

# If user specified a username.
if ( [ $1 != "-b" ]; ) then {
  sUsername=$1

  # Query the local spin for a bindn for this user.
sBindDN="`printf 'from coglib import spinwrapper\nus=spinwrapper.SpinWrapper()._AAAAaaUser.getAll(restrict={"username":"'"$sUsername"'"})\nif not len(us):\n  print "NO_SUCH_USER"\nelif not (us[0]["credential_store"]=="EXTERNAL"):\n  print "NOT_EXTERNAL_USER"\nelse:\n  print us[0]["external_auth_id"]\n' | env PYTHONPATH=/opt/opsware/pylibs /opt/opsware/bin/python -c 'import sys,string; eval(compile(string.join(sys.stdin.readlines(),""),"query_sas_user_blob","exec"));'`"

  # If the user is not an external user.
  if ( [ "$sBindDN" = "NOT_EXTERNAL_USER" ]; ) then {
    # Let user know and exit.
    echo "$sUsername: Not an external user."
    exit 1
  } elif ( [ "$sBindDN" = "NO_SUCH_USER" ]; ) then {
    # Let user know and exit.
    echo "$sUsername: Not a SAS user."
    exit 1
  } fi

  sBindDNArg="-b '$sBindDN' -u"
} else {
  # If no binddn is specified.
  if ( [ \! "$2" ]; ) then {
    PrintUsage
    exit 1
  } fi
} fi

# everything looks good, so lets fire it up.
echo "password=${sPassword}" | eval "$JAVA_BIN" ExternalUserUtil $sBindDNArg "$@"

# If we get here, then exit with error.
exit 1


#!/bin/sh

##
# Program Overview:
#
# This shell script is part of a SAS command line utility that allows a SAS
# user to change their password, or a SAS administrator to change the password
# of given SAS user.  The primary purpose of this shell script are to process
# initial command line parameters, place the tty into a secure mode for
# password acceptance and invoke the java program that is capable of effecting
# the password modification.
#

# Lets the user know that the command was interrupted and enables echo on the
# tty.
OnIntr( ) {
  echo Interrupted
  stty echo
  exit 1
}
trap OnIntr 2

# Print out the usage for this command.
Usage() {
  cat <<EOF
Usage: $0 [-d|-h|-s]

Options:
  -d  Debug mode.  (To see stack trace of errors from twist.)
  -h  Display this help page.
  -s  Set the password of a given user.  Prompts for admin credentials.
EOF
}

# Parameters for java command line.
sJavaCmdParams=""

# Setup a stderr file descriptor for /dev/null by default.
exec 4>/dev/null
nStdErr=4

# Itterate through all the command line options.
for sCurCmdOpt in "$@" ""
{
  case "$sCurCmdOpt" in
  "-h") {
    # print the usage and exit
    Usage
    exit
  } ;;
  "-s") {
    # Read the admin username to use for the password change.
    echo "Admin username:"
    read sAdminUN
    sJavaCmdParams="$sJavaCmdParams -a $sAdminUN"
  } ;;
  "-d") {
    nStdErr=2
    sJavaCmdParams="$sJavaCmdParams -d"
  };;
  esac
}

# Java classpath.
export CLASSPATH=/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/spoke/lib/opsware_common-latest.jar:/opt/opsware/spoke/lib/spinclient-latest.jar:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/hub/lib/wlclient.jar:$0

# Attempt to locate a java binary and let user know if we fail.
JavaBin="`ls /opt/opsware/j*dk*/bin/java | head -1`"
if { [ \! "$JavaBin" ]; } then {
  echo $0: Unable to locate a java binary on this system using glob pattern 
  echo '    /opt/opsware/j*dk*/bin/java'
  exit 1
} fi

# Look for a cleartext twist running on this machine.
if { [ \! "`netstat -na |grep 1026 |grep LIST 2>/dev/null`" ]; } then {
  echo $0: No cleartext twist found.  Looking for a TCP listener on port 1026.
  exit 1
} fi

# Read the username whose password we want to change.
echo "User whose password you want to change:"
read sUsername
sJavaCmdParams="$sJavaCmdParams $sUsername"

# Turn off tty echo
stty -echo

# If we failed to turn off the tty's echo.
if { [ "$?" -ne "0" ]; } then {
  echo $0: Failed to disable echo on tty, bailing out.
  exit 1
} fi

# Invoke the twist java rmi weblogic client to effect the password change.
/opt/opsware/j2sdk1.4/bin/java sas_passwd_rmi $sJavaCmdParams 2>&$nStdErr

# Restore tty echo.
stty echo

# Exit without error.
exit 0


#!/bin/sh

# Extract all arguments past the first as the command.
sCmd="`echo "$@"\  | perl -pe 's/^[^\s]+ //'`"

# Locate the python interpreter.
EINSTEIN_PYTHON_BIN="/opt/opsware/bin/python"
if ( [ -f "$EINSTEIN_PYTHON_BIN" ]; ) then {
  sPythonCmd="env PYTHONPATH=/opt/opsware/pylibs $EINSTEIN_PYTHON_BIN"
  sOgshEnvPath="/bin:/usr/bin:/usr/local/bin:/usr/sbin:/opt/opsware/ogfs/bin"
  sTtlgCmd="/opt/opsware/ogfs/bin/ttlg"
} else {
  echo $0: Could not locate the opsware python interpreter on this system.
  echo $0: '(Requires SAS 6.0+)'
  exit 1
} fi

# Locate the java interpreter and required libraries.
if ( [ -f "/opt/opsware/twist/lib/client/twistclient.jar" ]; ) then {
  sJavaCmd="/opt/opsware/j2sdk1.4/bin/java -classpath $0:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/bea/weblogic81/server/lib/wlclient.jar:/opt/opsware/twist/lib/opsware_common-latest.jar:/opt/opsware/twist/lib/spinclient-latest.jar:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/twist/lib/twist.jar:/opt/opsware/twist/lib/common-latest.jar"
} else {
  echo $0: Could not locate dependent twist jar libraries for the token generation step.
  echo $0: '(Requires SAS 6.0+)'
  exit 1
} fi

# Attempt to locate the user id of this user from the spin.
nUserID=`$sPythonCmd -c "from coglib import spinwrapper;import string;import sys;sys.stdout.write(string.replace(str(spinwrapper.SpinWrapper()._AAAAaaUser.getList(name='detuser')[0][0]),'L',''))"`

# If no user id was found.
if ( [ \! "$nUserID" ]; ) then {
  echo $0: "'"detuser"'": Could not locate the userid of this user from the spin.
  exit 1
} fi

# Invoke the java program.
$sJavaCmd ReplaceNullCAsWithSpace detuser $nUserID "$@"

exit 0

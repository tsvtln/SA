#!/bin/sh

# Calculate classpath.
export CLASSPATH=$0:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/twist/lib/opsware_common-latest.jar:/opt/opsware/twist/lib/spinclient-latest.jar:/opt/opsware/bea/weblogic81/server/lib/wlclient.jar

printf Username:\ >`tty`
read un

printf Password:\ >`tty`
stty -echo
read pw
stty sane
echo 1>&2

JAVA_BIN="`find /opt/opsware/j* -name java -a -type f | head -1`"
#/opt/opsware/j2sdk1.4/bin/java

if ( [ -f $JAVA_BIN ]; ) then {
  $JAVA_BIN DumpFolders $un $pw "$@"
} else {
  echo Can"'"t find the java binary: '"'$JAVA_BIN'"'
  exit 1
} fi

exit 0

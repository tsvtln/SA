#!/bin/sh

# Calculate classpath.
export CLASSPATH=$0:/opt/opsware/twist/lib/ldapbp.jar:/opt/opsware/twist/lib/ldapssl.jar:/opt/opsware/bea/weblogic81/server/lib/weblogic.jar:/var/opt/opsware/twist/twist/stage/_appsdir_main_ear/libref/TwistCommon.jar:/var/opt/opsware/twist/twist/stage/_appsdir_fido_ear/entity/fido-entity.jar:/var/opt/opsware/twist/twist/stage/_appsdir_fido_ear/session/fido-session.jar:/opt/opsware/twist/lib/commons-logging.jar:/opt/opsware/twist/lib/opsware_common-latest.jar:/opt/opsware/twist/lib/spinclient-latest.jar:/opt/opsware/twist/lib/common-latest.jar:.

# Add some 7.8 classpaths (TODO: make this more elegant.)
export CLASSPATH=${CLASSPATH}:`echo /var/opt/opsware/twist/servers/twist/tmp/_WL_user/_appsdir_main_ear/*/libref/TwistCommon.jar`:`echo /var/opt/opsware/twist/servers/twist/tmp/_WL_user/_appsdir_fido_ear/*/entity/fido-entity.jar`:`echo /var/opt/opsware/twist/servers/twist/tmp/_WL_user/_appsdir_fido_ear/*/session/fido-session.jar`

# Calculate java binary
JAVA_BIN="`ls /opt/opsware/j*/bin/java | head -1`"
if ( [ \! -f "$JAVA_BIN" ]; ) then {
  echo $0: 'Unable to locate java interpreter. (Is this a SAS 6.x+ box with a twist on it?)'
  exit 1
} fi

# everything looks good, so lets fire it up.
exec "$JAVA_BIN" ExternalUserUtil "$@"

# If we get here, then exit with error.
exit 1


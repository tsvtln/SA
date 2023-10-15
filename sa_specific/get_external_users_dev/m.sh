#!/bin/sh

export CLASSPATH=/opt/opsware/twist/lib/ldapbp.jar:/opt/opsware/twist/lib/ldapssl.jar:/opt/opsware/bea/weblogic81/server/lib/weblogic.jar:/var/opt/opsware/twist/twist/stage/_appsdir_main_ear/libref/TwistCommon.jar:/var/opt/opsware/twist/twist/stage/_appsdir_fido_ear/entity/fido-entity.jar:/var/opt/opsware/twist/twist/stage/_appsdir_fido_ear/session/fido-session.jar:/opt/opsware/twist/lib/commons-logging.jar:/opt/opsware/twist/lib/opsware_common-latest.jar:/opt/opsware/twist/lib/spinclient-latest.jar:/opt/opsware/twist/lib/common-latest.jar:.

`ls /opt/opsware/j*/bin/javac | head -1` ExternalUserUtil.java && \
zip -9 ExternalUserUtil.jar ExternalUserUtil.class && \
cat ExternalUserUtil.sh ExternalUserUtil.jar > get_external_users && chmod a+x get_external_users

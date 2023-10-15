#!/bin/sh

export CLASSPATH=.:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/bea/weblogic81/server/lib/wlclient.jar:/opt/opsware/twist/lib/opsware_common-latest.jar:/opt/opsware/twist/lib/spinclient-latest.jar:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/twist/lib/twist.jar:/opt/opsware/twist/lib/common-latest.jar

`ls /opt/opsware/j*/bin/javac | head -1` TokenFactory.java && \
`ls /opt/opsware/j*/bin/javac | head -1` GetDeviceInfo.java && \
zip GetDeviceInfo.jar `ls *.class` && \
cat GetDeviceInfo.sh GetDeviceInfo.jar > GetDeviceInfo && chmod a+x GetDeviceInfo

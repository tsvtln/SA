#!/bin/sh

export CLASSPATH=.:/cust/twist/lib/client/twistclient.jar:/cust/twist/lib/twist.jar:/cust/twist/lib/common-latest.jar:/cust/twist/lib/commons-codec-1.3.jar:/cust/twist/twist/stage/_appsdir_main_ear/session/patchmgmt-session.jar:/cust/bea/weblogic81/server/lib/weblogic.jar:/cust/twist/lib/opsware_common-latest.jar:/cust/twist/lib/spinclient-latest.jar

`ls /cust/j*/bin/javac | head -1` TokenFactory.java && \
`ls /cust/j*/bin/javac | head -1` DoStartAuditComplianceJob.java && \
zip DoStartAuditComplianceJob.jar `ls *.class` && \
cat DoStartAuditComplianceJob.sh DoStartAuditComplianceJob.jar > DoStartAuditComplianceJob && chmod a+x DoStartAuditComplianceJob

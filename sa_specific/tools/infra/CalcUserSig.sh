#!/bin/sh

# Setup the class path depending on whether we are running on einstein or darwin.
if ( [ -d /opt/opsware ]; ) then {
  export CLASSPATH=.:/opt/opsware/twist/lib/commons-logging.jar:/opt/opsware/twist/lib/commons-codec-1.3.jar:/opt/opsware/twist/lib/common-latest.jar
  PYTHON_BIN=/opt/opsware/bin/python
  JAVA_BIN=/opt/opsware/j2sdk1.4.2_10/bin/java
  JAVAC_BIN=/opt/opsware/j2sdk1.4.2_10/bin/javac
} else {
  export CLASSPATH=.:/cust/twist/lib/commons-logging.jar:/cust/twist/lib/commons-codec-1.3.jar:/cust/twist/lib/common-latest.jar
  PYTHON_BIN=/lc/bin/python
  JAVA_BIN=/cust/j2sdk1.4.2_10/bin/java
  JAVAC_BIN=/cust/j2sdk1.4.2_10/bin/javac
} fi

# Insure that the java class is compiled:
if ( [ ! -f ./CalcUserSig.class ]; ) then {
  echo '"'CalcUserSig.class'"' not found: Compiling...
  ${JAVAC_BIN} CalcUserSig.java
} fi

# For each command line argument the user provided:
for sCurUserID in "$@"
do
  ${PYTHON_BIN} CalcUserSig.py $sCurUserID | ${JAVA_BIN} CalcUserSig
done
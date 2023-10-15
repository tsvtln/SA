#!/bin/sh

exec /opt/opsware/jdk1.6/bin/java -cp "/opt/opsware/jdk1.6/lib/tools.jar:$0" jpatch $0 "$@"


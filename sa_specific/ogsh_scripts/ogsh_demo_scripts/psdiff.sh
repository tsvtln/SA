#!/bin/bash
 
TEMP1=/tmp/.tmp.$1
TEMP2=/tmp/.tmp.$2
 
rosh -n $1 -l root ps -eo user,cmd | grep -v "^UID" | sort -u > $TEMP1 &
rosh -n $2 -l root ps -eo user,cmd | grep -v "^UID" | sort -u > $TEMP2 &
wait
 
diff $TEMP1 $TEMP2
rm -f $TEMP1 $TEMP2

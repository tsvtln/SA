#!/bin/sh

infofiles=`grep "mfg:               DELL" /opsw/Server/@/*/info |cut -d: -f1`

for infofile in $infofiles; do
	os=`grep "os:" $infofile | sed -e 's/os:                //'`
	svr=`dirname $infofile`
	svr=`basename $svr`
	echo "$svr: $os"
done


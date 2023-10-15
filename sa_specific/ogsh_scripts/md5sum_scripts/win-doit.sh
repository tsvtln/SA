#!/bin/bash

date=`date +%Y-%m-%e-%H:%M:%S`

if [ ! -d results ]; then
	mkdir results
fi

for i in `cat win-hosts`; do
	echo $i
	BINPATH="/opsw/Server/@/$i/files/LocalSystem/C/Program Files/Loudcloud/bin"

	if [ ! -f "$BINPATH/win-md5sum.bat" ]; then
		echo "copying win-md5sum.bat to $i"
		cp win-md5sum.bat "$BINPATH"

		if [ $? != 0 ]; then
			echo "Error occurred accessing filesystem - check Opsware Agent functionality"
			exit 2
		fi
	fi

	if [ ! -f "$BINPATH/win-md5sum.py" ]; then
		echo "copying win-md5sum.py to $i"
		cp win-md5sum.py "$BINPATH"

		if [ $? != 0 ]; then
			echo "Error occurred accessing filesystem - check Opsware Agent functionality"
			exit 2
		fi
	fi

	if [ ! -d results/$i ]; then
		mkdir results/$i
	fi

	rosh -l LocalSystem -n $i c:/Program\ Files/Loudcloud/bin/win-md5sum.bat >> results/$i/$date
done

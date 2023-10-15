#!/bin/bash
# 

if [ $# != 2 ]; then
	echo "Usage: $0 hostname-list files-list"
	exit 1
fi

if [ ! -r $1 ]; then
	echo "Sorry, hosts file not found or not readable"
	exit 1
fi

if [ ! -r $2 ]; then
	echo "Sorry, files file not found or not readable"
	exit 1
fi

date=`date +%Y-%m-%e-%H:%M:%S`

if [ ! -d results ]; then
	mkdir results
fi

for i in `cat $1`; do
	if [ ! -f /opsw/Server/@/$i/files/root/opt/OPSW/bin/md5sum.py ]; then
		echo "copying md5sum.py to $i"
		cp -p md5sum.py /opsw/Server/@/$i/files/root/opt/OPSW/bin
	fi

	if [ ! -d results/$i ]; then
		mkdir results/$i
	fi

	for j in `cat $2`; do
		rosh -n $i -l root /opt/OPSW/bin/md5sum.py $j >> results/$i/$date.$$
	done

	cat results/$i/$date.$$ | sort > results/$i/$date
	rm results/$i/$date.$$

	if [ ! -d results/$i/$date-files ]; then
		mkdir results/$i/$date-files
	fi

	if [ -f /opsw/Server/@/$i/files/root/etc/passwd ]; then
		cp /opsw/Server/@/$i/files/root/etc/passwd results/$i/$date-files
	fi

	if [ -f /opsw/Server/@/$i/files/root/etc/shadow ]; then
		cp /opsw/Server/@/$i/files/root/etc/shadow results/$i/$date-files
	fi

	if [ -f /opsw/Server/@/$i/files/root/etc/inetd.conf ]; then
		cp /opsw/Server/@/$i/files/root/etc/inetd.conf results/$i/$date-files
	fi
done


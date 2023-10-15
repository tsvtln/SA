#!/bin/bash

if [ $# != 1 ] && [ $# != 3 ]; then
	echo ""
	echo "Usage: $0 server-name master compare-to"
	echo ""
	echo "Servers with available data sets (use $0 server-name to list"
	echo "last 10 available data sets):"
	ls -1 results
	exit 1
fi

if [ $# == 1 ]; then
	if [ -d results/$1 ]; then
		SRC=`ls -tr1 results/$1 | grep -v files\$ | tail -2 | head -1`
		DST=`ls -tr1 results/$1 | grep -v files\$ | tail -1`
	else
		echo ""
		echo "Server name $1 not found in results database"
		echo ""
	fi
fi

SRCDAT=results/$1/$SRC
DSTDAT=results/$1/$DST

RESULT=`diff $SRCDAT $DSTDAT | grep ^\>`

FILENAME=`echo $RESULT | cut -d' ' -f2`

EPOCHDATE=`echo $RESULT | cut -f3 -d' '`

if [ X$EPOCHDATE != "X" ]; then
	DATE=`./ctime.py $EPOCHDATE`
	BASE=`echo $FILENAME | cut -d'\' -f2`

	if [ $BASE == "WINDOWS" ]; then
		echo "Please create a remedy ticket and place in the ESA Windows Support queue."
		echo "$1,$FILENAME,$DATE"
	else
		echo "Please create a remedy ticket and place in the ESA Unix Sustainment queue."
		echo "$1,$FILENAME,$DATE"
	fi
else
	echo "No differences found"
fi

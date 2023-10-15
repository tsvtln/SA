#!/bin/sh
# moves a moin wiki page from one place to another, preserves its attachments,
# and creates a redirect from the old page to the new one
# use at your own risk, try to take a backup before you operate on the live
# wiki

recursive="" # off by default

if [ "$1" = "-r" ]; then
	recursive=0
	shift
fi

MovePage() 
{
	oldname=$1
	newname=$2
	
	if [ ! -d pages/$oldname ]; then
		echo "Can't find pages directory for $oldname."
		exit 1
	fi
	
	if [ ! -f text/$oldname ]; then
		echo "Can't find text file for $oldname."
		exit 1
	fi
	
	if [ -d pages/$newname ]; then
		echo "Pages directory for $newname already exists."
		exit 1
	fi
	
	if [ -f text/$newname ]; then
		echo "Text file for $newname already exists."
		exit 1
	fi
	
	# copy the old files
	mv pages/$oldname pages/$newname
	cp -p text/$oldname text/$newname
	
	newname=`echo $newname | sed 's@_2f@/@g'`
	echo "#REDIRECT $newname" > text/$oldname
	
	echo "Moved $oldname to $newname."
}	

convToMoinName() 
{
	pathname=$1
	moinname=`echo $pathname | sed 's@/@_2f@g'`
	moinname=`echo $moinname | sed 's@\.@_2e@g'`
}

# main
srcname=$1
dstname=$2

lastchar=`echo $dstname | sed 's@.*\(.\)$@\1@'`
	
# if their destination ends with a "/", treat it as a directory/parent page
# and move the old page into a subpage of the newpage, preserving the original
# page name
if [ x$lastchar = x'/' ]; then
	dstname=$dstname`basename $srcname`
	#echo "Dest is a parent page, new dstname=$dstname"
fi

convToMoinName $srcname
srcmoinname=$moinname
#`echo $srcname | sed 's@/@_2f@g'`
convToMoinName $dstname
dstmoinname=$moinname
#dstmoinname=`echo $dstname | sed 's@/@_2f@g'`

#echo "MovePage $srcmoinname $dstmoinname"
	
MovePage $srcmoinname $dstmoinname

if [ "$recursive" ]; then
	for i in text/${srcmoinname}_2f*; do
		if [ ! -f $i ]; then
			# probably the wildcard didn't match anything at all
			continue
		fi
		oldmoinname=`echo $i | sed 's@^text/@@'`
		newpart=`echo $i | sed "s@^text/${srcmoinname}_2f@@"`
		#echo "   newpart = $newpart"
		newmoinname=${dstmoinname}_2f$newpart
		#echo "   MovePage $oldmoinname $newmoinname"
		MovePage $oldmoinname $newmoinname
	done
fi



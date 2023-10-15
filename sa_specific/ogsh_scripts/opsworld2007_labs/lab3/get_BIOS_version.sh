#!/bin/sh
####################################################
# Script Name - get_BIOS_version.sh
# Function - 
# Argument - None
####################################################

# Globals needed for proper execution
PATH=/opsw/bin:$PATH
ROSH_USER=LocalSystem
cwd=`pwd`
cd "`dirname $0`"
MYDIR=`pwd`
cd "$cwd"
BIOS_SCRIPT_NAME="detect_bios_version_from_wmi.vbs"
BIOS_SCRIPT_PATH="$MYDIR/$BIOS_SCRIPT_NAME"

svrname=$1

if [ $# -ne 1 -o -z "$svrname" ]; then
	echo "usage: $0 <server name>"
	echo
	exit 1
fi

##################### main ####################

# make sure the server with the name specified exists and is reachable
if [[ `cat /opsw/Server/\@/$svrname/info 2>/dev/null | grep state | sed -e "s/state:[ ]*//g"` != "OK" ]]; then
	echo "Server $svrname doesn't exist or is not reachable, exiting."
	exit 2
fi

# look in the server's info file to see if it's a Windows box
IS_WINDOWS=`cat /opsw/Server/\@/$svrname/info | grep Microsoft 2>/dev/null`
if [ "x$IS_WINDOWS" = "x" ] ;
then
	echo "Server $svrname is not Windows, skipping."
	continue	
fi 

echo
echo "=== $svrname ==="
temp_dir="/opsw/Server/@/$svrname/files/$ROSH_USER/C/"

# run VB script check BIOS version
cp "$BIOS_SCRIPT_PATH" "$temp_dir"
cmd="cscript /nologo C:\\\\$BIOS_SCRIPT_NAME"
#echo Running rosh -n "$svrname" -l $ROSH_USER $cmd
bios_ver=`rosh -n "$svrname" -l $ROSH_USER $cmd`

if [ $? -ne 0 ]; then 
	echo "Failed to get BIOS version"
	rv=1
else
	echo "BIOS Version: $bios_ver"
	#echo "Setting bios_version custom field"
	#$svrname/method/setCustomField fieldName=biosversion strValue="$bios_ver"
	rv=0
fi
echo "===========================" 

# remove the VB script that we copied to the server temporarily
rm $temp_dir/$BIOS_SCRIPT_NAME

exit $rv

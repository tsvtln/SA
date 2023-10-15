#!/bin/sh
####################################################
# Script Name - FindSpaceAvailable.sh 
# Function - Returns space available in various file structs
# Argument - None
####################################################

cwd=`pwd`
cd "`dirname $0`"
MYDIR=`pwd`
cd "$cwd"

# Globals needed for proper execution
PATH=/opsw/bin:$PATH
TTLG_CMD=/opsw/bin/rosh
TTLG_USER=root
WINDOWS_TTLG_USER=Administrator
ARG_LIST=$1
SCRIPT_NAME=SpaceAvailable
LINUX_SCRIPT_NAME="$SCRIPT_NAME.sh"
SOLARIS_SCRIPT_NAME="$SCRIPT_NAME.sh"
HPUX_SCRIPT_NAME="$SCRIPT_NAME.sh"
AIX_SCRIPT_NAME="$SCRIPT_NAME.sh"
WINDOWS_SCRIPT_NAME="$SCRIPT_NAME.bat"
# Make sure the system knows where to find the endscripts
SCRIPT_LOCATION=$MYDIR/endscripts
WINDOWS_SCRIPT_LOCATION="$SCRIPT_LOCATION/Windows"
LINUX_SCRIPT_LOCATION="$SCRIPT_LOCATION/Unix/Linux"
SOLARIS_SCRIPT_LOCATION="$SCRIPT_LOCATION/Unix/Solaris"
HPUX_SCRIPT_LOCATION="$SCRIPT_LOCATION/Unix/HP-UX"
AIX_SCRIPT_LOCATION="$SCRIPT_LOCATION/Unix/AIX"

function findServers() {
#echo $1
IFS="
"
echo $PWD | grep -e "@$"
if [ $? -eq 0 ]
then
  ls $PWD

elif [ `echo $PWD | grep -e "^/opsw/Server$" > /dev/null; echo -n $?` -eq 0 ]
then
  ls $PWD/\@
elif [ -e $PWD/info ]
then
  echo $PWD | sed -e "s/\/.*\///g"
else
  if [ -z $1 ]
  then

    for x in `ls -1F $PWD | grep \/ | sed -e "s/.*:[0-9][0-9] \(.*\)$/\1/g"`
    do
      #echo $x
      if [[ $x == "@/" ]]
      then
        ls -1 $PWD/$x
      else
        findServers $PWD/$x
      fi
    done
  else
    for x in `ls -1F $1 | grep \/ | sed -e "s/.*:[0-9][0-9] \(.*\)$/\1/g"`
    do
      #echo $x
      if [[ $x == "@/" ]]
      then
        ls -1 $1$x
      else
        findServers $1$x
      fi
    done
  fi
fi
}


VALID_LOCATION=`pwd | grep "/opsw/Server"`
if [ $? -eq 1 ]; 
then
	echo "Script calling location incorrect:Pls call from underneath /opsw/Server"
	exit 1
fi


for x in `findServers | sort | uniq |  grep -v  "\@"`
do
  if [[ `cat /opsw/Server/\@/$x/info 2>/dev/null | grep state | sed -e "s/state:[ ]*//g"` == "OK" ]]
  then
	MY_OS=`cat /opsw/Server/\@/$x/info | grep os: | sed -e "s/os:[ ]*\([^ 0-9]*\).*/\1/g"`
#	echo "Hostname:$x"
# Logic for calling the appropriate script
	IS_SOLARIS_OS=`echo $MY_OS | egrep "SunOS|Solaris"`
	IS_WINDOWS_OS=`echo $MY_OS | egrep "Microsoft|Windows"`
	IS_HPUX_OS=`echo $MY_OS | egrep "HP-UX"`
	IS_AIX_OS=`echo $MY_OS | egrep "AIX"`
	IS_LINUX_OS=`echo $MY_OS | egrep "Linux|Red Hat"`
	if [ "x$IS_LINUX_OS" != "x" ] ;
	then
$TTLG_CMD -n$x -l$TTLG_USER -s $LINUX_SCRIPT_LOCATION/$LINUX_SCRIPT_NAME 
	fi 
        if [ "x$IS_SOLARIS_OS" != "x" ] ;
        then
                $TTLG_CMD -n$x -l$TTLG_USER -s $SOLARIS_SCRIPT_LOCATION/$SOLARIS_SCRIPT_NAME 
        fi
        if [ "x$IS_HPUX_OS" != "x" ] ;
        then
                $TTLG_CMD -n$x -l$TTLG_USER -s $HPUX_SCRIPT_LOCATION/$HPUX_SCRIPT_NAME 
        fi
        if [ "x$IS_AIX_OS" != "x" ] ;
        then
                $TTLG_CMD -n$x -l$TTLG_USER -s $AIX_SCRIPT_LOCATION/$AIX_SCRIPT_NAME 
        fi
        if [ "x$IS_WINDOWS_OS" != "x" ] ;
        then
                $TTLG_CMD -n$x -l$WINDOWS_TTLG_USER -s $WINDOWS_SCRIPT_LOCATION/$WINDOWS_SCRIPT_NAME
        fi
else
	  echo "$x is marked as not reachable"
fi
echo
done

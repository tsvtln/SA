#!/bin/sh
########################################################
# Script Name - FindTopNCpu.sh
# Function - Script to print a list of n processes in CPU
# Arguments -  a number as an integer
#########################################################

# Globals needed for proper execution
cwd=`pwd`
cd "`dirname $0`"
MYDIR=`pwd`
cd "$cwd"

PATH=/opsw/bin:$PATH
TTLG_CMD=/opsw/bin/rosh
TTLG_USER=root
WINDOWS_TTLG_USER=Administrator
ARG_LIST=$1
SCRIPT_NAME=ListCpuForN
LINUX_SCRIPT_NAME="$SCRIPT_NAME.sh"
SOLARIS_SCRIPT_NAME="$SCRIPT_NAME.sh"
HPUX_SCRIPT_NAME="$SCRIPT_NAME.sh"
AIX_SCRIPT_NAME="$SCRIPT_NAME.sh"
WINDOWS_SCRIPT_NAME="$SCRIPT_NAME.bat"
# Fix script location - expect it to be local
SCRIPT_LOCATION=$MYDIR/endscripts
WINDOWS_SCRIPT_LOCATION="$SCRIPT_LOCATION/Windows"
LINUX_SCRIPT_LOCATION="$SCRIPT_LOCATION/Unix/Linux"
SOLARIS_SCRIPT_LOCATION="$SCRIPT_LOCATION/Unix/Solaris"
HPUX_SCRIPT_LOCATION="$SCRIPT_LOCATION/Unix/HP-UX"
AIX_SCRIPT_LOCATION="$SCRIPT_LOCATION/Unix/AIX"
WINDOWS_RESULTS_FILE=/tmp/$SCRIPT_NAME-results
WINDOWS_RESULTS_FILETEMP=/tmp/$SCRIPT_NAME-resultstmp

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


ARG_LIST=$1
if  [ "x$ARG_LIST" == "x" ];
then
        echo "Missing argument: Please pass the no. of processes"
        exit 1
fi
if ! expr $ARG_LIST + 0 2>/dev/null 1>/dev/null ;
then
   echo "Invalid argument - needs an integer"
   exit 1
fi
if [ $ARG_LIST -lt 0 ]  || [ $ARG_LIST -gt 100  ] ;
then
   echo "Process count  should be between 0 and 100 "
   exit 1
fi
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
	echo
	echo "Hostname:$x"
# Logic for calling the appropriate script
	IS_SOLARIS_OS=`echo $MY_OS | egrep "SunOS|Solaris"`
	IS_WINDOWS_OS=`echo $MY_OS | egrep "Microsoft|Windows"`
	IS_HPUX_OS=`echo $MY_OS | egrep "HP-UX"`
	IS_AIX_OS=`echo $MY_OS | egrep "AIX"`
	IS_LINUX_OS=`echo $MY_OS | egrep "Linux|Red Hat"`
	if [ "x$IS_LINUX_OS" != "x" ] ;
	then
$TTLG_CMD -n$x -l$TTLG_USER -s $LINUX_SCRIPT_LOCATION/$LINUX_SCRIPT_NAME $ARG_LIST
	fi 
        if [ "x$IS_SOLARIS_OS" != "x" ] ;
        then
                $TTLG_CMD -n$x -l$TTLG_USER -s $SOLARIS_SCRIPT_LOCATION/$SOLARIS_SCRIPT_NAME $ARG_LIST
        fi
        if [ "x$IS_HPUX_OS" != "x" ] ;
        then
                $TTLG_CMD -n$x -l$TTLG_USER -s $HPUX_SCRIPT_LOCATION/$HPUX_SCRIPT_NAME $ARG_LIST
        fi
        if [ "x$IS_AIX_OS" != "x" ] ;
        then
                $TTLG_CMD -n$x -l$TTLG_USER -s $AIX_SCRIPT_LOCATION/$AIX_SCRIPT_NAME $ARG_LIST
        fi
        if [ "x$IS_WINDOWS_OS" != "x" ] ;
        then
                $TTLG_CMD -n$x -l$WINDOWS_TTLG_USER -s $WINDOWS_SCRIPT_LOCATION/$WINDOWS_SCRIPT_NAME   | grep -v System | sort -r -k 3  >  $WINDOWS_RESULTS_FILETEMP
                cat $WINDOWS_RESULTS_FILETEMP  | head -$ARG_LIST > $WINDOWS_RESULTS_FILE
		startcount=1
		cat $WINDOWS_RESULTS_FILE|
		while read line
		do
        		set $line
        		echo "#$startcount:$1:$3"
        startcount=`expr $startcount "+" 1`
done

		if [ -f $WINDOWS_RESULTS_FILE ];
		then
   	   	 rm $WINDOWS_RESULTS_FILE
   	   	 rm $WINDOWS_RESULTS_FILETEMP
        	fi
        fi
else
	echo
	echo "$x is marked as not reachable"
fi
done

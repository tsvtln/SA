#!/bin/sh
####################################################
# Script Name - check_sshd_status.sh
# Function - Checks whether sshd is installed and running on Linux servers
# Argument - None
####################################################

# Globals needed for proper execution
PATH=/opsw/bin:$PATH
ROSH_USER=root

# You can assume this function does what it's supposed to for this lab,
# it's not very interesting.  Scroll down to the ### main ### section
function findServers() {
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

##################### main ####################

VALID_LOCATION=`pwd | grep "/opsw/Server"`
if [ $? -eq 1 ]; 
then
	echo "Script calling location incorrect:Pls call from underneath /opsw/Server"
	exit 1
fi

if [ -z "$1" ]; then
	svrnames=`findServers | sort | uniq |  grep -v  "\@"`
else
	svrnames=$@
fi

for svrname in $svrnames
do
  if [[ `cat /opsw/Server/\@/$svrname/info 2>/dev/null | grep state | sed -e "s/state:[ ]*//g"` == "OK" ]]
  then
	# look in the server's info file to see if it's a Linux box
	IS_LINUX=`cat /opsw/Server/\@/$svrname/info | grep Linux 2>/dev/null`
	if [ "x$IS_LINUX" = "x" ] ;
	then
		echo "Server $svrname is not Linux, skipping."
		continue	
	fi 

	echo
	echo "=== $svrname ==="
	sshd_status_cust_attr="/opsw/Server/@/$svrname/CustAttr/sshd_status"

	# check if sshd is installed (based on the presence of an init script)
	sshd_loc="/opsw/Server/@/$svrname/files/$ROSH_USER/etc/init.d/sshd"
	if [ ! -f $sshd_loc ]; then
		echo "sshd status:   NOT INSTALLED"
		echo "not installed" > $sshd_status_cust_attr
		continue
	fi 
	echo "installed" > $sshd_status_cust_attr


	# check if sshd is running
	cmd="ps -ef | grep -v grep | grep -q sshd"
	rosh -n "$svrname" -l $ROSH_USER "$cmd"

	if [ $? -ne 0 ]; then 
		echo "sshd status:   INSTALLED BUT NOT RUNNING"
	else
		echo "sshd status:   INSTALLED AND RUNNING"
	fi
	echo "===========================" 
  else
  	echo "Server $svrname is not reachable."
  fi
done

#!/bin/sh

# you should be in a server group dir when you run this

cwd=`pwd`
cd "`dirname $0`"
mydir=`pwd`
cd "$cwd"

if [ $# -ne 1 ]; then
  echo "usage: $0 <config file>"
  exit 1
fi

for server in *; do
  if [ ! -d $server ] || [ ! -f $server/info ] || [ ! -d $server/files/root ]; then
    continue
  fi
  if [ `grep -q "Not Reachable" $server/info; echo $?` -eq 0 ]; then
    continue
  fi
  echo "Working on $server"
  cd $server/files/root

  $mydir/run_audit.py "$1" "."
  cd ../../..
done
  

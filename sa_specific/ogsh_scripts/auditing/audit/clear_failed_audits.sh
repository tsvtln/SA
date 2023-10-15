#!/bin/sh

# you should be in a server group dir when you run this

cwd=`pwd`
cd "`dirname $0`"
mydir=`pwd`
cd "$cwd"

for server in *; do
  if [ ! -d $server ] || [ ! -f $server/info ]; then
    continue
  fi
  echo "Clearing any failed audits for $server"
  cd $server/files/root

  $mydir/clear_failed_audits.py 
  cd ../../..
done
  

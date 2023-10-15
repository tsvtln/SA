#!/bin/sh

if [ $# -lt 1 ]; then
  echo "Usage: $0 <script to run on remote servers>"
  echo
  echo "$0 will run the specified script as root on all servers"
  echo "who's names are subdirectories of the current directory."
  echo "Ex. cd /opsw/Server/@Group/Public/All Unix and Linux Servers; $0 /var/tmp/test.sh"
  echo
  exit 1
fi


for i in *; do
  echo "Running \"$1\" on $i."
  rosh -l root -n $i $1
  echo
done 

#!/bin/sh

for server in *; do
  echo "Working on $server"
  cd $server/files/LocalSystem/C

  # make the temp\audit directory
  mkdir -p Temp/audit 2>/dev/null
  cd temp

  # copy the audit scripts and util
  cp ~/public/gac/* .

  # run the utility
  rosh run_gac_audit.bat
  cd ../../../../..
done

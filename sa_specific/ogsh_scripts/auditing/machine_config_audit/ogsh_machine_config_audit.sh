#!/bin/sh

# you should be in a server group that contains only Windows servers when you run this
# and you should have the utils you need in ~/public/machine_config

for server in *; do
  echo "Working on $server"
  cd $server/files/LocalSystem/C

  # make the temp\audit directory
  mkdir -p Temp/audit 2>/dev/null
  cd Temp

  # copy the audit scripts and util
  cp ~/public/machine_config_audit/* .

  # run the utility
  rosh run_machine_config_audit.bat 
  cd ../../../../..
done

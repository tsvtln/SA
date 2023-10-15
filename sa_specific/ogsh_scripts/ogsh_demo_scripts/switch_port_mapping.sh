#!/bin/sh

# Demonstration of how you can present data when you have NAS/SAS integration
# Prints out a list of ports on a switch and the server that is plugged into them
# Requires 6.0.1 or later

for i in `find Port/ -type l -exec echo {} \; | sed 's/ //g' | grep -v Link.ID`; do
  i=`echo $i | sed 's/LocalAreaConnection/Local Area Connection/'`
  port=`dirname "$i"`
  port=`dirname "$port"`
  port=`basename "$port"`
  #svr=`ls -al "$i" | cut -d" " -f10`
  if [ ! -f "$i"/../../.self:n ]; then
    continue
  fi
  svr=`cat "$i"/../../.self:n`
  echo "$port -> $svr"
done


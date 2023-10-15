#!/bin/sh

# this is sync_objects.sh
# its purpose is to synchronize all objects found to be
# out of sync by 2passcheck.sh
# it depends upon a small handful of other tools:
# dep_sorted_classes.py
# obj_count.py
# table_checker.py
# table_dict.py
# mk_rechk.py
# it also writes out some temporary shell scripts
# which can be deleted when it completes

passnum=1
#check if the file is empty
test -s obj.txt
retcode=$?
while [ $retcode = 0 ] ; do
  echo `date '+%Y-%m-%d_%H:%M:%S'` `wc -l obj.txt`
  echo 'pass number:' $passnum
  /opt/opsware/bin/python mk_rechk.py obj.txt recheck.sh
  if [ $? != 0 ]; then
    echo 'run of mk_rechk' $line 'failed'
  fi
  chmod +x recheck.sh
  mv obj.txt obj.txt.`date '+%Y-%m-%d_%H:%M:%S'`
  ./recheck.sh > check.out
  sort check.out | uniq | grep -v 'UTC 200' > obj.txt
  test -s obj.txt
  retcode=$?
  passnum=`expr $passnum + 1`
  if [ $retcode = 0 ] ; then
    /opt/opsware/bin/python -u sync_objects.py obj.txt
  fi
done

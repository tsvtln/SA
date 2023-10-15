#!/bin/sh

# this is the infinite_thinganizer.
# its purpose is to put cores back in sync.
# it will run in an infinite loop until everything
# is back in sync.  you should only use this if
# you really need it, and be sure to monitor its
# progress as it goes.
# it depends upon a small handful of other tools:
# curie_classes.py
# obj_count.py
# table_checker.py
# table_dict.py
# mk_rechk.py
# sync_objects.py
# it also writes out some temporary shell scripts
# which can be deleted when it completes

PYTHONPATH=/lc/blackshadow:/cust/usr/blackshadow:/cust/usr/blackshadow/spin:/opt/opsware/pylibs:/opt/opsware:/opt/opsware/spin

/opt/opsware/bin/python curie_classes.py | sort > classes.txt
if [ $? != 0 ]; then
  echo 'run of curie_classes failed' && exit 1
fi
for line in `cat classes.txt`; do
  echo `date '+%Y-%m-%d_%H:%M:%S'` AAA $line
  objcount=`/opt/opsware/bin/python obj_count.py $line`
  if [ $? != 0 ]; then
    echo 'run of obj_count' $line 'failed' && exit 1
  fi
  if test $objcount -lt 100000 ; then
    /opt/opsware/bin/python table_checker.py -c $line --simple >> table_checker.out
    if [ $? != 0 ]; then
      echo 'run of table_checker' $line 'failed'
    fi
  else
    /opt/opsware/bin/python table_dict.py truths.txt $line >> table_dict.out
    if [ $? != 0 ]; then
      echo 'run of table_dict' $line 'failed'
    fi
  fi
  echo `date '+%Y-%m-%d_%H:%M:%S'` ZZZ $line
done
cat table_checker.out table_dict.out | sort -u > obj.txt
mv table_checker.out table_checker.out.`date '+%Y-%m-%d_%H:%M:%S'`
mv table_dict.out       table_dict.out.`date '+%Y-%m-%d_%H:%M:%S'`
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

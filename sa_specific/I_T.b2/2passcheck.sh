#!/bin/sh

# this is 2passcheck.sh
# its purpose is to check then recheck all objects in a mesh
# it checks once to get a list of candidate objects
# then it checks that candidate list to make sure they were
# not in the middle of getting updated while it checked the
# first time
# it depends upon a small handful of other tools:
# dep_sorted_classes.py
# obj_count.py
# table_checker.py
# table_dict.py
# mk_rechk.py
# it also writes out some temporary shell scripts
# which can be deleted when it completes

/opt/opsware/bin/python dep_sorted_classes.py > classes.txt
if [ $? != 0 ]; then
  echo 'run of dep_sorted_classes failed' && exit 1
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
    /opt/opsware/bin/python table_dict.py $line >> table_dict.out
    if [ $? != 0 ]; then
      echo 'run of table_dict' $line 'failed'
    fi
  fi
  echo `date '+%Y-%m-%d_%H:%M:%S'` ZZZ $line
done
cat table_checker.out table_dict.out | sort -u > obj.txt
mv table_checker.out table_checker.out.`date '+%Y-%m-%d_%H:%M:%S'`
mv table_dict.out       table_dict.out.`date '+%Y-%m-%d_%H:%M:%S'`
/opt/opsware/bin/python mk_rechk.py obj.txt recheck.sh
if [ $? != 0 ]; then
  echo 'run of mk_rechk' $line 'failed'
fi
chmod +x recheck.sh
mv obj.txt obj.txt.`date '+%Y-%m-%d_%H:%M:%S'`
./recheck.sh > check.out
sort check.out | uniq | grep -v 'UTC 200' > obj.txt

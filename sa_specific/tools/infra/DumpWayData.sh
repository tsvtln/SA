#!/bin/sh

DUMP_DIR=/tmp/`basename $0`_$$

DUMP_PS='ps -auxwwm'
DUMP_LSOF='lsof'

DUMP_STRACE_PIDS="`ps -auxwwm | grep waybot.args | grep -v grep | awk '{printf " -p "$2}'`"
DUMP_STRACE="strace -tt -f $DUMP_STRACE_PIDS"

if { [ \! "$DUMP_STRACE_PIDS" ]; } then {
  echo $0: It appears that the way is not running on this box.
  exit 1
} fi

echo Dumping way debug data to "'"$DUMP_DIR"'".

mkdir $DUMP_DIR

echo "(1) Executing '$DUMP_PS'..."
$DUMP_PS > "$DUMP_DIR/ps.txt" 2> "$DUMP_DIR/ps.txt.err"

echo "(2) Executing '$DUMP_LSOF'..."
$DUMP_LSOF > "$DUMP_DIR/lsof.txt" 2> "$DUMP_DIR/lsof.txt.err"

echo "(3) Executing '$DUMP_STRACE' in the background..."
eval $DUMP_STRACE 2> "$DUMP_DIR/strace.txt" > "$DUMP_DIR/strace.txt.out" &

sleep 1

STRACE_PID=`ps -auxww|grep -- "$DUMP_STRACE_PIDS" | grep -v grep | head -1 | awk '{printf $2}'`

echo "Waiting for 30 seconds on strace command PID '$STRACE_PID'..."

sleep 30

echo "Done, Killing strace PID '$STRACE_PID'..."
kill $STRACE_PID

echo "Captured the following amount of strace date:"
ls -l "$DUMP_DIR/strace.txt"

echo "Taring up debug directory..."
echo tar czf ${DUMP_DIR}.tgz -C /tmp `basename $DUMP_DIR`
tar czf ${DUMP_DIR}.tgz -C /tmp `basename $DUMP_DIR`



#!/bin/sh

DUMP_DIR=/tmp/`basename $0`_$$

DUMP_PS='ps auxwwm'
DUMP_LSOF='lsof'

echo Dumping twist debug data to "'"$DUMP_DIR"'".

mkdir $DUMP_DIR

echo "(1) Executing system-wide '$DUMP_PS'..."
$DUMP_PS > "$DUMP_DIR/ps.txt" 2> "$DUMP_DIR/ps.txt.err"

echo "(2) Executing system-wide '$DUMP_LSOF'..."
$DUMP_LSOF > "$DUMP_DIR/lsof.txt" 2> "$DUMP_DIR/lsof.txt.err"

DUMP_STRACE_PIDS="`ps auxwwm | grep com.opsware.twist.WeblogicWrapper |grep -v grep | awk '{printf " -p "$2}'`"
KILL_CONT_PIDS="`ps auxwwm | grep com.opsware.twist.WeblogicWrapper |grep -v grep | awk '{printf " "$2}'`"
DUMP_STRACE="strace -tt -f $DUMP_STRACE_PIDS"

echo "(3) Collecting twist and spin logs..."
cp -R /var/log/opsware/twist "$DUMP_DIR/twist_logs"
cp -R /var/log/opsware/spin "$DUMP_DIR/spin_logs"

echo "(4) Executing '$DUMP_STRACE' in the background..."
eval $DUMP_STRACE 2> "$DUMP_DIR/strace.txt" > "$DUMP_DIR/strace.txt.out" &

sleep 1

STRACE_PID=`ps auxww|grep -- "$DUMP_STRACE_PIDS" | grep -v grep | head -1 | awk '{printf $2}'`

echo "Waiting for 30 seconds on strace command PID '$STRACE_PID'..."

sleep 30

echo "Done, Killing strace PID '$STRACE_PID'..."
kill $STRACE_PID

echo "Captured the following amount of strace date:"
ls -l "$DUMP_DIR/strace.txt"

echo "Sending unpause signal to twist... (In case strace didn't do it.)"
kill -CONT $KILL_CONT_PIDS

echo "Taring up debug directory..."
echo tar cjf ${DUMP_DIR}.tbz -C /tmp `basename $DUMP_DIR`
tar cjf ${DUMP_DIR}.tbz -C /tmp `basename $DUMP_DIR`



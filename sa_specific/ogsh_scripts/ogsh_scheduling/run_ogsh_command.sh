#!/bin/sh

mydir=`dirname $0`

/opt/opsware/bin/python $mydir/run_ogsh_command.py "$@"

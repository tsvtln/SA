#!/bin/sh

# this is the infinite_thinganizer.
# its purpose is to put cores back in sync.
# it will run in an infinite loop until everything
# is back in sync.  you should only use this if
# you really need it, and be sure to monitor its
# progress as it goes.
# it depends upon a small handful of other tools:
# 2passcheck.sh
# sync_objects.sh
# it also writes out some temporary shell scripts
# which can be deleted when it completes

./2passcheck.sh
./sync_objects.sh

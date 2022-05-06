#!/usr/bin/bash
# run the menu system at startup
pid_file="process.pid"

# this doesn't work! you should CD here before invoking.
# cd /home/pi/proj/PiLCDmenu/

python3 ./sr18_changer.py &

# this puts the process ID into a file
echo kill -SIGUSR1 $! > $pid_file

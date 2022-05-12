#!/usr/bin/bash
# run the menu system at startup

# saving this to /run seems problematic, so don't.
pid_file="sr18changer.pid"


# GRRR. How to do this other than hardcoded? It's not clear.
#
cd /home/pi/proj/piAlesisSR/

source ./setup.sh
python3 ./sr18_changer.py &

# this puts the process ID into a file
# echo kill -SIGUSR1 $! > $pid_file
echo $! > $pid_file

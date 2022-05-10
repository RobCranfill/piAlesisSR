#!/usr/bin/bash
# run the menu system at startup

# saving this to /run seems problematic, so don't.
pid_file="sr18changer.pid"


# We need to cd to 'here' so the data file can be found,
# but I can't figure out how to do that in a smart way.
# So make sure *you* set the current directory appropropriately.
#
# cd /home/pi/proj/whatIsThisDirectory?/

source ./setup.sh
python3 ./sr18_changer.py &

# this puts the process ID into a file
# echo kill -SIGUSR1 $! > $pid_file
echo $! > $pid_file

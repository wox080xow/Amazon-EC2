#!/bin/bash

# for Ubuntu 20.04
#dashPID=$( lsof -nPi | grep 805 | cut -d' ' -f 2 )
#kill -9 $dashPID

# for Mac OS X
dashPID=$(lsof -nPi | grep 805 | sed "s/    / /g" | cut -d' ' -f2)
kill $dashPID
echo $dashPID
echo 'All Dash Apps stoped.'

#!/bin/bash

dashPID=$( lsof -nPi | grep 805 | cut -d' ' -f 2 )
kill -9 $dashPID

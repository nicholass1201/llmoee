#!/bin/bash

# Set environment
. set_env.sh

if ps ax | grep -v grep | grep $PROC_NAME_OEE_SUMMARY > /dev/null
then
    echo "$PROC_NAME_OEE_SUMMARY service running. kill all"
else
    nohup python "$APP_PATH_OEE_SUMMARY/$PROC_NAME_OEE_SUMMARY" >> oeeSummary.out &
    echo "start oee_Summary service"
fi
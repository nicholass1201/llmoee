#!/bin/bash

# Set environment
. set_env.sh

if ps ax | grep -v grep | grep $PROC_NAME_OEE_CB > /dev/null
then
    echo "$PROC_NAME_OEE_CB service running. kill all"
else
    nohup python "$APP_PATH_OEE_SUMMARY/$PROC_NAME_OEE_CB" >> oeeSummary.out &
    echo "start oeeSummary service"
fi
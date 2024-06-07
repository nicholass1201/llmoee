#!/bin/bash

# Set environment
. set_env.sh

if ps ax | grep -v grep | grep $PROC_NAME_OEE_SUMMARY > /dev/null
then
    echo "$PROC_NAME_OEE_SUMMARY service running. kill all"
else
    nohup python "$APP_PATH_wcSummary/$PROC_NAME_OEE_SUMMARY" >> ac_wcSummary.out &
    echo "start wc_wcSummary service"
fi

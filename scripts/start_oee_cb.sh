#!/bin/bash

# Set environment
. set_env.sh

if ps ax | grep -v grep | grep $PROC_NAME_OEE_CB > /dev/null
then
    echo "$PROC_NAME_OEE_CB service running. kill all"
else
    nohup python "$APP_PATH_OEE_CB/$PROC_NAME_OEE_CB" >> oeeCb.out &
    echo "start oeeCb service"
fi
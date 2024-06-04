#!/bin/bash

# Set environment
. set_env.sh

if ps ax | grep -v grep | grep $PROC_NAME_OEE_CB_MGR > /dev/null
then
    echo "$PROC_NAME_OEE_CB_MGR service running. kill all"
else
    nohup python "$APP_PATH_OEE_CB_MGR/$PROC_NAME_OEE_CB_MGR" >> oeeCbMgr.out &
    echo "start oeeChatBot manager--->$PROC_NAME_OEE_CB_MGR"
fi
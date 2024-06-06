#!/bin/bash

# Set environment
. set_env.sh

if ps ax | grep -v grep | grep $PROC_NAME_OEE_SYS_ADMIN > /dev/null
then
    echo "$PROC_NAME_OEE_SYS_ADMIN service running. kill all"
else
    nohup python "$APP_PATH_OEE_SYS_ADMIN/$PROC_NAME_OEE_SYS_ADMIN" >> oeeSysAdmin.out &
    echo "start oeeSysAdmin service"
fi
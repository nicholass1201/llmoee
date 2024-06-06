#!/bin/bash

. profile.sh

# Lookup Process PID
oee_sys_admin_pid=$(ps ax | grep -v grep | grep ${PROC_NAME_OEE_SYS_ADMIN} | awk '{print $1}' | head -1)
echo "sysWcAdmin_pid [$oee_sys_admin_pid]"

kill_process()
{
    echo "kill $1"
    if pids=$(pgrep -P "$1");
    then
        for pid in $pids;
        do kill_process "$pid";
        done;
    fi;
    kill "$1";
};

if [ -n "$oee_sys_admin_pid" ]
then
    kill_process "$oee_sys_admin_pid"
    echo "stop $PROC_NAME_OEE_SYS_ADMIN [$oee_sys_admin_pid] service"
else
    echo "$PROC_NAME_OEE_SYS_ADMIN is not running"
fi
 
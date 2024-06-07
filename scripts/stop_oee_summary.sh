#!/bin/bash

# Set environment
. set_env.sh

# Lookup Summary Process PID 
oee_summary_pid=$(ps ax | grep -v grep | grep ${PROC_NAME_OEE_SUMMARY} | awk '{print $1}' | head -1)
echo "summary_pid [$oee_summary_pid]"

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

if [ -n "$oee_summary_pid" ]
then
    kill_process "$oee_summary_pid"
    echo "stop $PROC_NAME_OEE_SUMMARY [$oee_summary_pid] service"
else
    echo "$PROC_NAME_OEE_SUMMARY is not running"
fi
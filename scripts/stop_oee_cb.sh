#!/bin/bash

. profile.sh

echo "PROC_NAME_OEE_CB name: ---> $PROC_NAME_OEE_CB"

# 학습 Process PID 조회
oee_chat_pid=$(ps ax | grep -v grep | grep ${PROC_NAME_OEE_CB} | awk '{print $1}' | head -1)
echo "oee_chat_pid [$oee_chat_pid]"

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

if [ -n "$oee_chat_pid" ]
then
    kill_process "$oee_chat_pid"
    echo "stop $PROC_NAME_OEE_CB [$oee_chat_pid] service"
else
    echo "$PROC_NAME_OEE_CB is not running"
fi
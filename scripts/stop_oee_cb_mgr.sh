#!/bin/bash

. profile.sh

echo "PROC_NAME_OEE_CB_MGR name: ---> $PROC_NAME_OEE_CB_MGR"

# PID 조회
oeechatbot_mgr_pid=$(ps ax | grep -v grep | grep ${PROC_NAME_OEE_CB_MGR} | awk '{print $1}' | head -1)
echo "oeechatbot_mgr_pid [$oeechatbot_mgr_pid]"

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

if [ -n "$oeechatbot_mgr_pid" ]
then
    kill_process "$oeechatbot_mgr_pid"
    echo "stop $PROC_NAME_OEE_CB_MGR [$oeechatbot_mgr_pid] service"
else
    echo "$PROC_NAME_OEE_CB_MGR is not running"
fi
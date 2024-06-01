#!/bin/bash

. profile.sh

# 환경설정
echo "setenv_$WC_ENV.sh"
. setenv_"$WC_ENV".sh

echo "PROC_NAME_mngChatBot name: --->$PROC_NAME_mngChatBot"

# PID 조회
mngchatbot_pid=$(ps ax | grep -v grep | grep ${PROC_NAME_mngChatBot} | awk '{print $1}' | head -1)
echo "mngchatbot_pid [$mngchatbot_pid]"

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

if [ -n "$mngchatbot_pid" ]
then
    kill_process "$mngchatbot_pid"
    echo "stop $PROC_NAME_mngchatbot [$mngchatbot_pid] service"
else
    echo "$PROC_NAME_mngchatbot is not running"
fi

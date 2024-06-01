#!/bin/bash

. profile.sh

# 환경설정
echo "setenv_$WC_ENV.sh"
. setenv_"$WC_ENV".sh

if ps ax | grep -v grep | grep $PROC_NAME_wcChat > /dev/null
then
    echo "$APP_PATH_wcChat service running. kill all"
else
    nohup python "$APP_PATH_wcChat/$PROC_NAME_wcChat" >> wc_wcChat.out &
    echo "start wc_acChat service"
fi
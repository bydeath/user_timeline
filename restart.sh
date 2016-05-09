#!/usr/bin/env bash
# ===================================================================
#     FileName: restart.sh
#       Author: brucvv
#        Email: brucvv@gmail.com
#   CreateTime: 2016-05-09 17:42
# ===================================================================
PID=`netstat -lntp|grep 0.0.0.0:4000|sed 's/^.\+\([0-9]\{4,5\}\)\/ruby2.1/\1/'`
kill  -9 $PID
rm assets/*.jpg
rm _posts/*
nohup python3 twitter-to-md.py > twitter-to-md.log 2>&1 &

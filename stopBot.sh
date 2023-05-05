#!/bin/bash

PID=$(ps aux | grep '[b]ot_main.py' | awk '{print $2}')
if [[ -z $PID ]]; then
    echo "Bot is not running"
else
    kill $PID
    echo "Bot stopped"
fi

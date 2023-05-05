#!/bin/bash

if command -v python3 &>/dev/null; then
    nohup python3 bot_main.py &
elif command -v python &>/dev/null; then
    nohup python bot_main.py &
else
    echo "Python not found"
    exit 1
fi

#!/bin/bash

python RPi/wserver.py &
process1_pid=$!

python RPi/receiver.py &
process2_pid=$!

echo "Running Hiking Tour Assistant Raspberry PI support platform (wserver.py PID: $process1_pid) (receiver.py PID: $process2_pid). Press Ctrl+C to stop."

# Terminate processes
trap "kill $process1_pid $process2_pid; exit" SIGINT

wait


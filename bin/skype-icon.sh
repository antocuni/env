#!/bin/bash

function sleep_until() {
    echo "waiting for $1..."
    while ! test -f "$1"; do
        sleep 2
    done
}

while true
do
    sleep_until /tmp/resumed
    echo 'deleting /tmp/resumed'
    rm /tmp/resumed
    sleep 10
    killall unity-panel-service
    /usr/lib/x86_64-linux-gnu/unity/unity-panel-service &
done


#!/bin/bash

# Download images from:
# https://www.raspberrypi.com/software/operating-systems/

USAGE=$(cat <<EOF
Usage:
    ./flash.sh
    ./flash.sh IMAGE DEVICE

Example:
    ./flash.sh raspios.img /dev/sdb
EOF
)

if [ "$#" -eq 0 ]; then
    lsblk -I 8 -o RM,name,size,label,vendor,model,mountpoint,type,tran,path
    echo
    echo "To flash the image:"
    echo "./flash.sh IMAGE.img /dev/sdX"
    exit
elif [ "$#" -eq 2 ]; then
    IMAGE=$1
    DEV=$2
    ls -lh $IMAGE
    CMD="dd if=$IMAGE of=$DEV bs=4M status=progress"
    echo $CMD
    echo "Waiting 5 seconds before starting..."
    sleep 5 || exit
    $CMD
    sync
    exit
else
    echo "$USAGE"
    exit 1
fi

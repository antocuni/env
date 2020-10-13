#!/bin/bash

# my usb keyboard
USB_KEYBOARD_ID="04f2:0111"

if ! lsusb -d $USB_KEYBOARD_ID
then
    echo "only laptop"
    ~/.screenlayout/laptop.sh
else
    echo "docking station"
    ~/.screenlayout/docking.sh
fi

#!/bin/bash

# my usb keyboard
DOCKING_USB_KEYBOARD_ID="04f2:0111"
BETAHAUS_USB_KEYBOARD_ID="046d:c31c"

if lsusb -d $DOCKING_USB_KEYBOARD_ID
then
    echo "docking station"
    ~/.screenlayout/docking.sh
elif lsusb -d $BETAHAUS_USB_KEYBOARD_ID
then
    echo "betahaus"
    ~/.screenlayout/betahaus.sh
else
    echo "only laptop"
    ~/.screenlayout/laptop.sh
fi

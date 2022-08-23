#!/bin/bash

# my usb keyboard
MELE_USB_KEYBOARD_ID="04f2:0111"
BETAHAUS_USB_KEYBOARD_ID="046d:c31c"

if lsusb -d $MELE_USB_KEYBOARD_ID
then
    echo "mele"
    #~/.screenlayout/docking.sh
    ~/.screenlayout/mele.sh
elif lsusb -d $BETAHAUS_USB_KEYBOARD_ID
then
    echo "betahaus"
    ~/.screenlayout/betahaus.sh
else
    echo "only laptop"
    ~/.screenlayout/laptop.sh
fi

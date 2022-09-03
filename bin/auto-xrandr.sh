#!/bin/bash

# my usb keyboard
MELE_USB_KEYBOARD_ID="04f2:0111"
BETAHAUS_USB_KEYBOARD_ID="046d:c31c"  # logitech wired
BERLIN_USB_KEYBOARD_ID="046d:c52b"    # logitech wireless

if lsusb -d $MELE_USB_KEYBOARD_ID
then
    echo "mele"
    #~/.screenlayout/docking.sh
    ~/.screenlayout/mele.sh
elif lsusb -d $BERLIN_USB_KEYBOARD_ID
then
    echo "betahaus"
    ~/.screenlayout/betahaus.sh
else
    echo "only laptop"
    ~/.screenlayout/laptop.sh
fi

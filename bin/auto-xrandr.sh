#!/bin/bash

function has_external_screen() {
    xrandr | grep -v eDP-1 | grep " connected"
}

# my usb keyboards

LOGITECH_SILENT_TOUCH="046d:c534"

MELE_USB_KEYBOARD_ID="04f2:0111"
BETAHAUS_USB_KEYBOARD_ID="046d:c31c"  # logitech wired
BERLIN_USB_KEYBOARD_ID="046d:c52b"    # logitech wireless

MELE_USB_KEYBOARD_ID="$BERLIN_USB_KEYBOARD_ID"

if ! has_external_screen
then
    echo "no external screen, laptop"
    echo "laptop" | tee /tmp/antocuni-screen-config
    ~/.screenlayout/laptop.sh
elif lsusb -d $MELE_USB_KEYBOARD_ID
then
    echo "mele" | tee /tmp/antocuni-screen-config
    ~/.screenlayout/mele.sh
elif lsusb -d $LOGITECH_SILENT_TOUCH
then
     echo "valtournenche" | tee /tmp/antocuni-screen-config
     ~/.screenlayout/valtournenche.sh
else
    echo "laptop" | tee /tmp/antocuni-screen-config
    ~/.screenlayout/laptop.sh
fi

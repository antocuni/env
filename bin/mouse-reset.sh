#!/bin/bash

#sudo modprobe -r psmouse && sleep 2 && sudo modprobe psmouse

# NOTE: you can also pass numerical ids instead of the full name
# xinput test "Logitech USB Optical Mouse"
# xinput disable 'Logitech USB Optical Mouse'
# xinput enable 'Logitech USB Optical Mouse'



xinput disable "TPPS/2 Elan TrackPoint"
xinput disable "Synaptics TM3288-011"
xinput enable "TPPS/2 Elan TrackPoint"
xinput enable "Synaptics TM3288-011"

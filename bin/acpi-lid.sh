#!/bin/bash

# we need to put something in /etc/acpi/events:

## $ cat /etc/acpi/events/antocuni-lid
## # run a script on lid open/close events
## event=button/lid
## action=/home/antocuni/bin/acpi-lid.sh "%e"

echo "$@" >> /tmp/acpi-lid.log

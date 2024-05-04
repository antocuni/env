#!/bin/bash

SSID="Spreegold Guest"

nmcli device wifi # shows available connections
nmcli device wifi connect "$SSID"

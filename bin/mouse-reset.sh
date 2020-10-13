#!/bin/bash

sudo modprobe -r psmouse && sleep 2 && sudo modprobe psmouse

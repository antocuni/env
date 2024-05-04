#!/usr/bin/python3

# https://www.makeuseof.com/wake-your-linux-pc-from-suspend-using-usb-devices/

from subprocess import getoutput
from pathlib import Path

def enable_device(ID):
    fname = getoutput(f"grep {ID} /sys/bus/usb/devices/*/idProduct")
    dirname = Path(fname).parent
    wakeup = dirname.joinpath('power', 'wakeup')
    wakeup.write_text('enabled')
    print(f'cat {wakeup}')
    print(wakeup.read_text())

def main():
    # to find the ID, use lsusb
    enable_device("c52b") # ID 046d:c52b Logitech, Inc. Unifying Receiver


if __name__ == '__main__':
    main()

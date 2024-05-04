#!/usr/bin/python3

"""
If the kde panel disappears:
https://askubuntu.com/a/1093126

~/.config/plasma-org.kde.plasma.desktop-appletsrc

[Containments][1]
activityId=
formfactor=2
immutability=1
lastScreen=1                   # <<<< set lastScreen=0
location=4
plugin=org.kde.panel           # <<<< grep for this
wallpaperplugin=org.kde.image
"""

import sys
import os
import pyrandr

def find_screens():
    screens = pyrandr.connected_screens()
    if len(screens) == 1:
        return screens[0], None
    else:
        return screens[:2]

# =======

def only_laptop():
    screens = pyrandr.connected_screens()
    cmd = ['xrandr']
    cmd.append(f'--output {screens[0].name} --auto')
    for s in screens[1:]:
        cmd.append(f'--output {s.name} --off')

    cmd = ' '.join(cmd)
    print(cmd)
    os.system(cmd)
    write_screen_config("laptop")

def only_ext():
    laptop, ext = find_screens()
    if ext is None:
        return only_laptop()

    cmd = (f'xrandr ' +
           f'--output {laptop.name} --off ' +
           f'--output {ext.name} --mode 3840x2160')

    print(cmd)
    os.system(cmd)
    write_screen_config("valtournenche")

def both():
    laptop, ext = find_screens()
    if ext is None:
        return only_laptop()

    cmd = (f'xrandr ' +
           f'--output {ext.name} --mode 3840x2160 --primary '
           f'--output {laptop.name} --auto --right-of {ext.name}')

    print(cmd)
    os.system(cmd)
    write_screen_config("mele")

# ======

def write_screen_config(name):
    with open("/tmp/antocuni-screen-config", "w") as f:
        print(name, file=f)
    print(f"screen config: {name}")


def main():
    if len(sys.argv) > 1:
        what = sys.argv[1]
    else:
        what = 'ext'

    if what == 'laptop':
        only_laptop()
    elif what == 'ext':
        only_ext()
    elif what == 'both':
        both()
    else:
        print('Usage: auto-xrandr.py [laptop|ext|both]')


if __name__ == '__main__':
    main()

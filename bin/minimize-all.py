#!/usr/bin/python

import os
import wmctrl

def main():
    cmd = []
    for w in wmctrl.Window.list():
        cmd.append('windowminimize %s' % w.id)

    cmd = ' '.join(cmd)
    os.system('xdotool %s' % cmd)
    

if __name__ == '__main__':
    main()

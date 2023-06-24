#!/usr/bin/python2

import sys
import os
import wmctrl

def main():
    if len(sys.argv) != 2:
        print('Usage: minimize-all.py [all|chrome]')
        return
    what = sys.argv[1]
    if what == 'chrome':
        windows = wmctrl.Window.by_class('google-chrome.Google-chrome')
    elif what == 'all':
        windows = wmctrl.Window.list()
    else:
        assert False, what

    cmd = []
    for w in windows:
        cmd.append('windowminimize %s' % w.id)

    cmd = ' '.join(cmd)
    os.system('xdotool %s' % cmd)


if __name__ == '__main__':
    main()

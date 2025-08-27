#!/usr/bin/python

import sys
import os
import time
import super as super_py

def main():
    cmdline = ' '.join(sys.argv[1:])

    # XXX ideally I would like to switch to the proper tab
    super_py.main(['super.py', 'term']) # activate the terminal
    time.sleep(0.1)
    os.system('xdotool key ctrl+c')
    os.system('xdotool type --delay 1 "%s"' % cmdline)
    os.system('xdotool key Return')


if __name__ == '__main__':
    main()

#!/usr/bin/python2

from __future__ import print_function

import os
import time
import datetime

def log(*args):
    dt = datetime.datetime.now()
    dt = dt.strftime('%b %d %H:%M:%S')
    print(dt, *args)


def main():
    # clear znc buffers
    os.system("hexchat -e -c 'znc ClearAllBuffers'")
    os.system('sudo enable-resume-from-usb.py')

    # try at most N times
    for i in range(1):
        a = time.time()
        print()
        log('invoking systemctl suspend, try number', i+1)
        os.system('systemctl suspend')
        time.sleep(10) # give the system enough time to actually suspend
        b = time.time()
        elapsed = b-a
        log('Woken up! Elapsed: %d seconds' % elapsed)
        if elapsed < 90:
            log('Wake up too fast, try to suspend again')
        else:
            log('break')
            break
    print()


if __name__ == '__main__':
    main()

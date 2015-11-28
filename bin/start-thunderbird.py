#!/usr/bin/env python

import os
import time
import wmctrl

def main():
    os.system('google-chrome --app=http://gmail.com &')
    os.system('google-chrome --app=http://web.whatsapp.com')

    ## os.system('LC_ALL=en_IE.utf8 thunderbird &')

    ## while True:
    ##     windows = wmctrl.Window.by_name_endswith('Thunderbird')
    ##     if not windows:
    ##         time.sleep(0.5)
    ##         continue
    ##     for win in windows:
    ##         win.set_geometry(os.environ['THUNDERBIRD_GEOMETRY'])
    ##     break

if __name__ == '__main__':
    main()

#!/usr/bin/env python
import sys
import os
#open('/tmp/foo', 'a').write(str(sys.argv) + '\n')
import wmctrl

if len(sys.argv) == 2:
    arg = sys.argv[1]
else:
    print 'Usage: show.py [term|emacs]'
    sys.exit(1)

wlist = []
if arg == 'term':
    #wlist = wmctrl.Window.by_role("autoterm")
    os.system('wmctrl -x -a gnome-terminal')
elif arg == 'emacs':
    os.system('wmctrl -x -a emacs')
    ## wlist = wmctrl.Window.by_class('emacs.Emacs24')
    ## wlist += wmctrl.Window.by_class('emacs24.Emacs24')
elif arg == 'xchat':
    wlist = wmctrl.Window.by_class('xchat.Xchat')
    wlist.sort(key=lambda w: w.wm_name)
elif arg == 'zeal':
    # start zeal if it's not already
    wlist = wmctrl.Window.by_class('zeal.Zeal')
    if not wlist:
        os.system('zeal &')


if len(wlist) == 0:
    print 'No windows found'
elif len(wlist) == 1:
    wlist[0].activate()
else:
    current = wmctrl.Window.get_active()
    if current in wlist:
        i = wlist.index(current)
        i = (i+1) % len(wlist)
        wlist[i].activate()
    else:
        wlist[0].activate()


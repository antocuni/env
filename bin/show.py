#!/usr/bin/env python
import sys
import wmctrl

if len(sys.argv) == 2:
    arg = sys.argv[1]
else:
    print 'Usage: show.py [term|emacs]'
    sys.exit(1)

wlist = []
if arg == 'term':
    wlist = wmctrl.Window.by_role("autoterm")
elif arg == 'emacs':
    wlist = wmctrl.Window.by_class('emacs.Emacs24')

if wlist:
    wlist[0].activate()

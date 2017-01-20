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

def show_emacs_and_term(arg):
    emacs = wmctrl.Window.by_class('emacs.Emacs24')
    if emacs:
        emacs = emacs[0]
    #
    term = wmctrl.Window.by_role("autoterm")
    if term:
        term = term[0]
    #
    H = 2160
    if arg == 'emacs':
        emacs.resize_and_move(y=0, h=1680)
        #term.resize_and_move(y=1680, h=H-1680)
        return emacs
    else:
        term.resize_and_move(y=480, h=H-480)
        #emacs.resize_and_move(y=0, h=480)
        return term


wlist = []
if arg == 'term':
    ## wlist = wmctrl.Window.by_role("autoterm")
    os.system('wmctrl -x -a gnome-terminal')
elif arg == 'emacs':
    os.system('wmctrl -x -a emacs')
    sys.exit(0)
    ## wlist = wmctrl.Window.by_class('emacs.Emacs24')
    ## wlist += wmctrl.Window.by_class('emacs24.Emacs24')
## if arg in ('term', 'emacs'):
##     wlist = [show_emacs_and_term(arg)]
elif arg == 'xchat':
    wlist = wmctrl.Window.by_class('hexchat.Hexchat')
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


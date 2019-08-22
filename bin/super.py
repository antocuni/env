#!/usr/bin/python

import sys
import os
import wmctrl
WLIST = wmctrl.Window.list()

def show(cls, i):
    """
    Activate the i-th window of the given class.

    If there are less windows than i, activate the first.

    The logic is to prefer windows which are on the active desktop first. If
    there is NO window of that class on the active desktop, then consider also
    the windows on other desktops
    """
    desktop = wmctrl.Desktop.get_active()
    # try to find the windows on the current desktop
    wlist = [w for w in WLIST if w.wm_class == cls and w.desktop == desktop.num]
    if not wlist:
        # try to find the windows on all desktops
        wlist = [w for w in WLIST if w.wm_class == cls]
    if not wlist:
        # no windows found, give up
        print 'No windows found: %s' % cls
        return
    #
    if i == 'cycle':
        cycle(wlist)
        return
    if i >= len(wlist):
        # not enough windows, fall back to the first
        i = 0
    wlist[i].activate()

def cycle(wlist):
    # cycle through the list of windows
    current = wmctrl.Window.get_active()
    if current in wlist:
        i = wlist.index(current)
        i = (i+1) % len(wlist)
        wlist[i].activate()
    else:
        wlist[0].activate()


def main():
    chrome = 'google-chrome.Google-chrome'
    arg = sys.argv[1]

    if arg == 'emacs':   show('emacs.Emacs', 0)
    elif arg == 'term':  show('gnome-terminal-server.Gnome-terminal', 0)
    elif arg == '1':     show(chrome, 0)
    elif arg == '2':     show(chrome, 1)
    elif arg == '3':     show(chrome, 'cycle')
    elif arg == 'q':     show('web.whatsapp.com.Google-chrome', 0)
    elif arg == 'w':     show('Telegram.TelegramDesktop', 0)
    elif arg == 'e':     show('mail.google.com.Google-chrome', 0)
    elif arg == 'a':     show('mattermost.Mattermost', 0)
    elif arg == 's':     show('hexchat.Hexchat', 0)
    elif arg == 'F2':    os.system('reposition-windows.py')
    else:
        print 'Unknown arg:', arg



if __name__ == '__main__':
    main()

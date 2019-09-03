#!/usr/bin/python

import sys
import os
import wmctrl

CHROME = 'google-chrome.Google-chrome'
MATTERMOST = 'mattermost.smithersbet.com.Google-chrome' # chrome webapp
#MATTERMOST = 'mattermost.Mattermost' # native app

WLIST = wmctrl.Window.list()

def show(cls, i, no_switch, spawn=None):
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
    if not wlist and not no_switch:
        # try to find the windows on all desktops
        wlist = [w for w in WLIST if w.wm_class == cls]
    if not wlist:
        if spawn:
            return os.system(spawn)
        # no windows found, give up
        print 'No windows found: %s' % cls
        return 1
    #
    if i == 'cycle':
        return cycle(wlist)
    if i >= len(wlist):
        # not enough windows, fall back to the first
        i = 0
    wlist[i].activate()
    return 0

def cycle(wlist):
    # cycle through the list of windows
    current = wmctrl.Window.get_active()
    if current in wlist:
        i = wlist.index(current)
        i = (i+1) % len(wlist)
        wlist[i].activate()
    else:
        wlist[0].activate()
    return 0

def notify(summary, body):
    os.system('notify-send "%s" "%s"' % (summary, body))

def take_screenshot():
    ret = os.system('import /tmp/screenshot.png')
    if ret != 0:
        notify('Screenshot failed', 'Cannot run "import"')
        return ret
    ret = os.system('xclip -selection clipboard -t image/png -i /tmp/screenshot.png')
    if ret != 0:
        notify('Screenshot failed', 'Cannot run "xclip"')
        return ret
    return 0

def main():
    arg = sys.argv[1]
    no_switch = '--no-switch' in sys.argv

    if   arg == 'emacs': return show('emacs.Emacs', 0, no_switch)
    elif arg == 'term':  return show('gnome-terminal-server.Gnome-terminal', 0, no_switch)
    elif arg == '1':     return show(CHROME, 0, no_switch=True, spawn='/home/antocuni/env/apps/my-google-chrome.desktop')
    elif arg == '2':     return show(CHROME, 1, no_switch)
    elif arg == '3':     return show(CHROME, 'cycle', no_switch)
    elif arg == 'q':     return show('web.whatsapp.com.Google-chrome', 0, no_switch)
    elif arg == 'w':     return show('Telegram.TelegramDesktop', 0, no_switch)
    elif arg == 'e':     return show('mail.google.com.Google-chrome', 0, no_switch)
    elif arg == 'a':     return show(MATTERMOST, 0, no_switch)
    elif arg == 's':     return show('hexchat.Hexchat', 0, no_switch)
    elif arg == 'prtscrn': return take_screenshot()
    elif arg == 'F2':    return os.system('reposition-windows.py')
    elif arg == 'F3':    return os.system('kbd')
    else:
        print 'Unknown arg:', arg



if __name__ == '__main__':
    sys.exit(main())

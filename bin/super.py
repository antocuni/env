#!/usr/bin/python

"""
ZEAL user contributed docsets:
https://zealusercontributions.vercel.app/
"""

import sys
import os
import wmctrl

CHROME = 'google-chrome.Google-chrome'
MATTERMOST = 'mattermost.smithersbet.com.Google-chrome' # chrome webapp
#MATTERMOST = 'mattermost.Mattermost' # native app
TELEGRAM = 'Telegram.TelegramDesktop'
#TELEGRAM = 'crx_hadgilakbfohcfcgfbioeeehgpkopaga.Google-chrome' # chrome webapp

WLIST = wmctrl.Window.list()

def show(wm_class, i=0, spawn=None):
    """
    Activate the i-th window of the given class.
    If there are less windows than i, activate the first.

    The logic is to prefer:
      1. sticky windows first
      2. windows which are on the active desktop

    """
    # find the windows visible on the current desktop, sticky windows first
    desktop = wmctrl.Desktop.get_active()
    wlist = [w for w in WLIST if w.wm_class == wm_class and w.desktop in (-1, desktop.num)]
    wlist.sort(key=lambda w: w.desktop)
    #
    if not wlist:
        # no windows found
        if spawn:
            return os.system(spawn)
        print 'No windows found: %s' % wm_class
        return 1
    #
    if i == 'cycle':
        return cycle(wlist)
    if i >= len(wlist):
        # not enough windows, fall back to the first
        i = 0
    wlist[i].activate()
    return 0

def steal_and_show(wm_class, spawn=None, on_already_active=None):
    """
    Steal a window from other desktops, and show it.

    It assumes that there is only a window of the given class.

    on_already_active determines what to do if the window is already active:
      - 'move_to_0': move it to desktop 0
      - 'killall': runs 'killall %s' % spawn
    """
    assert on_already_active in (None, 'move_to_0', 'killall')
    # check whether the window exists and spawn if not
    wlist = ([w for w in WLIST if w.wm_class == wm_class])
    if not wlist:
        if spawn:
            return os.system(spawn)
        return 1
    #
    # check whether the window is already active
    win = wlist[0]
    current = wmctrl.Window.get_active()
    if win.id == current.id:
        if on_already_active == 'move_to_0':
            win.move_to_destktop(0)
            return 0
        elif on_already_active == 'killall':
            return os.system('killall %s' % spawn)
    #
    # window found: move it to the current desktop (if necessary) and activate
    desktop = wmctrl.Desktop.get_active()
    if win.desktop != desktop.num:
        win.move_to_destktop(desktop.num)
    win.activate()

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

    if   arg == 'emacs':   return show('emacs.Emacs')
    elif arg == 'term':    return show('gnome-terminal-server.Gnome-terminal', spawn='autoterm')
    elif arg == '1':       return show(CHROME, 0)
    elif arg == '2':       return show(CHROME, 1)
    elif arg == '3':       return show(CHROME, 'cycle')
    elif arg == 'q':       return show('web.whatsapp.com.Google-chrome')
    elif arg == 'w':       return show(TELEGRAM)
    elif arg == 'e':       return steal_and_show('mail.google.com.Google-chrome', on_already_active='move_to_0')
    elif arg == 'a':       return show(MATTERMOST)
    elif arg == 's':       return show('hexchat.Hexchat')
    elif arg == 'prtscrn': return take_screenshot()
    elif arg == 'esc':     return steal_and_show('goldendict.GoldenDict', spawn='goldendict', on_already_active='killall')
    elif arg == 'F1':      return steal_and_show('zeal.Zeal', spawn='zeal')
    elif arg == 'F2':
        os.system('/home/antocuni/env/conky/myconky.py')
        os.system('reposition-windows.py')
        return os.system('kbd')
    elif arg == 'F3':      return os.system('kbd')
    elif arg == 'F11':     return os.system('reposition-windows.py emergency')
    elif arg == 'F12':     return os.system('auto-xrandr.sh')
    else:
        print 'Unknown arg:', arg



if __name__ == '__main__':
    sys.exit(main())

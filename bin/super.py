#!/usr/bin/python

import sys
import os
import wmctrl

CHROME = 'google-chrome.Google-chrome'
MATTERMOST = 'mattermost.smithersbet.com.Google-chrome' # chrome webapp
#MATTERMOST = 'mattermost.Mattermost' # native app
TELEGRAM = 'Telegram.TelegramDesktop'
#TELEGRAM = 'crx_hadgilakbfohcfcgfbioeeehgpkopaga.Google-chrome' # chrome webapp

WLIST = wmctrl.Window.list()

def show(cls, i=0, spawn=None):
    """
    Activate the i-th window of the given class.
    If there are less windows than i, activate the first.

    The logic is to prefer:
      1. sticky windows first
      2. windows which are on the active desktop

    """
    desktop = wmctrl.Desktop.get_active()
    # try to find the windows on the current desktop
    wlist = ([w for w in WLIST if w.wm_class == cls and w.desktop == -1] +
             [w for w in WLIST if w.wm_class == cls and w.desktop == desktop.num])
    if not wlist:
        # no windows found
        if spawn:
            return os.system(spawn)
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

def show_zeal():
    # ZEAL user contributed docsets:
    # https://zealusercontributions.vercel.app/
    wlist = ([w for w in WLIST if w.wm_class == 'zeal.Zeal'])
    if wlist:
        # move the window to the current desktop and activate
        w = wlist[0]
        desktop = wmctrl.Desktop.get_active()
        if w.desktop != desktop.num:
            w.move_to_destktop(desktop.num)
        w.activate()
    else:
        # no window just run zeal. This works in two cases:
        #  1. if zeal is already in the taskbar, it does the right thing and
        #     open a window
        #  2. if zeal hasn't started yet, it opens it
        os.system('zeal')


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
    #elif arg == 'e':      return show('mail.google.com.Google-chrome', 0, no_switch)
    elif arg == 'a':       return show(MATTERMOST)
    elif arg == 's':       return show('hexchat.Hexchat')
    elif arg == 'prtscrn': return take_screenshot()
    elif arg == 'esc':     return show('goldendict.GoldenDict', spawn='goldendict')
    elif arg == 'F1':      return show_zeal()
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

#!/usr/bin/python2

import sys
import os
from wmctrl import Window

PANEL=64

#TELEGRAM = 'crx_hadgilakbfohcfcgfbioeeehgpkopaga.Google-chrome' # chrome webapp
TELEGRAM = 'Telegram.TelegramDesktop' # telegram native app


def unmaximize(win):
    win.set_properties(['remove', 'maximized_vert', 'maximized_horz'])

def set_hexchat_font(size):
    os.system("hexchat -e -c 'set text_font Inconsolata Medium %d'" % size)
    os.system("hexchat -e -c 'gui apply'")

def main_dock(flavor=None):
    X0 = 0       # x position of the leftmost screen
    X1 = 1440    # x position of the center screen
    X2 = X1+3840 # x position of the rightmost screen
    PANEL = 0
    if flavor == 'betahaus':
        #X1 = X2 = 2560
        X1 = 0

    ## BIG_W = 3840-70 # 70 is the size of panel
    ## COLUMN = BIG_W / 3.0 # let's divide the screen into 3 columns (plus the panel)

    for win in Window.by_class('emacs.Emacs'):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=X1+1806, y=0, w=2036, h=1900)
        #win.resize_and_move(x=X1+70+COLUMN, y=0, w=COLUMN*2, h=1900)

    for win in Window.by_role('autoterm'):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=X1+1809, y=0, w=2036, h=2160)

    for win in Window.by_class('mail.google.com.Google-chrome'):
        unmaximize(win)
        win.resize_and_move(x=X1+70, y=0, w=1740, h=1803)

    for win in Window.by_class('web.whatsapp.com.Google-chrome'):
        unmaximize(win)
        win.set_decorations(True)
        win.resize_and_move(x=0, y=0, w=1440, h=1200)
        win.sticky()

    for win in Window.by_class(TELEGRAM):
        unmaximize(win)
        if flavor == 'betahaus':
            win.set_decorations(False)
            win.resize_and_move(x=0, y=480, w=1440, h=770)
        else:
            win.set_decorations(True)
            win.resize_and_move(x=-18, y=1225, w=1476, h=1108)
        win.sticky()

    for win in Window.by_class('slack.Slack') + Window.by_class('discord.discord'):
        unmaximize(win)
        if flavor == 'betahaus':
            win.set_decorations(True)
            win.resize_and_move(x=X1+70, y=0, w=1740, h=2010)
        else:
            win.set_decorations(False)
            win.resize_and_move(x=X2, y=0, w=1080, h=956)
        win.sticky()

    for win in Window.by_class('hexchat.Hexchat'):
        unmaximize(win)
        win.set_decorations(False)
        win.sticky()
        if flavor == 'betahaus':
            set_hexchat_font(18)
            win.resize_and_move(x=1280, y=0, w=1280, h=1440)
        else:
            set_hexchat_font(9)
            win.resize_and_move(x=X2, y=960, w=1080, h=960)

    for win in Window.by_class('google-chrome.Google-chrome'):
        # position this at the center of the main screen
        W = 2000
        X = X1 + PANEL + (3840-2000-PANEL)/2
        #win.resize_and_move(x=X, y=0, w=W, h=2050)
        win.resize_and_move(x=X, y=-19, w=W, h=2050)

    for win in Window.by_class('vmplayer.Vmplayer'):
        win.move(X1, 0)

    for win in Window.by_class('conky.conky'):
        win.sticky()

def main_laptop():
    for win in Window.by_class('emacs.Emacs'):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=526, y=0, w=2036, h=1300)

    for win in Window.by_role('autoterm'):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=526, y=0, w=2036, h=1460)

    for win in Window.by_class('mail.google.com.Google-chrome'):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=PANEL, y=0, w=1428, h=1440)

    for win in Window.by_class('web.whatsapp.com.Google-chrome'):
        unmaximize(win)
        win.set_decorations(False)
        win.sticky()
        win.resize_and_move(x=PANEL, y=0, w=1428, h=900)

    for win in Window.by_class(TELEGRAM):
        unmaximize(win)
        win.set_decorations(False)
        win.sticky()
        win.resize_and_move(x=PANEL, y=200, w=1428, h=700)

    for win in Window.by_class('hexchat.Hexchat'):
        unmaximize(win)
        win.set_decorations(False)
        win.sticky()
        win.resize_and_move(x=PANEL, y=1440-960, w=1428, h=960)
        set_hexchat_font(16)

    for win in Window.by_class('google-chrome.Google-chrome'):
        # position this at the center of the main screen
        W = 1800
        X = PANEL + (2560-W-PANEL)/2
        # I don't know why, but with y=0 it's not at the actual top. Maybe it
        # has something to do with chrome's own title bar
        Y = -20
        win.resize_and_move(x=X, y=Y, w=W, h=1440)

    for win in Window.by_class('slack.Slack') + Window.by_class('discord.discord'):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=PANEL, y=0, w=1900, h=1440)
        win.sticky()

    for win in Window.by_class('conky.conky'):
        win.sticky()


def autodetect():
    MELE_USB_KEYBOARD_ID="04f2:0111"
    BETAHAUS_USB_KEYBOARD_ID="046d:c31c"  # logitech wired
    BERLIN_USB_KEYBOARD_ID="046d:c52b"    # logitech wireless

    ret = os.system('lsusb -d ' + MELE_USB_KEYBOARD_ID)
    if ret == 0:
        return 'mele'
    ret = os.system('lsusb -d ' + BERLIN_USB_KEYBOARD_ID)
    if ret == 0:
        return 'betahaus'
    return 'laptop'


def main_emergency():
    for win in Window.list():
        if win.wm_class != 'plasmashell.plasmashell':
            win.move(0, 0)


if __name__ == '__main__':
    # usage: reposition-windows.py [autodetect|laptop|mele|emergency]
    if len(sys.argv) < 2:
        conf = 'autodetect'
    else:
        conf = sys.argv[1]

    if conf == 'autodetect':
        conf = autodetect()

    if conf == 'emergency':
        main_emergency()
    elif conf == 'mele':
        main_dock(flavor='betahaus')
    elif conf == 'betahaus':
        main_dock(flavor='betahaus')
    else:
        main_laptop()

#!/usr/bin/env python

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

def main_dock():
    X0 = 0       # x position of the leftmost screen
    X1 = 1440    # x position of the center screen
    X2 = X1+3840 # x position of the rightmost screen

    for win in Window.by_class('emacs.Emacs'):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=X1+1806, y=0, w=2036, h=1900)

    for win in Window.by_role('autoterm'):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=X1+1809, y=0, w=2036, h=2160)

    for win in Window.by_class('mail.google.com.Google-chrome'):
        unmaximize(win)
        win.resize_and_move(x=1440+64, y=0, w=1740, h=1803)

    for win in Window.by_class('web.whatsapp.com.Google-chrome'):
        unmaximize(win)
        win.resize_and_move(x=0, y=0, w=1428, h=1200)
        win.sticky()

    for win in Window.by_class(TELEGRAM):
        unmaximize(win)
        win.resize_and_move(x=0, y=1288, w=1440, h=1000)
        win.sticky()

    mattermost_class = 'mattermost.smithersbet.com.Google-chrome' # chrome webapp
    #mattermost_class = 'mattermost.Mattermost' # native app
    for win in Window.by_class(mattermost_class):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=X2, y=0, w=1080, h=956)
        win.sticky()

    for win in Window.by_class('hexchat.Hexchat'):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=X2, y=960, w=1080, h=960)
        win.sticky()
        set_hexchat_font(9)

    for win in Window.by_class('google-chrome.Google-chrome'):
        # position this at the center of the main screen
        W = 2000
        X = X1 + PANEL + (3840-2000-PANEL)/2
        win.resize_and_move(x=X, y=0, w=W, h=2000)

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
        win.resize_and_move(x=PANEL, y=0, w=1428, h=900)

    for win in Window.by_class(TELEGRAM):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=PANEL, y=200, w=1428, h=700)

    mattermost_class = 'mattermost.smithersbet.com.Google-chrome' # chrome webapp
    #mattermost_class = 'mattermost.Mattermost' # native app
    for win in Window.by_class(mattermost_class):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=PANEL, y=0, w=1428, h=956)

    for win in Window.by_class('hexchat.Hexchat'):
        unmaximize(win)
        win.set_decorations(False)
        win.sticky()
        win.resize_and_move(x=PANEL, y=1440-960, w=1428, h=960)
        set_hexchat_font(12)

    for win in Window.by_class('google-chrome.Google-chrome'):
        # position this at the center of the main screen
        W = 1800
        X = PANEL + (2560-W-PANEL)/2
        win.resize_and_move(x=X, y=0, w=W, h=1500)


def autodetect():
    USB_KEYBOARD_ID="04f2:0111"
    ret = os.system('lsusb -d ' + USB_KEYBOARD_ID)
    if ret == 0:
        return 'docking'
    return 'laptop'


def main_emergency():
    for win in Window.list():
        if win.wm_class != 'plasmashell.plasmashell':
            win.move(0, 0)


if __name__ == '__main__':
    # usage: reposition-windows.py [autodetect|laptop|docking|emergency]
    if len(sys.argv) < 2:
        conf = 'autodetect'
    else:
        conf = sys.argv[1]

    if conf == 'autodetect':
        conf = autodetect()

    if conf == 'emergency':
        main_emergency()
    elif conf == 'docking':
        main_dock()
    else:
        main_laptop()

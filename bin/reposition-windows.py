#!/usr/bin/python2

import sys
import os
from wmctrl import Window

PANEL=64

#TELEGRAM = 'crx_hadgilakbfohcfcgfbioeeehgpkopaga.Google-chrome' # chrome webapp
TELEGRAM = 'Telegram.TelegramDesktop' # telegram native app


def unmaximize(win):
    win.set_properties(['remove', 'maximized_vert', 'maximized_horz'])

def maximize(win):
    win.set_properties(['add', 'maximized_vert', 'maximized_horz'])

def set_hexchat_font(size):
    os.system("hexchat -e -c 'set text_font Inconsolata Medium %d'" % size)
    os.system("hexchat -e -c 'gui apply'")

def set_emacs_font_height(h):
    elisp = "(set-face-attribute 'default (selected-frame) :height %d)" % h
    os.system('emacsclient -e "%s"' % elisp)

def get_whatsapps():
    """
    Keep in sync with super.py:is_whatsapp
    """
    return (
        Window.by_class('web.whatsapp.com.Google-chrome') +
        Window.by_name_startswith('https://web.whatsapp.com')
    )

def main_ext():
    X1 = 0       # x position of the big screen
    X2 = X1+3840 # x position of the rightmost screen

    COL0 = PANEL
    COL1 = 1516
    COL0_W = COL1-COL0
    COL1_W = 3840-COL1

    XE = 838 # X delta of emacs

    for win in Window.by_class('emacs.Emacs'):
        unmaximize(win)
        set_emacs_font_height(144)
        win.set_decorations(False)
        win.resize_and_move(x=X1+XE, y=0, w=2328, h=1900)

    for win in Window.by_class('code.Code'):
        unmaximize(win)
        #set_emacs_font_height(144)
        win.set_decorations(False)
        win.resize_and_move(x=X1+XE, y=0, w=2328, h=1890)

    for win in Window.by_class('autoterm.autoterm'):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=X1+XE, y=0, w=2328, h=2160)

    for win in Window.by_class('mail.google.com.Google-chrome'):
        unmaximize(win)
        win.resize_and_move(x=X1+70, y=0, w=1740, h=1803)

    for win in get_whatsapps():
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=PANEL, y=0, w=1440, h=1440)
        win.sticky()

    for win in Window.by_class(TELEGRAM):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=PANEL, y=0, w=1440, h=1440)
        win.sticky()

    for win in Window.by_class('chatgpt.com.Google-chrome'):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=PANEL, y=0, w=1440, h=2160)
        win.sticky()

    for win in Window.by_class('slack.Slack') + Window.by_class('discord.discord'):
        unmaximize(win)
        win.sticky()
        win.set_decorations(False)
        win.resize_and_move(x=PANEL, y=0, w=1850-PANEL, h=2010)

    for win in Window.by_class('hexchat.Hexchat'):
        unmaximize(win)
        win.set_decorations(False)
        win.sticky()
        set_hexchat_font(18)
        win.resize_and_move(x=X1+1516, y=0, w=2328, h=1440)

    for win in Window.by_class('google-chrome.Google-chrome'):
        unmaximize(win)
        # position this at the center of the main screen
        W = 2000
        X = X1 + PANEL + (3840-2000-PANEL)/2
        #win.resize_and_move(x=X, y=0, w=W, h=2050)
        win.resize_and_move(x=X, y=-14, w=W, h=2050)

    for win in Window.by_class('vmplayer.Vmplayer'):
        win.move(X1, 0)

    for win in Window.by_class('conky.conky'):
        win.sticky()

def main_laptop():
    for win in Window.by_class('emacs.Emacs'):
        #unmaximize(win)
        win.set_decorations(False)
        set_emacs_font_height(154)
        win.resize_and_move(x=526, y=0, w=2036, h=1300)
        maximize(win)

    #for win in Window.by_role('autoterm'):
    for win in Window.by_class('autoterm.autoterm'):
        #unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=526, y=0, w=2036, h=1440)
        maximize(win)


    for win in Window.by_class('mail.google.com.Google-chrome'):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=PANEL, y=0, w=1428, h=1440)

    #for win in Window.by_class('web.whatsapp.com.Google-chrome'):
    for win in get_whatsapps():
        unmaximize(win)
        win.set_decorations(False)
        win.sticky()
        win.resize_and_move(x=PANEL, y=0, w=1428, h=1440)

    for win in Window.by_class(TELEGRAM):
        unmaximize(win)
        win.set_decorations(False)
        win.sticky()
        win.resize_and_move(x=PANEL, y=0, w=1428, h=1440)

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
        Y = -14
        win.resize_and_move(x=X, y=Y, w=W, h=1498)

    for win in Window.by_class('slack.Slack') + Window.by_class('discord.discord'):
        #unmaximize(win)
        win.set_decorations(False)
        #win.resize_and_move(x=PANEL, y=0, w=1900, h=1440)
        win.sticky()
        maximize(win)

    for win in Window.by_class('conky.conky'):
        win.sticky()


def autodetect():
    try:
        with open('/tmp/antocuni-screen-config') as f:
            return f.read().strip()
    except IOError:
        return 'none'

def main_emergency():
    for win in Window.list():
        if win.wm_class != 'plasmashell.plasmashell':
            win.move(0, 0)


if __name__ == '__main__':
    # usage: reposition-windows.py [autodetect|laptop|ext]
    if len(sys.argv) < 2:
        conf = 'autodetect'
    else:
        conf = sys.argv[1]

    if conf == 'autodetect':
        conf = autodetect()
        print('detected screen config: %s' % conf)

    if conf == 'emergency':
        main_emergency()
    elif conf in ('both', 'ext'):
        main_ext()
    elif conf == 'laptop':
        main_laptop()
    else:
        print('WARNING: unsupported screen config: %s' % conf)
        main_laptop()

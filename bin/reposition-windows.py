#!/usr/bin/env python

import os
from wmctrl import Window

def unmaximize(win):
    win.set_properties(['remove', 'maximized_vert', 'maximized_horz'])

def main():
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

    #telegram_class = 'crx_hadgilakbfohcfcgfbioeeehgpkopaga.Google-chrome' # chrome webapp
    telegram_class = 'Telegram.TelegramDesktop' # telegram native app
    for win in Window.by_class(telegram_class):
        unmaximize(win)
        win.resize_and_move(x=0, y=1288, w=1440, h=1000)

    #mattermost_class = 'mattermost.smithersbet.com.Google-chrome' # chrome webapp
    mattermost_class = 'mattermost.Mattermost' # native app
    for win in Window.by_class(mattermost_class):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=X2, y=0, w=1080, h=956)

    for win in Window.by_class('hexchat.Hexchat'):
        unmaximize(win)
        win.set_decorations(False)
        win.resize_and_move(x=X2, y=960, w=1080, h=960)


if __name__ == '__main__':
    main()

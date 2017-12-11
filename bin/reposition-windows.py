#!/usr/bin/env python

import os
from wmctrl import Window

def unmaximize(win):
    win.set_properties(['remove', 'maximized_vert', 'maximized_horz'])

def main():
    # position windows on my 4k screen

    for win in Window.by_class('emacs.Emacs'):
        unmaximize(win)
        win.resize_and_move(x=1804, y=0, w=2036, h=1650)

    for win in Window.by_role('autoterm'):
        unmaximize(win)
        win.resize_and_move(x=1811, y=755, w=2029, h=1405)

    for win in Window.by_class('mail.google.com.Google-chrome'):
        unmaximize(win)
        win.resize_and_move(x=73, y=0, w=1728, h=1803)

if __name__ == '__main__':
    main()

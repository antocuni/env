#!/usr/bin/env python

import os
from wmctrl import Window

def unmaximize(win):
    return
    win.set_properties(['remove', 'maximized_vert', 'maximized_horz'])

WHATSAPP = Window.by_class('web.whatsapp.com.Google-chrome')[0]
TELEGRAM = Window.by_class('Telegram.TelegramDesktop')[0]


def tg():
    WHATSAPP.resize_and_move(x=0, y=0)
    TELEGRAM.resize_and_move(x=0, y=230)
    TELEGRAM.activate()

def wa():
    WHATSAPP.resize_and_move(x=0, y=230)
    WHATSAPP.activate()
    TELEGRAM.resize_and_move(x=0, y=0)


def tg():
    import gtk.gdk
    whatsapp = gtk.gdk.window_foreign_new(int(WHATSAPP.id, 16))
    telegram = gtk.gdk.window_foreign_new(int(TELEGRAM.id, 16))
    whatsapp.move(0, 0)
    telegram.move(0, 230)
    gtk.gdk.window_process_all_updates()
    gtk.gdk.flush()
    TELEGRAM.activate()


def wa():
    import gtk.gdk
    whatsapp = gtk.gdk.window_foreign_new(int(WHATSAPP.id, 16))
    telegram = gtk.gdk.window_foreign_new(int(TELEGRAM.id, 16))
    whatsapp.move(0, 230)
    telegram.move(0, 0)
    gtk.gdk.window_process_all_updates()
    gtk.gdk.flush()
    WHATSAPP.activate()


if __name__ == '__main__':
    #tryit()
    import sys
    if sys.argv[1] == 'wa':
        wa()
    else:
        tg()

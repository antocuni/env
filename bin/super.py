#!/usr/bin/python

"""
ZEAL user contributed docsets:
https://zealusercontributions.vercel.app/
"""

import sys
import os
import wmctrl

#TERMINAL = 'gnome-terminal-server.Gnome-terminal'
TERMINAL = 'autoterm.autoterm'
CHROME = 'google-chrome.Google-chrome'
TELEGRAM = 'Telegram.TelegramDesktop'
CHATGPT = 'chatgpt.com.Google-chrome'
#TELEGRAM = 'crx_hadgilakbfohcfcgfbioeeehgpkopaga.Google-chrome' # chrome webapp

WLIST = wmctrl.Window.list()

def is_whatsapp(w):
    """
    Select whatsapp windows both on chrome and firefox.
    Keep in sync with reposition-windows.py:get_whatsapps
    """
    return (w.wm_name.startswith('https://web.whatsapp.com') or
            w.wm_class == 'web.whatsapp.com.Google-chrome')


def show(wm_class, i=0, spawn=None, on_already_active=None):
    """
    Activate the i-th window of the given class.
    If there are less windows than i, activate the first.

    The logic is to prefer:
      1. sticky windows first
      2. windows which are on the active desktop

    """
    # find the windows visible on the current desktop, sticky windows first
    desktop = wmctrl.Desktop.get_active()
    if wm_class == '--WHATSAPP--':
        # hack hack: selects both firefox and chrome windows with whatsapp
        wlist = [w for w in WLIST if is_whatsapp(w) and  w.desktop in (-1, desktop.num)]
    else:
        wlist = [w for w in WLIST if w.wm_class == wm_class and w.desktop in (-1, desktop.num)]

    wlist.sort(key=lambda w: w.desktop)
    #
    if not wlist:
        # no windows found
        if spawn:
            return os.system(spawn)
        print('No windows found: %s' % wm_class)
        return 1
    #
    if i == 'cycle':
        return cycle(wlist)
    if i >= len(wlist):
        # not enough windows, fall back to the first
        i = 0

    # check whether the window is already active
    win = wlist[i]
    current = wmctrl.Window.get_active()
    if win.id == current.id and on_already_active == 'minimize':
        return os.system('xdotool windowminimize %s' % win.id)

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
    assert on_already_active in (None, 'move_to_0', 'minimize', 'killall')
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
        elif on_already_active == 'minimize':
            return minimize(win)
        elif on_already_active == 'killall':
            return os.system('killall %s' % spawn)
    #
    # window found: move it to the current desktop (if necessary) and activate
    desktop = wmctrl.Desktop.get_active()
    if win.desktop != desktop.num:
        win.move_to_destktop(desktop.num)
    win.activate()

def minimize(win):
    return os.system('xdotool windowminimize %s' % win.id)

def cycle_classes(*wm_classes):
    desktop = wmctrl.Desktop.get_active()
    wlist = []
    for wm_class in wm_classes:
        wlist += [win for win in wmctrl.Window.by_class(wm_class)
                  if win.desktop in (-1, desktop.num)]
    if wlist:
        cycle(wlist)
    else:
        return 1

def cycle(wlist):
    # cycle through the list of windows
    current = wmctrl.Window.get_active()
    if current == wlist[-1]:
        # this was the last, minimize everything
        for w in wlist:
            minimize(w)
    elif current in wlist:
        # we are someone in the middle, activate the next
        i = wlist.index(current)
        wlist[i+1].activate()
    else:
        # activate the first
        wlist[0].activate()

    return 0

def focus_mode():
    current = wmctrl.Window.get_active()
    if current.wm_class in (TERMINAL, 'emacs.Emacs'):
        to_keep = wmctrl.Window.by_class(TERMINAL)
        to_keep += wmctrl.Window.by_class('emacs.Emacs')
    else:
        to_keep = [current]

    wlist = wmctrl.Window.list()
    for win in wlist:
        if win not in to_keep:
            minimize(win)

def notify(summary, body):
    os.system('notify-send "%s" "%s"' % (summary, body))

def take_screenshot():
    # spectacle doesn't have a command line option to hide the mouse
    # pointer. As a workaround, I move the mouse in a corner, start
    # spectacle, mouve the mouse back, and wait for spectacle to finish
    #
    # UPDATE: in theory, spectacle has a --copy-image option, but it doesn't
    # seem to work now. Instead, let's save the screenshot to a file and copy
    # it with xclip
    #cmd = os.system('import /tmp/screenshot.png')
    cmd = """
    eval $(xdotool getmouselocation --shell);
    xdotool mousemove 10000 10000
    #spectacle --b -r -c &
    spectacle --background --region -o /tmp/screenshot.png &
    sleep 0.5
    xdotool mousemove $X $Y
    wait
    """
    ret = os.system(cmd)
    if ret != 0:
        notify('Screenshot failed', 'Cannot run "import"')
        return ret
    ret = os.system('xclip -selection clipboard -t image/png -i /tmp/screenshot.png')
    if ret != 0:
        notify('Screenshot failed', 'Cannot run "xclip"')
        return ret
    return 0

def current_windows():
    """
    Return the list of windows on the current desktop
    """
    desktop = wmctrl.Desktop.get_active()
    return [w for w in wmctrl.Window.list() if w.desktop in (-1, desktop.num)]


def show_emacs_or_code():
    """
    If vscode is running, show emacs, otherwise show vscode. If none
    is running, show the last chosen.
    """
    wlist = current_windows()
    has_emacs = any([w.wm_class == 'emacs.Emacs' for w in wlist])
    has_vscode = any([w.wm_class == 'code.Code' for w in wlist])

    current = wmctrl.Window.get_active()
    if current.wm_class == 'code.Code' and has_emacs:
        cycle_classes('code.Code', 'emacs.Emacs')
        os.system('rm /tmp/vscode')
    elif current.wm_class == 'emacs.Emacs' and has_vscode:
        cycle_classes('emacs.Emacs', 'code.Code')
        os.system('touch /tmp/vscode')
    else:
        if os.path.exists('/tmp/vscode'):
            show('code.Code')
        else:
            show_openscad_maybe()
            show('emacs.Emacs')

def has_emacs():
    wlist = current_windows()
    res = any([w.wm_class == 'emacs.Emacs' for w in wlist])
    #print(res)
    return int(not res)


def show_openscad_maybe():
    d = wmctrl.Desktop.get_active()
    if d.name != '3d':
        return
    openscad = wmctrl.Window.by_class('openscad.OpenSCAD')
    if not openscad:
        return
    # poor's man way to detect whether openscad if locked to the left
    w = openscad[0]
    if w.x == 76 and w.w == 1844:
        w.activate()



def main(argv):
    arg = argv[1]
    no_switch = '--no-switch' in argv

    if arg == 'dev':
        show_openscad_maybe()
        return

    if   arg == 'emacs':     return show_emacs_or_code()
    elif arg == 'has_emacs': return has_emacs()
    elif arg == 'term':    return show(TERMINAL, spawn='autoterm')
    elif arg == '1':       return show(CHROME, 1, on_already_active='minimize')
    elif arg == '2':       return show(CHROME, 0, on_already_active='minimize')
    elif arg == '3':       return show(CHROME, 'cycle')
    elif arg == 'q':       return show('--WHATSAPP--', on_already_active='minimize')
    elif arg == 'w':       return show(TELEGRAM, on_already_active='minimize')
    elif arg == 'e':       return steal_and_show('mail.google.com.Google-chrome', on_already_active='move_to_0')
    elif arg == 'tab':     return show(CHATGPT, on_already_active='minimize')
    #elif arg == 'a':       return show('slack.Slack', on_already_active='minimize')
    elif arg == 'a':       return cycle_classes('slack.Slack', 'discord.discord')

    elif arg == 's':       return show('hexchat.Hexchat', on_already_active='minimize')
    elif arg == 'prtscrn': return take_screenshot()
    elif arg == 'esc':     return steal_and_show('goldendict.GoldenDict', spawn='goldendict', on_already_active='minimize')
    elif arg == 'F1':      return steal_and_show('zeal.Zeal', spawn='zeal', on_already_active='minimize')
    elif arg == 'F2':
        os.system('/home/antocuni/env/conky/myconky.py')
        os.system('reposition-windows.py')
        return os.system('kbd')
    elif arg == 'F3':      return os.system('kbd')
    elif arg == 'F11':     return os.system('reposition-windows.py emergency')
    elif arg == 'F12':
        os.system('auto-xrandr.py')
        return os.system('reposition-windows.py')
    elif arg == 'pause':   return os.system('robust-suspend.py')
    elif arg == 'backspace': return focus_mode()
    else:
        print('Unknown arg:', arg)



if __name__ == '__main__':
    sys.exit(main(sys.argv))

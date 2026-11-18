#!/usr/bin/env python3

import sys
import os
import time
import platform
import tempfile
import subprocess

MAC = platform.system() == 'Darwin'


def main():
    cmdline = ' '.join(sys.argv[1:])
    if MAC:
        run_macos(cmdline)
    else:
        run_linux(cmdline)


def run_linux(cmdline):
    import super as super_py
    # XXX ideally I would like to switch to the proper tab
    super_py.main(['super.py', 'term']) # activate the terminal
    time.sleep(0.1)
    os.system('xdotool key ctrl+c')
    os.system('xdotool type --delay 1 "%s"' % cmdline)
    os.system('xdotool key Return')


def run_macos(cmdline):
    # macOS has no xdotool: use Hammerspoon, which is already installed and has
    # the Accessibility permission which is needed to synthesize keystrokes.
    # Type as soon as kitty is focused, instead of after a fixed delay; leave a
    # short pause between the events because kitty drops a Return which arrives
    # immediately after the typed text. The third argument of keyStroke is the
    # gap between key-down and key-up, which defaults to a slow 200ms.
    path = os.path.join(tempfile.mkdtemp(prefix='pytest-launcher-'),
                        'launcher.lua')
    lua = '''local path = %r
local cmd = [==[%s]==]
local deadline = os.time() + 2

local function type_command()
    hs.eventtap.keyStroke({"ctrl"}, "c", 2000)
    hs.timer.usleep(100000)
    hs.eventtap.keyStrokes(cmd)
    hs.timer.usleep(200000)
    hs.eventtap.keyStroke({}, "return", 2000)
    os.remove(path)
end

local wait_for_kitty
wait_for_kitty = function()
    local app = hs.application.frontmostApplication()
    if (app and app:name() == "kitty") or os.time() > deadline then
        type_command()
    else
        hs.timer.doAfter(0.02, wait_for_kitty)
    end
end

hs.application.launchOrFocus("kitty")
wait_for_kitty()
''' % (path, cmdline)
    with open(path, 'w') as f:
        f.write(lua)
    ret = subprocess.call(['hs', '-c', 'dofile(%r)' % path])
    if ret != 0:
        print('cannot talk to Hammerspoon (hs exited with %d)' % ret)
        print('check that Hammerspoon is running and Accessibility is allowed')
        sys.exit(1)


if __name__ == '__main__':
    main()

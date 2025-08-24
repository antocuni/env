#!/usr/bin/env python3

import sys
import subprocess
import json
import socketserver
import time

class UtilsHandler(socketserver.StreamRequestHandler):
    def reply(self, s):
        print("[send]", s)
        bs = (s + "\n").encode("utf-8")
        self.wfile.write(bs)

    def handle(self):
        raw = self.rfile.read()  # bytes until client closes
        try:
            argv = json.loads(raw.decode("utf-8"))
        except Exception as e:
            self.reply(f"Invalid JSON payload: {e}")
            return

        print("[recv]", " ".join(argv))
        if not argv:
            self.reply("no command")
            return

        cmd = argv[0]
        if cmd in ("aplay", "e", "xdg-open"):
            subprocess.run(argv)
            return

        meth = getattr(self, f'do_{cmd}', None)
        if meth is None:
            self.reply(f"Invalid command: {cmd}")
        else:
            meth(*argv[1:])

    def do_ping(self, *args):
        pong = ('pong', ) + args
        self.reply(" ".join(pong))

    def do_sleep(self, x):
        x = float(x)
        time.sleep(x)
        self.reply('OK')

    def do_sleep_hook(self, phase, sleep_type):
        ## if phase == 'pre':
        ##     self.reply('goodnight')
        ##     return

        if phase == 'post' and sleep_type == 'suspend':
            auto_xrandr()
            self.reply('good morning')


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def auto_xrandr():
    """
    run auto-xrandr.py, and reposition-windows.py ONLY if we switched
    screen config
    """
    def get_config():
        try:
            with open('/tmp/antocuni-screen-config') as f:
                return f.read().strip()
        except IOError:
            return 'none'

    old_config = get_config()
    subprocess.run('auto-xrandr.py')
    new_config = get_config()
    print(f'[auto-xrandr.py] {old_config} => {new_config}')
    if old_config != new_config:
        subprocess.run('reposition-windows.py')



if __name__ == "__main__":
    HOST, PORT = "localhost", 4242
    with ReusableTCPServer((HOST, PORT), UtilsHandler) as server:
        server.serve_forever()

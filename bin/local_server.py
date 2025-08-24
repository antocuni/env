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


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    HOST, PORT = "localhost", 4242
    with ReusableTCPServer((HOST, PORT), UtilsHandler) as server:
        server.serve_forever()

#!/usr/bin/env python3

import sys
import subprocess
import json
import socketserver
import time

class UtilsHandler(socketserver.StreamRequestHandler):
    def handle(self):
        raw = self.rfile.read()  # bytes until client closes
        try:
            argv = json.loads(raw.decode("utf-8"))
        except Exception as e:
            print(f"Invalid JSON payload: {e}", file=sys.stderr)
            return

        print(argv)
        if not argv:
            print("Empty argv", file=sys.stderr)
            return

        cmd = argv[0]
        if cmd == "ping":
            print(" ".join(argv), file=sys.stderr)
        elif cmd in ("aplay", "e", "xdg-open"):
            subprocess.run(argv)
        elif cmd  == "sleep":
            self.do_sleep(*argv[1:])
        else:
            print(f"Invalid command: {cmd}", file=sys.stderr)

    def do_sleep(self, x):
        x = float(x)
        time.sleep(x)
        self.wfile.write(b'OK\n')


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    HOST, PORT = "localhost", 4242
    with ReusableTCPServer((HOST, PORT), UtilsHandler) as server:
        server.serve_forever()

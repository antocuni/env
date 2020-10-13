#!/usr/bin/env python

import sys
import subprocess
import json
import SocketServer

class UtilsHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        argv = self.rfile.read()
        argv = json.loads(argv.decode('utf-8'))
        cmd = argv[0]
        if cmd not in ('aplay', 'e'):
            print >> sys.stderr, 'Invalid command: %s' % cmd
            return
        subprocess.Popen(argv).wait()

if __name__ == "__main__":
    HOST, PORT = "localhost", 4242
    server = SocketServer.TCPServer((HOST, PORT), UtilsHandler)
    server.allow_reuse_address = True
    server.serve_forever()

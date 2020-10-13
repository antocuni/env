#!/usr/bin/python3

import sys
import socket
import json

if len(sys.argv) < 2:
    print('Usage: %s command' % sys.argv[0], file=sys.stderr)
    sys.exit(1)

sock = socket.socket()
try:
    sock.connect(('localhost', 4242))
    args = json.dumps(sys.argv[1:]).encode('utf-8')
    sock.send(args)
    sock.close()
except IOError as e:
    print(str(e), file=sys.stderr)
    sys.exit(2)

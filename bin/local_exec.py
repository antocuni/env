#!/usr/bin/python2

import sys
import socket
import cPickle

if len(sys.argv) < 2:
    print >> sys.stderr, 'Usage: %s command' % sys.argv[0]
    sys.exit(1)

sock = socket.socket()
try:
    sock.connect(('localhost', 4242))
    args = cPickle.dumps(sys.argv[1:])
    sock.send(args)
    sock.close()
except IOError, e:
    print >> sys.stderr, str(e)
    sys.exit(2)

#!/usr/bin/python2

import os
import random
import string
import sys

if len(sys.argv) == 2:
    # existing file
    fpath = sys.argv[1]
    _, fname = os.path.split(fpath)
else:
    letters = string.lowercase + string.uppercase + string.digits
    ID = [random.choice(letters) for i in range(8)]
    fname = '%s.png' % ''.join(ID)

    fpath = '/tmp/pastescreen/%s' % fname
    os.system('mkdir -p /tmp/pastescreen')
    os.system('import %s' % fpath)
    os.system('echo -n wait | xsel -i -b')

os.system('scp %s antocuni.eu:www/antocuni.eu/misc/img' % fpath)

URL = 'http://antocuni.eu/misc/img/%s' % fname
print URL
os.system('echo -n %s | xsel -i -b' % URL)

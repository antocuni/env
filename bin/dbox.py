#!/usr/bin/env python

import sys
import os.path
from glob import glob
import re
import shutil
from collections import defaultdict
from opster import command, dispatch, ParseError
from color import color, GREEN, YELLOW

@command()
def resolve(name, winner_owner=('w', '', 'owner of the file to keep')):
    "Resolve a conflict"
    def resolve_one(name):
        basename, ext = os.path.splitext(name)
        winner_pattern = "%s (%s's conflicted copy *)%s" % (basename, winner_owner, ext)
        winners = glob(winner_pattern)
        if len(winners) != 1:
            print >> sys.stderr, 'Cannot determine the winner (%d files match):' % len(winners)
            for winner in winners:
                print >> sys.stderr, '   ', winner
            return
        winner = winners[0]
        shutil.move(winner, name)

    if winner_owner is '':
        raise ParseError('resolve', 'winner is required')
    resolve_one(name)

@command()
def conflicts():
    "Show conflicted files"
    parse = re.compile(r"(.*) \((.*)'s conflicted copy (.*)\)(.*)")
    d = defaultdict(list)
    for name in os.listdir('.'):
        match = parse.match(name)
        if match:
            basename, owner, date, ext = match.groups()
            origname = basename+ext
            d[origname].append('%s %s' % (color(owner, GREEN), date))
    if d:
        print 'Conflicted files:'
        for origname, copies in d.iteritems():
            print '%s:' % color(origname, YELLOW), ', '.join(copies)



if __name__ == '__main__':
    dispatch()


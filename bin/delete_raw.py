#!/usr/bin/python

import py

def main():
    d = py.path.local('.')
    count = 0
    raws = d.listdir('*.CR3') + d.listdir('*.dng')
    for raw in sorted(raws):
        jpg = raw.new(ext='JPG')
        if jpg.check(exists=False):
            print raw
            raw.remove()
            count += 1
    print '%d files deleted' % count

main()

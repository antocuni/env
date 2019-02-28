#!/usr/bin/python

import py

def main():
    d = py.path.local('.')
    count = 0
    for cr3 in sorted(d.listdir('*.CR3')):
        jpg = cr3.new(ext='JPG')
        if jpg.check(exists=False):
            cr3.remove()
            count += 1
    print '%d files deleted' % count

main()

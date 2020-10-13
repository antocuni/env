#!/usr/bin/python

import py

def main():
    dirname = '.'
    d = py.path.local(dirname)
    mp3s = d.listdir('*.mp3')
    mp3s.sort()
    print '#EXTM3U'
    print '#TTPLAYLIST_NAME:%s' % d.purebasename
    for mp3 in mp3s:
        print mp3.basename

if __name__ == '__main__':
    main()

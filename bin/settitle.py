#!/usr/bin/env python

import glob
import shutil
import sys
import ID3

def read_titles():
    f = open('album.txt')
    artist = f.readline().strip()
    album = f.readline().strip()
    songs = map(str.strip, f.readlines())
    f.close()
    return artist, album, songs

def parse_song(song):
    try:
        num, name = song.split(' ', 1)
        num = int(num)
        return num, name
    except ValueError:
        return -1, song


def main():
    dummy = '--dummy' in sys.argv
    mp3s = glob.glob('*.mp3') + glob.glob('*.MP3')
    mp3s.sort()
    artist, album, songs = read_titles()
    if len(mp3s) != len(songs):
        print >> sys.stderr, "Invalid number of titles"
        sys.exit(1)

    for filename, song in zip(mp3s, songs):
        tracknum, songname = parse_song(song)
        if dummy:
            print '%s --> %s' % (filename, song + '.mp3')
        else:
            tag = ID3.ID3(filename)
            tag.album = album
            tag.artist = artist
            tag.title = songname
            if tracknum != -1:
                tag.track = tracknum
            tag.write()
            shutil.move(filename, song + '.mp3')

if __name__ == '__main__':
    main()

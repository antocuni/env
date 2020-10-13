#!/usr/bin/python3

"""
dcim.py /media/antocuni/6330-3432/DCIM/100CANON/ ~/foto/unsorted/
"""

import sys
import pathlib
import shutil

class DCIM:

    def __init__(self, src, dst):
        self.src = pathlib.Path(sys.argv[1])
        self.dst = pathlib.Path(sys.argv[2])
        self.read_last_imported()

    def read_last_imported(self):
        f = self.dst.joinpath('last_imported.txt')
        if f.is_file():
            self.last_imported = f.read_text().strip()
            print('Last imported file was %s' % self.last_imported)
        else:
            print('last_imported.txt not found, importing everything')
            self.last_imported = ''

    def do_import(self):
        last_imported = None
        for f in sorted(self.src.iterdir()):
            if f.name > self.last_imported:
                print('COPY %s' % f)
                shutil.copy(f, self.dst)
                last_imported = f
        #
        if last_imported is not None:
            print('Setting last_imported.txt to %s' % f.name)
            self.dst.joinpath('last_imported.txt').write_text(f.name)

def main():
    if len(sys.argv) != 3:
        print('Usage: dcim.py FROM TO')
        print('Example: dcim.py /media/antocuni/6330-3432/DCIM/100CANON/ ~/foto/unsorted/')
        return 1
    src = sys.argv[1]
    dst = sys.argv[2]
    dcim = DCIM(src, dst)
    dcim.do_import()



if __name__ == '__main__':
    sys.exit(main())

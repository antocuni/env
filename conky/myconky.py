#!/usr/bin/python3

import os
from pathlib import Path

ROOT = Path(__file__).parent.absolute()

TMP = Path('/tmp/myconky')
TMP.mkdir(parents=True, exist_ok=True)

class Conky:
    def make_conkyrc(self):
        out = TMP.joinpath(f'conkyrc.{self.__class__.__name__}')
        with out.open('w') as f:
            for rc in self.RC:
                rc = ROOT.joinpath(rc)
                content = Path(rc).read_text()
                f.write(f'# === {rc} ===\n')
                f.write(content)
                f.write('\n')
        return out

    def run(self):
        conkyrc = self.make_conkyrc()
        os.system(f'conky --daemonize -c {conkyrc}')


class Main(Conky):
    RC = ['base.conky', 'main.conky']

class Calendar(Conky):
    RC = ['base.conky', 'calendar.conky']

def main():
    os.system('killall conky')
    Main().run()
    Calendar().run()


if __name__ == '__main__':
    main()

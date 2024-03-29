#!/usr/bin/env python3

"""
Usage: calendarterm.py [options]

Options:
  --conky                 Output colors in conky mode
  --max-lines=N           Maximum number of lines to print
  -h --help               show this
"""

import sys
import docopt
import datetime
from pathlib import Path
from icalevents import icalevents

URL = Path(__file__).with_name('calendarterm.url').read_text().strip()
TODAY = datetime.date.today()

def conky_color(col, line):
    return '${color %s}%s${color}' % (col, line)

def dummy_color(col, line):
    return line

def ansi_color(col, line):
    return Color.set(col, line)

class Color:
    black = '30'
    darkred = '31'
    darkgreen = '32'
    brown = '33'
    darkblue = '34'
    purple = '35'
    teal = '36'
    lightgray = '37'
    darkgray = '30;01'
    red = '31;01'
    green = '32;01'
    yellow = '33;01'
    blue = '34;01'
    fuchsia = '35;01'
    turquoise = '36;01'
    white = '37;01'

    @classmethod
    def set(cls, color, string):
        try:
            color = getattr(cls, color)
        except AttributeError:
            pass
        return '\x1b[%sm%s\x1b[00m' % (color, string)



def main():
    args = docopt.docopt(__doc__)
    if args['--conky']:
        color = conky_color
    else:
        #color = dummy_color
        color = ansi_color
    max_lines = args['--max-lines']
    if max_lines is None:
        max_lines = sys.maxsize
    else:
        max_lines = int(max_lines)

    lines_printed = 0
    start = datetime.date.today()
    events = icalevents.events(URL, start=start)
    #events = icalevents.events(file="/tmp/download/acuni@anaconda.com.ics", start=start)
    events.sort()
    last_day = datetime.date(1, 1, 1) # dummy day
    for ev in events:
        day = ev.start.date()
        if day != last_day:
            s_date = ev.start.strftime('%a %d %b')
        else:
            s_date = ''
        last_day = day
        #
        s_time = ev.start.strftime('%H:%M')
        line = f'{s_date:<12}{s_time:<5}   {ev.summary}'

        delta = day - TODAY
        if delta.days == 0:
            # today
            line = color('red', line)
        elif delta.days == 1:
            # tomorrow
            line = color('yellow', line)

        if lines_printed == max_lines - 1:
            print('...')
            break
        else:
            print(line)
            lines_printed += 1

if __name__ == '__main__':
    main()

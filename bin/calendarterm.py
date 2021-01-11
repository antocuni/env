#!/usr/bin/env python3

import sys
import datetime
from pathlib import Path
from icalevents import icalevents

URL = Path(__file__).with_name('calendarterm.url').read_text().strip()
TODAY = datetime.date.today()

def conky_color(col, line):
    return '${color %s}%s${color}' % (col, line)

def dummy_color(col, line):
    return line

def main(conky):
    if conky:
        color = conky_color
    else:
        color = dummy_color

    start = datetime.date.today()
    events = icalevents.events(URL, start=start)
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

        print(line)

if __name__ == '__main__':
    conky = '--conky' in sys.argv
    main(conky)

#!/usr/bin/env python

import sys
import numpy

def main():
    numbers = map(float, sys.stdin)
    print 'Average: %.4f' % numpy.mean(numbers)
    print 'Median:  %.4f' % numpy.median(numbers)
    print 'Stddev:  %.4f' % numpy.std(numbers)
    print 'Max:     %.4f' % numpy.max(numbers)
    print 'Min:     %.4f' % numpy.min(numbers)


if __name__ == '__main__':
    main()

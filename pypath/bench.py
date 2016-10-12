import time
import atexit
from functools import wraps
from collections import Counter

def bench(fn):
    def inner(*args, **kwds):
        start = time.clock()
        res = fn(*args, **kwds)
        end = time.clock()
        try:
            name = fn.__name__
        except AttributeError:
            name = repr(fn)
        #
        print '%s: %.2f seconds' % (name, end-start)
        return res
    return inner


def benchmark(fn):
    @wraps(fn)
    def inner(*args, **kwds):
        a = time.time()
        try:
            return fn(*args, **kwds)
        finally:
            b = time.time()
            benchmark.timings[fn.__name__] += (b-a)
    return inner
    
benchmark.timings = Counter()

## @atexit.register
## def print_benchmarks():
##     print
##     print 'BENCHMARKS'
##     for key, value in benchmark.timings.most_common():
##         print '%20s %.2f' % (key, value)

from __future__ import print_function
import sys
import bdb

def isatty(stream):
    return hasattr(stream, 'isatty') and stream.isatty()

def info(type, value, tb):
    ontty = isatty(sys.stderr) and isatty(sys.stdout) and isatty(sys.stdin)
    ## if hasattr(sys, 'ps1') or not ontty or type is bdb.BdbQuit or \
    ##         str(value) == 'underlying C/C++ object has been deleted':
    if hasattr(sys, 'ps1') or not ontty or type is bdb.BdbQuit:
        # You are in interactive mode or don't have a tty-like
        # device, so call the default hook
        sys.__excepthook__(type, value, tb)
    else:
        import traceback, pdb
        # You are not in interactive mode; print the exception
        traceback.print_exception(type, value, tb)
        print()
        # ... then star the debugger in post-mortem mode
        pdb.pm()

sys.excepthook = info


if sys.version_info < (3, 0):
    import __builtin__ as builtins
else:
    import builtins

## import timing
## builtins.Timing = timing.Timing

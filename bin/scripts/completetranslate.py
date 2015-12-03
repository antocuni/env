#!/usr/bin/env python

""" To make it work, you need to execute (ie push in .bashrc)
complete -o bashdefault -o default -C <path to this file> ./translate.py

blame bash
"""
import os, sys
sys.path.insert(0, '.')
import autopath
from pypy.config.config import to_optparse
from pypy.config.translationoption import get_combined_translation_config
from pypy.config.pypyoption import get_pypy_config

line = os.environ['COMP_LINE']
lines = line.split(" ")
last = lines[-1]
was = 'targetpypystandalone.py' in lines
if not last:
    sys.exit(0)

def get_optp(conf):
    optp = to_optparse(conf)
    opts = optp.option_list
    for i in [g.option_list for g in optp.option_groups]:
        opts += i
    opt_s = [i.get_opt_string() for i in opts]
    return opt_s

if not was:
    opt_s = get_optp(get_combined_translation_config())
else:
    opt_s = get_optp(get_pypy_config())
to_p = [i for i in opt_s if i.startswith(last)]
for i in to_p:
    print i
#d = [config.getkey(path) for path in config.getpaths()]


#! /usr/bin/env python

# Magic line for bash (blame obscure shells):
#
#    complete -o bashdefault -o default -C /path/to/completepytest.py py.test

import sys

command, wordstart, previousword = sys.argv[1:4]
if wordstart == '-k':
    wordstart = ''
    addspace = '-k '
else:
    if previousword != '-k':
        sys.exit(0)    # use default completion
    addspace = ''

import os
line = os.environ['COMP_LINE']

filenames = line.split()
for arg in filenames:
    if arg.endswith('.py'):
        if 'test' in arg: #os.path.basename(arg).startswith('test_') or os.path.basename(arg).endswith('_tests.py'):
            try:
                f = open(arg, 'r')
                lines = f.readlines()
                f.close()
            except (OSError, IOError):
                continue
            for line in lines:
                line = line.lstrip()
                if line.startswith('def test_'):
                    testname = line[4:]
                    i = testname.find('(')
                    if i < 0:
                        continue
                    testname = testname[:i]
                    if testname.startswith(wordstart):
                        print addspace + testname
                elif line.startswith('# =='):
                    # follow comments of the form:
                    # ===> relative_file_path.py
                    parts = line.split(None, 2)
                    if len(parts) == 3:
                        fn = parts[2].strip()
                        fn = os.path.join(os.path.dirname(arg), fn)
                        fn = os.path.abspath(fn)
                        if fn not in filenames:
                            filenames.append(fn)

#!/usr/bin/env python3
"""
Add OSC 8 clickable links to a git diff. Clicking a "+" line opens the file
at that line using local_server.py's HTTP endpoint.

Preserves git's own coloring — pass color.diff=always so git colors survive
the pipe:

    git -c color.diff=always diff | magic_diff.py
    git -c color.diff=always log -p | magic_diff.py

Or configure git to always use magic_diff.py as the pager for diff:

    git config --global pager.diff 'magic_diff.py | less -R'
"""

import sys
import os
import re
import subprocess
from urllib.parse import quote

SERVER = "http://localhost:4242"

# Strip ANSI escape sequences for pattern matching only
ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def strip_ansi(s):
    return ANSI_RE.sub('', s)

def osc8_link(url, text):
    """Wrap text in an OSC 8 hyperlink."""
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

def get_git_toplevel():
    """Get the git repo root, or fall back to cwd."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        pass
    return os.getcwd()

def main():
    repo_root = get_git_toplevel()
    current_file = None
    hunk_new_line = None

    diff_line_re = re.compile(r'^\+\+\+ [ab]/(.+)$')
    hunk_re = re.compile(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@')

    for raw_line in sys.stdin:
        line = raw_line.rstrip('\n')
        clean = strip_ansi(line)

        # Detect file from +++ line
        m = diff_line_re.match(clean)
        if m:
            current_file = os.path.join(repo_root, m.group(1))
            hunk_new_line = None
            print(line)
            continue

        # Detect hunk header
        m = hunk_re.match(clean)
        if m:
            hunk_new_line = int(m.group(1))
            print(line)
            continue

        if hunk_new_line is None:
            print(line)
            continue

        if clean.startswith('+'):
            url = f"{SERVER}/e?file={quote(current_file)}&line={hunk_new_line}"
            print(osc8_link(url, line))
            hunk_new_line += 1
        elif clean.startswith('-'):
            print(line)
        else:
            print(line)
            hunk_new_line += 1

if __name__ == "__main__":
    main()

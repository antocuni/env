#!/usr/bin/env python

import os.path
import glob
from getpass import getpass

HGRC_AUTH = """
[auth]
bb.prefix = https://bitbucket.org/
bb.username = antocuni
bb.password = %s
"""

RED = 31
GREEN = 32
YELLOW = 33

home = os.path.expanduser('~')
etc_dir = os.path.join(home, 'env', 'etc')
excludes = ['create_symlinks.py', 'scripts', 'elisp', 'gtk-3.0']

def system(cmd):
    ret = os.system(cmd)
    if ret != 0:
        print color('Command failed :(', RED), cmd
        sys.exit(ret)

def color(s, fg=1, bg=1):
    template = '\033[%02d;%02dm%s\033[0m'
    return template % (bg, fg, s)

def write_hgrc_auth():
    filename = os.path.join(home, '.hgrc.auth')
    if os.path.exists(filename):
        print color('~/.hgrc.auth already exists', GREEN)
        return
    bbpasswd = getpass("antocuni's bitbucket.org password:")
    content = HGRC_AUTH % bbpasswd
    with open(filename, 'w') as f:
        f.write(content)
    print color('Wrote ~/.hgrc.auth', YELLOW)

def clone_env():
    os.chdir(home)
    if os.path.exists('env'):
        print color('~/env already exists', GREEN)
        return
    print color('Cloning env...', YELLOW)
    url = 'https://bitbucket.org/antocuni/env'
    system('hg clone %s' % url)


def symlink(src, dst):
    # check if dst is already a symlink to src
    try:
        link = os.readlink(dst)
        if link == src:
            return # nothing to do
        if link.startswith('/home/antocuni/pypy/user/antocuni/') or\
           link.startswith('pypy/user/antocuni') or\
           not os.path.exists(link):
            # old location, kill it
            os.remove(dst)
    except OSError:
        pass
    os.symlink(src, dst)

def do_symlink(src, dst):
    try:
        print '    %s -> %s' % (src.replace(etc_dir, '.'), dst.replace(home, '~')),
        symlink(src, dst)
        print
    except Exception, msg:
        print color("Failed: %s" % (msg,), RED)

def create_symlinks():
    print color('Creating symlinks', YELLOW)
    for f in os.listdir(etc_dir):
        if (f.startswith('.') or
            f.endswith('~') or
            f.endswith('.pyc') or
            f in excludes):
            continue
        dst = os.path.join(home, '.' + f)
        src = os.path.join(etc_dir, f)
        src = os.path.abspath(src)
        do_symlink(src, dst)

    more_links = [
        ('~/env/src/pdb/pdbrc.py', '~/.pdbrc.py'),
        ('~/env/bin', '~/bin'),
        ('~/env/src', '~/src'),
        ('~/env/etc/gtk-3.0', '~/.config/gtk-3.0'),
        ]
    for src, dst in more_links:
        src = os.path.expanduser(src)
        dst = os.path.expanduser(dst)
        do_symlink(src, dst)


if __name__ == '__main__':
    write_hgrc_auth()
    clone_env()
    create_symlinks()


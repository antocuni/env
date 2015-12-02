#!/usr/bin/env python

import sys
import os.path
import glob
import subprocess
from getpass import getpass

GUI = '--gui' in sys.argv

REPOS = [
    ('hg', 'https://bitbucket.org/antocuni/env', '~/env'),
    ('hg', 'https://bitbucket.org/antocuni/fancycompleter', '~/src/fancycompleter'),
    ('hg', 'https://bitbucket.org/antocuni/wmctrl', '~/src/wmctrl'),
    ('hg', 'https://bitbucket.org/antocuni/pdb', '~/src/pdb'),
    ('hg', 'https://bitbucket.org/antocuni/pytest-emacs', '~/src/pytest-emacs'),
    ('hg', 'https://bitbucket.org/pypy/pyrepl', '~/src/pyrepl'),
]

APT_PACKAGES = ['emacs', 'git', 'build-essential', 'python-dev']
if GUI:
    APT_PACKAGES += ['wmctrl', 'libgtk2.0-dev', 'fonts-inconsolata']

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
env_dir = os.path.join(home, 'env')
etc_dir = os.path.join(env_dir, 'etc')
excludes = ['create_symlinks.py', 'scripts', 'elisp', 'gtk-3.0']

def system(cmd):
    ret = os.system(cmd)
    if ret != 0:
        print color('Command failed: ', RED), cmd
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

def clone_repos():
    print
    print color('Cloning repos:', YELLOW)
    for kind, url, dst in REPOS:
        if kind == 'hg':
            clone_hg_repo(url, dst)
        else:
            raise KeyError('unknown repo kind: %s' % kind)

def clone_hg_repo(url, dst):
    dst = os.path.expanduser(dst)
    if os.path.exists(dst):
        print '    %s: ' % dst, color('already exists', GREEN)
        return
    print '    %s: ' % dst, color('cloning from %s' % url, YELLOW)
    system('hg clone %s %s' % (url, dst))
    print

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
    print
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
        ('~/env/bin', '~/bin'),
        ('~/env/etc/gtk-3.0/gtk.css', '~/.config/gtk-3.0/gtk.css'),
        ('~/env/etc/bash_profile', '~/.profile'),
        ('~/env/etc/icons', '~/.icons'),
        ('~/src/pdb/pdbrc.py', '~/.pdbrc.py'),
        ]
    for src, dst in more_links:
        src = os.path.expanduser(src)
        dst = os.path.expanduser(dst)
        do_symlink(src, dst)

def apt_install():
    print
    packages = ' '.join(APT_PACKAGES)
    ret = os.system('dpkg -s %s >/dev/null 2>&1' % packages)
    if ret == 0:
        print color('apt packages: already installed', GREEN)
    else:
        print color('install apt-packages', YELLOW)
        system('sudo apt-get install %s' % packages)

def compile_terminal_hack():
    print
    print color('gnome-terminal-hack', YELLOW)
    dirname = os.path.join(home, 'env', 'src', 'gnome-terminal-hack')
    system('make -C %s' % dirname)

def import_dconf():
    print
    print color('import dconf settings', YELLOW)
    dirname = os.path.join(etc_dir, 'dconf')
    for filename in glob.glob('%s/*.sh' % dirname):
        print '    ', filename
        system(filename)

def install_desktop_apps():
    print
    print color('installing apps/*.desktop', YELLOW)
    dirname = os.path.join(env_dir, 'apps')
    for fullname in glob.glob('%s/*.desktop' % dirname):
        basename = os.path.basename(fullname)
        dst = os.path.join('~/.local/share/applications/', basename)
        dst = os.path.expanduser(dst)
        do_symlink(fullname, dst)

if __name__ == '__main__':
    write_hgrc_auth()
    clone_repos()
    create_symlinks()
    apt_install()
    if GUI:
        compile_terminal_hack()
        import_dconf()
        install_desktop_apps()
    elif 'SSH_CLIENT' not in os.environ:
        print color('WARNING: did you forget --gui?', RED)

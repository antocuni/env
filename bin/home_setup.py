#!/usr/bin/python3

# for ALT+` on gnome3: http://andrewpearson.org/?p=605
# gsettings set org.gnome.desktop.wm.keybindings switch-group "['disabled']"

import sys
import os.path
import glob
import subprocess
from pathlib import Path

# ==============================================================
# configuration
#

HOME = Path('~').expanduser()
ENV = HOME / 'env'
DOTFILES = ENV / 'dotfiles'
GUI_SENTINEL = HOME / '.gui'

REPOS = [
    ('git', 'https://github.com/pytest-dev/py', '~/src/py'),
    ('hg', 'https://bitbucket.org/antocuni/env', '~/env'),
    ('git', 'git@github.com:pdbpp/fancycompleter.git', '~/src/fancycompleter'),
    ('git', 'git@github.com:antocuni/wmctrl.git', '~/src/wmctrl'),
    ('git', 'git@github.com:pdbpp/pdbpp.git', '~/src/pdb'),
#    ('hg', 'https://bitbucket.org/antocuni/pytest-emacs', '~/src/pytest-emacs'),
#    ('hg', 'https://bitbucket.org/pypy/pyrepl', '~/src/pyrepl'),
]

APT_PACKAGES = ['emacs', 'git', 'build-essential', 'python-dev']
APT_PACKAGES_GUI = ['wmctrl', 'libgtk2.0-dev', 'fonts-inconsolata', 'xsel',
                    'hexchat']

#
# end of configuration
# ==============================================================

# misc utility functions
# ----------------------

RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34

def color(s, fg=1, bg=1):
    template = '\033[%02d;%02dm%s\033[0m'
    return template % (bg, fg, s)

def system(cmd):
    ret = os.system(cmd)
    if ret != 0:
        print(color('Command failed: ', RED), cmd)
        sys.exit(ret)

NO_SUDO = False
def sudo(cmd):
    if NO_SUDO:
        print(color('NO SUDO', RED))
    else:
        system('sudo ' + cmd)



def main():
    global NO_SUDO
    gui = '--gui' in sys.argv or GUI_SENTINEL.exists()
    NO_SUDO = '--nosudo' in sys.argv or '--no-sudo' in sys.argv
    clone_repos()
    create_symlinks()
    apt_install(APT_PACKAGES)
    if gui:
        GUI_SENTINEL.write_text('this file tells home_setup.py that this is a GUI environment\n')
        apt_install(APT_PACKAGES_GUI)
        apt_install_zeal()
        compile_terminal_hack()
        import_dconf()
        install_desktop_apps()
        check_sysrq()
    elif 'SSH_CLIENT' not in os.environ:
        print(color('WARNING: did you forget --gui?', RED))


def clone_repos():
    print()
    print(color('Cloning repos:', YELLOW))
    for kind, url, dst in REPOS:
        clone_one_repo(kind, url, dst)

def clone_one_repo(kind, url, dst):
    dst = os.path.expanduser(dst)
    if os.path.exists(dst):
        print('    %s: ' % dst, color('already exists', GREEN))
        return
    print('    %s: ' % dst, color('cloning from %s' % url, YELLOW))
    system('%s clone %s %s' % (kind, url, dst))
    print()

def symlink(src, dst):
    # check if dst is already a symlink to src
    try:
        link = dst.resolve()
        if link == src:
            return # nothing to do
        if not os.path.exists(link):
            # old location, kill it
            dst.unlink()
    except OSError:
        pass
    dst.symlink_to(src)


def do_symlink(src, dst):
    # create the destination dir if needed
    src = Path(src)
    dst = Path(dst)
    dstdir = dst.parent
    if not dstdir.exists():
        print(color('    mkdir %s' % dstdir, BLUE))
        dstdir.mkdir(parents=True)

    try:
        print('    %s -> %s' % (str(src).replace(str(DOTFILES), '.'),
                                str(dst).replace(str(HOME), '~')),
              end='')
        symlink(src, dst)
        print()
    except Exception as msg:
        print(color(" Failed: %s" % (msg,), RED))

def create_symlinks():
    print()
    print(color('Creating symlinks', YELLOW))
    for src in DOTFILES.iterdir():
        dst = HOME.joinpath('.' + src.name)
        if (src.name.startswith('.') or
            src.name.endswith('~') or
            src.name.endswith('.pyc')):
            continue
        if src.name.endswith('sshrc'):
            continue # this is handled by more_links
        do_symlink(src, dst)

    hexchat_dir = os.path.expanduser('~/.config/hexchat')
    if not os.path.exists(hexchat_dir):
        os.makedirs(hexchat_dir)
    more_links = [
        ('~/env/bin', '~/bin'),
        ('~/env/hacks/gnome-terminal-hack/gtk.css', '~/.config/gtk-3.0/gtk.css'),
        ('~/env/dotfiles/bash_profile', '~/.profile'),
        ('~/env/dotfiles/icons', '~/.icons'),
        ('~/env/dotfiles/sshrc', '~/.ssh/rc'),
        ('~/env/hacks/fijalcolor.py', '~/.config/hexchat/addons/fijalcolor.py'),
        ]
    for src, dst in more_links:
        src = Path(src).expanduser()
        dst = Path(dst).expanduser()
        do_symlink(src, dst)

def apt_install(package_list):
    packages = ' '.join(package_list)
    ret = os.system('dpkg -s %s >/dev/null 2>&1' % packages)
    if ret != 0:
        print()
        print(color('install apt-packages', YELLOW))
        sudo('apt-get install %s' % packages)

def apt_install_zeal():
    files = list(Path('/etc/apt/sources.list.d').glob('zeal-developers*'))
    if files:
        print(color('zeal ppa: already enabled', GREEN))
    else:
        print(color('zeal ppa: add-apt-repository', YELLOW))
        sudo('add-apt-repository ppa:zeal-developers/ppa')
        sudo('apt-get update')
    apt_install(['zeal'])

def compile_terminal_hack():
    print()
    print(color('gnome-terminal-hack', YELLOW))
    dirname = ENV / 'hacks/gnome-terminal-hack'
    system('make -C %s' % dirname)

def import_dconf():
    print()
    print(color('import dconf settings', YELLOW))
    dirname = ENV / 'dconf'
    for filename in dirname.glob('*.sh'):
        print('    ', filename)
        system(filename)

def install_desktop_apps():
    print()
    print(color('installing apps/*.desktop', YELLOW))
    dirname = ENV / 'apps'
    for fullname in dirname.glob('*.desktop'):
        basename = os.path.basename(fullname)
        dst = os.path.join('~/.local/share/applications/', basename)
        dst = os.path.expanduser(dst)
        do_symlink(fullname, dst)

def check_sysrq():
    def sysrq_enabled():
        out = subprocess.getoutput('sysctl -n kernel.sysrq')
        return int(out) == 1

    print()
    if not sysrq_enabled() and not NO_SUDO:
        print(color('kernel.sysrq is disabled, fixing it', YELLOW))
        system('echo kernel.sysrq = 1 | sudo tee /etc/sysctl.d/10-magic-sysrq.conf')
        sudo('sysctl --system')

    if sysrq_enabled():
        print(color('kernel.sysrq is enabled', GREEN))
    else:
        print(color('kernel.sysrq is disabled, plese look at it manually', RED))

if __name__ == '__main__':
    main()

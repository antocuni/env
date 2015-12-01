#!/bin/sh

set -xe

dconf load /org/gnome/settings-daemon/plugins/media-keys/ <<EOF
[/]
custom-keybindings=['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/emacs/', '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/terminal/']
[custom-keybindings/emacs]
binding='<Super>grave'
command="$HOME/bin/show.py emacs"
name='Emacs'
[custom-keybindings/terminal]
binding='Menu'
command="$HOME/bin/show.py term"
name='Terminal'
EOF

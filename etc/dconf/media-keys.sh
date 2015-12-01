#!/bin/sh

# apparently, if these keys are already in dconf and you overwrite them, the
# keybingings stop to work and you need to logout and login to make them
# working again. Workaround :(
if dconf dump /org/gnome/settings-daemon/plugins/media-keys/ | grep -q emacs
then
    echo media-keys keybingings already installed, skipping
    exit
fi

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

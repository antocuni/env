#!/bin/sh

dconf load /org/gnome/desktop/wm/keybindings/ <<EOF
[/]
toggle-maximized=['<Alt>z']
EOF

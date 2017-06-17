#!/bin/sh

dconf load / <<EOF

[org/gnome/terminal/legacy]
new-terminal-mode='tab'
tab-position='bottom'

[org/gnome/terminal/legacy/keybindings]
prev-tab='<Super>Left'
move-tab-right='<Alt><Super>Right'
next-tab='<Super>Right'
move-tab-left='<Alt><Super>Left'

EOF

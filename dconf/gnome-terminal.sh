#!/bin/sh

dconf load / <<EOF

[org/gnome/terminal/legacy]
new-terminal-mode='tab'
tab-position='bottom'

EOF

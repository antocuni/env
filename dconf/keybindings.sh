#!/bin/sh

dconf load / <<EOF
# ===============================#
#        custom shortcuts        #
# ===============================#

[org/compiz/integrated]

run-command-1=['<Super>grave']
command-1="$HOME/bin/show.py emacs"

run-command-2=['Menu']
command-2="$HOME/bin/show.py term"

run-command-3=['<Shift><Control>c']
command-3="$HOME/bin/pastebin-from-xsel"

show-hud=['<Alt>Menu']


# ===============================#
#    window manager shortcuts    #
# ===============================#

[org/gnome/desktop/wm/keybindings]
toggle-maximized=['<Alt>z']

EOF

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

show-hud=['<Alt>Menu']


# ===============================#
#    window manager shortcuts    #
# ===============================#

[org/gnome/desktop/wm/keybindings]
toggle-maximized=['<Alt>z']

EOF

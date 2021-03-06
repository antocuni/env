#!/bin/sh

dconf load / <<EOF
# ===============================#
#        custom shortcuts        #
# ===============================#

[org/compiz/integrated]

show-hud=['<Alt>Menu']

run-command-1=['<Super>grave']
command-1="$HOME/bin/show.py emacs"

run-command-2=['Menu']
command-2="$HOME/bin/show.py term"

run-command-3=['<Shift><Control>c']
command-3="$HOME/bin/pastebin-from-xsel"

run-command-4=['XF86Messenger']
command-4="$HOME/bin/show.py xchat"

run-command-5=['<Control>F1']
command-5="$HOME/bin/show.py zeal"

run-command-6=['Print']
command-6='gnome-screenshot -a -c'

run-command-7=['XF86Sleep']
command-7='systemctl suspend'

run-command-8=['XF86AudioPlay']
command-8='$HOME/bin/spotify-cmd play'

run-command-9=['XF86AudioNext']
command-9='$HOME/bin/spotify-cmd next'

run-command-10=['XF86AudioPrev']
command-10='$HOME/bin/spotify-cmd prev'

run-command-11=['XF86AudioStop']
command-11='$HOME/bin/spotify-cmd stop'

run-command-12=['XF86AudioLowerVolume']
command-12='amixer -q sset Master 3%-'

run-command-13=['XF86AudioRaiseVolume']
command-13='amixer -q sset Master 3%+'

run-command-5=['<Control>F2']
command-5="$HOME/bin/reposition-windows.py"


# ===============================#
#    window manager shortcuts    #
# ===============================#

[org/gnome/desktop/wm/keybindings]
toggle-maximized=['<Alt>z']

# resize window with Alt+Right mouse button
[org/gnome/desktop/wm/preferences]
mouse-button-modifier='<Alt>'
resize-with-right-button=true

[org/compiz/profiles/unity/plugins/resize]
rectangle-modifier=@ai []
fill-color='#fb8b0046'
centered-modifier=[0]
mode=2


EOF

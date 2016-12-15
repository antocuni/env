#!/bin/sh

dconf load / <<EOF

# ====================================================
#   disable unity switcher and enable compiz switcher
# ====================================================

# add switcher to the active plugins; XXX: it would be nice if there was a way
# to just "add" it, instead of overriding everything
[org/compiz/profiles/unity/plugins/core]
active-plugins=['core', 'composite', 'opengl', 'vpswitch', 'wall', 'grid', 'mousepoll', 'place', 'commands', 'regex', 'resize', 'move', 'copytex', 'imgpng', 'snap', 'compiztoolbox', 'session', 'animation', 'expo', 'unitymtgrabhandles', 'fade', 'ezoom', 'workarounds', 'scale', 'switcher', 'unityshell']

# compiz switcher settings
[org/compiz/profiles/unity/plugins/switcher]
background-color='#fff9a58e'
use-background-color=true
zoom=0.0
mipmap=false

# disable unity switcher
[org/compiz/profiles/unity/plugins/unityshell]
alt-tab-forward-all='Disabled'
alt-tab-prev-all='Disabled'
alt-tab-forward='Disabled'
alt-tab-prev='Disabled'

EOF

#!/bin/bash

echo "Please use toggle-theme for kitty"
exit

PROF=/org/gnome/terminal/legacy/profiles:

DEFAULT=$PROF/:b1dcc9dd-5262-4d8d-a863-c897e6d979b9
DARK=$PROF/:7afc3a38-768f-4d09-b96e-083f2b866152
LIGHT=$PROF/:454cc147-1870-4455-bde8-55809317b591

CURRENT=`dconf read $DEFAULT/visible-name`
if [ $CURRENT = "'Default-Dark'" ]
then
    echo "Dark ==> Light"
    #kitty +kitten themes --reload-in=all Atom One Light
    #kitty +kitten themes --reload-in=all 1984 Light
    kitty +kitten themes --cache-age=-1 --reload-in=all Alabaster

    dconf dump $LIGHT/ | dconf load $DEFAULT/
    dconf write $DEFAULT/visible-name "'Default-Light'"
    cat > /tmp/gitconfig_colordiff <<EOF
# this file has been generated by ~/bin/switch-gnome-terminal-profile.sh
[color "diff"]
  meta = "#000000" bold
  frag = red bold
  old = "#000000" "#dddddd" # black over gray
  new = "#000000" "#bbffbb" # black over pastel green
EOF

else
    echo "Light ==> Dark"
    kitty +kitten themes --cache-age=-1 --reload-in=all Default

    dconf dump $DARK/ | dconf load $DEFAULT/
    dconf write $DEFAULT/visible-name "'Default-Dark'"
    rm -f /tmp/gitconfig_colordiff
fi

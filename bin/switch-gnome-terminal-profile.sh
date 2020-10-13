#!/bin/bash

PROF=/org/gnome/terminal/legacy/profiles:

DEFAULT=$PROF/:b1dcc9dd-5262-4d8d-a863-c897e6d979b9
DARK=$PROF/:7afc3a38-768f-4d09-b96e-083f2b866152
LIGHT=$PROF/:454cc147-1870-4455-bde8-55809317b591

CURRENT=`dconf read $DEFAULT/visible-name`
if [ $CURRENT = "'Default-Dark'" ]
then
    echo "Dark ==> Light"
    dconf dump $LIGHT/ | dconf load $DEFAULT/
    dconf write $DEFAULT/visible-name "'Default-Light'"
else
    echo "Light ==> Dark"
    dconf dump $DARK/ | dconf load $DEFAULT/
    dconf write $DEFAULT/visible-name "'Default-Dark'"
fi

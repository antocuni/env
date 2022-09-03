#!/bin/bash

# this command must be used AFTER the first boot, because it assumes that the
# home directory has already been created. As such, these ssh/scp commands
# will use password authentication

if [ "$#" -eq 0 ]; then
    echo "Usage:  ./post_boot_setup.sh ADDRESS"
    echo "  e.g.  ./post_boot_setup.sh mypi.local"
    exit 1
fi

ADDRESS=$1

function install_ssh_keys() {
    ssh ${ADDRESS} bash -c "'mkdir -p ~/.ssh'"
    cat ~/.ssh/id_rsa.pub | ssh ${ADDRESS} "cat > ~/.ssh/authorized_keys"
}

function fix_locale() {
    # this fixes the annoying warning:
    #     perl: warning: Setting locale failed.
    #
    # To solve it, we need to generate some locales; these are the ones which
    # I found I need with my current setup, you might need to tweak the script
    # if you keep seeing the warning.
    #
    #
    (cat <<EOF
it_IT.UTF-8 UTF-8
en_GB.UTF-8 UTF-8
EOF
    ) | ssh ${ADDRESS} sudo tee -a /etc/locale.gen
    ssh ${ADDRESS} sudo /usr/sbin/locale-gen
}

install_ssh_keys
fix_locale

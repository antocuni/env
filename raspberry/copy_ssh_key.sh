#!/bin/bash

# this command must be used AFTER the first boot, because it assumes that the
# home directory has already been created. As such, these ssh/scp commands
# will use password authentication

if [ "$#" -eq 0 ]; then
    echo "Usage:  ./copy_ssh_keys.sh ADDRESS"
    echo "  e.g.  ./copy_ssh_keys.sh mypi.local"
    exit 1
fi

ADDRESS=$1

ssh ${ADDRESS} bash -c "'mkdir -p ~/.ssh'"
cat ~/.ssh/id_rsa.pub | ssh ${ADDRESS} "cat > ~/.ssh/authorized_keys"

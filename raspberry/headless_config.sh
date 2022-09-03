#!/bin/bash

# perform a headless setup of a freshly-flashed raspbian image. It assumes
# that the two image partitions have been mounted on
# /media/$USER/{boot,rootfs}

# some docs can be found here:
# https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi
# https://www.raspberrypi.com/documentation/computers/configuration.html#boot-folder-contents


BOOT=/media/$USER/boot
ROOTFS=/media/$USER/rootfs

mountpoint $BOOT || exit
mountpoint $ROOTFS || exit

function setup_user() {
    # create an user for the rpi. Change the following line to tweak the settings
    # The default is the same username as the one executing this command
    pi_user=$USER
    #pi_user="pi"

    echo
    echo "Creating user: ${pi_user}"
    read -s -p "Password: " password
    hash=$(echo $password | openssl passwd -6 -stdin)
    echo "${pi_user}:${hash}" > ${BOOT}/userconf.txt
    echo "Wrote ${BOOT}/userconf.txt"
}

function setup_wifi() {
    echo

    if [ -f "wpa_supplicant.conf" ]; then
        echo "cp wpa_supplicant.conf $BOOT"
        cp wpa_supplicant.conf $BOOT
    else
        echo "ERROR: wpa_supplicant.conf not found"
        echo "you can create one by copying & adapting wpa_supplicant.conf.template"
        exit 1
    fi

    touch "${BOOT}/ssh"
    echo "Wrote ${BOOT}/ssh"
}

function setup_hostname() {
    # inspired by:
    # https://raspberrypi.stackexchange.com/a/116575

    ETC=${ROOTFS}/etc
    old_hostname=$(cat ${ETC}/hostname)
    echo
    echo "Current hostname: ${old_hostname}"
    read -p "New hostname (empty to keep the current one): " new_hostname
    if [ -z ${new_hostname} ]; then
        echo "keeping the existing hostname, nothing to do"
        return
    fi

    echo "Setting the hostname to ${new_hostname}, requiring sudo"
    echo $new_hostname | sudo tee ${ETC}/hostname
    sudo sed -i "/127.0.1.1/s/${old_hostname}/${new_hostname}/" ${ETC}/hosts
}


setup_user
setup_wifi
setup_hostname

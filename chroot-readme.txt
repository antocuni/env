# here we are in the host system

$ mkdir jammy-22.04
$ sudo debootstrap jammy jammy-22.04 http://archive.ubuntu.com/ubuntu
$ sudo chroot jammy-22.04/ /bin/bash

# === now we are inside the chroot (and we enter as root) ===

$ # add "universe" to sources.list
$ nano /etc/apt/sources.list
deb http://archive.ubuntu.com/ubuntu jammy main
deb http://archive.ubuntu.com/ubuntu jammy universe

$ apt update
$ apt install mg

$ mg /etc/locale.gen
it_IT.UTF-8 UTF-8
en_GB.UTF-8 UTF-8
en_US.UTF-8 UTF-8

$ locale-gen

$ addgroup antocuni --gid 1020
$ adduser antocuni --uid 1020 --gid 1020

$ echo "antocuni ALL=(ALL:ALL) ALL" >> /etc/sudoers

$ exit

# ===========================

To enter the chroot, run:

$ ./chroot.sh

# === now we are inside the chroot and everything should work as expected

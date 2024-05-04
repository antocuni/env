mount_bind_maybe() {
    local src="$1"
    local dst="$2"

    # Check if the mountpoint is already mounted
    if ! grep -qs "${dst}" /proc/mounts; then
        echo sudo mount --bind "${src}" "${dst}"
        sudo mount --bind "${src}" "${dst}"
    else
        echo "${dst}: already mounted."
    fi
}

mount_bind_maybe /dev/pts /home/acuni/jammy-22.04/dev/pts
mount_bind_maybe /proc /home/acuni/jammy-22.04/proc

if [[ "$1" == "--root" ]]; then
    # enter as root
    sudo chroot jammy-22.04/ /bin/bash
else
    # enter as antocuni
    sudo chroot jammy-22.04/ env SSH_CONNECTION="$SSH_CONNECTION" SSH_CLIENT="$SSH_CLIENT" su --whitelist-environment=SSH_CONNECTION,SSH_CLIENT --login antocuni
fi

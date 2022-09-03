To setup a new raspian SD card:

1. download raspian
2. ./flash.sh
3. mount /boot and /rootfs
4. ./headless_setup.sh
5. umount /boot and /rootfs
6. insert SD card in the rpi and boot
7. (optional) once booted, ./post_boot_setup.sh
8. (optional): "sudo apt remove man-db --purge"

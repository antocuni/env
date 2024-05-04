function disable() {
    grep "$1.*enabled" < /proc/acpi/wakeup >/dev/null && echo "$1" | sudo tee /proc/acpi/wakeup
}

# originally, these were enabled
# GLAN	  S4	*enabled   pci:0000:00:1f.6
# XHC	  S3	*enabled   pci:0000:00:14.0
# RP01	  S4	*enabled   pci:0000:00:1c.0
# RP05	  S4	*enabled   pci:0000:00:1c.4
# RP09	  S4	*enabled   pci:0000:00:1d.0
# PXSX	  S4	*enabled   pci:0000:05:00.0
# SLPB	  S3	*enabled   platform:PNP0C0E:00
# LID	  S4	*enabled   platform:PNP0C0D:00


disable GLAN
disable XHC
disable RP01
disable RP05
disable RP09
disable PXSX
echo
cat /proc/acpi/wakeup | grep enabled

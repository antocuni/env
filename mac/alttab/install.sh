#!/bin/sh
set -e
if [ "$(uname -s)" != Darwin ]; then
    echo "alttab/install.sh: macOS only" >&2
    exit 1
fi
here=$(cd "$(dirname "$0")" && pwd)
defaults import com.lwouis.alt-tab-macos "$here/alttab.plist"
echo "Imported AltTab settings. Quit and relaunch AltTab to apply."

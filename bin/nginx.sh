#!/bin/bash

# https://gist.github.com/asterite3/89236d1753a669e173531aca4b87afdc
# Bash script to run nginx on command line as regular (non-root) user to serve
# files from current directory (using current folder as doc-root, a
# replacement for python -m SimpleHTTPServer)

# Usage:
# ./nginx.sh
# ./nginx.sh 8888
# ./nginx.sh 0.0.0.0 8080

set -e

#HOST="127.0.0.1"
HOST="0.0.0.0"
PORT="8000"

if [ ! -z "$1" ] ; then
    if [  -z "$2" ] ; then
        PORT="$1"
    else
        HOST="$1"
        PORT="$2"
    fi
fi

echo Serving $PWD in $HOST:$PORT

CONFIG_PATH=`mktemp`
PID_FILE=`mktemp`

exec 3<"$CONFIG_PATH"
exec 4>"$PID_FILE"

rm "$PID_FILE"

if [ -f "/etc/nginx/mime.types" ]; then
    MIME_TYPES_INCLUDE="include /etc/nginx/mime.types;"
fi

cat << EOF > "$CONFIG_PATH"
daemon off;
worker_processes auto;
pid /dev/fd/4;
error_log /dev/stderr;
events {}
http {
    $MIME_TYPES_INCLUDE
    access_log /dev/stdout;
    server {
        listen $HOST:$PORT;
        location / {
            autoindex on;
            autoindex_exact_size off;
            root .;
        }
    }
}
EOF
rm "$CONFIG_PATH"

exec nginx -p . -c "/dev/fd/3"

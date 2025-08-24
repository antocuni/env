#!/usr/bin/python3

import sys
import argparse
import socket
import json

HOST, PORT = "localhost", 4242

def main():
    parser = argparse.ArgumentParser(
        description="Send a command to local_server.py"
    )
    parser.add_argument("--wait", action="store_true",
                        help="wait for a reply from the server (30s timeout)")
    parser.add_argument("command", nargs=argparse.REMAINDER,
                        help="command and args to send, e.g. ping or xdg-open <file>")
    args = parser.parse_args()

    if not args.command:
        parser.error("no command provided")

    payload = json.dumps(args.command).encode("utf-8")

    try:
        # connect with a short connect timeout
        with socket.create_connection((HOST, PORT), timeout=5) as sock:
            if args.wait:
                # we might read a response; set a 30s overall read timeout
                sock.settimeout(30)

            # send request
            sock.sendall(payload)

            if not args.wait:
                # fire-and-forget: close and exit
                return 0

            # tell the server we're done sending but keep the socket open for reading
            try:
                sock.shutdown(socket.SHUT_WR)
            except OSError:
                # if shutdown not supported or already closed, proceed to read anyway
                pass

            # receive until EOF or timeout
            chunks = []
            try:
                while True:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    chunks.append(chunk)
            except socket.timeout:
                print("Timed out waiting for server reply (30s).", file=sys.stderr)
                return 3

            if chunks:
                sys.stdout.write(b"".join(chunks).decode("utf-8", errors="replace"))
            return 0

    except (OSError, ConnectionError) as e:
        print(str(e), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())

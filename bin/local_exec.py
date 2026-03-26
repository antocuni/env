#!/usr/bin/python3

import sys
import json
import socket
import argparse
from urllib.request import urlopen, Request
from urllib.parse import quote

HOST, PORT = "localhost", 4242
SERVER = f"http://{HOST}:{PORT}"

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

    cmd = args.command[0]
    cmd_args = args.command[1:]

    # Build the URL: /CMD?arg0=val0&arg1=val1&...
    # For "e" command: /e?file=FILE&line=LINE (special handling for +LINE syntax)
    if cmd == "e":
        params = []
        filepath = None
        line = None
        for a in cmd_args:
            if a.startswith("+"):
                line = a[1:]
            else:
                filepath = a
        if not filepath:
            print("e: missing file argument", file=sys.stderr)
            return 1
        url = f"{SERVER}/e?file={quote(filepath)}"
        if line:
            url += f"&line={quote(line)}"
    else:
        # Generic: POST /exec with JSON body
        url = f"{SERVER}/exec"

    if args.wait:
        try:
            if cmd == "e":
                req = Request(url)
            else:
                payload = json.dumps(args.command).encode("utf-8")
                req = Request(url, data=payload, headers={"Content-Type": "application/json"})
            resp = urlopen(req, timeout=30)
            body = resp.read().decode("utf-8", errors="replace")
            if body:
                sys.stdout.write(body)
                if not body.endswith("\n"):
                    sys.stdout.write("\n")
            return 0
        except Exception as e:
            print(str(e), file=sys.stderr)
            return 2
    else:
        # Fire-and-forget: send raw HTTP request over a socket and close
        try:
            path = url[len(SERVER):]
            if cmd == "e":
                raw = f"GET {path} HTTP/1.0\r\nConnection: close\r\n\r\n"
            else:
                payload = json.dumps(args.command)
                raw = (
                    f"POST {path} HTTP/1.0\r\n"
                    f"Content-Type: application/json\r\n"
                    f"Content-Length: {len(payload)}\r\n"
                    f"Connection: close\r\n"
                    f"\r\n"
                    f"{payload}"
                )
            sock = socket.create_connection((HOST, PORT), timeout=5)
            sock.sendall(raw.encode("utf-8"))
            sock.close()
            return 0
        except (OSError, ConnectionError) as e:
            print(str(e), file=sys.stderr)
            return 2

if __name__ == "__main__":
    sys.exit(main())

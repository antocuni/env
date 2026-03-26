#!/usr/bin/env python3

import subprocess
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime


def log(*args, **kwargs):
    """Print a log message with timestamp."""
    timestamp = datetime.now().strftime("[%H:%M]")
    print(timestamp, *args, **kwargs)


def dispatch(argv):
    """
    Dispatch a command. Returns (status, body).
    """
    if not argv:
        return 400, "no command"

    cmd = argv[0]
    log("[exec]", " ".join(argv))

    if cmd in ("aplay", "e", "xdg-open"):
        subprocess.run(argv)
        return 200, "ok"

    dispatch_table = {
        "ping": cmd_ping,
        "sleep": cmd_sleep,
        "sleep_hook": cmd_sleep_hook,
    }
    func = dispatch_table.get(cmd)
    if func is None:
        return 404, f"Invalid command: {cmd}"
    return func(*argv[1:])


def cmd_ping(*args):
    import time; time.sleep(2)
    pong = ('pong',) + args
    return 200, " ".join(pong)


def cmd_sleep(x):
    x = float(x)
    time.sleep(x)
    return 200, "OK"


def cmd_sleep_hook(phase, sleep_type):
    if phase == 'pre':
        return 200, 'goodnight'
    if phase == 'post' and sleep_type == 'suspend':
        log('[resume]', 'waiting for 10 seconds...')
        time.sleep(10)
        auto_xrandr()
        return 200, 'good morning'
    return 200, "ok"


class UtilsHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        log("[http]", format % args)

    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)

        if parsed.path == "/e":
            filepath = qs.get("file", [None])[0]
            line = qs.get("line", [None])[0]
            if not filepath:
                self._reply(400, "missing 'file' parameter")
                return
            argv = ["e"]
            if line:
                argv.append(f"+{line}")
            argv.append(filepath)
            status, body = dispatch(argv)
            self._reply(status, body)
        else:
            self._reply(404, f"unknown route: {parsed.path}")

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/exec":
            content_length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(content_length)
            try:
                argv = json.loads(raw.decode("utf-8"))
            except Exception as e:
                self._reply(400, f"Invalid JSON: {e}")
                return
            status, body = dispatch(argv)
            self._reply(status, body)
        else:
            self._reply(404, f"unknown route: {parsed.path}")

    def _reply(self, status, body):
        try:
            self.send_response(status)
            self.send_header("Content-Type", "text/plain")
            encoded = body.encode("utf-8")
            self.send_header("Content-Length", len(encoded))
            self.end_headers()
            self.wfile.write(encoded)
        except BrokenPipeError:
            pass  # client already disconnected (fire-and-forget)


def auto_xrandr():
    """
    run auto-xrandr.py, and reposition-windows.py ONLY if we switched
    screen config
    """
    def get_config():
        try:
            with open('/tmp/antocuni-screen-config') as f:
                return f.read().strip()
        except IOError:
            return 'none'

    old_config = get_config()
    log('[screen]', f'current screen config: {old_config}, running auto-xrandr.py')
    subprocess.run('auto-xrandr.py')
    new_config = get_config()

    if old_config == new_config:
        log('[screen]', f'screen config unchanged')
    else:
        log('[screen]', f'{old_config} => {new_config}, running reposition-windows.py')
        subprocess.run('reposition-windows.py')



if __name__ == "__main__":
    HOST, PORT = "localhost", 4242
    server = HTTPServer((HOST, PORT), UtilsHandler)
    server.allow_reuse_address = True
    log(f"Listening on {HOST}:{PORT}")
    server.serve_forever()

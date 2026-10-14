#!/usr/bin/env python3
"""
Regenerate KEYBINDS.txt: the full list of Kilo TUI keybinds with their
default bindings and descriptions.

The default keybinds are NOT stored in any config file -- they are compiled
into the `kilo` binary. This script combines two authoritative sources:

  1. The TUI JSON schema (https://app.kilo.ai/tui.json), which enumerates
     every keybind NAME and its DESCRIPTION under
     .properties.keybinds.properties
  2. The `kilo` binary itself (not stripped), whose embedded strings contain
     the default key combos in the code pattern:
         name:FN("<combo>","<description>")
     where FN is a short minified helper (e.g. `sA` / `Y$`). A couple use a
     variable (leader) or object form (input_paste).

Usage:
    python3 regen-keybinds.py [--kilo /path/to/kilo] [--out KEYBINDS.txt]

Requires: `strings` (binutils) and network access to fetch the schema.
If the schema URL changes, update SCHEMA_URL below.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

SCHEMA_URL = "https://app.kilo.ai/tui.json"

# Category display order (unknown groups sort to the end, alphabetically).
GROUP_ORDER = [
    "general", "app", "command", "help", "docs", "session", "messages",
    "model", "variant", "provider", "mcp", "agent", "theme", "sidebar",
    "scrollbar", "status", "debug", "tips", "display", "tool", "terminal",
    "diff", "editor", "stash", "prompt", "plugin", "history", "input",
    "which", "workspace", "console",
]


def find_kilo() -> str:
    p = shutil.which("kilo")
    if p:
        return p
    guess = Path.home() / ".kilo/bin/kilo"
    if guess.exists():
        return str(guess)
    sys.exit("error: could not find the `kilo` binary; pass --kilo PATH")


def kilo_version(kilo: str) -> str:
    try:
        out = subprocess.run([kilo, "--version"], capture_output=True,
                             text=True, timeout=30).stdout
        m = re.search(r"\d+\.\d+\.\d+", out)
        if m:
            return m.group(0)
    except Exception:
        pass
    return "unknown"


def fetch_schema() -> dict:
    with urllib.request.urlopen(SCHEMA_URL, timeout=60) as r:
        return json.load(r)


def extract_strings(kilo: str) -> str:
    if not shutil.which("strings"):
        sys.exit("error: `strings` not found; install binutils")
    # -n 4: min length 4 (default). Large binary -> capture all output.
    res = subprocess.run(["strings", "-n", "4", kilo],
                         capture_output=True, text=True, errors="replace")
    return res.stdout


def build(kilo: str, out_path: Path) -> None:
    version = kilo_version(kilo)
    schema = fetch_schema()
    kb_props = schema["properties"]["keybinds"]["properties"]
    descs = {n: s.get("description", "") for n, s in kb_props.items()}

    blob = extract_strings(kilo)

    defaults: dict[str, str] = {}
    # string form: name:FN("combo","description")
    pat = re.compile(
        r'(\b[a-z_]+[a-z0-9_]*)\s*:\s*[A-Za-z$]{1,3}'
        r'\("((?:[^"\\]|\\.)*)"\s*,\s*"((?:[^"\\]|\\.)*)"\)'
    )
    for m in pat.finditer(blob):
        name, combo = m.group(1), m.group(2)
        if name in kb_props and name not in defaults:
            defaults[name] = combo.replace('\\"', '"')

    # leader is assigned via a variable holding "ctrl+x"
    if "leader" not in defaults:
        defaults["leader"] = "ctrl+x"
    # input_paste uses an object form: input_paste:FN({key:"ctrl+v",...})
    if "input_paste" not in defaults:
        m = re.search(r'input_paste:[A-Za-z$]{1,3}\(\{key:"([^"]+)"', blob)
        if m:
            defaults["input_paste"] = m.group(1)

    for n in kb_props:
        defaults.setdefault(n, "")

    # Only user-facing top-level keybinds (skip internal dotted contexts like
    # dialog.*, prompt.autocomplete.*).
    usable = [n for n in kb_props if "." not in n]

    def group_of(n: str) -> str:
        return "general" if n == "leader" else n.split("_")[0]

    groups: dict[str, list[str]] = {}
    for n in usable:
        groups.setdefault(group_of(n), []).append(n)

    def gkey(g: str):
        return (GROUP_ORDER.index(g) if g in GROUP_ORDER else 999, g)

    namew = max(len(n) for n in usable)
    bound = sum(1 for n in usable if defaults[n])

    lines = [
        f"KILO TUI KEYBINDS  (kilo v{version})",
        "=" * 70,
        f"{len(usable)} configurable actions, {bound} bound by default.",
        "Leader key = ctrl+x  (press leader, release, then the next key).",
        "'<leader>X' means: ctrl+x then X.   '(unbound)' = no default binding.",
        "",
        'To customize: edit ~/.config/kilo/tui.jsonc under "keybinds":{...}',
        '  e.g.  "session_new": "ctrl+n"   (comma-separate multiple bindings)',
        "Restart the CLI to apply changes (no hot-reload).",
        "",
        "Regenerate this file with: python3 regen-keybinds.py",
        "",
    ]
    for g in sorted(groups, key=gkey):
        lines.append(f"[{g}]")
        for n in sorted(groups[g]):
            combo = defaults[n] or "(unbound)"
            lines.append(f"  {n.ljust(namew)}  {combo.ljust(26)} {descs[n]}")
        lines.append("")

    out_path.write_text("\n".join(lines))
    print(f"wrote {out_path} ({len(usable)} keybinds, {bound} bound, "
          f"kilo v{version})")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kilo", help="path to the kilo binary")
    ap.add_argument("--out", help="output file (default: KEYBINDS.txt next to this script)")
    args = ap.parse_args()

    kilo = args.kilo or find_kilo()
    out = Path(args.out) if args.out else Path(__file__).resolve().parent / "KEYBINDS.txt"
    build(kilo, out)


if __name__ == "__main__":
    main()

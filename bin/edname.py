#!/usr/bin/env python3

import os
import sys
import readline

def main():
    if len(sys.argv) != 2:
        print("Usage: edname.py <filename>")
        sys.exit(1)

    original = sys.argv[1]

    if not os.path.exists(original):
        print(f"Error: file '{original}' does not exist.")
        sys.exit(1)

    # Prefill current filename and allow editing
    def prefill_hook():
        readline.insert_text(original)
        readline.redisplay()
    readline.set_pre_input_hook(prefill_hook)

    try:
        new_name = input("🖊️ ").strip()
    finally:
        readline.set_pre_input_hook()  # clear hook

    if not new_name:
        print("Error: empty name not allowed.")
        sys.exit(1)

    if new_name == original:
        print("No changes made.")
        sys.exit(0)

    if os.path.exists(new_name):
        print(f"Error: file '{new_name}' already exists.")
        sys.exit(1)

    os.rename(original, new_name)
    print(f"Renamed '{original}' to '{new_name}'.")

if __name__ == "__main__":
    main()

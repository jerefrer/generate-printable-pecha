#!/usr/bin/env python3

import sys

def run_gui():
    import lib.ui

def run_cli():
    import lib.command_line

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_gui()
#!/usr/bin/env python3
"""Repository convenience entry point; the portable skill owns the implementation."""
from pathlib import Path
import runpy

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).resolve().parents[1] / 'skills' /
                       'hermes-free-first-setup' / 'scripts' / 'setup_free_first.py'),
                   run_name='__main__')

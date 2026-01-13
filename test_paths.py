#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script to check paths"""

from pathlib import Path
import os

print("=" * 60)
print("PATH TESTING")
print("=" * 60)

# Get current file location
current_file = Path(__file__).absolute()
print(f"Current file: {current_file}")

# Get parent directory
parent_dir = current_file.parent
print(f"Parent directory: {parent_dir}")

# Check for required files
venv_python = parent_dir / "venv" / "Scripts" / "python.exe"
run_py = parent_dir / "run.py"

print(f"\nChecking files:")
print(f"  venv/Scripts/python.exe: {venv_python}")
print(f"    Exists: {venv_python.exists()}")
print(f"  run.py: {run_py}")
print(f"    Exists: {run_py.exists()}")

print(f"\nCurrent working directory: {os.getcwd()}")

print("=" * 60)
input("Press Enter to exit...")


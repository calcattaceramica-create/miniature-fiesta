#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify launcher functionality
"""

import subprocess
from pathlib import Path

# Test paths
app_dir = Path(r"C:\Users\DELL\Desktop\DED_App")
python_exe = app_dir / "venv" / "Scripts" / "python.exe"
run_py = app_dir / "run.py"

print(f"App directory: {app_dir}")
print(f"App directory exists: {app_dir.exists()}")
print(f"Python exe: {python_exe}")
print(f"Python exe exists: {python_exe.exists()}")
print(f"run.py: {run_py}")
print(f"run.py exists: {run_py.exists()}")

if python_exe.exists() and run_py.exists():
    print("\n✅ All files found!")
    print("\nTrying to start Flask...")
    
    try:
        process = subprocess.Popen(
            [str(python_exe), str(run_py)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(app_dir),
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        print(f"✅ Process started with PID: {process.pid}")
        print("Waiting 3 seconds...")
        import time
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Process is still running!")
            print("Terminating process...")
            process.terminate()
            process.wait()
            print("✅ Process terminated")
        else:
            print(f"❌ Process exited with code: {process.returncode}")
            stdout, stderr = process.communicate()
            print(f"STDOUT: {stdout.decode('utf-8', errors='ignore')}")
            print(f"STDERR: {stderr.decode('utf-8', errors='ignore')}")
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("\n❌ Some files are missing!")


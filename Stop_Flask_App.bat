@echo off
taskkill /F /FI "WINDOWTITLE eq *run.py*" /T 2>nul
taskkill /F /FI "COMMANDLINE eq *run.py*" /T 2>nul


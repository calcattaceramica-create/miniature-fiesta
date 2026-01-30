@echo off
cd /d "%~dp0"

echo Starting DED ERP Application...
echo URL: http://localhost:5000
echo Username: admin
echo Password: admin123
echo.
echo Keep this window open!
echo Press CTRL+C to stop
echo.

"%~dp0venv\Scripts\python.exe" "%~dp0start.py"

pause


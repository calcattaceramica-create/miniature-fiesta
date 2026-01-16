@echo off
REM ========================================
REM DED ERP System - Background Server
REM ========================================

echo.
echo ========================================
echo Starting DED ERP Server in Background
echo ========================================
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Start the server in a hidden window
start /B pythonw run_production.py

echo Server started in background!
echo.
echo Server URL: http://localhost:5000
echo Username: admin
echo Password: admin123
echo.
echo To stop the server, use stop_server.bat
echo.
pause


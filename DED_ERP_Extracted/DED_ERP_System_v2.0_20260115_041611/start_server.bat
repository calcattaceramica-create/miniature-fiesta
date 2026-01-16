@echo off
chcp 65001 >nul
title DED ERP System v2.0 - Server

echo.
echo ================================================================================
echo   DED ERP System v2.0 - Starting Server
echo ================================================================================
echo.

echo [1/3] Clearing Python cache (to ensure latest code is used)...
echo.

REM Clear __pycache__ directories
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    rd /s /q "%%d" 2>nul
    echo       Cleared: %%d
)

REM Clear .pyc files
del /s /q *.pyc 2>nul

echo.
echo       Done! Cache cleared.
echo.

echo [2/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo.
echo [3/3] Starting Flask server...
echo.
echo ================================================================================
echo   Server Information:
echo   - URL: http://127.0.0.1:5000
echo   - Default User: admin
echo   - Press Ctrl+C to stop the server
echo ================================================================================
echo.

python run.py

if errorlevel 1 (
    echo.
    echo ================================================================================
    echo   ERROR: Server failed to start!
    echo ================================================================================
    echo.
    echo Possible solutions:
    echo   1. Make sure all dependencies are installed: pip install -r requirements.txt
    echo   2. Check if port 5000 is already in use
    echo   3. Check the error message above
    echo.
    pause
    exit /b 1
)

pause


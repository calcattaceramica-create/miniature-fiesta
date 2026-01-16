@echo off
title DED ERP Server - Keep This Window Open!
color 0A
cls

echo.
echo ========================================
echo    DED ERP System Server
echo ========================================
echo.
echo [*] Starting server...
echo.
echo Server URL: http://localhost:5000
echo Username: admin
echo Password: admin123
echo.
echo ========================================
echo   IMPORTANT: DO NOT CLOSE THIS WINDOW!
echo ========================================
echo.

cd /d "%~dp0"
python run.py

echo.
echo ========================================
echo Server stopped!
echo ========================================
pause


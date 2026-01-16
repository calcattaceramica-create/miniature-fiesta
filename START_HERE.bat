@echo off
chcp 65001 >nul
color 0A
title DED ERP System - Server

cls
echo.
echo ================================================================
echo.
echo           DED ERP System - Starting Server
echo.
echo ================================================================
echo.
echo  Server Information:
echo.
echo  URL:      http://localhost:5000
echo  Username: admin
echo  Password: admin123
echo.
echo  IMPORTANT: Keep this window OPEN while using the system!
echo  Press CTRL+C to stop the server
echo.
echo ================================================================
echo.

python run_server.py

echo.
echo ================================================================
echo Server stopped!
echo ================================================================
pause


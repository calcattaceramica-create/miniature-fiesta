@echo off
title DED ERP Server
echo ========================================
echo Starting DED ERP Server
echo ========================================
echo.
echo Server URL: http://localhost:5000
echo Username: admin
echo Password: admin123
echo.
echo Keep this window open!
echo Press CTRL+C to stop the server
echo ========================================
echo.

REM Use test server for better error reporting
python test_server.py
pause


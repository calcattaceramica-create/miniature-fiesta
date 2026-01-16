@echo off
chcp 65001 >nul
color 0A
cls

echo.
echo ================================================================
echo.
echo                   DED ERP System
echo                   Server Startup
echo.
echo ================================================================
echo.
echo Starting server...
echo.

python run_server.py

if errorlevel 1 (
    echo.
    echo ================================================================
    echo ERROR: Failed to start server!
    echo ================================================================
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo Server stopped
echo ================================================================
pause


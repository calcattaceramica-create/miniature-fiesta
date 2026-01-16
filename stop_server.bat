@echo off
REM ========================================
REM DED ERP System - Stop Server
REM ========================================

echo.
echo ========================================
echo Stopping DED ERP Server
echo ========================================
echo.

REM Kill all Python processes (be careful!)
echo Stopping all Python processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1

echo.
echo Server stopped!
echo.
pause


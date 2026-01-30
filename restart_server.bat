@echo off
echo ========================================
echo Restarting Flask Server
echo ========================================
echo.
echo Killing any existing Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul
echo.
echo Starting Flask server...
start "Flask Server" cmd /k python run.py
echo.
echo ========================================
echo Server started in new window!
echo ========================================
echo.
echo Now open your browser and go to:
echo http://localhost:5000/reports/inventory
echo.
echo Press Ctrl+Shift+Delete to clear cache
echo OR use Incognito mode (Ctrl+Shift+N)
echo OR add ?v=4 to the URL
echo.
pause


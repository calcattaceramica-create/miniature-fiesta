@echo off
taskkill /F /IM pythonw.exe >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Flask*" >nul 2>&1
timeout /t 1 /nobreak >nul
cd /d "%USERPROFILE%\Desktop"
start "" /B pythonw.exe DED_Modern_Launcher.pyw
exit


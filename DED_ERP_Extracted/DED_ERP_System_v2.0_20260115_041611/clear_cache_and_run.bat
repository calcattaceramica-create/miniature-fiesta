@echo off
echo ================================================================================
echo Clearing Python Cache and Restarting System
echo ================================================================================
echo.

echo [1/4] Stopping any running Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo [2/4] Clearing Python cache files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul

echo.
echo [3/4] Cache cleared successfully!
echo.

echo [4/4] Starting the system...
echo.
python run.py

pause


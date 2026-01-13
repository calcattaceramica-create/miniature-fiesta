@echo off
chcp 65001 >nul
title 🔐 DED License Manager

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║           🔐 DED License Manager - مدير التراخيص             ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 🚀 جاري تشغيل مدير التراخيص...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Activate virtual environment if exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Run the GUI application
pythonw License_Manager_GUI.pyw

if errorlevel 1 (
    echo.
    echo ❌ فشل تشغيل التطبيق!
    echo.
    echo جاري المحاولة بدون البيئة الافتراضية...
    python License_Manager_GUI.pyw
    pause
)


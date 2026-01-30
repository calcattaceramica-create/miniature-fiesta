@echo off
chcp 65001 >nul
title 🔐 License Manager - نظام إدارة التراخيص

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║     🔐 License Manager - نظام إدارة التراخيص العصري         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🚀 جاري تشغيل نظام إدارة التراخيص...
echo 🚀 Starting License Manager...
echo.

cd /d "%~dp0"

"%~dp0venv\Scripts\python.exe" "%~dp0license_gui_modern.py"

if errorlevel 1 (
    echo.
    echo ❌ حدث خطأ أثناء التشغيل!
    echo ❌ Error occurred!
    echo.
    pause
) else (
    echo.
    echo ✅ تم إغلاق البرنامج بنجاح
    echo ✅ Program closed successfully
    echo.
)

pause


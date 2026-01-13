@echo off
chcp 65001 >nul
title 🔐 License Manager - مدير التراخيص

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║           🔐 License Manager - مدير التراخيص                    ║
echo ║                                                                  ║
echo ║                    Professional Edition v2.0                     ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo.
echo [36m⏳ جاري تشغيل التطبيق... Starting Application...[0m
echo.

REM تشغيل التطبيق
pythonw License_Manager_App.pyw

if errorlevel 1 (
    echo.
    echo [31m❌ فشل تشغيل التطبيق - Failed to start application[0m
    echo.
    echo [33m💡 جرب:[0m
    echo    python License_Manager_App.pyw
    echo.
    pause
) else (
    echo.
    echo [32m✅ تم تشغيل التطبيق بنجاح - Application started successfully[0m
    echo.
    timeout /t 2 >nul
)


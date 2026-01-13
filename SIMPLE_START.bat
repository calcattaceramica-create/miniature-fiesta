@echo off
chcp 65001 >nul
title DED System

REM Change to DED_App directory
cd /d "C:\Users\DELL\Desktop\DED_App"

echo ========================================
echo       DED Management System
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo ❌ البيئة الافتراضية غير موجودة!
    echo.
    echo قم بتشغيل setup.bat أولاً
    echo.
    pause
    exit /b 1
)

echo ✅ تشغيل التطبيق...
echo.
echo الرابط: http://127.0.0.1:5000
echo.
echo بيانات الدخول:
echo   Username: admin
echo   Password: admin123
echo.
echo ========================================
echo.
echo لإيقاف التطبيق: اضغط Ctrl+C
echo.
echo ========================================
echo.

REM Open browser after 3 seconds
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:5000"

REM Activate venv and run
call venv\Scripts\activate.bat && python run.py

echo.
echo ========================================
echo التطبيق توقف
echo ========================================
echo.
pause


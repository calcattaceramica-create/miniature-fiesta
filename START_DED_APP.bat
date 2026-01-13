@echo off
chcp 65001 >nul
title DED System

REM Change to DED_App directory
cd /d "C:\Users\DELL\Desktop\DED_App"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ========================================
    echo البيئة الافتراضية غير موجودة
    echo ========================================
    echo.
    echo سيتم تشغيل setup.bat للتثبيت...
    echo الرجاء الانتظار 2-3 دقائق...
    echo.
    
    if exist "setup.bat" (
        call setup.bat
        if errorlevel 1 (
            echo.
            echo فشل التثبيت!
            pause
            exit /b 1
        )
    ) else (
        echo ملف setup.bat غير موجود!
        echo.
        echo قم بتشغيل الأوامر التالية يدوياً:
        echo   1. python -m venv venv
        echo   2. venv\Scripts\activate
        echo   3. pip install -r requirements.txt
        echo   4. python init_db.py
        echo.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if database exists
if not exist "instance\ded.db" (
    echo ========================================
    echo قاعدة البيانات غير موجودة
    echo ========================================
    echo.
    echo سيتم إنشاؤها الآن...
    echo.
    python init_db.py
    if errorlevel 1 (
        echo.
        echo فشل إنشاء قاعدة البيانات!
        pause
        exit /b 1
    )
    echo.
    echo تم إنشاء قاعدة البيانات بنجاح!
    echo.
)

cls
echo ========================================
echo       DED Management System
echo ========================================
echo.
echo التطبيق يعمل الآن!
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

REM Start the application
python run.py

REM If application stops
echo.
echo ========================================
echo التطبيق توقف
echo ========================================
echo.
pause


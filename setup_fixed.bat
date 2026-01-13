@echo off
chcp 65001 >nul
title DED System - Setup

echo ========================================
echo       DED System - التثبيت
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo المسار الحالي: %CD%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت!
    echo.
    echo الرجاء تثبيت Python من:
    echo https://www.python.org/downloads/
    echo.
    echo تأكد من تفعيل "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python مثبت
python --version
echo.

REM Remove old venv if exists
if exist "venv" (
    echo 🗑️ حذف البيئة الافتراضية القديمة...
    rmdir /s /q venv
    echo.
)

REM Create virtual environment
echo 📦 إنشاء البيئة الافتراضية...
python -m venv venv
if errorlevel 1 (
    echo.
    echo ❌ فشل إنشاء البيئة الافتراضية!
    pause
    exit /b 1
)
echo ✅ تم إنشاء البيئة الافتراضية
echo.

REM Activate virtual environment
echo 🔄 تفعيل البيئة الافتراضية...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo ❌ فشل تفعيل البيئة الافتراضية!
    pause
    exit /b 1
)
echo ✅ تم تفعيل البيئة الافتراضية
echo.

REM Upgrade pip
echo 📦 تحديث pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
if exist "requirements.txt" (
    echo 📦 تثبيت المكتبات المطلوبة...
    echo الرجاء الانتظار 2-3 دقائق...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ❌ فشل تثبيت المكتبات!
        pause
        exit /b 1
    )
    echo.
    echo ✅ تم تثبيت المكتبات بنجاح
    echo.
) else (
    echo ⚠️ ملف requirements.txt غير موجود!
    echo.
)

REM Create instance directory
if not exist "instance" (
    echo 📁 إنشاء مجلد instance...
    mkdir instance
    echo.
)

REM Initialize database
if exist "init_db.py" (
    echo 🗄️ إنشاء قاعدة البيانات...
    python init_db.py
    if errorlevel 1 (
        echo.
        echo ⚠️ حدث خطأ في إنشاء قاعدة البيانات
        echo سيتم إنشاؤها عند أول تشغيل
        echo.
    ) else (
        echo ✅ تم إنشاء قاعدة البيانات بنجاح
        echo.
    )
) else (
    echo ⚠️ ملف init_db.py غير موجود!
    echo.
)

echo ========================================
echo       ✅ التثبيت اكتمل بنجاح!
echo ========================================
echo.
echo يمكنك الآن تشغيل التطبيق بإحدى الطرق:
echo.
echo 1. انقر مرتين على "Start DED" على سطح المكتب
echo 2. شغل ملف START_DED_APP.bat
echo 3. شغل ملف RUN_DED.bat
echo.
echo ========================================
echo.
pause


@echo off
chcp 65001 >nul
title اختبار التطبيق - Test Application

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                         اختبار نظام DED ERP
echo                         Testing DED ERP System
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

echo 🔍 فحص البيئة الافتراضية...
echo 🔍 Checking virtual environment...
if exist "venv\Scripts\python.exe" (
    echo ✅ البيئة الافتراضية موجودة
    echo ✅ Virtual environment found
) else (
    echo ❌ البيئة الافتراضية غير موجودة!
    echo ❌ Virtual environment not found!
    pause
    exit /b 1
)

echo.
echo 🔍 فحص ملف start.py...
echo 🔍 Checking start.py...
if exist "start.py" (
    echo ✅ ملف start.py موجود
    echo ✅ start.py found
) else (
    echo ❌ ملف start.py غير موجود!
    echo ❌ start.py not found!
    pause
    exit /b 1
)

echo.
echo 🔍 فحص ملف license_system_manager.py...
echo 🔍 Checking license_system_manager.py...
if exist "license_system_manager.py" (
    echo ✅ ملف license_system_manager.py موجود
    echo ✅ license_system_manager.py found
) else (
    echo ❌ ملف license_system_manager.py غير موجود!
    echo ❌ license_system_manager.py not found!
    pause
    exit /b 1
)

echo.
echo 🔍 فحص مكتبات Python...
echo 🔍 Checking Python libraries...
"%~dp0venv\Scripts\python.exe" -c "import flask; print('✅ Flask installed')"
"%~dp0venv\Scripts\python.exe" -c "import sqlalchemy; print('✅ SQLAlchemy installed')"
"%~dp0venv\Scripts\python.exe" -c "import tabulate; print('✅ Tabulate installed')"

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo ✅ جميع الفحوصات نجحت!
echo ✅ All checks passed!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo الآن يمكنك تشغيل التطبيق من الاختصارات على سطح المكتب:
echo Now you can run the application from desktop shortcuts:
echo.
echo 1. DED ERP System.lnk - لتشغيل التطبيق الرئيسي
echo 2. License Manager.lnk - لإدارة التراخيص
echo.
pause


"""
Create Portable Application Package
إنشاء حزمة تطبيق محمولة
"""
import os
import shutil
import sys
from pathlib import Path

def create_portable_package():
    """Create a portable package of the application"""
    
    # Get desktop path
    desktop = Path.home() / "Desktop"
    
    # Create portable app folder
    portable_folder = desktop / "DED_Portable_App"
    
    print("🚀 بدء إنشاء التطبيق المحمول...")
    print(f"📁 المجلد: {portable_folder}")
    
    # Remove old folder if exists
    if portable_folder.exists():
        print("🗑️ حذف النسخة القديمة...")
        shutil.rmtree(portable_folder)
    
    # Create new folder
    portable_folder.mkdir(exist_ok=True)
    
    # List of files and folders to copy
    items_to_copy = [
        'app',
        'migrations',
        'tenant_databases',
        'run.py',
        'config.py',
        'requirements.txt',
        'licenses.json',
        'licenses_master.db',
        'erp_system.db',
    ]
    
    # Copy tenant databases
    print("📦 نسخ الملفات...")
    for item in items_to_copy:
        src = Path(item)
        if src.exists():
            dst = portable_folder / item
            if src.is_dir():
                shutil.copytree(src, dst)
                print(f"  ✅ تم نسخ المجلد: {item}")
            else:
                shutil.copy2(src, dst)
                print(f"  ✅ تم نسخ الملف: {item}")
        else:
            print(f"  ⚠️ غير موجود: {item}")
    
    # Copy all tenant databases
    print("📊 نسخ قواعد بيانات التراخيص...")
    for db_file in Path('.').glob('tenant_*.db'):
        shutil.copy2(db_file, portable_folder / db_file.name)
        print(f"  ✅ تم نسخ: {db_file.name}")
    
    # Create start.bat file
    print("📝 إنشاء ملف التشغيل...")
    start_bat = portable_folder / "START_APP.bat"
    start_bat_content = """@echo off
chcp 65001 >nul
title DED Inventory System

echo ========================================
echo    DED Inventory Management System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python 3.8 or newer from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python found
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created
    echo.
    
    echo Installing required packages...
    call venv\\Scripts\\activate.bat
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install packages!
        pause
        exit /b 1
    )
    echo All packages installed
    echo.
) else (
    call venv\\Scripts\\activate.bat
)

echo Starting application...
echo.
echo ========================================
echo   Application is running!
echo ========================================
echo.
echo Open your browser at:
echo    http://localhost:5000
echo    http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the application
echo ========================================
echo.

python run.py

pause
"""
    start_bat.write_text(start_bat_content, encoding='utf-8')
    print(f"  ✅ تم إنشاء: START_APP.bat")

    # Create README file
    print("📄 إنشاء ملف التعليمات...")
    readme = portable_folder / "README.txt"
    readme_content = """
========================================
DED Inventory Management System
========================================

REQUIREMENTS:
------------------
1. Python 3.8 or newer
   Download from: https://www.python.org/downloads/

2. Web browser (Chrome, Firefox, Edge, etc)


HOW TO RUN:
------------------
1. Make sure Python is installed on the computer
2. Double-click on: START_APP.bat
3. Wait for the application to start (may take a minute on first run)
4. Open browser at: http://localhost:5000


DEFAULT LOGIN:
---------------------------
Username: admin
Password: admin123
License Key: [Enter your license key]


FOLDER CONTENTS:
------------------
- START_APP.bat: Application launcher
- STOP_APP.bat: Stop the application
- app/: Main application folder
- run.py: Server startup file
- requirements.txt: Required packages list
- master.db: Main database
- tenant_*.db: License databases


IMPORTANT NOTES:
------------------
1. Do not delete any files from this folder
2. Keep backup copies of .db files
3. When copying to USB, copy the entire folder
4. Make sure Python is installed on target computer


TROUBLESHOOTING:
------------------
- If app doesn't start, make sure Python is installed
- If errors appear, try deleting venv folder and restart
- For technical support, contact the developer


========================================
Created by DED System
(C) 2026 All Rights Reserved
========================================
"""
    readme.write_text(readme_content, encoding='utf-8')
    print(f"  ✅ تم إنشاء: README.txt")

    # Create stop script
    stop_bat = portable_folder / "STOP_APP.bat"
    stop_bat_content = """@echo off
chcp 65001 >nul
title Stop Application

echo ========================================
echo   Stopping Application
echo ========================================
echo.

taskkill /F /IM python.exe /FI "WINDOWTITLE eq DED*" 2>nul

if errorlevel 1 (
    echo WARNING: Application not found running
) else (
    echo Application stopped successfully
)

echo.
pause
"""
    stop_bat.write_text(stop_bat_content, encoding='utf-8')
    print(f"  ✅ تم إنشاء: STOP_APP.bat")

    print("\n" + "="*50)
    print("✅ تم إنشاء التطبيق المحمول بنجاح!")
    print("="*50)
    print(f"\n📁 المجلد: {portable_folder}")
    print("\n📋 الخطوات التالية:")
    print("  1. انسخ المجلد بالكامل إلى الفلاشة")
    print("  2. على أي جهاز آخر، افتح المجلد")
    print("  3. انقر نقراً مزدوجاً على START_APP.bat")
    print("  4. انتظر حتى يبدأ التطبيق")
    print("  5. افتح المتصفح على http://localhost:5000")
    print("\n⚠️ ملاحظة: يجب تثبيت Python على الجهاز المستهدف!")
    print("="*50)

    return portable_folder

if __name__ == '__main__':
    try:
        folder = create_portable_package()
    except Exception as e:
        print(f"\n❌ حدث خطأ: {e}")
        import traceback
        traceback.print_exc()

    input("\nاضغط Enter للخروج...")


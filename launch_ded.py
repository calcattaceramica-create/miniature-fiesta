#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DED System Launcher
تشغيل نظام DED مباشرة
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def main():
    """Launch DED System"""
    
    # Get the directory where this script is located
    app_dir = Path(__file__).parent.absolute()
    os.chdir(app_dir)
    
    print("=" * 60)
    print("تشغيل نظام DED")
    print("=" * 60)
    print()
    
    # Check if virtual environment exists
    venv_path = app_dir / "venv"
    if not venv_path.exists():
        print("البيئة الافتراضية غير موجودة")
        print("سيتم تشغيل setup.bat أولاً...")
        print()
        
        setup_bat = app_dir / "setup.bat"
        if setup_bat.exists():
            subprocess.run([str(setup_bat)], shell=True, check=True)
        else:
            print("ملف setup.bat غير موجود!")
            print("قم بتشغيل: python -m venv venv")
            input("\nاضغط Enter للخروج...")
            sys.exit(1)
    
    # Check if database exists
    db_path = app_dir / "erp_system.db"
    if not db_path.exists():
        print("قاعدة البيانات غير موجودة")
        print("سيتم إنشاؤها الآن...")
        print()
        
        # Activate venv and run init_db.py
        if sys.platform == "win32":
            python_exe = venv_path / "Scripts" / "python.exe"
        else:
            python_exe = venv_path / "bin" / "python"
        
        init_db = app_dir / "init_db.py"
        if init_db.exists():
            subprocess.run([str(python_exe), str(init_db)], check=True)
            print()
            print("تم إنشاء قاعدة البيانات بنجاح!")
            print()
        else:
            print("ملف init_db.py غير موجود!")
            input("\nاضغط Enter للخروج...")
            sys.exit(1)
    
    print("=" * 60)
    print("التطبيق يعمل الآن!")
    print("=" * 60)
    print()
    print("الرابط: http://127.0.0.1:5000")
    print()
    print("بيانات الدخول:")
    print("   Username: admin")
    print("   Password: admin123")
    print()
    print("=" * 60)
    print()
    print("لإيقاف التطبيق: اضغط Ctrl+C")
    print()
    print("=" * 60)
    print()
    
    # Start the Flask application
    if sys.platform == "win32":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    run_py = app_dir / "run.py"
    
    # Open browser after 3 seconds
    def open_browser():
        time.sleep(3)
        webbrowser.open("http://127.0.0.1:5000")
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run the application
    try:
        subprocess.run([str(python_exe), str(run_py)], check=True)
    except KeyboardInterrupt:
        print("\n\nالتطبيق توقف")
        print()
    except Exception as e:
        print(f"\nخطأ: {e}")
        input("\nاضغط Enter للخروج...")
        sys.exit(1)

if __name__ == "__main__":
    main()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DED System GUI Launcher
تشغيل نظام DED بواجهة رسومية
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import threading

def check_and_setup():
    """Check requirements and setup if needed"""
    app_dir = Path(__file__).parent.absolute()
    os.chdir(app_dir)
    
    # Check if virtual environment exists
    venv_path = app_dir / "venv"
    if not venv_path.exists():
        response = messagebox.askyesno(
            "التثبيت مطلوب",
            "البيئة الافتراضية غير موجودة.\n\nهل تريد تشغيل setup.bat للتثبيت؟\n(قد يستغرق 2-3 دقائق)"
        )
        if response:
            setup_bat = app_dir / "setup.bat"
            if setup_bat.exists():
                subprocess.run([str(setup_bat)], shell=True, check=True)
            else:
                messagebox.showerror("خطأ", "ملف setup.bat غير موجود!")
                return False
        else:
            return False
    
    # Check if database exists
    db_path = app_dir / "erp_system.db"
    if not db_path.exists():
        if sys.platform == "win32":
            python_exe = venv_path / "Scripts" / "python.exe"
        else:
            python_exe = venv_path / "bin" / "python"
        
        init_db = app_dir / "init_db.py"
        if init_db.exists():
            subprocess.run([str(python_exe), str(init_db)], check=True)
        else:
            messagebox.showerror("خطأ", "ملف init_db.py غير موجود!")
            return False
    
    return True

def launch_app():
    """Launch the DED application"""
    app_dir = Path(__file__).parent.absolute()
    venv_path = app_dir / "venv"
    
    if sys.platform == "win32":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    run_py = app_dir / "run.py"
    
    # Start Flask in background
    process = subprocess.Popen(
        [str(python_exe), str(run_py)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    )
    
    # Wait for server to start
    time.sleep(3)
    
    # Open browser
    webbrowser.open("http://127.0.0.1:5000")
    
    # Show success message
    messagebox.showinfo(
        "نظام DED",
        "تم تشغيل نظام DED بنجاح!\n\n"
        "الرابط: http://127.0.0.1:5000\n\n"
        "بيانات الدخول:\n"
        "Username: admin\n"
        "Password: admin123\n\n"
        "ملاحظة: التطبيق يعمل في الخلفية"
    )

def main():
    """Main function"""
    # Hide the main window
    root = tk.Tk()
    root.withdraw()
    
    try:
        # Check and setup
        if check_and_setup():
            # Launch app in background thread
            thread = threading.Thread(target=launch_app)
            thread.daemon = True
            thread.start()
            thread.join()
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ:\n{str(e)}")
    finally:
        root.destroy()

if __name__ == "__main__":
    main()


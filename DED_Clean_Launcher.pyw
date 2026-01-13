#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DED System - Clean Simple Launcher
مشغل نظام DED البسيط والنظيف
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import threading
import time

class CleanLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("DED System Launcher")
        self.root.geometry("500x400")
        self.root.configure(bg='#1e293b')
        
        # Get correct paths
        self.app_dir = Path(__file__).parent.absolute()
        os.chdir(self.app_dir)
        
        self.flask_process = None
        self.is_running = False
        
        # Create UI
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="نظام DED الإداري المتكامل",
            font=("Arial", 20, "bold"),
            bg='#1e293b',
            fg='white'
        )
        title.pack(pady=30)
        
        # Status
        self.status_label = tk.Label(
            self.root,
            text="● التطبيق متوقف",
            font=("Arial", 14),
            bg='#1e293b',
            fg='#94a3b8'
        )
        self.status_label.pack(pady=20)
        
        # Start Button
        self.start_btn = tk.Button(
            self.root,
            text="▶ تشغيل التطبيق\nStart Application",
            font=("Arial", 12, "bold"),
            bg='#10b981',
            fg='white',
            command=self.start_app,
            width=20,
            height=3,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.start_btn.pack(pady=10)
        
        # Stop Button
        self.stop_btn = tk.Button(
            self.root,
            text="⏹ إيقاف التطبيق\nStop Application",
            font=("Arial", 12, "bold"),
            bg='#ef4444',
            fg='white',
            command=self.stop_app,
            width=20,
            height=3,
            relief=tk.FLAT,
            cursor="hand2",
            state="disabled"
        )
        self.stop_btn.pack(pady=10)
        
        # Browser Button
        browser_btn = tk.Button(
            self.root,
            text="🌐 فتح المتصفح\nOpen Browser",
            font=("Arial", 11),
            bg='#3b82f6',
            fg='white',
            command=lambda: webbrowser.open("http://127.0.0.1:5000"),
            width=20,
            height=2,
            relief=tk.FLAT,
            cursor="hand2"
        )
        browser_btn.pack(pady=10)
        
        # Info
        info = tk.Label(
            self.root,
            text=f"📁 {self.app_dir}",
            font=("Arial", 8),
            bg='#1e293b',
            fg='#64748b'
        )
        info.pack(side=tk.BOTTOM, pady=10)
        
    def start_app(self):
        if self.is_running:
            messagebox.showwarning("تحذير", "التطبيق يعمل بالفعل!")
            return
            
        try:
            # Build paths
            python_exe = self.app_dir / "venv" / "Scripts" / "python.exe"
            run_py = self.app_dir / "run.py"
            
            # Check files
            if not python_exe.exists():
                messagebox.showerror(
                    "خطأ",
                    f"Python not found!\n\n{python_exe}\n\nExpected at: {self.app_dir}"
                )
                return
                
            if not run_py.exists():
                messagebox.showerror(
                    "خطأ",
                    f"run.py not found!\n\n{run_py}\n\nExpected at: {self.app_dir}"
                )
                return
            
            # Start Flask
            self.flask_process = subprocess.Popen(
                [str(python_exe), str(run_py)],
                cwd=str(self.app_dir),
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            self.is_running = True
            self.status_label.config(text="● التطبيق يعمل", fg='#10b981')
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            
            # Open browser after delay
            threading.Thread(target=self.delayed_open, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"Failed to start:\n{str(e)}")
            
    def delayed_open(self):
        time.sleep(3)
        webbrowser.open("http://127.0.0.1:5000")
        
    def stop_app(self):
        if self.flask_process:
            self.flask_process.terminate()
            self.flask_process = None
        self.is_running = False
        self.status_label.config(text="● التطبيق متوقف", fg='#94a3b8')
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CleanLauncher(root)
    root.mainloop()


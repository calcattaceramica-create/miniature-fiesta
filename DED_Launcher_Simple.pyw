#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""DED System - Simple Launcher"""

import os
import subprocess
import webbrowser
import time
import threading
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

class SimpleLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("DED Management System")
        self.root.geometry("700x600")
        self.root.configure(bg='#0f172a')
        
        # Find app directory
        current = Path(__file__).parent.absolute()
        if current.name == "DED_App":
            self.app_dir = current
        elif (current / "DED_App").exists():
            self.app_dir = current / "DED_App"
        else:
            self.app_dir = current
        
        os.chdir(self.app_dir)
        
        self.flask_process = None
        self.is_running = False
        
        self.create_ui()
    
    def create_ui(self):
        # Header
        header = tk.Frame(self.root, bg='#1e293b', height=150)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="🚀", font=("Arial", 48), bg='#1e293b', fg='white').pack(pady=10)
        tk.Label(header, text="نظام DED الإداري المتكامل", font=("Arial", 20, "bold"), 
                bg='#1e293b', fg='white').pack()
        tk.Label(header, text="DED Management System", font=("Arial", 12), 
                bg='#1e293b', fg='#94a3b8').pack(pady=5)
        
        # Status
        status_frame = tk.Frame(self.root, bg='#0f172a')
        status_frame.pack(pady=30)
        
        self.status_label = tk.Label(status_frame, text="● التطبيق متوقف", 
                                     font=("Arial", 16), bg='#0f172a', fg='#ef4444')
        self.status_label.pack()
        
        # Buttons
        btn_frame = tk.Frame(self.root, bg='#0f172a')
        btn_frame.pack(pady=20)
        
        self.start_btn = tk.Button(btn_frame, text="▶ تشغيل التطبيق\nStart Application",
                                   font=("Arial", 14, "bold"), bg='#10b981', fg='white',
                                   width=20, height=3, command=self.start_app, cursor="hand2")
        self.start_btn.pack(pady=10)
        
        self.stop_btn = tk.Button(btn_frame, text="⏹ إيقاف التطبيق\nStop Application",
                                 font=("Arial", 14, "bold"), bg='#ef4444', fg='white',
                                 width=20, height=3, command=self.stop_app, state='disabled')
        self.stop_btn.pack(pady=10)
        
        tk.Button(btn_frame, text="🌐 فتح المتصفح\nOpen Browser",
                 font=("Arial", 14, "bold"), bg='#3b82f6', fg='white',
                 width=20, height=3, command=self.open_browser, cursor="hand2").pack(pady=10)
        
        # Info
        info_frame = tk.Frame(self.root, bg='#1e293b')
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(info_frame, text="📋 معلومات الدخول - Login Information", 
                font=("Arial", 12, "bold"), bg='#1e293b', fg='white').pack(pady=10)
        
        tk.Label(info_frame, text="🌐 URL: http://127.0.0.1:5000", 
                font=("Arial", 11), bg='#1e293b', fg='#3b82f6').pack(pady=5)
        tk.Label(info_frame, text="👤 Username: admin", 
                font=("Arial", 11), bg='#1e293b', fg='#3b82f6').pack(pady=5)
        tk.Label(info_frame, text="🔑 Password: admin123", 
                font=("Arial", 11), bg='#1e293b', fg='#3b82f6').pack(pady=5)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def start_app(self):
        if self.is_running:
            messagebox.showwarning("تحذير", "التطبيق يعمل بالفعل!")
            return
        
        try:
            python_exe = self.app_dir / "venv" / "Scripts" / "python.exe"
            run_py = self.app_dir / "run.py"
            
            if not python_exe.exists() or not run_py.exists():
                messagebox.showerror("خطأ", f"الملفات غير موجودة!\n{python_exe}\n{run_py}")
                return
            
            # Kill old processes
            subprocess.run("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq Flask*\" 2>nul", 
                          shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(0.5)
            
            # Start Flask
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0
            
            self.flask_process = subprocess.Popen(
                [str(python_exe), str(run_py)],
                cwd=str(self.app_dir),
                creationflags=subprocess.CREATE_NO_WINDOW,
                startupinfo=startupinfo,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            self.is_running = True
            self.status_label.config(text="● التطبيق يعمل", fg='#10b981')
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal', cursor="hand2")
            
            # Open browser
            threading.Thread(target=self.delayed_browser, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل التشغيل:\n{str(e)}")
    
    def stop_app(self):
        if self.flask_process:
            self.flask_process.terminate()
            self.flask_process = None
        
        subprocess.run("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq Flask*\" 2>nul",
                      shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        self.is_running = False
        self.status_label.config(text="● التطبيق متوقف", fg='#ef4444')
        self.start_btn.config(state='normal', cursor="hand2")
        self.stop_btn.config(state='disabled', cursor="")
    
    def delayed_browser(self):
        time.sleep(3)
        webbrowser.open("http://127.0.0.1:5000")
    
    def open_browser(self):
        webbrowser.open("http://127.0.0.1:5000")
    
    def on_close(self):
        if self.is_running:
            if messagebox.askyesno("تأكيد", "التطبيق يعمل. هل تريد إيقافه والخروج؟"):
                self.stop_app()
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleLauncher(root)
    root.mainloop()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DED System - Simple Launcher (Guaranteed to Work!)
واجهة تشغيل نظام DED البسيطة والموثوقة
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import time
import threading

class SimpleLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("DED System Launcher")
        self.root.geometry("600x500")
        
        # Bring to front
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))
        
        # Colors
        self.bg_color = "#1e293b"
        self.fg_color = "#f8fafc"
        self.btn_start = "#10b981"
        self.btn_stop = "#ef4444"
        self.btn_browser = "#3b82f6"
        self.btn_license = "#f59e0b"
        
        self.root.configure(bg=self.bg_color)
        
        # Working directory
        self.app_dir = Path(__file__).parent.absolute()
        os.chdir(self.app_dir)
        
        # Process
        self.flask_process = None
        self.is_running = False
        
        # Build UI
        self.create_ui()
    
    def create_ui(self):
        """Create simple UI"""
        # Title
        title = tk.Label(
            self.root,
            text="🚀 نظام DED الإداري",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title.pack(pady=30)
        
        # Subtitle
        subtitle = tk.Label(
            self.root,
            text="DED Management System",
            font=("Arial", 12),
            bg=self.bg_color,
            fg="#94a3b8"
        )
        subtitle.pack(pady=5)
        
        # Status
        self.status_label = tk.Label(
            self.root,
            text="● التطبيق متوقف",
            font=("Arial", 14),
            bg=self.bg_color,
            fg="#94a3b8"
        )
        self.status_label.pack(pady=20)
        
        # Info frame
        info_frame = tk.Frame(self.root, bg="#334155", padx=20, pady=15)
        info_frame.pack(pady=20, padx=40, fill=tk.X)
        
        tk.Label(info_frame, text="🌐 http://127.0.0.1:5000", font=("Arial", 11), bg="#334155", fg=self.fg_color).pack()
        tk.Label(info_frame, text="👤 admin  |  🔑 admin123", font=("Arial", 11), bg="#334155", fg=self.fg_color).pack(pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=20, padx=40, fill=tk.X)
        
        # Start button
        self.start_btn = tk.Button(
            btn_frame,
            text="▶ تشغيل التطبيق",
            font=("Arial", 12, "bold"),
            bg=self.btn_start,
            fg="white",
            command=self.start_app,
            height=2,
            cursor="hand2"
        )
        self.start_btn.pack(fill=tk.X, pady=5)
        
        # Stop button
        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹ إيقاف التطبيق",
            font=("Arial", 12, "bold"),
            bg=self.btn_stop,
            fg="white",
            command=self.stop_app,
            height=2,
            state="disabled"
        )
        self.stop_btn.pack(fill=tk.X, pady=5)
        
        # Browser button
        tk.Button(
            btn_frame,
            text="🌐 فتح المتصفح",
            font=("Arial", 12, "bold"),
            bg=self.btn_browser,
            fg="white",
            command=self.open_browser,
            height=2,
            cursor="hand2"
        ).pack(fill=tk.X, pady=5)
        
        # License button
        tk.Button(
            btn_frame,
            text="🔐 مدير التراخيص",
            font=("Arial", 12, "bold"),
            bg=self.btn_license,
            fg="white",
            command=self.open_license,
            height=2,
            cursor="hand2"
        ).pack(fill=tk.X, pady=5)
        
        # Footer
        tk.Label(
            self.root,
            text="DED System v1.2.0 | صُنع بـ ❤️ في السعودية",
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#64748b"
        ).pack(side=tk.BOTTOM, pady=10)
    
    def start_app(self):
        """Start Flask app"""
        if self.is_running:
            messagebox.showwarning("تحذير", "التطبيق يعمل بالفعل!")
            return

        try:
            # Use BAT file for more reliable startup
            start_bat = self.app_dir / "Start_Flask_App.bat"

            if not start_bat.exists():
                # Fallback to direct Python execution
                python_exe = self.app_dir / "venv" / "Scripts" / "python.exe"
                run_py = self.app_dir / "run.py"

                if not python_exe.exists() or not run_py.exists():
                    messagebox.showerror(
                        "خطأ - Error",
                        "الملفات المطلوبة غير موجودة!\n"
                        "Required files not found!\n\n"
                        "الرجاء تشغيل setup.bat أولاً\n"
                        "Please run setup.bat first"
                    )
                    return

                # Start Flask directly
                self.flask_process = subprocess.Popen(
                    [str(python_exe), str(run_py)],
                    cwd=str(self.app_dir),
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
            else:
                # Start using BAT file
                self.flask_process = subprocess.Popen(
                    [str(start_bat)],
                    cwd=str(self.app_dir),
                    shell=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )

            self.is_running = True
            self.update_status(True)

            # Open browser after delay
            threading.Thread(target=self.delayed_browser, daemon=True).start()

            messagebox.showinfo(
                "✅ تم - Success",
                "تم تشغيل التطبيق!\n"
                "Application started!\n\n"
                "سيفتح المتصفح خلال 3 ثواني...\n"
                "Browser will open in 3 seconds..."
            )

        except Exception as e:
            self.is_running = False
            messagebox.showerror("خطأ - Error", f"فشل التشغيل:\n{str(e)}\n\nFailed to start:\n{str(e)}")
    
    def stop_app(self):
        """Stop Flask app"""
        if not self.is_running:
            return
        
        try:
            if self.flask_process:
                self.flask_process.terminate()
                self.flask_process.wait(timeout=5)
        except:
            if self.flask_process:
                self.flask_process.kill()
        
        self.is_running = False
        self.flask_process = None
        self.update_status(False)
        messagebox.showinfo("تم", "تم إيقاف التطبيق بنجاح!")
    
    def delayed_browser(self):
        """Open browser after delay"""
        time.sleep(3)
        webbrowser.open("http://127.0.0.1:5000")
    
    def open_browser(self):
        """Open browser"""
        webbrowser.open("http://127.0.0.1:5000")
    
    def open_license(self):
        """Open License Manager"""
        try:
            license_file = self.app_dir / "License_Manager_GUI.pyw"
            if not license_file.exists():
                messagebox.showerror("خطأ", "ملف مدير التراخيص غير موجود!")
                return
            
            subprocess.Popen(
                ["pythonw", str(license_file)],
                cwd=str(self.app_dir),
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            messagebox.showinfo("تم", "تم فتح مدير التراخيص!")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل فتح مدير التراخيص:\n{str(e)}")
    
    def update_status(self, running):
        """Update status"""
        if running:
            self.status_label.config(text="● التطبيق يعمل", fg="#10b981")
            self.start_btn.config(state="disabled", cursor="")
            self.stop_btn.config(state="normal", cursor="hand2")
        else:
            self.status_label.config(text="● التطبيق متوقف", fg="#94a3b8")
            self.start_btn.config(state="normal", cursor="hand2")
            self.stop_btn.config(state="disabled", cursor="")
    
    def on_close(self):
        """Handle window close"""
        if self.is_running:
            if messagebox.askyesno("تأكيد", "التطبيق يعمل. هل تريد إيقافه والخروج؟"):
                self.stop_app()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    root = tk.Tk()
    app = SimpleLauncher(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f'+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()


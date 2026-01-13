#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DED System Launcher - Modern GUI Version
واجهة تشغيل نظام DED الحديثة
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class ModernButton(tk.Canvas):
    """Custom modern button with hover effects"""
    def __init__(self, parent, text, command, bg_color, hover_color, text_color="white", width=200, height=50):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0)

        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_enabled = True

        # Draw button
        self.rect = self.create_rectangle(0, 0, width, height, fill=bg_color, outline="", width=0)
        self.text = self.create_text(width/2, height/2, text=text, fill=text_color,
                                     font=("Segoe UI", 11, "bold"))

        # Bind events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def on_enter(self, e):
        if self.is_enabled:
            self.itemconfig(self.rect, fill=self.hover_color)
            self.config(cursor="hand2")

    def on_leave(self, e):
        if self.is_enabled:
            self.itemconfig(self.rect, fill=self.bg_color)
            self.config(cursor="")

    def on_click(self, e):
        if self.is_enabled and self.command:
            self.command()

    def set_enabled(self, enabled):
        self.is_enabled = enabled
        if enabled:
            self.itemconfig(self.rect, fill=self.bg_color)
            self.itemconfig(self.text, fill=self.text_color)
        else:
            self.itemconfig(self.rect, fill="#bdc3c7")
            self.itemconfig(self.text, fill="#7f8c8d")

class DEDLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("DED Management System")
        self.root.geometry("700x650")
        self.root.resizable(True, True)
        self.root.minsize(600, 550)

        # Colors
        self.colors = {
            'bg': '#1a1a2e',
            'secondary': '#16213e',
            'accent': '#0f3460',
            'success': '#27ae60',
            'success_hover': '#229954',
            'danger': '#e74c3c',
            'danger_hover': '#c0392b',
            'info': '#3498db',
            'info_hover': '#2980b9',
            'warning': '#f39c12',
            'text': '#ecf0f1',
            'text_secondary': '#95a5a6',
            'card': '#2c3e50'
        }

        # Configure root
        self.root.configure(bg=self.colors['bg'])

        # Get app directory
        self.app_dir = Path(__file__).parent.absolute()
        os.chdir(self.app_dir)

        # Process variable
        self.flask_process = None
        self.is_running = False

        # Setup UI
        self.setup_ui()

        # Check status on startup
        self.root.after(500, self.check_requirements)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Set background color
        self.root.configure(bg="#ecf0f1")

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.configure(style="Main.TFrame")

        # Title
        title_label = tk.Label(
            main_frame,
            text="🚀 نظام DED الإداري المتكامل",
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg="#ecf0f1"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="DED Management System",
            font=("Arial", 12),
            fg="#7f8c8d",
            bg="#ecf0f1"
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="الحالة - Status", padding="15")
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.status_label = tk.Label(
            status_frame,
            text="⚪ التطبيق متوقف - Application Stopped",
            font=("Arial", 11),
            fg="#e74c3c"
        )
        self.status_label.pack()
        
        # Info frame
        info_frame = ttk.LabelFrame(main_frame, text="معلومات الدخول - Login Info", padding="15")
        info_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        info_text = tk.Text(info_frame, height=6, width=50, font=("Courier", 10))
        info_text.pack()
        info_text.insert("1.0", """
🌐 الرابط - URL: http://127.0.0.1:5000

👤 بيانات الدخول - Login Credentials:
   Username: admin
   Password: admin123

⚠️  غيّر كلمة المرور بعد أول تسجيل دخول!
        """)
        info_text.config(state="disabled")
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Start button
        self.start_button = tk.Button(
            buttons_frame,
            text="▶ تشغيل التطبيق\nStart Application",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            width=20,
            height=3,
            command=self.start_application,
            cursor="hand2"
        )
        self.start_button.grid(row=0, column=0, padx=10)
        
        # Stop button
        self.stop_button = tk.Button(
            buttons_frame,
            text="⏹ إيقاف التطبيق\nStop Application",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=20,
            height=3,
            command=self.stop_application,
            state="disabled",
            cursor="hand2"
        )
        self.stop_button.grid(row=0, column=1, padx=10)
        
        # Open browser button
        self.browser_button = tk.Button(
            buttons_frame,
            text="🌐 فتح المتصفح\nOpen Browser",
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            width=20,
            height=2,
            command=self.open_browser,
            cursor="hand2"
        )
        self.browser_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Footer
        footer_label = tk.Label(
            main_frame,
            text="DED System v1.2.0 | صُنع بـ ❤️ في السعودية",
            font=("Arial", 9),
            fg="#95a5a6"
        )
        footer_label.grid(row=5, column=0, columnspan=2, pady=20)
    
    def check_requirements(self):
        """Check if all requirements are met"""
        venv_path = self.app_dir / "venv" / "Scripts" / "python.exe"
        db_path = self.app_dir / "erp_system.db"
        
        if not venv_path.exists():
            messagebox.showerror(
                "خطأ - Error",
                "البيئة الافتراضية غير موجودة!\n\nالرجاء تشغيل setup.bat أولاً\n\n"
                "Virtual environment not found!\nPlease run setup.bat first"
            )
            return False
        
        if not db_path.exists():
            response = messagebox.askyesno(
                "قاعدة البيانات - Database",
                "قاعدة البيانات غير موجودة.\n\nهل تريد إنشاءها الآن؟\n\n"
                "Database not found.\nDo you want to create it now?"
            )
            if response:
                self.create_database()
            return False
        
        return True
    
    def create_database(self):
        """Create the database"""
        try:
            python_exe = self.app_dir / "venv" / "Scripts" / "python.exe"
            init_db = self.app_dir / "init_db.py"
            
            subprocess.run([str(python_exe), str(init_db)], check=True)
            
            messagebox.showinfo(
                "نجح - Success",
                "تم إنشاء قاعدة البيانات بنجاح!\n\nDatabase created successfully!"
            )
        except Exception as e:
            messagebox.showerror(
                "خطأ - Error",
                f"فشل إنشاء قاعدة البيانات:\n{str(e)}\n\n"
                f"Failed to create database:\n{str(e)}"
            )
    
    def start_application(self):
        """Start the Flask application"""
        if self.is_running:
            messagebox.showwarning(
                "تحذير - Warning",
                "التطبيق يعمل بالفعل!\n\nApplication is already running!"
            )
            return
        
        try:
            python_exe = self.app_dir / "venv" / "Scripts" / "python.exe"
            run_py = self.app_dir / "run.py"
            
            # Start Flask in background
            self.flask_process = subprocess.Popen(
                [str(python_exe), str(run_py)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
            self.is_running = True
            
            # Update UI
            self.status_label.config(
                text="🟢 التطبيق يعمل - Application Running",
                fg="#27ae60"
            )
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # Wait 3 seconds then open browser
            threading.Thread(target=self.delayed_browser_open, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror(
                "خطأ - Error",
                f"فشل تشغيل التطبيق:\n{str(e)}\n\n"
                f"Failed to start application:\n{str(e)}"
            )
    
    def delayed_browser_open(self):
        """Open browser after delay"""
        time.sleep(3)
        webbrowser.open("http://127.0.0.1:5000")
    
    def stop_application(self):
        """Stop the Flask application"""
        if not self.is_running or not self.flask_process:
            return
        
        try:
            self.flask_process.terminate()
            self.flask_process.wait(timeout=5)
        except:
            self.flask_process.kill()
        
        self.is_running = False
        self.flask_process = None
        
        # Update UI
        self.status_label.config(
            text="⚪ التطبيق متوقف - Application Stopped",
            fg="#e74c3c"
        )
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        
        messagebox.showinfo(
            "تم - Done",
            "تم إيقاف التطبيق بنجاح!\n\nApplication stopped successfully!"
        )
    
    def open_browser(self):
        """Open browser"""
        webbrowser.open("http://127.0.0.1:5000")
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            response = messagebox.askyesno(
                "تأكيد - Confirm",
                "التطبيق يعمل. هل تريد إيقافه والخروج؟\n\n"
                "Application is running. Stop and exit?"
            )
            if response:
                self.stop_application()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    """Main function"""
    root = tk.Tk()
    app = DEDLauncher(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()


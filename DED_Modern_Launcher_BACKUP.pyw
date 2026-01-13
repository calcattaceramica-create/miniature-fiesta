#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DED System - Modern Launcher
واجهة تشغيل نظام DED الحديثة والجميلة
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

class ModernLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("DED Management System")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        self.root.minsize(700, 600)

        # Bring window to front
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        
        # Modern color scheme
        self.colors = {
            'bg_dark': '#0f172a',
            'bg_medium': '#1e293b',
            'bg_light': '#334155',
            'accent_blue': '#3b82f6',
            'accent_blue_hover': '#2563eb',
            'success': '#10b981',
            'success_hover': '#059669',
            'danger': '#ef4444',
            'danger_hover': '#dc2626',
            'warning': '#f59e0b',
            'text_white': '#f8fafc',
            'text_gray': '#cbd5e1',
            'text_muted': '#94a3b8',
            'border': '#475569'
        }
        
        self.root.configure(bg=self.colors['bg_dark'])
        
        # App directory - detect automatically
        current_dir = Path(__file__).parent.absolute()

        # Always use current directory where the launcher is located
        # This is where venv, run.py, and app folder should be
        self.app_dir = current_dir

        # Change to app directory
        os.chdir(self.app_dir)
        print(f"Working directory: {self.app_dir}")

        # Verify critical files exist
        venv_python = self.app_dir / "venv" / "Scripts" / "python.exe"
        run_py = self.app_dir / "run.py"
        print(f"Python exists: {venv_python.exists()}")
        print(f"run.py exists: {run_py.exists()}")
        
        # Process
        self.flask_process = None
        self.is_running = False
        
        # Build UI
        self.create_modern_ui()
        
        # Check requirements
        self.root.after(300, self.check_requirements)
    
    def create_modern_ui(self):
        """Create modern beautiful UI"""
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Header section
        self.create_header(main_container)
        
        # Status card
        self.create_status_card(main_container)
        
        # Info card
        self.create_info_card(main_container)
        
        # Action buttons
        self.create_action_buttons(main_container)
        
        # Footer
        self.create_footer(main_container)
    
    def create_header(self, parent):
        """Create header with logo and title"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Logo emoji
        logo_label = tk.Label(
            header_frame,
            text="🚀",
            font=("Segoe UI Emoji", 48),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_white']
        )
        logo_label.pack()
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="نظام DED الإداري المتكامل",
            font=("Arial", 28, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_white']
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="DED Management System - Professional Edition",
            font=("Segoe UI", 12),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_muted']
        )
        subtitle_label.pack()
    
    def create_status_card(self, parent):
        """Create status card"""
        card = tk.Frame(parent, bg=self.colors['bg_medium'], relief=tk.FLAT)
        card.pack(fill=tk.X, pady=(0, 20))
        
        # Card header
        card_header = tk.Frame(card, bg=self.colors['bg_light'])
        card_header.pack(fill=tk.X)
        
        tk.Label(
            card_header,
            text="📊 حالة النظام - System Status",
            font=("Segoe UI", 13, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            anchor="w",
            padx=20,
            pady=12
        ).pack(fill=tk.X)
        
        # Status content
        status_content = tk.Frame(card, bg=self.colors['bg_medium'])
        status_content.pack(fill=tk.X, padx=20, pady=20)
        
        self.status_indicator = tk.Label(
            status_content,
            text="●",
            font=("Arial", 24),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_muted']
        )
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 15))
        
        self.status_text = tk.Label(
            status_content,
            text="التطبيق متوقف - Application Stopped",
            font=("Segoe UI", 14),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_gray'],
            anchor="w"
        )
        self.status_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def create_info_card(self, parent):
        """Create info card with login details"""
        card = tk.Frame(parent, bg=self.colors['bg_medium'], relief=tk.FLAT)
        card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Card header
        card_header = tk.Frame(card, bg=self.colors['bg_light'])
        card_header.pack(fill=tk.X)
        
        tk.Label(
            card_header,
            text="🔐 معلومات الدخول - Login Information",
            font=("Segoe UI", 13, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            anchor="w",
            padx=20,
            pady=12
        ).pack(fill=tk.X)

        # Info content
        info_content = tk.Frame(card, bg=self.colors['bg_medium'])
        info_content.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        # URL
        self.create_info_row(info_content, "🌐 الرابط - URL:", "http://127.0.0.1:5000", 0)

        # Separator
        tk.Frame(info_content, bg=self.colors['border'], height=1).grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=15
        )

        # Username
        self.create_info_row(info_content, "👤 اسم المستخدم - Username:", "admin", 2)

        # Password
        self.create_info_row(info_content, "🔑 كلمة المرور - Password:", "admin123", 3)

        # Warning
        warning_frame = tk.Frame(info_content, bg=self.colors['warning'], relief=tk.FLAT)
        warning_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(15, 0))

        tk.Label(
            warning_frame,
            text="⚠️  غيّر كلمة المرور بعد أول تسجيل دخول!",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['warning'],
            fg=self.colors['bg_dark'],
            pady=10
        ).pack()

    def create_info_row(self, parent, label_text, value_text, row):
        """Create info row"""
        tk.Label(
            parent,
            text=label_text,
            font=("Segoe UI", 11),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_muted'],
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=8)

        value_label = tk.Label(
            parent,
            text=value_text,
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['accent_blue'],
            anchor="w"
        )
        value_label.grid(row=row, column=1, sticky="w", padx=(20, 0), pady=8)

        # Make value selectable
        value_label.bind("<Button-1>", lambda e: self.copy_to_clipboard(value_text))
        value_label.bind("<Enter>", lambda e: value_label.config(cursor="hand2", fg=self.colors['accent_blue_hover']))
        value_label.bind("<Leave>", lambda e: value_label.config(cursor="", fg=self.colors['accent_blue']))

    def create_action_buttons(self, parent):
        """Create action buttons"""
        buttons_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        buttons_frame.pack(fill=tk.X, pady=(0, 20))

        # Configure grid
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.columnconfigure(2, weight=1)

        # Start button
        self.start_btn = self.create_modern_button(
            buttons_frame,
            "▶ تشغيل التطبيق\nStart Application",
            self.start_application,
            self.colors['success'],
            self.colors['success_hover']
        )
        self.start_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Stop button
        self.stop_btn = self.create_modern_button(
            buttons_frame,
            "⏹ إيقاف التطبيق\nStop Application",
            self.stop_application,
            self.colors['danger'],
            self.colors['danger_hover'],
            state="disabled"
        )
        self.stop_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Browser button
        self.browser_btn = self.create_modern_button(
            buttons_frame,
            "🌐 فتح المتصفح\nOpen Browser",
            self.open_browser,
            self.colors['accent_blue'],
            self.colors['accent_blue_hover']
        )
        self.browser_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # License Manager button (new row)
        self.license_btn = self.create_modern_button(
            buttons_frame,
            "🔐 مدير التراخيص\nLicense Manager",
            self.open_license_manager,
            self.colors['warning'],
            '#d97706'  # darker warning color for hover
        )
        self.license_btn.grid(row=1, column=0, columnspan=3, padx=5, pady=(10, 5), sticky="ew")

    def create_modern_button(self, parent, text, command, bg_color, hover_color, state="normal"):
        """Create modern button with hover effect"""
        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 11, "bold"),
            bg=bg_color,
            fg=self.colors['text_white'],
            activebackground=hover_color,
            activeforeground=self.colors['text_white'],
            relief=tk.FLAT,
            cursor="hand2" if state == "normal" else "",
            command=command,
            state=state,
            height=3,
            bd=0
        )

        # Hover effects
        if state == "normal":
            btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
            btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))

        return btn

    def create_footer(self, parent):
        """Create footer"""
        footer_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        footer_frame.pack(fill=tk.X)

        # Separator
        tk.Frame(footer_frame, bg=self.colors['border'], height=1).pack(fill=tk.X, pady=(0, 15))

        # Footer text
        tk.Label(
            footer_frame,
            text="DED System v1.2.0 Professional | صُنع بـ ❤️ في السعودية",
            font=("Segoe UI", 9),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_muted']
        ).pack()

    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("✅ تم النسخ", f"تم نسخ: {text}")

    def check_requirements(self):
        """Check requirements"""
        venv_path = self.app_dir / "venv" / "Scripts" / "python.exe"
        db_path = self.app_dir / "erp_system.db"

        if not venv_path.exists():
            messagebox.showerror(
                "❌ خطأ - Error",
                "البيئة الافتراضية غير موجودة!\n\nالرجاء تشغيل setup.bat أولاً\n\n"
                "Virtual environment not found!\nPlease run setup.bat first"
            )
            return False

        if not db_path.exists():
            response = messagebox.askyesno(
                "⚠️ قاعدة البيانات",
                "قاعدة البيانات غير موجودة.\n\nهل تريد إنشاءها الآن؟\n\n"
                "Database not found.\nDo you want to create it now?"
            )
            if response:
                self.create_database()
            return False

        return True

    def create_database(self):
        """Create database"""
        try:
            python_exe = self.app_dir / "venv" / "Scripts" / "python.exe"
            init_db = self.app_dir / "init_db.py"

            subprocess.run([str(python_exe), str(init_db)], check=True)

            messagebox.showinfo(
                "✅ نجح - Success",
                "تم إنشاء قاعدة البيانات بنجاح!\n\nDatabase created successfully!"
            )
        except Exception as e:
            messagebox.showerror(
                "❌ خطأ - Error",
                f"فشل إنشاء قاعدة البيانات:\n{str(e)}\n\n"
                f"Failed to create database:\n{str(e)}"
            )

    def start_application(self):
        """Start Flask application"""
        if self.is_running:
            messagebox.showwarning(
                "⚠️ تحذير",
                "التطبيق يعمل بالفعل!\n\nApplication is already running!"
            )
            return

        try:
            # Kill any existing Flask processes first
            try:
                subprocess.run(
                    'taskkill /F /FI "WINDOWTITLE eq Flask*" /T',
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=2
                )
            except:
                pass

            python_exe = self.app_dir / "venv" / "Scripts" / "python.exe"
            run_py = self.app_dir / "run.py"

            # Debug: Print actual paths
            print(f"DEBUG: app_dir = {self.app_dir}")
            print(f"DEBUG: python_exe = {python_exe}")
            print(f"DEBUG: run_py = {run_py}")
            print(f"DEBUG: python_exe.exists() = {python_exe.exists()}")
            print(f"DEBUG: run_py.exists() = {run_py.exists()}")

            # Verify files exist
            if not python_exe.exists():
                messagebox.showerror(
                    "❌ خطأ - Error",
                    f"الملفات المطلوبة غير موجودة!\nRequired files not found!\n\n"
                    f"Python: {python_exe}\n"
                    f"Exists: {python_exe.exists()}\n\n"
                    f"Working Dir: {self.app_dir}"
                )
                raise FileNotFoundError(f"Python not found: {python_exe}")
            if not run_py.exists():
                messagebox.showerror(
                    "❌ خطأ - Error",
                    f"الملفات المطلوبة غير موجودة!\nRequired files not found!\n\n"
                    f"run.py: {run_py}\n"
                    f"Exists: {run_py.exists()}\n\n"
                    f"Working Dir: {self.app_dir}"
                )
                raise FileNotFoundError(f"run.py not found: {run_py}")

            # Start Flask with proper flags
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE

            self.flask_process = subprocess.Popen(
                [str(python_exe), str(run_py)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                cwd=str(self.app_dir),
                creationflags=subprocess.CREATE_NO_WINDOW,
                startupinfo=startupinfo
            )

            # Mark as running immediately
            self.is_running = True
            self.root.after(100, lambda: self.update_status(True))

            # Open browser after delay
            threading.Thread(target=self.delayed_browser_open, daemon=True).start()

        except Exception as e:
            self.is_running = False
            messagebox.showerror(
                "❌ خطأ - Error",
                f"فشل تشغيل التطبيق:\n{str(e)}\n\n"
                f"Failed to start application:\n{str(e)}"
            )

    def stop_application(self):
        """Stop Flask application"""
        if not self.is_running or not self.flask_process:
            return

        try:
            self.flask_process.terminate()
            self.flask_process.wait(timeout=5)
        except:
            self.flask_process.kill()

        self.is_running = False
        self.flask_process = None
        self.update_status(False)

        messagebox.showinfo(
            "✅ تم - Done",
            "تم إيقاف التطبيق بنجاح!\n\nApplication stopped successfully!"
        )

    def delayed_browser_open(self):
        """Open browser after delay"""
        time.sleep(3)
        webbrowser.open("http://127.0.0.1:5000")

    def open_browser(self):
        """Open browser"""
        webbrowser.open("http://127.0.0.1:5000")

    def open_license_manager(self):
        """Open License Manager GUI"""
        try:
            # Check if License_Manager_GUI.pyw exists
            license_gui = self.app_dir / "License_Manager_GUI.pyw"

            # If not in app_dir, check parent directory
            if not license_gui.exists():
                license_gui = self.app_dir.parent / "License_Manager_GUI.pyw"

            if not license_gui.exists():
                messagebox.showerror(
                    "❌ خطأ - Error",
                    "ملف مدير التراخيص غير موجود!\n\n"
                    "License Manager file not found!\n\n"
                    f"Expected at: {license_gui}"
                )
                return

            # Get python executable
            python_exe = self.app_dir / "venv" / "Scripts" / "pythonw.exe"

            # If venv doesn't exist, try system python
            if not python_exe.exists():
                python_exe = "pythonw.exe"

            # Launch License Manager
            subprocess.Popen(
                [str(python_exe), str(license_gui)],
                cwd=str(license_gui.parent),
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )

            messagebox.showinfo(
                "✅ تم - Success",
                "تم فتح مدير التراخيص!\n\n"
                "License Manager opened!"
            )

        except Exception as e:
            messagebox.showerror(
                "❌ خطأ - Error",
                f"فشل فتح مدير التراخيص:\n{str(e)}\n\n"
                f"Failed to open License Manager:\n{str(e)}"
            )

    def update_status(self, running):
        """Update status display"""
        if running:
            self.status_indicator.config(fg=self.colors['success'])
            self.status_text.config(
                text="التطبيق يعمل - Application Running",
                fg=self.colors['success']
            )
            self.start_btn.config(state="disabled", cursor="")
            self.stop_btn.config(state="normal", cursor="hand2")

            # Re-bind hover effects for stop button
            self.stop_btn.bind("<Enter>", lambda e: self.stop_btn.config(bg=self.colors['danger_hover']))
            self.stop_btn.bind("<Leave>", lambda e: self.stop_btn.config(bg=self.colors['danger']))
        else:
            self.status_indicator.config(fg=self.colors['text_muted'])
            self.status_text.config(
                text="التطبيق متوقف - Application Stopped",
                fg=self.colors['text_gray']
            )
            self.start_btn.config(state="normal", cursor="hand2")
            self.stop_btn.config(state="disabled", cursor="")

            # Re-bind hover effects for start button
            self.start_btn.bind("<Enter>", lambda e: self.start_btn.config(bg=self.colors['success_hover']))
            self.start_btn.bind("<Leave>", lambda e: self.start_btn.config(bg=self.colors['success']))

    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            response = messagebox.askyesno(
                "⚠️ تأكيد - Confirm",
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
    app = ModernLauncher(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()

if __name__ == "__main__":
    main()


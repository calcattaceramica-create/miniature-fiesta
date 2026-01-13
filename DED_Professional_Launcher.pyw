#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""DED System - Professional Launcher with Modern UI"""

import os
import subprocess
import webbrowser
import time
import threading
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import socket

class ProfessionalLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("DED Management System - Professional Edition")
        self.root.geometry("900x750")
        self.root.resizable(False, False)
        
        # Modern color palette
        self.colors = {
            'primary': '#0ea5e9',
            'primary_dark': '#0284c7',
            'success': '#22c55e',
            'success_dark': '#16a34a',
            'danger': '#ef4444',
            'danger_dark': '#dc2626',
            'warning': '#f59e0b',
            'bg_dark': '#0f172a',
            'bg_medium': '#1e293b',
            'bg_light': '#334155',
            'bg_card': '#1e293b',
            'text_white': '#f8fafc',
            'text_gray': '#cbd5e1',
            'text_muted': '#94a3b8',
            'border': '#475569',
            'accent': '#8b5cf6'
        }
        
        self.root.configure(bg=self.colors['bg_dark'])
        
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

        # Get local IP address
        self.local_ip = self.get_local_ip()

        self.create_professional_ui()
        self.animate_startup()
    
    def create_professional_ui(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header with gradient effect (simulated)
        self.create_header(main_container)
        
        # Content area
        content = tk.Frame(main_container, bg=self.colors['bg_dark'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Status card
        self.create_status_card(content)
        
        # Control panel
        self.create_control_panel(content)
        
        # Info cards
        self.create_info_cards(content)
        
        # Footer
        self.create_footer(main_container)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_header(self, parent):
        """Create professional header"""
        header = tk.Frame(parent, bg=self.colors['bg_medium'], height=180)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Logo and title container
        title_container = tk.Frame(header, bg=self.colors['bg_medium'])
        title_container.pack(expand=True)
        
        # Animated logo
        self.logo_label = tk.Label(
            title_container,
            text="🚀",
            font=("Segoe UI Emoji", 56),
            bg=self.colors['bg_medium'],
            fg=self.colors['primary']
        )
        self.logo_label.pack(pady=(20, 10))
        
        # Main title
        tk.Label(
            title_container,
            text="نظام DED الإداري المتكامل",
            font=("Arial", 26, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_white']
        ).pack()
        
        # Subtitle
        tk.Label(
            title_container,
            text="DED Management System - Professional Edition",
            font=("Segoe UI", 11),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_muted']
        ).pack(pady=(5, 20))
    
    def create_status_card(self, parent):
        """Create status card with modern design"""
        card = self.create_card(parent)
        card.pack(fill=tk.X, pady=(0, 20))
        
        # Card header
        header = tk.Frame(card, bg=self.colors['bg_light'], height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📊  حالة النظام - System Status",
            font=("Segoe UI", 13, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            anchor="w"
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Status content
        status_content = tk.Frame(card, bg=self.colors['bg_card'])
        status_content.pack(fill=tk.X, padx=25, pady=20)
        
        # Status indicator
        indicator_frame = tk.Frame(status_content, bg=self.colors['bg_card'])
        indicator_frame.pack()
        
        self.status_dot = tk.Label(
            indicator_frame,
            text="●",
            font=("Arial", 32),
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted']
        )
        self.status_dot.pack(side=tk.LEFT, padx=(0, 15))
        
        status_text_frame = tk.Frame(indicator_frame, bg=self.colors['bg_card'])
        status_text_frame.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(
            status_text_frame,
            text="التطبيق متوقف",
            font=("Arial", 18, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_gray']
        )
        self.status_label.pack(anchor="w")
        
        self.status_sublabel = tk.Label(
            status_text_frame,
            text="Application Stopped",
            font=("Segoe UI", 11),
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted']
        )
        self.status_sublabel.pack(anchor="w")

    def create_control_panel(self, parent):
        """Create control panel with modern buttons"""
        card = self.create_card(parent)
        card.pack(fill=tk.X, pady=(0, 20))

        # Card header
        header = tk.Frame(card, bg=self.colors['bg_light'], height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🎮  لوحة التحكم - Control Panel",
            font=("Segoe UI", 13, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            anchor="w"
        ).pack(side=tk.LEFT, padx=20, pady=15)

        # Buttons container
        btn_container = tk.Frame(card, bg=self.colors['bg_card'])
        btn_container.pack(fill=tk.X, padx=25, pady=25)

        # Configure grid
        btn_container.columnconfigure(0, weight=1)
        btn_container.columnconfigure(1, weight=1)
        btn_container.columnconfigure(2, weight=1)

        # Start button
        self.start_btn = self.create_modern_button(
            btn_container,
            "▶  تشغيل التطبيق",
            "Start Application",
            self.colors['success'],
            self.colors['success_dark'],
            self.start_app
        )
        self.start_btn.grid(row=0, column=0, padx=8, pady=5, sticky="ew")

        # Stop button
        self.stop_btn = self.create_modern_button(
            btn_container,
            "⏹  إيقاف التطبيق",
            "Stop Application",
            self.colors['danger'],
            self.colors['danger_dark'],
            self.stop_app,
            state='disabled'
        )
        self.stop_btn.grid(row=0, column=1, padx=8, pady=5, sticky="ew")

        # Browser button
        self.browser_btn = self.create_modern_button(
            btn_container,
            "🌐  فتح المتصفح",
            "Open Browser",
            self.colors['primary'],
            self.colors['primary_dark'],
            self.open_browser
        )
        self.browser_btn.grid(row=0, column=2, padx=8, pady=5, sticky="ew")

        # Network browser button (second row)
        if self.local_ip:
            self.network_btn = self.create_modern_button(
                btn_container,
                "🌍  فتح رابط الشبكة",
                "Open Network URL",
                self.colors['accent'],
                '#7c3aed',
                self.open_network_browser
            )
            self.network_btn.grid(row=1, column=0, columnspan=3, padx=8, pady=(10, 5), sticky="ew")

    def create_info_cards(self, parent):
        """Create info cards"""
        cards_container = tk.Frame(parent, bg=self.colors['bg_dark'])
        cards_container.pack(fill=tk.BOTH, expand=True)

        # Configure grid
        cards_container.columnconfigure(0, weight=1)
        cards_container.columnconfigure(1, weight=1)

        # Login info card
        login_card = self.create_card(cards_container)
        login_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        self.create_info_card_content(
            login_card,
            "🔐  معلومات الدخول",
            "Login Information",
            [
                ("👤  اسم المستخدم", "admin"),
                ("🔑  كلمة المرور", "admin123")
            ]
        )

        # Connection info card
        conn_card = self.create_card(cards_container)
        conn_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        network_url = f"http://{self.local_ip}:5000" if self.local_ip else "http://127.0.0.1:5000"

        self.create_info_card_content(
            conn_card,
            "🌐  معلومات الاتصال",
            "Connection Info",
            [
                ("💻  الرابط المحلي", "http://127.0.0.1:5000"),
                ("🌍  رابط الشبكة", network_url),
                ("📡  المنفذ", "5000")
            ]
        )

    def create_info_card_content(self, card, title_ar, title_en, items):
        """Create content for info card"""
        # Header
        header = tk.Frame(card, bg=self.colors['bg_light'], height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text=title_ar,
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            anchor="w"
        ).pack(side=tk.LEFT, padx=20, pady=15)

        # Content
        content = tk.Frame(card, bg=self.colors['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        for label, value in items:
            item_frame = tk.Frame(content, bg=self.colors['bg_card'])
            item_frame.pack(fill=tk.X, pady=8)

            tk.Label(
                item_frame,
                text=label,
                font=("Segoe UI", 10),
                bg=self.colors['bg_card'],
                fg=self.colors['text_muted'],
                anchor="w"
            ).pack(anchor="w")

            value_label = tk.Label(
                item_frame,
                text=value,
                font=("Consolas", 11, "bold"),
                bg=self.colors['bg_card'],
                fg=self.colors['primary'],
                anchor="w",
                cursor="hand2"
            )
            value_label.pack(anchor="w", pady=(2, 0))
            value_label.bind("<Button-1>", lambda e, v=value: self.copy_to_clipboard(v))
            value_label.bind("<Enter>", lambda e, l=value_label: l.config(fg=self.colors['accent']))
            value_label.bind("<Leave>", lambda e, l=value_label: l.config(fg=self.colors['primary']))

    def create_footer(self, parent):
        """Create footer"""
        footer = tk.Frame(parent, bg=self.colors['bg_medium'], height=60)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)

        # Separator line
        tk.Frame(footer, bg=self.colors['border'], height=1).pack(fill=tk.X)

        footer_content = tk.Frame(footer, bg=self.colors['bg_medium'])
        footer_content.pack(expand=True)

        # Copyright
        tk.Label(
            footer_content,
            text="© 2026 DED Management System - All Rights Reserved",
            font=("Segoe UI", 9),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_muted']
        ).pack(side=tk.LEFT, padx=20)

        # Version
        tk.Label(
            footer_content,
            text="v1.2.0",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['primary']
        ).pack(side=tk.RIGHT, padx=20)

    def create_card(self, parent):
        """Create a modern card container"""
        card = tk.Frame(parent, bg=self.colors['bg_card'], relief=tk.FLAT, bd=0)
        # Add subtle shadow effect with border
        card.configure(highlightbackground=self.colors['border'], highlightthickness=1)
        return card

    def create_modern_button(self, parent, text_ar, text_en, bg_color, hover_color, command, state='normal'):
        """Create modern button with hover effect"""
        btn = tk.Button(
            parent,
            text=f"{text_ar}\n{text_en}",
            font=("Segoe UI", 11, "bold"),
            bg=bg_color,
            fg=self.colors['text_white'],
            activebackground=hover_color,
            activeforeground=self.colors['text_white'],
            relief=tk.FLAT,
            cursor="hand2" if state == 'normal' else "",
            command=command,
            state=state,
            height=3,
            bd=0
        )

        # Hover effects
        if state == 'normal':
            btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
            btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))

        return btn

    def get_local_ip(self):
        """Get local IP address"""
        try:
            # Create a socket to get the local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return None

    def animate_startup(self):
        """Animate logo on startup"""
        def pulse():
            for size in [56, 60, 56]:
                self.logo_label.config(font=("Segoe UI Emoji", size))
                self.root.update()
                time.sleep(0.1)

        threading.Thread(target=pulse, daemon=True).start()

    def start_app(self):
        """Start Flask application"""
        if self.is_running:
            messagebox.showwarning(
                "⚠️ تحذير - Warning",
                "التطبيق يعمل بالفعل!\n\nApplication is already running!",
                parent=self.root
            )
            return

        try:
            python_exe = self.app_dir / "venv" / "Scripts" / "python.exe"
            run_py = self.app_dir / "run.py"

            if not python_exe.exists() or not run_py.exists():
                messagebox.showerror(
                    "❌ خطأ - Error",
                    f"الملفات المطلوبة غير موجودة!\n\nRequired files not found!\n\n{python_exe}\n{run_py}",
                    parent=self.root
                )
                return

            # Kill old processes
            subprocess.run(
                "taskkill /F /IM python.exe /FI \"WINDOWTITLE eq Flask*\" 2>nul",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
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
            self.update_status(True)

            # Open browser after delay
            threading.Thread(target=self.delayed_browser, daemon=True).start()

            # Show success message
            self.show_notification("✅ نجح - Success", "تم تشغيل التطبيق بنجاح!\n\nApplication started successfully!")

        except Exception as e:
            messagebox.showerror(
                "❌ خطأ - Error",
                f"فشل تشغيل التطبيق:\n\nFailed to start application:\n\n{str(e)}",
                parent=self.root
            )

    def stop_app(self):
        """Stop Flask application"""
        if self.flask_process:
            self.flask_process.terminate()
            self.flask_process = None

        subprocess.run(
            "taskkill /F /IM python.exe /FI \"WINDOWTITLE eq Flask*\" 2>nul",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        self.is_running = False
        self.update_status(False)

        self.show_notification("⏹ تم الإيقاف - Stopped", "تم إيقاف التطبيق بنجاح!\n\nApplication stopped successfully!")

    def delayed_browser(self):
        """Open browser after delay"""
        time.sleep(3)
        webbrowser.open("http://127.0.0.1:5000")

    def open_browser(self):
        """Open browser immediately"""
        webbrowser.open("http://127.0.0.1:5000")
        self.show_notification("🌐 المتصفح - Browser", "تم فتح المتصفح!\n\nBrowser opened!")

    def open_network_browser(self):
        """Open network browser"""
        if self.local_ip:
            url = f"http://{self.local_ip}:5000"
            webbrowser.open(url)
            self.show_notification("🌍 رابط الشبكة - Network URL", f"تم فتح رابط الشبكة!\n\n{url}")

    def update_status(self, running):
        """Update status display"""
        if running:
            self.status_dot.config(fg=self.colors['success'])
            self.status_label.config(text="التطبيق يعمل", fg=self.colors['success'])
            self.status_sublabel.config(text="Application Running")
            self.start_btn.config(state='disabled', cursor="")
            self.stop_btn.config(state='normal', cursor="hand2")

            # Animate status dot
            self.animate_status_dot()
        else:
            self.status_dot.config(fg=self.colors['text_muted'])
            self.status_label.config(text="التطبيق متوقف", fg=self.colors['text_gray'])
            self.status_sublabel.config(text="Application Stopped")
            self.start_btn.config(state='normal', cursor="hand2")
            self.stop_btn.config(state='disabled', cursor="")

    def animate_status_dot(self):
        """Animate status dot when running"""
        if self.is_running:
            current_color = self.status_dot.cget('fg')
            new_color = self.colors['success_dark'] if current_color == self.colors['success'] else self.colors['success']
            self.status_dot.config(fg=new_color)
            self.root.after(800, self.animate_status_dot)

    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.show_notification("📋 تم النسخ - Copied", f"تم نسخ: {text}\n\nCopied: {text}")

    def show_notification(self, title, message):
        """Show notification toast"""
        # Create notification window
        notif = tk.Toplevel(self.root)
        notif.title(title)
        notif.geometry("400x120")
        notif.resizable(False, False)
        notif.configure(bg=self.colors['bg_medium'])

        # Remove window decorations
        notif.overrideredirect(True)

        # Position at bottom right
        x = self.root.winfo_x() + self.root.winfo_width() - 420
        y = self.root.winfo_y() + self.root.winfo_height() - 140
        notif.geometry(f"+{x}+{y}")

        # Border
        notif.configure(highlightbackground=self.colors['primary'], highlightthickness=2)

        # Content
        tk.Label(
            notif,
            text=title,
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_white']
        ).pack(pady=(15, 5))

        tk.Label(
            notif,
            text=message,
            font=("Segoe UI", 9),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_gray'],
            justify=tk.CENTER
        ).pack(pady=(0, 15))

        # Auto close after 2 seconds
        notif.after(2000, notif.destroy)

        # Fade in effect
        notif.attributes('-alpha', 0.0)
        self.fade_in(notif)

    def fade_in(self, window, alpha=0.0):
        """Fade in animation"""
        if alpha < 1.0:
            alpha += 0.1
            window.attributes('-alpha', alpha)
            window.after(30, lambda: self.fade_in(window, alpha))

    def on_close(self):
        """Handle window close"""
        if self.is_running:
            if messagebox.askyesno(
                "⚠️ تأكيد الخروج - Confirm Exit",
                "التطبيق يعمل حالياً. هل تريد إيقافه والخروج؟\n\nApplication is running. Stop and exit?",
                parent=self.root
            ):
                self.stop_app()
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalLauncher(root)
    root.mainloop()



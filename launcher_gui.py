#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DED ERP System - Beautiful GUI Launcher
Launches both Application and License Manager
"""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys
import webbrowser
import threading
import time

class DEDLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("DED ERP System - نظام DED")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Set colors
        self.bg_color = "#2C3E50"
        self.accent_color = "#3498DB"
        self.success_color = "#27AE60"
        self.warning_color = "#E74C3C"
        
        self.root.configure(bg=self.bg_color)
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_ui()
        
        # Process references
        self.app_process = None
        self.license_process = None
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_ui(self):
        """Create the user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.accent_color, height=100)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="🏢 DED ERP System",
            font=("Arial", 24, "bold"),
            bg=self.accent_color,
            fg="white"
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text="نظام تخطيط موارد المؤسسات",
            font=("Arial", 12),
            bg=self.accent_color,
            fg="white"
        )
        subtitle_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Application button
        app_btn = tk.Button(
            content_frame,
            text="🚀 تشغيل التطبيق الرئيسي\nLaunch Main Application",
            font=("Arial", 14, "bold"),
            bg=self.success_color,
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            height=3,
            command=self.launch_application
        )
        app_btn.pack(fill=tk.X, pady=10)
        
        # License Manager button
        license_btn = tk.Button(
            content_frame,
            text="🔑 نظام إدارة التراخيص\nLicense Manager",
            font=("Arial", 14, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground="#2980B9",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            height=3,
            command=self.launch_license_manager
        )
        license_btn.pack(fill=tk.X, pady=10)
        
        # Open Browser button
        browser_btn = tk.Button(
            content_frame,
            text="🌐 فتح التطبيق في المتصفح\nOpen in Browser",
            font=("Arial", 12),
            bg="#8E44AD",
            fg="white",
            activebackground="#7D3C98",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            height=2,
            command=self.open_browser
        )
        browser_btn.pack(fill=tk.X, pady=10)
        
        # Info frame
        info_frame = tk.Frame(content_frame, bg="#34495E", relief=tk.RIDGE, bd=2)
        info_frame.pack(fill=tk.X, pady=20)
        
        info_text = tk.Label(
            info_frame,
            text="📍 URL: http://localhost:5000\n👤 Username: admin | 🔑 Password: admin123",
            font=("Arial", 10),
            bg="#34495E",
            fg="white",
            justify=tk.LEFT,
            padx=10,
            pady=10
        )
        info_text.pack()
        
        # Exit button
        exit_btn = tk.Button(
            content_frame,
            text="❌ خروج - Exit",
            font=("Arial", 11),
            bg=self.warning_color,
            fg="white",
            activebackground="#C0392B",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.exit_app
        )
        exit_btn.pack(fill=tk.X, pady=10)
        
    def launch_application(self):
        """Launch the main ERP application"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            bat_file = os.path.join(script_dir, "Launch_ERP_Application.bat")
            
            if not os.path.exists(bat_file):
                messagebox.showerror(
                    "خطأ - Error",
                    "ملف التشغيل غير موجود!\nLaunch file not found!"
                )
                return
            
            # Launch in new window
            self.app_process = subprocess.Popen(
                [bat_file],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                cwd=script_dir
            )
            
            messagebox.showinfo(
                "نجح - Success",
                "✅ تم تشغيل التطبيق!\n✅ Application launched!\n\n"
                "سيفتح المتصفح تلقائياً بعد ثوانٍ...\n"
                "Browser will open automatically in seconds..."
            )
            
        except Exception as e:
            messagebox.showerror(
                "خطأ - Error",
                f"فشل تشغيل التطبيق!\nFailed to launch application!\n\n{str(e)}"
            )
    
    def launch_license_manager(self):
        """Launch the License Manager"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            bat_file = os.path.join(script_dir, "Launch_License_Manager.bat")
            
            if not os.path.exists(bat_file):
                messagebox.showerror(
                    "خطأ - Error",
                    "ملف نظام التراخيص غير موجود!\nLicense Manager file not found!"
                )
                return
            
            # Launch in new window
            self.license_process = subprocess.Popen(
                [bat_file],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                cwd=script_dir
            )
            
            messagebox.showinfo(
                "نجح - Success",
                "✅ تم تشغيل نظام التراخيص!\n✅ License Manager launched!"
            )
            
        except Exception as e:
            messagebox.showerror(
                "خطأ - Error",
                f"فشل تشغيل نظام التراخيص!\nFailed to launch License Manager!\n\n{str(e)}"
            )
    
    def open_browser(self):
        """Open the application in browser"""
        try:
            webbrowser.open('http://localhost:5000')
            messagebox.showinfo(
                "نجح - Success",
                "✅ تم فتح المتصفح!\n✅ Browser opened!\n\n"
                "إذا لم يفتح التطبيق، تأكد من تشغيله أولاً.\n"
                "If app doesn't open, make sure to launch it first."
            )
        except Exception as e:
            messagebox.showerror(
                "خطأ - Error",
                f"فشل فتح المتصفح!\nFailed to open browser!\n\n{str(e)}"
            )
    
    def exit_app(self):
        """Exit the launcher"""
        if messagebox.askokcancel(
            "خروج - Exit",
            "هل تريد الخروج؟\nDo you want to exit?"
        ):
            self.root.destroy()

def main():
    root = tk.Tk()
    app = DEDLauncher(root)
    root.mainloop()

if __name__ == '__main__':
    main()


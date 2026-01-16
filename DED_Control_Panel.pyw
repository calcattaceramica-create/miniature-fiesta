import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta
import hashlib
import secrets
import webbrowser
import sys
import os
import uuid
import platform
import sqlite3
from werkzeug.security import generate_password_hash

class DEDControlPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 DED Control Panel - لوحة التحكم الشاملة")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        self.root.minsize(1000, 700)

        # Modern Light Theme Colors - واضح وجميل
        self.colors = {
            'bg': '#f8fafc',              # خلفية فاتحة جداً
            'bg_light': '#ffffff',         # أبيض نقي
            'card': '#ffffff',             # بطاقات بيضاء
            'accent': '#3b82f6',          # أزرق حديث
            'accent_hover': '#2563eb',    # أزرق داكن عند التمرير
            'success': '#22c55e',         # أخضر واضح
            'success_hover': '#16a34a',   # أخضر داكن
            'danger': '#ef4444',          # أحمر واضح
            'danger_hover': '#dc2626',    # أحمر داكن
            'warning': '#f59e0b',         # برتقالي
            'warning_hover': '#d97706',   # برتقالي داكن
            'info': '#06b6d4',            # سماوي
            'text': '#1e293b',            # نص داكن واضح
            'text_gray': '#64748b',       # نص رمادي
            'text_muted': '#94a3b8',      # نص باهت
            'border': '#e2e8f0',          # حدود فاتحة
            'green_line': '#22c55e',      # خط أخضر
            'purple_tab': '#a855f7',      # بنفسجي
            'shadow': '#00000010'          # ظل خفيف
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # App directory
        self.app_dir = Path.cwd()
        self.license_file = self.app_dir / "licenses.json"
        self.licenses = self.load_licenses()
        
        # Flask process
        self.flask_process = None
        self.is_running = False
        
        # Build UI
        self.create_ui()
        self.center_window()
        
        # Check status
        self.root.after(500, self.check_status)
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_licenses(self):
        if self.license_file.exists():
            try:
                with open(self.license_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_licenses(self):
        with open(self.license_file, 'w', encoding='utf-8') as f:
            json.dump(self.licenses, f, indent=2, ensure_ascii=False)
    
    def create_ui(self):
        # Main container with gradient effect
        main = tk.Frame(self.root, bg=self.colors['bg'])
        main.pack(fill=tk.BOTH, expand=True)

        # Header with shadow effect
        header = tk.Frame(main, bg=self.colors['bg_light'], height=120)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Add subtle shadow line
        tk.Frame(main, bg=self.colors['border'], height=1).pack(fill=tk.X)

        header_content = tk.Frame(header, bg=self.colors['bg_light'])
        header_content.pack(expand=True, pady=20)

        # Logo with gradient background
        logo_frame = tk.Frame(header_content, bg=self.colors['accent'], width=80, height=80)
        logo_frame.pack(side=tk.LEFT, padx=(30, 20))
        logo_frame.pack_propagate(False)

        tk.Label(
            logo_frame,
            text="🚀",
            font=("Segoe UI Emoji", 45),
            bg=self.colors['accent'],
            fg='white'
        ).pack(expand=True)

        # Title section
        title_frame = tk.Frame(header_content, bg=self.colors['bg_light'])
        title_frame.pack(side=tk.LEFT)

        tk.Label(
            title_frame,
            text="DED Control Panel",
            font=("Segoe UI", 28, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text']
        ).pack(anchor='w')

        tk.Label(
            title_frame,
            text="لوحة التحكم الشاملة - نظام إدارة متكامل وسهل الاستخدام",
            font=("Segoe UI", 12),
            bg=self.colors['bg_light'],
            fg=self.colors['text_gray']
        ).pack(anchor='w', pady=(5, 0))

        # Decorative line
        tk.Frame(main, bg=self.colors['green_line'], height=4).pack(fill=tk.X)

        # Tabs
        self.create_tabs(main)
    
    def create_tabs(self, parent):
        # Tab container with padding
        tab_container = tk.Frame(parent, bg=self.colors['bg'])
        tab_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Tab buttons frame with modern design
        tab_buttons = tk.Frame(tab_container, bg=self.colors['bg'])
        tab_buttons.pack(fill=tk.X, pady=(0, 15))

        # Tab button 1 - App Control (larger and clearer)
        self.app_tab_btn = tk.Button(
            tab_buttons,
            text="📱 تشغيل التطبيق\nApp Control",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['accent'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.switch_tab(0),
            padx=30,
            pady=15,
            borderwidth=0,
            activebackground=self.colors['accent_hover'],
            activeforeground='white'
        )
        self.app_tab_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Tab button 2 - License Manager (larger and clearer)
        self.license_tab_btn = tk.Button(
            tab_buttons,
            text="🔐 مدير التراخيص\nLicense Manager",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['text_gray'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.switch_tab(1),
            padx=30,
            pady=15,
            borderwidth=0,
            activebackground=self.colors['purple_tab'],
            activeforeground='white'
        )
        self.license_tab_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Content frame with card design
        self.content_frame = tk.Frame(tab_container, bg=self.colors['bg'])
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Create tab contents
        self.app_tab = tk.Frame(self.content_frame, bg=self.colors['bg'])
        self.license_tab = tk.Frame(self.content_frame, bg=self.colors['bg'])

        self.create_app_tab()
        self.create_license_tab()

        # Show first tab
        self.current_tab = 0
        self.switch_tab(0)

    def switch_tab(self, tab_index):
        # Hide all tabs
        self.app_tab.pack_forget()
        self.license_tab.pack_forget()

        # Reset button colors to inactive state
        self.app_tab_btn.config(bg=self.colors['text_gray'], fg='white')
        self.license_tab_btn.config(bg=self.colors['text_gray'], fg='white')

        # Show selected tab with active color
        if tab_index == 0:
            self.app_tab.pack(fill=tk.BOTH, expand=True)
            self.app_tab_btn.config(bg=self.colors['accent'], fg='white')
        else:
            self.license_tab.pack(fill=tk.BOTH, expand=True)
            self.license_tab_btn.config(bg=self.colors['purple_tab'], fg='white')

        self.current_tab = tab_index

    def create_app_tab(self):
        # Status Card with modern design
        status_card = tk.Frame(self.app_tab, bg=self.colors['card'], relief=tk.FLAT, borderwidth=0)
        status_card.pack(fill=tk.X, padx=10, pady=(0, 20))

        # Add border effect
        tk.Frame(status_card, bg=self.colors['border'], height=1).pack(fill=tk.X)

        # Card header
        tk.Label(
            status_card,
            text="📊 حالة النظام - System Status",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(pady=(20, 10))

        # Status indicator with larger font
        self.status_label = tk.Label(
            status_card,
            text="⚫ متوقف - Stopped",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text_gray']
        )
        self.status_label.pack(pady=15)

        # URL with better visibility
        self.url_label = tk.Label(
            status_card,
            text="🌐 http://127.0.0.1:5000",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['card'],
            fg=self.colors['info'],
            cursor="hand2"
        )
        self.url_label.pack(pady=(0, 20))
        self.url_label.bind("<Button-1>", lambda e: self.open_browser())

        # Bottom border
        tk.Frame(status_card, bg=self.colors['border'], height=1).pack(fill=tk.X)

        # Control Buttons with modern card design
        btn_frame = tk.Frame(self.app_tab, bg=self.colors['bg'])
        btn_frame.pack(pady=10, padx=10, fill=tk.X)

        # Start button - larger and clearer
        self.start_btn = tk.Button(
            btn_frame,
            text="▶️ تشغيل التطبيق\nStart Application",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start_app,
            width=25,
            height=4,
            borderwidth=0,
            activebackground=self.colors['success_hover'],
            activeforeground='white'
        )
        self.start_btn.grid(row=0, column=0, padx=10, pady=5, sticky='ew')

        # Stop button - larger and clearer
        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹️ إيقاف التطبيق\nStop Application",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['danger'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=self.stop_app,
            width=25,
            height=4,
            state='disabled',
            borderwidth=0,
            activebackground=self.colors['danger_hover'],
            activeforeground='white'
        )
        self.stop_btn.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

        # Open browser button - larger and clearer
        tk.Button(
            btn_frame,
            text="🌐 فتح المتصفح\nOpen Browser",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['accent'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=self.open_browser,
            width=25,
            height=4,
            borderwidth=0,
            activebackground=self.colors['accent_hover'],
            activeforeground='white'
        ).grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='ew')

        # Make columns expand equally
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        # Info Card with modern design
        info_card = tk.Frame(self.app_tab, bg=self.colors['card'], relief=tk.FLAT)
        info_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Top border
        tk.Frame(info_card, bg=self.colors['border'], height=1).pack(fill=tk.X)

        tk.Label(
            info_card,
            text="ℹ️ معلومات النظام - System Information",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(pady=(20, 15))

        # Info items with better formatting
        info_items = [
            ("🌐", "عنوان التطبيق - URL", "http://127.0.0.1:5000"),
            ("👤", "اسم المستخدم - Username", "admin"),
            ("🔑", "كلمة المرور - Password", "admin123"),
            ("📁", "مسار التطبيق - Path", str(self.app_dir))
        ]

        for icon, label, value in info_items:
            item_frame = tk.Frame(info_card, bg=self.colors['card'])
            item_frame.pack(fill=tk.X, padx=30, pady=8)

            tk.Label(
                item_frame,
                text=f"{icon} {label}:",
                font=("Segoe UI", 13, "bold"),
                bg=self.colors['card'],
                fg=self.colors['text'],
                anchor='w'
            ).pack(side=tk.LEFT, padx=(0, 10))

            tk.Label(
                item_frame,
                text=value,
                font=("Segoe UI", 13),
                bg=self.colors['card'],
                fg=self.colors['info'],
                anchor='w'
            ).pack(side=tk.LEFT)

        # Bottom padding
        tk.Frame(info_card, bg=self.colors['card'], height=20).pack()

        # Bottom border
        tk.Frame(info_card, bg=self.colors['border'], height=1).pack(fill=tk.X)

        # License Management Quick Access Card
        license_quick_card = tk.Frame(self.app_tab, bg=self.colors['card'], relief=tk.FLAT)
        license_quick_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Top border
        tk.Frame(license_quick_card, bg=self.colors['border'], height=1).pack(fill=tk.X)

        tk.Label(
            license_quick_card,
            text="🔐 إدارة التراخيص السريعة - Quick License Management",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(pady=(20, 15))

        # License Statistics Row
        stats_row = tk.Frame(license_quick_card, bg=self.colors['card'])
        stats_row.pack(fill=tk.X, padx=30, pady=(0, 15))

        # Helper function for stat cards
        def create_stat_card(parent, icon, title, value_var_name, color):
            card = tk.Frame(parent, bg=color, relief=tk.FLAT)
            card.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.BOTH)

            tk.Label(
                card,
                text=icon,
                font=("Segoe UI Emoji", 32),
                bg=color,
                fg='white'
            ).pack(pady=(15, 5))

            value_label = tk.Label(
                card,
                text="0",
                font=("Segoe UI", 28, "bold"),
                bg=color,
                fg='white'
            )
            value_label.pack()
            setattr(self, value_var_name, value_label)

            tk.Label(
                card,
                text=title,
                font=("Segoe UI", 11, "bold"),
                bg=color,
                fg='white'
            ).pack(pady=(5, 15))

            return card

        # Create stat cards
        create_stat_card(stats_row, "📊", "إجمالي التراخيص\nTotal Licenses",
                        "total_licenses_label", self.colors['accent'])
        create_stat_card(stats_row, "✅", "تراخيص نشطة\nActive Licenses",
                        "active_licenses_label", self.colors['success'])
        create_stat_card(stats_row, "⏸️", "تراخيص معلقة\nSuspended",
                        "suspended_licenses_label", self.colors['warning'])
        create_stat_card(stats_row, "⚠️", "تراخيص منتهية\nExpired",
                        "expired_licenses_label", self.colors['danger'])

        # Recent Licenses Section
        recent_frame = tk.Frame(license_quick_card, bg=self.colors['card'])
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(10, 15))

        tk.Label(
            recent_frame,
            text="📋 آخر التراخيص المضافة - Recent Licenses",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 10))

        # Recent licenses list with scrollbar
        recent_list_frame = tk.Frame(recent_frame, bg=self.colors['bg'])
        recent_list_frame.pack(fill=tk.BOTH, expand=True)

        recent_scrollbar = tk.Scrollbar(recent_list_frame)
        recent_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.recent_licenses_listbox = tk.Listbox(
            recent_list_frame,
            font=("Segoe UI", 11),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            borderwidth=0,
            yscrollcommand=recent_scrollbar.set,
            height=5,
            selectbackground=self.colors['accent'],
            selectforeground='white'
        )
        self.recent_licenses_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        recent_scrollbar.config(command=self.recent_licenses_listbox.yview)

        # Quick Action Buttons
        quick_actions = tk.Frame(license_quick_card, bg=self.colors['card'])
        quick_actions.pack(fill=tk.X, padx=30, pady=(10, 20))

        tk.Button(
            quick_actions,
            text="➕ إضافة ترخيص جديد\nAdd New License",
            font=("Segoe UI", 13, "bold"),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.switch_tab(1),
            padx=25,
            pady=12,
            borderwidth=0,
            activebackground=self.colors['success_hover'],
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        tk.Button(
            quick_actions,
            text="📋 عرض جميع التراخيص\nView All Licenses",
            font=("Segoe UI", 13, "bold"),
            bg=self.colors['accent'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.switch_tab(1),
            padx=25,
            pady=12,
            borderwidth=0,
            activebackground=self.colors['accent_hover'],
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        tk.Button(
            quick_actions,
            text="🔄 تحديث الإحصائيات\nRefresh Stats",
            font=("Segoe UI", 13, "bold"),
            bg=self.colors['info'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=self.update_license_stats,
            padx=25,
            pady=12,
            borderwidth=0,
            activebackground=self.colors['accent'],
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Bottom border
        tk.Frame(license_quick_card, bg=self.colors['border'], height=1).pack(fill=tk.X)

        # Update license stats initially
        self.update_license_stats()

    def create_license_tab(self):
        # Create main container with scrollbar
        main_container = tk.Frame(self.license_tab, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Create canvas and scrollbar
        canvas = tk.Canvas(main_container, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)

        # Bind canvas width to scrollable frame width
        def on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)

        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add License Card with modern design
        add_card = tk.Frame(scrollable_frame, bg=self.colors['card'], relief=tk.FLAT)
        add_card.pack(fill=tk.X, padx=10, pady=(10, 15))

        # Top border
        tk.Frame(add_card, bg=self.colors['border'], height=1).pack(fill=tk.X)

        tk.Label(
            add_card,
            text="➕ إضافة ترخيص جديد - Add New License",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(pady=(20, 15))

        form = tk.Frame(add_card, bg=self.colors['card'])
        form.pack(padx=30, pady=(0, 20), fill=tk.X)

        # Helper function to create form rows
        def create_form_row(parent, label_text, entry_var_name, default_value="", show_char=None):
            row = tk.Frame(parent, bg=self.colors['card'])
            row.pack(fill=tk.X, pady=8)

            # Label on the right
            tk.Label(
                row,
                text=label_text,
                font=("Segoe UI", 14, "bold"),
                bg=self.colors['card'],
                fg=self.colors['text'],
                width=25,
                anchor='e'
            ).pack(side=tk.RIGHT, padx=15)

            # Entry on the left
            entry = tk.Entry(
                row,
                font=("Segoe UI", 14),
                width=40,
                relief=tk.FLAT,
                bg=self.colors['bg'],
                fg=self.colors['text'],
                insertbackground=self.colors['text'],
                show=show_char if show_char else ""
            )
            entry.pack(side=tk.LEFT, padx=15, ipady=8)
            if default_value:
                entry.insert(0, default_value)

            setattr(self, entry_var_name, entry)
            return entry

        # Company Name
        create_form_row(form, "🏢 اسم الشركة - Company:", "company_entry")

        # Duration
        create_form_row(form, "⏱️ المدة (أيام) - Duration:", "duration_entry", "365")

        # Username
        create_form_row(form, "👤 اسم المستخدم - Username:", "username_entry")

        # Password
        create_form_row(form, "🔑 كلمة المرور - Password:", "password_entry", show_char="*")

        # Email
        create_form_row(form, "📧 البريد الإلكتروني - Email:", "email_entry")

        # Phone
        create_form_row(form, "📱 رقم الهاتف - Phone:", "phone_entry")

        # Max Users
        create_form_row(form, "👥 عدد المستخدمين - Max Users:", "max_users_entry", "10")

        # Notes
        create_form_row(form, "📝 ملاحظات - Notes:", "notes_entry")

        # Bottom border
        tk.Frame(add_card, bg=self.colors['border'], height=1).pack(fill=tk.X)

        # Buttons with modern design
        btn_frame = tk.Frame(add_card, bg=self.colors['card'])
        btn_frame.pack(pady=(10, 20), padx=30, fill=tk.X)

        tk.Button(
            btn_frame,
            text="✨ إنشاء ترخيص\nGenerate License",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=self.generate_license,
            padx=30,
            pady=15,
            borderwidth=0,
            activebackground=self.colors['success_hover'],
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        tk.Button(
            btn_frame,
            text="🔄 مسح الحقول\nClear Form",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['warning'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_form,
            padx=30,
            pady=15,
            borderwidth=0,
            activebackground=self.colors['warning_hover'],
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        tk.Button(
            btn_frame,
            text="🔧 تطبيق Migration\nApply Migration",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['info'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=self.apply_migration,
            padx=30,
            pady=15,
            borderwidth=0,
            activebackground=self.colors['accent'],
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Licenses List with modern design
        list_card = tk.Frame(scrollable_frame, bg=self.colors['card'], relief=tk.FLAT)
        list_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Top border
        tk.Frame(list_card, bg=self.colors['border'], height=1).pack(fill=tk.X)

        tk.Label(
            list_card,
            text="📋 التراخيص المسجلة - Registered Licenses",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(pady=(20, 15))

        # Treeview with modern styling
        tree_frame = tk.Frame(list_card, bg=self.colors['bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        # Configure treeview style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       fieldbackground=self.colors['bg'],
                       borderwidth=0,
                       font=('Segoe UI', 11))
        style.configure("Treeview.Heading",
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       font=('Segoe UI', 12, 'bold'))
        style.map('Treeview', background=[('selected', self.colors['accent'])])

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=('company', 'key', 'expiry', 'status'),
            show='headings',
            yscrollcommand=scrollbar.set,
            height=10
        )

        self.tree.heading('company', text='🏢 الشركة - Company')
        self.tree.heading('key', text='🔑 مفتاح الترخيص - License Key')
        self.tree.heading('expiry', text='📅 تاريخ الانتهاء - Expiry')
        self.tree.heading('status', text='✅ الحالة - Status')

        self.tree.column('company', width=250, anchor='center')
        self.tree.column('key', width=400, anchor='center')
        self.tree.column('expiry', width=200, anchor='center')
        self.tree.column('status', width=150, anchor='center')

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)

        # Action buttons with modern design
        action_frame = tk.Frame(list_card, bg=self.colors['card'])
        action_frame.pack(pady=(10, 20), padx=20, fill=tk.X)

        # Helper function for action buttons
        def create_action_btn(parent, text, command, bg_color, hover_color):
            btn = tk.Button(
                parent,
                text=text,
                font=("Segoe UI", 12, "bold"),
                bg=bg_color,
                fg='white',
                relief=tk.FLAT,
                cursor="hand2",
                command=command,
                padx=20,
                pady=12,
                borderwidth=0,
                activebackground=hover_color,
                activeforeground='white'
            )
            return btn

        # Row 1
        row1 = tk.Frame(action_frame, bg=self.colors['card'])
        row1.pack(fill=tk.X, pady=(0, 8))

        create_action_btn(row1, "📋 نسخ المفتاح\nCopy Key",
                         self.copy_key, self.colors['accent'], self.colors['accent_hover']).pack(
                         side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        create_action_btn(row1, "✅ تفعيل\nActivate",
                         self.activate_license, self.colors['success'], self.colors['success_hover']).pack(
                         side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        create_action_btn(row1, "⏸️ إيقاف مؤقت\nSuspend",
                         self.suspend_license, self.colors['warning'], self.colors['warning_hover']).pack(
                         side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        create_action_btn(row1, "🗑️ حذف\nDelete",
                         self.delete_license, self.colors['danger'], self.colors['danger_hover']).pack(
                         side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Row 2
        row2 = tk.Frame(action_frame, bg=self.colors['card'])
        row2.pack(fill=tk.X)

        create_action_btn(row2, "✏️ تعديل\nEdit",
                         self.edit_license, self.colors['info'], self.colors['accent']).pack(
                         side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        create_action_btn(row2, "📄 عرض التفاصيل\nView Details",
                         self.view_license_details, self.colors['purple_tab'], self.colors['accent']).pack(
                         side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        create_action_btn(row2, "🔄 تحديث\nRefresh",
                         self.refresh_list, self.colors['success'], self.colors['success_hover']).pack(
                         side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Bottom border
        tk.Frame(list_card, bg=self.colors['border'], height=1).pack(fill=tk.X)

        # Load licenses
        self.refresh_list()

    # App Control Methods
    def start_app(self):
        try:
            # Start Flask app
            self.flask_process = subprocess.Popen(
                [sys.executable, "run.py"],
                cwd=self.app_dir,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            self.is_running = True
            self.update_status()
            messagebox.showinfo("نجح - Success", "تم تشغيل التطبيق!\nApplication started!")
        except Exception as e:
            messagebox.showerror("خطأ - Error", f"فشل تشغيل التطبيق:\n{str(e)}")

    def stop_app(self):
        if self.flask_process:
            try:
                self.flask_process.terminate()
                self.flask_process.wait(timeout=5)
            except:
                self.flask_process.kill()
            self.flask_process = None

        self.is_running = False
        self.update_status()
        messagebox.showinfo("نجح - Success", "تم إيقاف التطبيق!\nApplication stopped!")

    def open_browser(self):
        """Open browser and check if app is running"""
        if not self.is_running:
            response = messagebox.askyesno(
                "تحذير - Warning",
                "⚠️ التطبيق غير مشغّل!\nApplication is not running!\n\n"
                "هل تريد تشغيل التطبيق أولاً؟\n"
                "Do you want to start the application first?"
            )
            if response:
                self.start_app()
                # Wait a moment for the app to start
                self.root.after(2000, lambda: webbrowser.open("http://127.0.0.1:5000"))
            return

        webbrowser.open("http://127.0.0.1:5000")

    def check_status(self):
        # Check if Flask is running
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 5000))
            sock.close()

            if result == 0:
                self.is_running = True
            else:
                self.is_running = False
                if self.flask_process:
                    self.flask_process = None
        except:
            self.is_running = False

        self.update_status()

    def update_status(self):
        if self.is_running:
            self.status_label.config(text="🟢 يعمل - Running", fg=self.colors['success'])
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
        else:
            self.status_label.config(text="⚫ متوقف - Stopped", fg=self.colors['text_gray'])
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')

    # License Management Methods
    def generate_license(self):
        company = self.company_entry.get().strip()
        duration = self.duration_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        max_users = self.max_users_entry.get().strip()
        notes = self.notes_entry.get().strip()

        # Validation
        if not company:
            messagebox.showerror("خطأ - Error", "الرجاء إدخال اسم الشركة!\nPlease enter company name!")
            return

        if not username:
            messagebox.showerror("خطأ - Error", "الرجاء إدخال اسم المستخدم!\nPlease enter username!")
            return

        if not password:
            messagebox.showerror("خطأ - Error", "الرجاء إدخال كلمة المرور!\nPlease enter password!")
            return

        try:
            days = int(duration)
            if days <= 0:
                raise ValueError("Duration must be positive")
        except:
            messagebox.showerror("خطأ - Error", "المدة يجب أن تكون رقماً موجباً!\nDuration must be a positive number!")
            return

        try:
            max_users_int = int(max_users)
            if max_users_int <= 0:
                raise ValueError("Max users must be positive")
        except:
            messagebox.showerror("خطأ - Error", "عدد المستخدمين يجب أن يكون رقماً موجباً!\nMax users must be a positive number!")
            return

        # Generate license key with machine binding
        machine_id = self.get_machine_id()
        key = self.create_license_key(company, machine_id)
        expiry = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save license with full details
        self.licenses[key] = {
            'company': company,
            'expiry': expiry,
            'created': created_date,
            'duration_days': days,
            'machine_id': machine_id,
            'license_type': 'Standard',
            'max_users': max_users_int,
            'features': ['all'],
            'status': 'active',
            'activation_count': 0,
            'last_check': None,
            'username': username,
            'password': password,
            'contact_email': email,
            'contact_phone': phone,
            'notes': notes
        }

        self.save_licenses()

        # Sync with database (create user account)
        self.sync_license_to_database(key, self.licenses[key])

        self.refresh_list()
        self.update_license_stats()  # Update statistics
        self.clear_form()

        # Show detailed license info
        self.show_license_details(key, self.licenses[key])

    def create_license_key(self, company, machine_id=""):
        # Create unique license key with multiple components
        timestamp = datetime.now().isoformat()
        random_part = secrets.token_hex(16)

        # Combine all parts
        data = f"{company}-{machine_id}-{timestamp}-{random_part}"
        hash_obj = hashlib.sha256(data.encode())

        # Format as XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX
        full_key = hash_obj.hexdigest()[:32].upper()
        formatted_key = '-'.join([full_key[i:i+4] for i in range(0, 32, 4)])

        return formatted_key

    def get_machine_id(self):
        # Get unique machine identifier
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['wmic', 'csproduct', 'get', 'uuid'],
                                      capture_output=True, text=True, timeout=5)
                machine_id = result.stdout.split('\n')[1].strip()
            else:
                machine_id = str(uuid.getnode())

            return hashlib.md5(machine_id.encode()).hexdigest()[:16].upper()
        except:
            return secrets.token_hex(8).upper()

    def show_license_details(self, key, data):
        # Create detailed license info window
        detail_window = tk.Toplevel(self.root)
        detail_window.title("تفاصيل الترخيص - License Details")
        detail_window.geometry("700x650")
        detail_window.configure(bg=self.colors['bg'])
        detail_window.resizable(False, False)

        # Center window
        detail_window.update_idletasks()
        x = (detail_window.winfo_screenwidth() // 2) - (700 // 2)
        y = (detail_window.winfo_screenheight() // 2) - (650 // 2)
        detail_window.geometry(f'700x650+{x}+{y}')

        # Header
        header = tk.Frame(detail_window, bg=self.colors['success'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="✅ تم إنشاء الترخيص بنجاح!",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors['success'],
            fg='white'
        ).pack(expand=True)

        # Content with scrollbar
        content_frame = tk.Frame(detail_window, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Canvas for scrolling
        canvas = tk.Canvas(content_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # License info card
        info_card = tk.Frame(scrollable_frame, bg=self.colors['card'], relief=tk.FLAT)
        info_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            info_card,
            text="📋 معلومات الترخيص الكاملة - Complete License Information",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(pady=(15, 10))

        # License details
        details = [
            ("🏢 اسم الشركة - Company Name", data.get('company', 'N/A')),
            ("🔑 مفتاح الترخيص - License Key", key),
            ("👤 اسم المستخدم - Username", data.get('username', 'N/A')),
            ("🔒 كلمة المرور - Password", data.get('password', 'N/A')),
            ("📅 تاريخ الإنشاء - Created Date", data.get('created', 'N/A')),
            ("⏱️ المدة - Duration", f"{data.get('duration_days', 0)} يوم / days"),
            ("📆 تاريخ الانتهاء - Expiry Date", data.get('expiry', 'N/A')),
            ("💻 معرف الجهاز - Machine ID", data.get('machine_id', 'N/A')),
            ("📊 نوع الترخيص - License Type", data.get('license_type', 'Standard')),
            ("👥 عدد المستخدمين - Max Users", str(data.get('max_users', 10))),
            ("✨ الميزات - Features", ', '.join(data.get('features', ['all']))),
            ("🔄 الحالة - Status", data.get('status', 'active').upper()),
            ("🔢 عدد التفعيلات - Activation Count", str(data.get('activation_count', 0))),
            ("📧 البريد الإلكتروني - Email", data.get('contact_email', 'N/A')),
            ("📞 رقم الهاتف - Phone", data.get('contact_phone', 'N/A')),
            ("📝 ملاحظات - Notes", data.get('notes', 'N/A'))
        ]

        for label, value in details:
            item_frame = tk.Frame(info_card, bg=self.colors['bg_light'])
            item_frame.pack(fill=tk.X, padx=20, pady=4)

            tk.Label(
                item_frame,
                text=label,
                font=("Segoe UI", 9),
                bg=self.colors['bg_light'],
                fg=self.colors['text_muted'],
                anchor='w'
            ).pack(anchor='w', padx=12, pady=(6, 2))

            # Make key copyable
            if "License Key" in label:
                key_label = tk.Label(
                    item_frame,
                    text=value,
                    font=("Courier New", 10, "bold"),
                    bg=self.colors['bg_light'],
                    fg=self.colors['accent'],
                    anchor='w',
                    cursor="hand2"
                )
                key_label.pack(anchor='w', padx=12, pady=(2, 6))
                key_label.bind("<Button-1>", lambda e, k=value: self.copy_to_clipboard(k, detail_window))
            else:
                tk.Label(
                    item_frame,
                    text=value,
                    font=("Segoe UI", 10, "bold"),
                    bg=self.colors['bg_light'],
                    fg=self.colors['text'],
                    anchor='w'
                ).pack(anchor='w', padx=12, pady=(2, 6))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Buttons
        btn_frame = tk.Frame(detail_window, bg=self.colors['bg'])
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="📋 نسخ المفتاح - Copy Key",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['accent'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.copy_to_clipboard(key, detail_window),
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="💾 حفظ كملف - Save to File",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.save_license_to_file(key, data),
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="❌ إغلاق - Close",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['danger'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=detail_window.destroy,
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

    def copy_to_clipboard(self, text, window=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("نجح - Success", "تم نسخ المفتاح!\nKey copied to clipboard!", parent=window if window else self.root)

    def save_license_to_file(self, key, data):
        try:
            filename = f"License_{data['company'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = self.app_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("DED MANAGEMENT SYSTEM - LICENSE CERTIFICATE\n")
                f.write("نظام إدارة DED - شهادة الترخيص\n")
                f.write("=" * 80 + "\n\n")

                f.write(f"Company Name / اسم الشركة: {data['company']}\n")
                f.write(f"\nLicense Key / مفتاح الترخيص:\n{key}\n\n")
                f.write(f"Created Date / تاريخ الإنشاء: {data['created']}\n")
                f.write(f"Duration / المدة: {data['duration_days']} days / يوم\n")
                f.write(f"Expiry Date / تاريخ الانتهاء: {data['expiry']}\n")
                f.write(f"Machine ID / معرف الجهاز: {data['machine_id']}\n")
                f.write(f"License Type / نوع الترخيص: {data['license_type']}\n")
                f.write(f"Max Users / عدد المستخدمين: {data['max_users']}\n")
                f.write(f"Features / الميزات: {', '.join(data['features'])}\n")
                f.write(f"Status / الحالة: {data['status']}\n")
                f.write(f"Activation Count / عدد التفعيلات: {data['activation_count']}\n\n")

                f.write("=" * 80 + "\n")
                f.write("IMPORTANT NOTES / ملاحظات مهمة:\n")
                f.write("=" * 80 + "\n")
                f.write("- Keep this license key safe / احتفظ بمفتاح الترخيص في مكان آمن\n")
                f.write("- Do not share with unauthorized users / لا تشاركه مع مستخدمين غير مصرح لهم\n")
                f.write("- Contact support for renewal / اتصل بالدعم للتجديد\n")
                f.write("- This license is bound to the machine ID / هذا الترخيص مرتبط بمعرف الجهاز\n")
                f.write("=" * 80 + "\n")

            messagebox.showinfo(
                "نجح - Success",
                f"تم حفظ الترخيص في:\nLicense saved to:\n\n{filepath}"
            )
        except Exception as e:
            messagebox.showerror("خطأ - Error", f"فشل حفظ الملف:\n{str(e)}")

    def clear_form(self):
        self.company_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.duration_entry.insert(0, "365")
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.max_users_entry.delete(0, tk.END)
        self.max_users_entry.insert(0, "10")
        self.notes_entry.delete(0, tk.END)

    def refresh_list(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Reload licenses
        self.licenses = self.load_licenses()

        # Add to tree with enhanced status
        for key, data in self.licenses.items():
            company = data.get('company', 'N/A')
            expiry = data.get('expiry', 'N/A')

            # Format key for display (show first and last parts)
            display_key = f"{key[:19]}...{key[-13:]}" if len(key) > 35 else key

            # Check if expired with days remaining
            try:
                expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
                days_left = (expiry_date - datetime.now()).days

                if days_left < 0:
                    status = f"❌ منتهي ({abs(days_left)} يوم)"
                elif days_left <= 7:
                    status = f"🔴 {days_left} يوم"
                elif days_left <= 30:
                    status = f"⚠️ {days_left} يوم"
                else:
                    status = f"✅ نشط ({days_left} يوم)"
            except:
                status = "❓ غير معروف"

            self.tree.insert('', 'end', values=(company, display_key, expiry, status))

    def update_license_stats(self):
        """Update license statistics in the app tab"""
        # Reload licenses
        self.licenses = self.load_licenses()

        # Count statistics
        total = len(self.licenses)
        active = 0
        suspended = 0
        expired = 0
        recent_list = []

        for key, data in self.licenses.items():
            company = data.get('company', 'N/A')
            expiry = data.get('expiry', 'N/A')
            status = data.get('status', 'active')

            # Check expiry
            try:
                expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
                days_left = (expiry_date - datetime.now()).days

                if days_left < 0:
                    expired += 1
                    status_icon = "❌"
                    status_text = "منتهي"
                elif status == 'suspended':
                    suspended += 1
                    status_icon = "⏸️"
                    status_text = "معلق"
                else:
                    active += 1
                    if days_left <= 7:
                        status_icon = "🔴"
                    elif days_left <= 30:
                        status_icon = "⚠️"
                    else:
                        status_icon = "✅"
                    status_text = f"نشط ({days_left} يوم)"
            except:
                status_icon = "❓"
                status_text = "غير معروف"

            # Add to recent list (show last 5)
            recent_list.append(f"{status_icon} {company} - {status_text}")

        # Update stat labels
        self.total_licenses_label.config(text=str(total))
        self.active_licenses_label.config(text=str(active))
        self.suspended_licenses_label.config(text=str(suspended))
        self.expired_licenses_label.config(text=str(expired))

        # Update recent licenses listbox
        self.recent_licenses_listbox.delete(0, tk.END)

        if not recent_list:
            self.recent_licenses_listbox.insert(tk.END, "📭 لا توجد تراخيص - No licenses yet")
        else:
            # Show last 5 licenses
            for item in recent_list[-5:]:
                self.recent_licenses_listbox.insert(0, item)

        # Also refresh the tree if we're on license tab
        if hasattr(self, 'tree'):
            # Store current selection
            current_selection = self.tree.selection()
            self.refresh_list()
            # Restore selection if possible
            if current_selection:
                try:
                    self.tree.selection_set(current_selection)
                except:
                    pass

    def copy_key(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير - Warning", "الرجاء اختيار ترخيص!\nPlease select a license!")
            return

        item = self.tree.item(selected[0])
        company = item['values'][0]

        # Find full key from licenses
        full_key = None
        for key, data in self.licenses.items():
            if data.get('company') == company:
                full_key = key
                break

        if full_key:
            self.root.clipboard_clear()
            self.root.clipboard_append(full_key)

            # Show key in message
            messagebox.showinfo(
                "نجح - Success",
                f"تم نسخ المفتاح الكامل!\nFull key copied to clipboard!\n\n{full_key}"
            )
        else:
            messagebox.showerror("خطأ - Error", "لم يتم العثور على المفتاح!\nKey not found!")

    def delete_license(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير - Warning", "الرجاء اختيار ترخيص!\nPlease select a license!")
            return

        item = self.tree.item(selected[0])
        company = item['values'][0]

        # Find full key
        full_key = None
        license_data = None
        for key, data in self.licenses.items():
            if data.get('company') == company:
                full_key = key
                license_data = data
                break

        if not full_key:
            messagebox.showerror("خطأ - Error", "لم يتم العثور على الترخيص!\nLicense not found!")
            return

        # Show detailed confirmation
        confirm_msg = (
            f"هل أنت متأكد من حذف هذا الترخيص؟\n"
            f"Are you sure you want to delete this license?\n\n"
            f"الشركة - Company: {company}\n"
            f"تاريخ الإنشاء - Created: {license_data.get('created', 'N/A')}\n"
            f"تاريخ الانتهاء - Expiry: {license_data.get('expiry', 'N/A')}\n\n"
            f"هذا الإجراء لا يمكن التراجع عنه!\n"
            f"This action cannot be undone!"
        )

        if messagebox.askyesno("تأكيد الحذف - Confirm Deletion", confirm_msg):
            del self.licenses[full_key]
            self.save_licenses()
            self.refresh_list()
            self.update_license_stats()  # Update statistics
            messagebox.showinfo("نجح - Success", "تم حذف الترخيص بنجاح!\nLicense deleted successfully!")

    def activate_license(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير - Warning", "الرجاء اختيار ترخيص!\nPlease select a license!")
            return

        item = self.tree.item(selected[0])
        company = item['values'][0]

        # Find license
        full_key = None
        license_data = None
        for key, data in self.licenses.items():
            if data.get('company') == company:
                full_key = key
                license_data = data
                break

        if full_key:
            self.licenses[full_key]['status'] = 'active'
            self.save_licenses()

            # Sync to database
            self.sync_license_to_database(full_key, self.licenses[full_key])

            self.refresh_list()
            self.update_license_stats()  # Update statistics
            messagebox.showinfo("نجح - Success", f"تم تفعيل ترخيص {company}!\nLicense activated for {company}!")

    def suspend_license(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير - Warning", "الرجاء اختيار ترخيص!\nPlease select a license!")
            return

        item = self.tree.item(selected[0])
        company = item['values'][0]

        # Find license
        full_key = None
        license_data = None
        for key, data in self.licenses.items():
            if data.get('company') == company:
                full_key = key
                license_data = data
                break

        if full_key:
            self.licenses[full_key]['status'] = 'suspended'
            self.save_licenses()

            # Sync to database
            self.sync_license_to_database(full_key, self.licenses[full_key])

            self.refresh_list()
            self.update_license_stats()  # Update statistics
            messagebox.showinfo("نجح - Success", f"تم إيقاف ترخيص {company} مؤقتاً!\nLicense suspended for {company}!")

    def edit_license(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير - Warning", "الرجاء اختيار ترخيص!\nPlease select a license!")
            return

        item = self.tree.item(selected[0])
        company = item['values'][0]

        # Find license
        full_key = None
        license_data = None
        for key, data in self.licenses.items():
            if data.get('company') == company:
                full_key = key
                license_data = data
                break

        if not full_key:
            messagebox.showerror("خطأ - Error", "لم يتم العثور على الترخيص!\nLicense not found!")
            return

        # Create edit window
        self.show_edit_window(full_key, license_data)

    def view_license_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير - Warning", "الرجاء اختيار ترخيص!\nPlease select a license!")
            return

        item = self.tree.item(selected[0])
        company = item['values'][0]

        # Find license
        full_key = None
        license_data = None
        for key, data in self.licenses.items():
            if data.get('company') == company:
                full_key = key
                license_data = data
                break

        if full_key:
            self.show_license_details(full_key, license_data)

    def show_edit_window(self, key, data):
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("تعديل الترخيص - Edit License")
        edit_window.geometry("600x550")
        edit_window.configure(bg=self.colors['bg'])
        edit_window.resizable(False, False)

        # Center window
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (edit_window.winfo_screenheight() // 2) - (550 // 2)
        edit_window.geometry(f'600x550+{x}+{y}')

        # Header
        header = tk.Frame(edit_window, bg=self.colors['info'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="✏️ تعديل معلومات الترخيص - Edit License Information",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['info'],
            fg='white'
        ).pack(expand=True)

        # Form
        form_frame = tk.Frame(edit_window, bg=self.colors['bg'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Company (read-only)
        tk.Label(
            form_frame,
            text="اسم الشركة - Company:",
            font=("Segoe UI", 11),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).grid(row=0, column=0, sticky='e', padx=10, pady=8)

        company_label = tk.Label(
            form_frame,
            text=data.get('company', ''),
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        company_label.grid(row=0, column=1, sticky='w', padx=10, pady=8)

        # Username
        tk.Label(
            form_frame,
            text="اسم المستخدم - Username:",
            font=("Segoe UI", 11),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).grid(row=1, column=0, sticky='e', padx=10, pady=8)

        username_var = tk.StringVar(value=data.get('username', ''))
        username_edit = tk.Entry(form_frame, textvariable=username_var, font=("Segoe UI", 11), width=30)
        username_edit.grid(row=1, column=1, sticky='w', padx=10, pady=8)

        # Password
        tk.Label(
            form_frame,
            text="كلمة المرور - Password:",
            font=("Segoe UI", 11),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).grid(row=2, column=0, sticky='e', padx=10, pady=8)

        password_var = tk.StringVar(value=data.get('password', ''))
        password_edit = tk.Entry(form_frame, textvariable=password_var, font=("Segoe UI", 11), width=30, show="*")
        password_edit.grid(row=2, column=1, sticky='w', padx=10, pady=8)

        # Email
        tk.Label(
            form_frame,
            text="البريد الإلكتروني - Email:",
            font=("Segoe UI", 11),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).grid(row=3, column=0, sticky='e', padx=10, pady=8)

        email_var = tk.StringVar(value=data.get('contact_email', ''))
        email_edit = tk.Entry(form_frame, textvariable=email_var, font=("Segoe UI", 11), width=30)
        email_edit.grid(row=3, column=1, sticky='w', padx=10, pady=8)

        # Phone
        tk.Label(
            form_frame,
            text="رقم الهاتف - Phone:",
            font=("Segoe UI", 11),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).grid(row=4, column=0, sticky='e', padx=10, pady=8)

        phone_var = tk.StringVar(value=data.get('contact_phone', ''))
        phone_edit = tk.Entry(form_frame, textvariable=phone_var, font=("Segoe UI", 11), width=30)
        phone_edit.grid(row=4, column=1, sticky='w', padx=10, pady=8)

        # Max Users
        tk.Label(
            form_frame,
            text="عدد المستخدمين - Max Users:",
            font=("Segoe UI", 11),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).grid(row=5, column=0, sticky='e', padx=10, pady=8)

        max_users_var = tk.StringVar(value=str(data.get('max_users', 10)))
        max_users_edit = tk.Entry(form_frame, textvariable=max_users_var, font=("Segoe UI", 11), width=30)
        max_users_edit.grid(row=5, column=1, sticky='w', padx=10, pady=8)

        # Notes
        tk.Label(
            form_frame,
            text="ملاحظات - Notes:",
            font=("Segoe UI", 11),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).grid(row=6, column=0, sticky='e', padx=10, pady=8)

        notes_var = tk.StringVar(value=data.get('notes', ''))
        notes_edit = tk.Entry(form_frame, textvariable=notes_var, font=("Segoe UI", 11), width=30)
        notes_edit.grid(row=6, column=1, sticky='w', padx=10, pady=8)

        # Save function
        def save_changes():
            try:
                max_users_int = int(max_users_var.get())
                if max_users_int <= 0:
                    raise ValueError()
            except:
                messagebox.showerror("خطأ - Error", "عدد المستخدمين يجب أن يكون رقماً موجباً!", parent=edit_window)
                return

            # Update license
            self.licenses[key]['username'] = username_var.get().strip()
            self.licenses[key]['password'] = password_var.get().strip()
            self.licenses[key]['contact_email'] = email_var.get().strip()
            self.licenses[key]['contact_phone'] = phone_var.get().strip()
            self.licenses[key]['max_users'] = max_users_int
            self.licenses[key]['notes'] = notes_var.get().strip()

            self.save_licenses()
            self.refresh_list()

            messagebox.showinfo("نجح - Success", "تم تحديث الترخيص بنجاح!\nLicense updated successfully!", parent=edit_window)
            edit_window.destroy()

        # Buttons
        btn_frame = tk.Frame(edit_window, bg=self.colors['bg'])
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="💾 حفظ التغييرات - Save Changes",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=save_changes,
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="❌ إلغاء - Cancel",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['danger'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=edit_window.destroy,
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

    def sync_license_to_database(self, license_key, license_data):
        """Sync license to database by creating/updating user account"""
        try:
            db_path = self.app_dir / "erp_system.db"

            if not db_path.exists():
                print(f"Database not found at {db_path}")
                return

            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            # Calculate expiry datetime
            expiry_date = datetime.strptime(license_data.get('expiry'), "%Y-%m-%d")

            # Insert or update license
            cursor.execute("""
                INSERT OR REPLACE INTO licenses
                (license_key, company_name, machine_id, expiry_date, duration_days,
                 license_type, max_users, features, status, activation_count,
                 contact_email, contact_phone, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                license_key,
                license_data.get('company'),
                license_data.get('machine_id'),
                expiry_date,
                license_data.get('duration_days', 365),
                license_data.get('license_type', 'Standard'),
                license_data.get('max_users', 10),
                'all',  # features as JSON string
                license_data.get('status', 'active'),
                license_data.get('activation_count', 0),
                license_data.get('contact_email'),
                license_data.get('contact_phone'),
                license_data.get('notes'),
                datetime.now()
            ))

            # Get license ID
            license_id = cursor.lastrowid
            if license_id == 0:
                # License already exists, get its ID
                cursor.execute("SELECT id FROM licenses WHERE license_key = ?", (license_key,))
                result = cursor.fetchone()
                if result:
                    license_id = result[0]

            # Check if user exists
            username = license_data.get('username')
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_exists = cursor.fetchone()

            if not user_exists:
                # Create new user
                password_hash = generate_password_hash(license_data.get('password'))

                cursor.execute("""
                    INSERT INTO users
                    (username, email, password_hash, full_name, phone, is_active,
                     is_admin, language, license_id, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    username,
                    license_data.get('contact_email', f"{username}@example.com"),
                    password_hash,
                    license_data.get('company'),
                    license_data.get('contact_phone'),
                    1 if license_data.get('status') == 'active' else 0,
                    0,  # is_admin
                    'ar',  # language
                    license_id,
                    datetime.now()
                ))
                print(f"✅ Created user: {username} with license: {license_key[:20]}...")
            else:
                # Update existing user
                cursor.execute("""
                    UPDATE users
                    SET license_id = ?,
                        is_active = ?,
                        email = ?,
                        phone = ?
                    WHERE username = ?
                """, (
                    license_id,
                    1 if license_data.get('status') == 'active' else 0,
                    license_data.get('contact_email', f"{username}@example.com"),
                    license_data.get('contact_phone'),
                    username
                ))
                print(f"✅ Updated user: {username} with license: {license_key[:20]}...")

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"❌ Error syncing license to database: {e}")
            import traceback
            traceback.print_exc()

    def apply_migration(self):
        """Apply database migration for license system"""
        try:
            # Check if database exists first
            db_path = self.app_dir / "erp_system.db"

            if not db_path.exists():
                messagebox.showerror(
                    "خطأ - Error",
                    "❌ قاعدة البيانات غير موجودة!\n"
                    "Database not found!\n\n"
                    "⚠️ يجب تشغيل التطبيق أولاً لإنشاء قاعدة البيانات:\n"
                    "You must start the application first to create the database:\n\n"
                    "1️⃣ اذهب إلى تبويب 'تشغيل التطبيق'\n"
                    "   Go to 'App Control' tab\n\n"
                    "2️⃣ اضغط على 'تشغيل التطبيق'\n"
                    "   Click 'Start Application'\n\n"
                    "3️⃣ انتظر حتى يتم تشغيل التطبيق\n"
                    "   Wait for the application to start\n\n"
                    "4️⃣ ثم ارجع وحاول مرة أخرى\n"
                    "   Then come back and try again"
                )
                return

            # Check if application is running
            if not self.is_running:
                response = messagebox.askyesno(
                    "تحذير - Warning",
                    "⚠️ التطبيق غير قيد التشغيل!\n"
                    "Application is not running!\n\n"
                    "يُفضل تشغيل التطبيق أولاً لضمان نجاح Migration.\n"
                    "It's recommended to start the application first.\n\n"
                    "هل تريد المتابعة على أي حال؟\n"
                    "Do you want to continue anyway?"
                )
                if not response:
                    return

            result = subprocess.run(
                [sys.executable, "apply_license_migration.py"],
                cwd=self.app_dir,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0 or "Migration completed successfully" in result.stdout:
                # Extract key information from output
                success_msg = "✅ تم تطبيق Migration بنجاح!\n✅ Migration applied successfully!\n\n"

                if "Licenses table already exists" in result.stdout:
                    success_msg += "✓ جدول التراخيص موجود بالفعل\n  Licenses table already exists\n\n"
                elif "Licenses table created" in result.stdout:
                    success_msg += "✓ تم إنشاء جدول التراخيص\n  Licenses table created\n\n"

                if "license_id column added" in result.stdout:
                    success_msg += "✓ تم إضافة عمود license_id لجدول المستخدمين\n  license_id column added to users table\n\n"
                elif "already has license_id column" in result.stdout:
                    success_msg += "✓ جدول المستخدمين يحتوي بالفعل على عمود license_id\n  Users table already has license_id column\n\n"

                success_msg += "🎉 يمكنك الآن استخدام نظام التراخيص!\n🎉 You can now use the license system!"

                messagebox.showinfo("نجح - Success", success_msg)
            else:
                messagebox.showerror(
                    "خطأ - Error",
                    f"❌ فشل تطبيق Migration!\nMigration failed!\n\n{result.stdout}\n{result.stderr}"
                )
        except subprocess.TimeoutExpired:
            messagebox.showerror("خطأ - Error", "⏱️ انتهت مهلة التطبيق!\nApplication timeout!")
        except Exception as e:
            messagebox.showerror("خطأ - Error", f"❌ خطأ في تطبيق Migration:\n{str(e)}")

    def on_closing(self):
        if self.is_running:
            if messagebox.askyesno("تأكيد - Confirm", "التطبيق يعمل. هل تريد إيقافه والخروج?\nApp is running. Stop and exit?"):
                self.stop_app()
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DEDControlPanel(root)
    root.mainloop()


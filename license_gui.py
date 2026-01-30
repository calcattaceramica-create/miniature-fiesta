#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modern License Manager GUI - واجهة عصرية لإدارة التراخيص
Ultra Modern Design with Gradients and Animations
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.license_manager import LicenseManager
from app.models_license import License


class ModernLicenseManagerGUI:
    """Ultra Modern License Manager with Beautiful UI"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔐 License Manager - نظام إدارة التراخيص")
        self.root.geometry("1400x850")
        self.root.resizable(True, True)

        # Modern gradient colors - Updated for better aesthetics
        self.colors = {
            'bg_gradient_start': '#f5f7fa',
            'bg_gradient_end': '#c3cfe2',
            'card_bg': '#FFFFFF',
            'primary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#16a085',
            'text_dark': '#2c3e50',
            'text_light': '#7f8c8d',
            'border': '#e0e0e0',
            'hover': '#ecf0f1'
        }

        # Configure root background with modern color
        self.root.configure(bg='#ecf0f1')
        
        # Initialize Flask app
        self.app = create_app()
        
        # Setup modern UI
        self.setup_modern_ui()
        
        # Center window
        self.center_window()

    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_modern_ui(self):
        """Setup ultra modern user interface"""
        # Main container with modern background
        main_container = tk.Frame(self.root, bg='#ecf0f1')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header card
        self.create_modern_header(main_container)

        # Content area
        content_frame = tk.Frame(main_container, bg='#ecf0f1')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=15)

        # Left sidebar - Modern menu
        self.create_modern_sidebar(content_frame)

        # Right content - Modern cards
        self.create_modern_content(content_frame)

    def create_modern_header(self, parent):
        """Create modern header with gradient effect"""
        # Header container with shadow
        header_container = tk.Frame(parent, bg='#bdc3c7')
        header_container.pack(fill=tk.X, pady=(0, 15))

        header_card = tk.Frame(header_container, bg='white', relief=tk.FLAT)
        header_card.pack(fill=tk.X, padx=2, pady=2)

        # Gradient top border
        gradient_border = tk.Frame(header_card, bg='#3498db', height=6)
        gradient_border.pack(fill=tk.X)

        # Header content
        header_content = tk.Frame(header_card, bg='white')
        header_content.pack(fill=tk.BOTH, padx=30, pady=25)
        
        # Icon and title
        title_frame = tk.Frame(header_content, bg='white')
        title_frame.pack(side=tk.LEFT)

        # Modern icon with background
        icon_container = tk.Frame(title_frame, bg='#3498db', width=70, height=70)
        icon_container.pack(side=tk.LEFT, padx=(0, 20))
        icon_container.pack_propagate(False)

        icon_label = tk.Label(
            icon_container,
            text="🔐",
            font=('Segoe UI Emoji', 36),
            bg='#3498db',
            fg='white'
        )
        icon_label.pack(expand=True)

        # Title and subtitle
        text_frame = tk.Frame(title_frame, bg='white')
        text_frame.pack(side=tk.LEFT)

        title = tk.Label(
            text_frame,
            text="License Manager",
            font=('Segoe UI', 26, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(anchor=tk.W)

        subtitle = tk.Label(
            text_frame,
            text="نظام إدارة التراخيص العصري | Modern License Management System",
            font=('Segoe UI', 11),
            bg='white',
            fg='#7f8c8d'
        )
        subtitle.pack(anchor=tk.W)
        
        # Stats in header
        stats_frame = tk.Frame(header_content, bg='white')
        stats_frame.pack(side=tk.RIGHT)

        self.update_header_stats(stats_frame)

    def update_header_stats(self, parent):
        """Update header statistics"""
        with self.app.app_context():
            total = License.query.count()
            active = License.query.filter_by(is_active=True, is_suspended=False).count()

        # Total licenses stat
        self.create_stat_badge(parent, "📊", str(total), "Total", '#3498db')
        self.create_stat_badge(parent, "✅", str(active), "Active", '#27ae60')

    def create_stat_badge(self, parent, icon, value, label, color):
        """Create a modern stat badge with background"""
        # Badge container
        badge_container = tk.Frame(parent, bg='#ecf0f1')
        badge_container.pack(side=tk.LEFT, padx=8)

        badge = tk.Frame(badge_container, bg='white', relief=tk.FLAT)
        badge.pack(padx=2, pady=2)

        # Colored left border
        left_border = tk.Frame(badge, bg=color, width=4)
        left_border.pack(side=tk.LEFT, fill=tk.Y)

        # Content
        content = tk.Frame(badge, bg='white')
        content.pack(side=tk.LEFT, padx=15, pady=12)

        # Icon and value in same row
        top_row = tk.Frame(content, bg='white')
        top_row.pack()

        icon_label = tk.Label(
            top_row,
            text=icon,
            font=('Segoe UI Emoji', 20),
            bg='white'
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 8))

        value_label = tk.Label(
            top_row,
            text=value,
            font=('Segoe UI', 22, 'bold'),
            bg='white',
            fg=color
        )
        value_label.pack(side=tk.LEFT)

        # Label
        label_label = tk.Label(
            content,
            text=label,
            font=('Segoe UI', 9),
            bg='white',
            fg='#7f8c8d'
        )
        label_label.pack()

    def create_modern_sidebar(self, parent):
        """Create modern sidebar with menu buttons"""
        sidebar = tk.Frame(parent, bg='#2c3e50', width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        sidebar.pack_propagate(False)

        # Sidebar header with gradient effect
        sidebar_header_frame = tk.Frame(sidebar, bg='#34495e', height=80)
        sidebar_header_frame.pack(fill=tk.X)
        sidebar_header_frame.pack_propagate(False)

        sidebar_header = tk.Label(
            sidebar_header_frame,
            text="📋 Menu",
            font=('Segoe UI', 18, 'bold'),
            bg='#34495e',
            fg='white'
        )
        sidebar_header.pack(expand=True)

        # Separator
        separator = tk.Frame(sidebar, bg='#1abc9c', height=3)
        separator.pack(fill=tk.X)

        # Menu buttons with modern styling
        self.create_menu_button(sidebar, "➕", "Create License", self.show_create_license, '#27ae60')
        self.create_menu_button(sidebar, "📋", "All Licenses", self.show_all_licenses, '#3498db')
        self.create_menu_button(sidebar, "🔍", "Search License", self.show_search_license, '#f39c12')
        self.create_menu_button(sidebar, "👁️", "License Details", self.show_license_details, '#9b59b6')
        self.create_menu_button(sidebar, "📊", "Extend License", self.extend_license, '#16a085')
        self.create_menu_button(sidebar, "⏸️", "Suspend License", self.suspend_license, '#e74c3c')
        self.create_menu_button(sidebar, "▶️", "Activate License", self.activate_license, '#2ecc71')
        self.create_menu_button(sidebar, "🗑️", "Delete License", self.delete_license, '#c0392b')

        # Exit button at bottom
        exit_frame = tk.Frame(sidebar, bg='#2c3e50')
        exit_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        exit_btn = tk.Button(
            exit_frame,
            text="❌ Exit",
            font=('Segoe UI', 12, 'bold'),
            bg='#95a5a6',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.root.quit,
            padx=20,
            pady=12
        )
        exit_btn.pack(fill=tk.X, padx=15)
        exit_btn.bind('<Enter>', lambda e: exit_btn.config(bg='#7f8c8d'))
        exit_btn.bind('<Leave>', lambda e: exit_btn.config(bg='#95a5a6'))

    def create_menu_button(self, parent, icon, text, command, color):
        """Create a modern menu button with hover effects"""
        btn_frame = tk.Frame(parent, bg='#2c3e50')
        btn_frame.pack(fill=tk.X, padx=15, pady=8)

        btn = tk.Button(
            btn_frame,
            text=f"{icon}  {text}",
            font=('Segoe UI', 11, 'bold'),
            bg=color,
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=command,
            anchor=tk.W,
            padx=20,
            pady=15,
            borderwidth=0,
            highlightthickness=0
        )
        btn.pack(fill=tk.X)

        # Advanced hover effects
        def on_enter(e):
            btn.config(bg=self.lighten_color(color), padx=25)

        def on_leave(e):
            btn.config(bg=color, padx=20)

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

    def lighten_color(self, color):
        """Lighten a hex color"""
        # Simple lightening by adding to RGB values
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'

    def create_modern_content(self, parent):
        """Create modern content area"""
        self.content_area = tk.Frame(parent, bg=self.colors['card_bg'])
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Welcome screen by default
        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Show modern welcome screen with animations"""
        self.clear_content()

        welcome_frame = tk.Frame(self.content_area, bg=self.colors['card_bg'])
        welcome_frame.pack(expand=True)

        # Large animated icon
        icon = tk.Label(
            welcome_frame,
            text="🔐",
            font=('Segoe UI Emoji', 100),
            bg=self.colors['card_bg']
        )
        icon.pack(pady=30)

        # Welcome text with gradient effect
        welcome_text = tk.Label(
            welcome_frame,
            text="Welcome to License Manager",
            font=('Segoe UI', 28, 'bold'),
            bg=self.colors['card_bg'],
            fg='#2c3e50'
        )
        welcome_text.pack()

        subtitle = tk.Label(
            welcome_frame,
            text="مرحباً بك في نظام إدارة التراخيص العصري",
            font=('Segoe UI', 16),
            bg=self.colors['card_bg'],
            fg='#7f8c8d'
        )
        subtitle.pack(pady=15)

        # Instruction text
        instruction = tk.Label(
            welcome_frame,
            text="Select an option from the menu to get started",
            font=('Segoe UI', 12, 'italic'),
            bg=self.colors['card_bg'],
            fg='#95a5a6'
        )
        instruction.pack(pady=10)

        # Quick stats with modern cards
        stats_container = tk.Frame(welcome_frame, bg=self.colors['card_bg'])
        stats_container.pack(pady=40)

        with self.app.app_context():
            total = License.query.count()
            active = License.query.filter_by(is_active=True, is_suspended=False).count()
            suspended = License.query.filter_by(is_suspended=True).count()

            # Calculate expiring soon
            expiring_soon = 0
            for lic in License.query.all():
                if lic.expires_at:
                    days_left = (lic.expires_at - datetime.utcnow()).days
                    if 0 < days_left <= 7:
                        expiring_soon += 1

        self.create_welcome_stat(stats_container, "📊", total, "Total Licenses", '#3498db')
        self.create_welcome_stat(stats_container, "✅", active, "Active", '#27ae60')
        self.create_welcome_stat(stats_container, "⏸️", suspended, "Suspended", '#e74c3c')
        self.create_welcome_stat(stats_container, "⚠️", expiring_soon, "Expiring Soon", '#f39c12')

    def create_welcome_stat(self, parent, icon, value, label, color):
        """Create modern welcome screen stat card with color"""
        # Card container with shadow
        card_container = tk.Frame(parent, bg='#ecf0f1')
        card_container.pack(side=tk.LEFT, padx=15)

        card = tk.Frame(card_container, bg='white', relief=tk.RAISED, bd=0)
        card.pack(padx=2, pady=2)

        # Colored top border
        top_border = tk.Frame(card, bg=color, height=5)
        top_border.pack(fill=tk.X)

        content = tk.Frame(card, bg='white')
        content.pack(padx=35, pady=25)

        # Icon
        icon_label = tk.Label(content, text=icon, font=('Segoe UI Emoji', 36), bg='white')
        icon_label.pack()

        # Value with color
        value_label = tk.Label(content, text=str(value), font=('Segoe UI', 32, 'bold'),
                              bg='white', fg=color)
        value_label.pack(pady=5)

        # Label
        label_label = tk.Label(content, text=label, font=('Segoe UI', 11),
                              bg='white', fg='#7f8c8d')
        label_label.pack()

    def clear_content(self):
        """Clear content area"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_create_license(self):
        """Show create license form"""
        self.clear_content()

        # Header
        header = tk.Label(
            self.content_area,
            text="➕ Create New License",
            font=('Segoe UI', 20, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark']
        )
        header.pack(pady=20, padx=30, anchor=tk.W)

        # Form container
        form_frame = tk.Frame(self.content_area, bg=self.colors['card_bg'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        # Create form fields
        fields = [
            ("👤 Client Name:", "client_name"),
            ("📧 Email:", "client_email"),
            ("📞 Phone:", "client_phone"),
            ("🏢 Company:", "client_company"),
            ("👨‍💼 Admin Username:", "admin_username"),
            ("🔒 Admin Password:", "admin_password"),
        ]

        self.form_entries = {}

        for label_text, field_name in fields:
            field_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
            field_frame.pack(fill=tk.X, pady=8)

            label = tk.Label(
                field_frame,
                text=label_text,
                font=('Segoe UI', 11),
                bg=self.colors['card_bg'],
                fg=self.colors['text_dark'],
                width=20,
                anchor=tk.W
            )
            label.pack(side=tk.LEFT)

            if field_name == "admin_password":
                entry = tk.Entry(field_frame, font=('Segoe UI', 11), show='*', width=40)
            else:
                entry = tk.Entry(field_frame, font=('Segoe UI', 11), width=40)
            entry.pack(side=tk.LEFT, padx=10)
            self.form_entries[field_name] = entry

        # License type
        type_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
        type_frame.pack(fill=tk.X, pady=8)

        type_label = tk.Label(
            type_frame,
            text="📊 License Type:",
            font=('Segoe UI', 11),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark'],
            width=20,
            anchor=tk.W
        )
        type_label.pack(side=tk.LEFT)

        self.license_type_var = tk.StringVar(value="monthly")
        type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.license_type_var,
            values=["trial", "monthly", "yearly", "lifetime"],
            state="readonly",
            font=('Segoe UI', 11),
            width=37
        )
        type_combo.pack(side=tk.LEFT, padx=10)

        # Max users
        users_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
        users_frame.pack(fill=tk.X, pady=8)

        users_label = tk.Label(
            users_frame,
            text="👥 Max Users:",
            font=('Segoe UI', 11),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark'],
            width=20,
            anchor=tk.W
        )
        users_label.pack(side=tk.LEFT)

        self.max_users_var = tk.StringVar(value="10")
        users_entry = tk.Entry(users_frame, textvariable=self.max_users_var, font=('Segoe UI', 11), width=40)
        users_entry.pack(side=tk.LEFT, padx=10)

        # Buttons
        btn_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
        btn_frame.pack(pady=30)

        create_btn = tk.Button(
            btn_frame,
            text="✅ Create License",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.create_license_action,
            padx=30,
            pady=12
        )
        create_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=('Segoe UI', 12),
            bg=self.colors['text_light'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.show_welcome_screen,
            padx=30,
            pady=12
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def create_license_action(self):
        """Create a new license with separate tenant database"""
        try:
            # Get form data
            client_name = self.form_entries['client_name'].get()
            client_email = self.form_entries['client_email'].get()
            client_phone = self.form_entries['client_phone'].get()
            client_company = self.form_entries['client_company'].get()
            admin_username = self.form_entries['admin_username'].get()
            admin_password = self.form_entries['admin_password'].get()
            license_type = self.license_type_var.get()
            max_users = int(self.max_users_var.get())

            # Validate
            if not all([client_name, client_email, admin_username, admin_password]):
                messagebox.showerror("Error", "Please fill all required fields!")
                return

            # Calculate duration
            duration_map = {
                'trial': 30,
                'monthly': 30,
                'yearly': 365,
                'lifetime': None
            }
            duration = duration_map.get(license_type)

            # Create license in master database
            with self.app.app_context():
                print("=" * 60)
                print("🔧 Creating new license...")

                # Step 1: Create license record
                license = LicenseManager.create_license(
                    client_name=client_name,
                    client_email=client_email,
                    client_phone=client_phone,
                    client_company=client_company,
                    license_type=license_type,
                    max_users=max_users,
                    max_branches=5,
                    duration_days=duration,
                    admin_username=admin_username,
                    admin_password=admin_password
                )

                print(f"✅ License record created: {license.license_key}")

                # Step 2: Create tenant database
                from app.tenant_manager import TenantManager

                print(f"🗄️  Creating tenant database for {license.license_key}...")
                db_created = TenantManager.create_tenant_database(license.license_key, self.app)

                if not db_created:
                    # Rollback license creation if database creation fails
                    db.session.delete(license)
                    db.session.commit()
                    messagebox.showerror(
                        "❌ Error",
                        "Failed to create tenant database!\n\n"
                        "License creation cancelled."
                    )
                    return

                print(f"✅ Tenant database created successfully")

                # Step 3: Initialize tenant data
                print(f"📦 Initializing tenant data...")
                data_initialized = TenantManager.initialize_tenant_data(
                    license.license_key,
                    self.app,
                    license
                )

                if not data_initialized:
                    messagebox.showwarning(
                        "⚠️ Warning",
                        "License created but failed to initialize default data.\n\n"
                        f"🔑 License Key: {license.license_key}\n\n"
                        "You may need to initialize data manually."
                    )
                else:
                    print(f"✅ Tenant data initialized successfully")

                print("=" * 60)

                # Show success message
                messagebox.showinfo(
                    "✅ Success",
                    f"License created successfully!\n\n"
                    f"🔑 License Key: {license.license_key}\n"
                    f"👤 Client: {license.client_name}\n"
                    f"🏢 Company: {license.client_company or 'N/A'}\n"
                    f"📊 Type: {license.license_type.upper()}\n"
                    f"👥 Max Users: {license.max_users}\n"
                    f"🏪 Max Branches: {license.max_branches}\n\n"
                    f"🗄️  Tenant Database: Created\n"
                    f"📦 Default Data: {'Initialized' if data_initialized else 'Failed'}\n\n"
                    f"🔐 Admin Username: {admin_username}\n"
                    f"🔑 Admin Password: {admin_password}"
                )

                self.show_welcome_screen()

        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("❌ Error", f"Failed to create license:\n\n{str(e)}")

    def show_all_licenses(self):
        """Show all licenses in a modern card layout"""
        self.clear_content()

        # Header
        header = tk.Label(
            self.content_area,
            text="📋 All Licenses",
            font=('Segoe UI', 20, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark']
        )
        header.pack(pady=20, padx=30, anchor=tk.W)

        # Scrollable frame
        canvas = tk.Canvas(self.content_area, bg=self.colors['card_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['card_bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Get all licenses
        with self.app.app_context():
            licenses = License.query.all()

        if not licenses:
            no_data = tk.Label(
                scrollable_frame,
                text="📭 No licenses found",
                font=('Segoe UI', 14),
                bg=self.colors['card_bg'],
                fg=self.colors['text_light']
            )
            no_data.pack(pady=50)
        else:
            # Display licenses as cards
            for license in licenses:
                self.create_license_card(scrollable_frame, license)

        canvas.pack(side="left", fill="both", expand=True, padx=30)
        scrollbar.pack(side="right", fill="y")

    def create_license_card(self, parent, license):
        """Create a modern license card with gradient header"""
        # Determine card color based on status
        if license.is_suspended:
            border_color = '#e74c3c'
            status_text = "⏸️ Suspended"
            status_color = '#e74c3c'
            header_gradient = '#e74c3c'
        elif license.is_active:
            border_color = '#27ae60'
            status_text = "✅ Active"
            status_color = '#27ae60'
            header_gradient = '#27ae60'
        else:
            border_color = '#95a5a6'
            status_text = "⭕ Inactive"
            status_color = '#95a5a6'
            header_gradient = '#95a5a6'

        # Card container with shadow effect
        card_container = tk.Frame(parent, bg='#f8f9fa')
        card_container.pack(fill=tk.X, pady=12, padx=15)

        card = tk.Frame(card_container, bg='white', relief=tk.RAISED, bd=0)
        card.pack(fill=tk.X, padx=3, pady=3)

        # Gradient header
        header = tk.Frame(card, bg=header_gradient, height=8)
        header.pack(fill=tk.X)

        # Card content
        content = tk.Frame(card, bg='white')
        content.pack(fill=tk.BOTH, padx=25, pady=20)

        # Top row - License key and status
        top_row = tk.Frame(content, bg='white')
        top_row.pack(fill=tk.X, pady=(0, 15))

        # License key with modern styling
        key_container = tk.Frame(top_row, bg='#ecf0f1', relief=tk.FLAT)
        key_container.pack(side=tk.LEFT, fill=tk.X, expand=True)

        key_inner = tk.Frame(key_container, bg='#ecf0f1')
        key_inner.pack(padx=15, pady=10)

        key_label = tk.Label(
            key_inner,
            text=f"🔑 {license.license_key}",
            font=('Consolas', 13, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        key_label.pack(side=tk.LEFT)

        # Copy button with modern design
        copy_btn = tk.Button(
            key_inner,
            text="📋 Copy",
            font=('Segoe UI', 9, 'bold'),
            bg='#3498db',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=lambda: self.copy_to_clipboard(license.license_key),
            padx=12,
            pady=5
        )
        copy_btn.pack(side=tk.LEFT, padx=10)
        copy_btn.bind('<Enter>', lambda e: copy_btn.config(bg='#2980b9'))
        copy_btn.bind('<Leave>', lambda e: copy_btn.config(bg='#3498db'))

        # Status badge with rounded corners
        status_label = tk.Label(
            top_row,
            text=status_text,
            font=('Segoe UI', 10, 'bold'),
            bg=status_color,
            fg='white',
            padx=20,
            pady=8
        )
        status_label.pack(side=tk.RIGHT, padx=10)

        # Info grid
        info_frame = tk.Frame(content, bg='white')
        info_frame.pack(fill=tk.X, pady=10)

        # Left column
        left_col = tk.Frame(info_frame, bg='white')
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.add_info_row(left_col, "👤", "Client", license.client_name)
        self.add_info_row(left_col, "🏢", "Company", license.client_company or "N/A")
        self.add_info_row(left_col, "📧", "Email", license.client_email)
        self.add_info_row(left_col, "🔐", "Admin User", license.admin_username or "N/A")

        # Right column
        right_col = tk.Frame(info_frame, bg='white')
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.add_info_row(right_col, "📊", "Type", license.license_type.upper())
        self.add_info_row(right_col, "👥", "Max Users", str(license.max_users))

        if license.expires_at:
            days_left = (license.expires_at - datetime.utcnow()).days
            expire_text = f"{days_left} days left" if days_left > 0 else "Expired"
        else:
            expire_text = "Lifetime ∞"

        self.add_info_row(right_col, "⏰", "Expires", expire_text)

        # Action buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        view_btn = tk.Button(
            btn_frame,
            text="👁️ View",
            font=('Segoe UI', 10),
            bg=self.colors['info'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=lambda: self.view_license_details(license.license_key),
            padx=15,
            pady=5
        )
        view_btn.pack(side=tk.LEFT, padx=5)

        # Extend button
        extend_btn = tk.Button(
            btn_frame,
            text="📊 Extend",
            font=('Segoe UI', 10),
            bg='#16a085',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=lambda: self.extend_license_from_card(license.license_key),
            padx=15,
            pady=5
        )
        extend_btn.pack(side=tk.LEFT, padx=5)
        extend_btn.bind('<Enter>', lambda e: extend_btn.config(bg='#138d75'))
        extend_btn.bind('<Leave>', lambda e: extend_btn.config(bg='#16a085'))

        # Show Activate button if license is suspended OR inactive
        if license.is_suspended or not license.is_active:
            activate_btn = tk.Button(
                btn_frame,
                text="▶️ Activate",
                font=('Segoe UI', 10),
                bg=self.colors['success'],
                fg='white',
                relief=tk.FLAT,
                cursor='hand2',
                command=lambda: self.activate_license_action(license.license_key),
                padx=15,
                pady=5
            )
            activate_btn.pack(side=tk.LEFT, padx=5)
            activate_btn.bind('<Enter>', lambda e: activate_btn.config(bg='#229954'))
            activate_btn.bind('<Leave>', lambda e: activate_btn.config(bg=self.colors['success']))
        else:
            # Show Suspend button only if license is active and not suspended
            suspend_btn = tk.Button(
                btn_frame,
                text="⏸️ Suspend",
                font=('Segoe UI', 10),
                bg=self.colors['warning'],
                fg='white',
                relief=tk.FLAT,
                cursor='hand2',
                command=lambda: self.suspend_license_action(license.license_key),
                padx=15,
                pady=5
            )
            suspend_btn.pack(side=tk.LEFT, padx=5)
            suspend_btn.bind('<Enter>', lambda e: suspend_btn.config(bg='#d68910'))
            suspend_btn.bind('<Leave>', lambda e: suspend_btn.config(bg=self.colors['warning']))

        # Delete button
        delete_btn = tk.Button(
            btn_frame,
            text="🗑️ Delete",
            font=('Segoe UI', 10),
            bg=self.colors['danger'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=lambda: self.delete_license_action(license.license_key),
            padx=15,
            pady=5
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        delete_btn.bind('<Enter>', lambda e: delete_btn.config(bg='#c0392b'))
        delete_btn.bind('<Leave>', lambda e: delete_btn.config(bg=self.colors['danger']))

    def add_info_row(self, parent, icon, label, value):
        """Add an info row to license card"""
        row = tk.Frame(parent, bg='white')
        row.pack(fill=tk.X, pady=3)

        label_text = tk.Label(
            row,
            text=f"{icon} {label}:",
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['text_light'],
            width=12,
            anchor=tk.W
        )
        label_text.pack(side=tk.LEFT)

        value_text = tk.Label(
            row,
            text=str(value),
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=self.colors['text_dark'],
            anchor=tk.W
        )
        value_text.pack(side=tk.LEFT)



    def copy_to_clipboard(self, text):
        """Copy text to clipboard with visual feedback"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()  # Ensure clipboard is updated

            # Create a modern toast notification
            toast = tk.Toplevel(self.root)
            toast.title("")
            toast.overrideredirect(True)
            toast.attributes('-topmost', True)

            # Position at top-right
            toast_width = 350
            toast_height = 100
            x = self.root.winfo_x() + self.root.winfo_width() - toast_width - 20
            y = self.root.winfo_y() + 20
            toast.geometry(f'{toast_width}x{toast_height}+{x}+{y}')

            # Toast content with gradient
            toast_frame = tk.Frame(toast, bg='#27ae60', relief=tk.FLAT)
            toast_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

            toast_content = tk.Frame(toast_frame, bg='#27ae60')
            toast_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

            icon_label = tk.Label(
                toast_content,
                text="✅",
                font=('Segoe UI Emoji', 24),
                bg='#27ae60',
                fg='white'
            )
            icon_label.pack(side=tk.LEFT, padx=10)

            text_frame = tk.Frame(toast_content, bg='#27ae60')
            text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            title_label = tk.Label(
                text_frame,
                text="تم النسخ بنجاح!",
                font=('Segoe UI', 12, 'bold'),
                bg='#27ae60',
                fg='white',
                anchor=tk.W
            )
            title_label.pack(anchor=tk.W)

            msg_label = tk.Label(
                text_frame,
                text=f"Copied: {text[:30]}...",
                font=('Segoe UI', 9),
                bg='#27ae60',
                fg='white',
                anchor=tk.W
            )
            msg_label.pack(anchor=tk.W)

            # Auto-close after 2 seconds
            toast.after(2000, toast.destroy)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {str(e)}")

    def show_search_license(self):
        """Show search license interface"""
        self.clear_content()

        # Header
        header = tk.Label(
            self.content_area,
            text="🔍 Search License",
            font=('Segoe UI', 20, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark']
        )
        header.pack(pady=20, padx=30, anchor=tk.W)

        # Search frame
        search_frame = tk.Frame(self.content_area, bg=self.colors['card_bg'])
        search_frame.pack(fill=tk.X, padx=30, pady=20)

        search_label = tk.Label(
            search_frame,
            text="🔑 License Key:",
            font=('Segoe UI', 12),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark']
        )
        search_label.pack(side=tk.LEFT, padx=10)

        self.search_entry = tk.Entry(search_frame, font=('Consolas', 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=10)

        search_btn = tk.Button(
            search_frame,
            text="🔍 Search",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['info'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.search_license_action,
            padx=20,
            pady=8
        )
        search_btn.pack(side=tk.LEFT, padx=10)

        # Result frame
        self.search_result_frame = tk.Frame(self.content_area, bg=self.colors['card_bg'])
        self.search_result_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

    def search_license_action(self):
        """Search for a license"""
        license_key = self.search_entry.get().strip()

        if not license_key:
            messagebox.showwarning("Warning", "Please enter a license key!")
            return

        # Clear previous results
        for widget in self.search_result_frame.winfo_children():
            widget.destroy()

        with self.app.app_context():
            license = License.query.filter_by(license_key=license_key).first()

        if license:
            self.create_license_card(self.search_result_frame, license)
        else:
            no_result = tk.Label(
                self.search_result_frame,
                text="❌ License not found!",
                font=('Segoe UI', 14),
                bg=self.colors['card_bg'],
                fg=self.colors['danger']
            )
            no_result.pack(pady=50)

    def show_license_details(self):
        """Show license details interface"""
        self.show_search_license()

    def view_license_details(self, license_key):
        """View detailed license information"""
        with self.app.app_context():
            license = License.query.filter_by(license_key=license_key).first()

        if not license:
            messagebox.showerror("Error", "License not found!")
            return

        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"License Details - {license_key}")
        details_window.geometry("600x700")
        details_window.configure(bg=self.colors['card_bg'])

        # Header
        header = tk.Label(
            details_window,
            text="🔑 License Details",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            pady=20
        )
        header.pack(fill=tk.X)

        # Content
        content = tk.Frame(details_window, bg=self.colors['card_bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # License key
        key_frame = tk.Frame(content, bg='#f8f9fa', relief=tk.FLAT)
        key_frame.pack(fill=tk.X, pady=10)

        key_content = tk.Frame(key_frame, bg='#f8f9fa')
        key_content.pack(padx=20, pady=15)

        key_label = tk.Label(
            key_content,
            text=license.license_key,
            font=('Consolas', 16, 'bold'),
            bg='#f8f9fa',
            fg=self.colors['primary']
        )
        key_label.pack()

        # Details
        details_data = [
            ("👤 Client Name", license.client_name),
            ("🏢 Company", license.client_company or "N/A"),
            ("📧 Email", license.client_email),
            ("📞 Phone", license.client_phone or "N/A"),
            ("📊 License Type", license.license_type.upper()),
            ("👥 Max Users", str(license.max_users)),
            ("🏪 Max Branches", str(license.max_branches)),
            ("👨‍💼 Admin Username", license.admin_username),
            ("📅 Created At", license.created_at.strftime('%Y-%m-%d %H:%M') if license.created_at else "N/A"),
            ("✅ Activated At", license.activated_at.strftime('%Y-%m-%d %H:%M') if license.activated_at else "Not activated"),
            ("⏰ Expires At", license.expires_at.strftime('%Y-%m-%d') if license.expires_at else "Lifetime ∞"),
            ("🔄 Status", "Active" if license.is_active else "Inactive"),
            ("⏸️ Suspended", "Yes" if license.is_suspended else "No"),
        ]

        for label, value in details_data:
            row = tk.Frame(content, bg=self.colors['card_bg'])
            row.pack(fill=tk.X, pady=5)

            label_widget = tk.Label(
                row,
                text=label + ":",
                font=('Segoe UI', 11),
                bg=self.colors['card_bg'],
                fg=self.colors['text_light'],
                width=20,
                anchor=tk.W
            )
            label_widget.pack(side=tk.LEFT)

            value_widget = tk.Label(
                row,
                text=str(value),
                font=('Segoe UI', 11, 'bold'),
                bg=self.colors['card_bg'],
                fg=self.colors['text_dark'],
                anchor=tk.W
            )
            value_widget.pack(side=tk.LEFT)

        # Close button
        close_btn = tk.Button(
            details_window,
            text="✖️ Close",
            font=('Segoe UI', 11),
            bg=self.colors['text_light'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=details_window.destroy,
            padx=30,
            pady=10
        )
        close_btn.pack(pady=20)

    def extend_license(self):
        """Show extend license interface"""
        self.clear_content()

        # Header
        header = tk.Label(
            self.content_area,
            text="📊 Extend License",
            font=('Segoe UI', 20, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark']
        )
        header.pack(pady=20, padx=30, anchor=tk.W)

        # Form
        form_frame = tk.Frame(self.content_area, bg=self.colors['card_bg'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30)

        # License key input
        key_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
        key_frame.pack(fill=tk.X, pady=10)

        key_label = tk.Label(
            key_frame,
            text="🔑 License Key:",
            font=('Segoe UI', 11),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark'],
            width=20,
            anchor=tk.W
        )
        key_label.pack(side=tk.LEFT)

        self.extend_key_entry = tk.Entry(key_frame, font=('Segoe UI', 11), width=40)
        self.extend_key_entry.pack(side=tk.LEFT, padx=10)

        # Days input
        days_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
        days_frame.pack(fill=tk.X, pady=10)

        days_label = tk.Label(
            days_frame,
            text="📅 Extend Days:",
            font=('Segoe UI', 11),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark'],
            width=20,
            anchor=tk.W
        )
        days_label.pack(side=tk.LEFT)

        self.extend_days_entry = tk.Entry(days_frame, font=('Segoe UI', 11), width=40)
        self.extend_days_entry.insert(0, "30")
        self.extend_days_entry.pack(side=tk.LEFT, padx=10)

        # Buttons
        btn_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
        btn_frame.pack(pady=30)

        extend_btn = tk.Button(
            btn_frame,
            text="✅ Extend License",
            font=('Segoe UI', 12, 'bold'),
            bg='#16a085',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.extend_license_action,
            padx=30,
            pady=12
        )
        extend_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=('Segoe UI', 12),
            bg=self.colors['text_light'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.show_welcome_screen,
            padx=30,
            pady=12
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def extend_license_action(self):
        """Extend a license"""
        license_key = self.extend_key_entry.get().strip()
        days = self.extend_days_entry.get().strip()

        if not license_key or not days:
            messagebox.showwarning("⚠️ Warning", "Please fill all fields!")
            return

        try:
            days = int(days)
            if days <= 0:
                messagebox.showerror("❌ Error", "Days must be a positive number!")
                return

            with self.app.app_context():
                license = License.query.filter_by(license_key=license_key).first()
                if not license:
                    messagebox.showerror("❌ Error", "License not found!")
                    return

                # Store old expiry for display
                old_expiry = license.expires_at.strftime('%Y-%m-%d') if license.expires_at else "Lifetime"

                # Extend license
                if license.expires_at:
                    # If license has expiry date, extend from that date
                    new_expiry = license.expires_at + timedelta(days=days)

                    # If the new expiry is still in the past, extend from today
                    if new_expiry < datetime.utcnow():
                        license.expires_at = datetime.utcnow() + timedelta(days=days)
                    else:
                        license.expires_at = new_expiry
                else:
                    # If lifetime, set expiry from today
                    license.expires_at = datetime.utcnow() + timedelta(days=days)

                new_expiry_str = license.expires_at.strftime('%Y-%m-%d %H:%M')

                db.session.commit()

                messagebox.showinfo(
                    "✅ Success",
                    f"License extended successfully!\n\n"
                    f"🔑 License Key: {license_key}\n"
                    f"📅 Extended by: {days} days\n"
                    f"📆 Old expiry: {old_expiry}\n"
                    f"⏰ New expiry: {new_expiry_str}"
                )
                self.show_welcome_screen()

        except ValueError:
            messagebox.showerror("❌ Error", "Days must be a valid number!")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to extend license:\n{str(e)}")

    def suspend_license(self):
        """Show suspend license interface"""
        self.show_search_license()

    def suspend_license_action(self, license_key):
        """Suspend a license"""
        try:
            with self.app.app_context():
                # Find license by key
                license = License.query.filter_by(license_key=license_key).first()
                if not license:
                    messagebox.showerror("❌ Error", "License not found!")
                    return

                # Check if license is already suspended
                if license.is_suspended:
                    messagebox.showwarning(
                        "⚠️ Already Suspended",
                        f"License is already suspended!\n\n"
                        f"🔑 License Key: {license_key}\n"
                        f"⏸️ Status: Suspended\n"
                        f"⚠️ Reason: {license.suspension_reason or 'N/A'}"
                    )
                    return

                # Ask for suspension reason
                reason_dialog = tk.Toplevel(self.root)
                reason_dialog.title("⏸️ Suspend License")
                reason_dialog.geometry("450x250")
                reason_dialog.configure(bg='white')
                reason_dialog.transient(self.root)
                reason_dialog.grab_set()

                # Center dialog
                reason_dialog.update_idletasks()
                x = self.root.winfo_x() + (self.root.winfo_width() - 450) // 2
                y = self.root.winfo_y() + (self.root.winfo_height() - 250) // 2
                reason_dialog.geometry(f'450x250+{x}+{y}')

                # Header
                header = tk.Label(
                    reason_dialog,
                    text="⏸️ Suspend License",
                    font=('Segoe UI', 16, 'bold'),
                    bg='#f39c12',
                    fg='white',
                    pady=15
                )
                header.pack(fill=tk.X)

                # Content
                content = tk.Frame(reason_dialog, bg='white')
                content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

                # License info
                info_label = tk.Label(
                    content,
                    text=f"🔑 License: {license_key}\n👤 Client: {license.client_name}",
                    font=('Segoe UI', 10),
                    bg='white',
                    fg='#2c3e50',
                    justify=tk.LEFT
                )
                info_label.pack(anchor=tk.W, pady=(0, 15))

                # Reason input
                reason_label = tk.Label(
                    content,
                    text="⚠️ Suspension Reason:",
                    font=('Segoe UI', 10, 'bold'),
                    bg='white',
                    fg='#2c3e50'
                )
                reason_label.pack(anchor=tk.W, pady=(0, 5))

                reason_entry = tk.Entry(content, font=('Segoe UI', 11), width=40)
                reason_entry.insert(0, "Suspended by admin")
                reason_entry.pack(fill=tk.X, pady=(0, 15))
                reason_entry.focus_set()
                reason_entry.select_range(0, tk.END)

                # Buttons
                btn_frame = tk.Frame(content, bg='white')
                btn_frame.pack(fill=tk.X)

                def do_suspend():
                    reason = reason_entry.get().strip()
                    if not reason:
                        reason = "No reason provided"

                    try:
                        # Use app context for database operations
                        with self.app.app_context():
                            # Re-query the license to ensure we're in the right context
                            lic = License.query.filter_by(license_key=license_key).first()
                            if not lic:
                                messagebox.showerror("❌ Error", "License not found!")
                                return

                            # Suspend license
                            lic.is_suspended = True
                            lic.suspension_reason = reason
                            db.session.commit()

                            # Show success message
                            messagebox.showinfo(
                                "✅ Success",
                                f"License suspended successfully!\n\n"
                                f"🔑 License Key: {license_key}\n"
                                f"👤 Client: {lic.client_name}\n"
                                f"⏸️ Status: Suspended\n"
                                f"⚠️ Reason: {reason}"
                            )

                            # Close dialog and refresh
                            reason_dialog.destroy()
                            self.show_all_licenses()

                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        messagebox.showerror("❌ Error", f"Failed to suspend license:\n\n{str(e)}")

                suspend_btn = tk.Button(
                    btn_frame,
                    text="⏸️ Suspend",
                    font=('Segoe UI', 11, 'bold'),
                    bg='#f39c12',
                    fg='white',
                    relief=tk.FLAT,
                    cursor='hand2',
                    command=do_suspend,
                    padx=20,
                    pady=8
                )
                suspend_btn.pack(side=tk.LEFT, padx=(0, 10))

                cancel_btn = tk.Button(
                    btn_frame,
                    text="❌ Cancel",
                    font=('Segoe UI', 11),
                    bg='#95a5a6',
                    fg='white',
                    relief=tk.FLAT,
                    cursor='hand2',
                    command=reason_dialog.destroy,
                    padx=20,
                    pady=8
                )
                cancel_btn.pack(side=tk.LEFT)

        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to suspend license:\n\n{str(e)}")

    def activate_license(self):
        """Show activate license interface"""
        self.show_search_license()

    def activate_license_action(self, license_key):
        """Activate a suspended or inactive license"""
        print(f"DEBUG: activate_license_action called with key: {license_key}")
        try:
            with self.app.app_context():
                # Find license by key
                license = License.query.filter_by(license_key=license_key).first()
                print(f"DEBUG: License found: {license}")

                if not license:
                    messagebox.showerror("❌ Error", "License not found!")
                    return

                print(f"DEBUG: License is_active: {license.is_active}, is_suspended: {license.is_suspended}")

                # Check if license is already active and not suspended
                if license.is_active and not license.is_suspended:
                    messagebox.showwarning(
                        "⚠️ Already Active",
                        f"License is already active!\n\n"
                        f"🔑 License Key: {license_key}\n"
                        f"✅ Status: Active\n"
                        f"📊 Type: {license.license_type.upper()}"
                    )
                    return

                # Determine current status
                if license.is_suspended:
                    old_status = "Suspended"
                    reason = license.suspension_reason or "No reason provided"
                elif not license.is_active:
                    old_status = "Inactive"
                    reason = "License was not activated"
                else:
                    old_status = "Unknown"
                    reason = "N/A"

                # Confirm activation
                confirm = messagebox.askyesno(
                    "🔓 Confirm Activation",
                    f"Are you sure you want to activate this license?\n\n"
                    f"🔑 License Key: {license_key}\n"
                    f"👤 Client: {license.client_name}\n"
                    f"🏢 Company: {license.client_company or 'N/A'}\n"
                    f"📊 Current Status: {old_status}\n"
                    f"⚠️ Reason: {reason}"
                )

                print(f"DEBUG: User confirmed: {confirm}")

                if not confirm:
                    return

                print(f"DEBUG: About to activate license...")

                # Activate license - set both flags
                license.is_active = True
                license.is_suspended = False
                license.suspension_reason = None

                # Set activation date if not set
                if not license.activated_at:
                    license.activated_at = datetime.utcnow()

                print(f"DEBUG: License updated, committing to database...")
                db.session.commit()

                print(f"DEBUG: Database committed successfully!")

                # Show success message
                messagebox.showinfo(
                    "✅ Success",
                    f"License activated successfully!\n\n"
                    f"🔑 License Key: {license_key}\n"
                    f"👤 Client: {license.client_name}\n"
                    f"📊 Old Status: {old_status}\n"
                    f"⚠️ Reason: {reason}\n"
                    f"✅ New Status: Active"
                )

                print(f"DEBUG: Refreshing view...")
                # Refresh the view
                self.show_all_licenses()
                print(f"DEBUG: Activation complete!")

        except Exception as e:
            print(f"DEBUG ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("❌ Error", f"Failed to activate license:\n\n{str(e)}")

    def delete_license(self):
        """Show delete license interface"""
        self.show_search_license()

    def extend_license_from_card(self, license_key):
        """Extend license from card - opens dialog"""
        # Create extend dialog
        extend_dialog = tk.Toplevel(self.root)
        extend_dialog.title(f"Extend License - {license_key}")
        extend_dialog.geometry("500x300")
        extend_dialog.configure(bg='white')
        extend_dialog.transient(self.root)
        extend_dialog.grab_set()

        # Center dialog
        extend_dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 500) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 300) // 2
        extend_dialog.geometry(f'500x300+{x}+{y}')

        # Header
        header = tk.Label(
            extend_dialog,
            text="📊 Extend License",
            font=('Segoe UI', 18, 'bold'),
            bg='#16a085',
            fg='white',
            pady=20
        )
        header.pack(fill=tk.X)

        # Content
        content = tk.Frame(extend_dialog, bg='white')
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # License key display
        key_frame = tk.Frame(content, bg='#ecf0f1')
        key_frame.pack(fill=tk.X, pady=10)

        key_label = tk.Label(
            key_frame,
            text=f"🔑 {license_key}",
            font=('Consolas', 12, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50',
            pady=10
        )
        key_label.pack()

        # Current expiry info
        with self.app.app_context():
            lic = License.query.filter_by(license_key=license_key).first()
            if lic and lic.expires_at:
                current_expiry = lic.expires_at.strftime('%Y-%m-%d')
                days_left = (lic.expires_at - datetime.utcnow()).days
                if days_left < 0:
                    expiry_info = f"⚠️ Expired {abs(days_left)} days ago"
                    expiry_color = '#e74c3c'
                else:
                    expiry_info = f"⏰ {days_left} days left"
                    expiry_color = '#27ae60' if days_left > 30 else '#f39c12'
            else:
                current_expiry = "Lifetime ∞"
                expiry_info = "♾️ No expiry"
                expiry_color = '#3498db'

        info_frame = tk.Frame(content, bg='#ecf0f1')
        info_frame.pack(fill=tk.X, pady=10)

        info_content = tk.Frame(info_frame, bg='#ecf0f1')
        info_content.pack(padx=15, pady=10)

        current_label = tk.Label(
            info_content,
            text=f"Current Expiry: {current_expiry}",
            font=('Segoe UI', 10),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        current_label.pack()

        status_label = tk.Label(
            info_content,
            text=expiry_info,
            font=('Segoe UI', 10, 'bold'),
            bg='#ecf0f1',
            fg=expiry_color
        )
        status_label.pack()

        # Days input
        days_frame = tk.Frame(content, bg='white')
        days_frame.pack(fill=tk.X, pady=20)

        days_label = tk.Label(
            days_frame,
            text="📅 Extend by (days):",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        days_label.pack(anchor=tk.W, pady=5)

        days_entry = tk.Entry(
            days_frame,
            font=('Segoe UI', 14),
            width=20,
            justify='center'
        )
        days_entry.insert(0, "30")
        days_entry.pack(fill=tk.X, pady=5)
        days_entry.focus_set()
        days_entry.select_range(0, tk.END)

        # Buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(pady=20)

        def do_extend():
            days = days_entry.get().strip()
            if not days:
                messagebox.showwarning("⚠️ Warning", "Please enter number of days!")
                return

            try:
                days = int(days)
                if days <= 0:
                    messagebox.showerror("❌ Error", "Days must be a positive number!")
                    return

                with self.app.app_context():
                    license = License.query.filter_by(license_key=license_key).first()
                    if not license:
                        messagebox.showerror("❌ Error", "License not found!")
                        return

                    # Store old expiry for display
                    old_expiry = license.expires_at.strftime('%Y-%m-%d') if license.expires_at else "Lifetime"

                    # Extend license
                    if license.expires_at:
                        # If license has expiry date, extend from that date
                        # Even if it's in the past
                        new_expiry = license.expires_at + timedelta(days=days)

                        # If the new expiry is still in the past, extend from today
                        if new_expiry < datetime.utcnow():
                            license.expires_at = datetime.utcnow() + timedelta(days=days)
                        else:
                            license.expires_at = new_expiry
                    else:
                        # If lifetime, set expiry from today
                        license.expires_at = datetime.utcnow() + timedelta(days=days)

                    new_expiry_str = license.expires_at.strftime('%Y-%m-%d %H:%M')

                    # Commit changes
                    db.session.commit()

                    # Show success message
                    messagebox.showinfo(
                        "✅ Success",
                        f"License extended successfully!\n\n"
                        f"🔑 License Key: {license_key}\n"
                        f"📅 Extended by: {days} days\n"
                        f"📆 Old expiry: {old_expiry}\n"
                        f"⏰ New expiry: {new_expiry_str}"
                    )

                    # Close dialog and refresh
                    extend_dialog.destroy()
                    self.show_all_licenses()

            except ValueError:
                messagebox.showerror("❌ Error", "Days must be a valid number!")
            except Exception as e:
                messagebox.showerror("❌ Error", f"Failed to extend license:\n{str(e)}")

        extend_btn = tk.Button(
            btn_frame,
            text="✅ Extend",
            font=('Segoe UI', 11, 'bold'),
            bg='#16a085',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=do_extend,
            padx=25,
            pady=10
        )
        extend_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=('Segoe UI', 11),
            bg='#95a5a6',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=extend_dialog.destroy,
            padx=25,
            pady=10
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def delete_license_action(self, license_key):
        """Delete a license"""
        if messagebox.askyesno(
            "⚠️ Confirm Delete",
            f"Are you sure you want to DELETE this license?\n\n"
            f"🔑 License Key: {license_key}\n\n"
            f"⚠️ This action CANNOT be undone!"
        ):
            try:
                with self.app.app_context():
                    license = License.query.filter_by(license_key=license_key).first()
                    if license:
                        db.session.delete(license)
                        db.session.commit()
                        messagebox.showinfo("Success", "✅ License deleted successfully!")
                        self.show_all_licenses()
                    else:
                        messagebox.showerror("Error", "License not found!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete license:\n{str(e)}")

    def run(self):
        """Run the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    app = ModernLicenseManagerGUI()
    app.run()


if __name__ == '__main__':
    main()


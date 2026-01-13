#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║           🔐 License Manager - مدير التراخيص                    ║
║                                                                  ║
║                    Professional Edition v2.0                     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

تطبيق سطح مكتب احترافي لإدارة التراخيص
Professional Desktop Application for License Management

المطور: DED Team
التاريخ: 2026-01-12
الإصدار: 2.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import json
import uuid
from datetime import datetime, timedelta
import os
import sys

# ═══════════════════════════════════════════════════════════════════
# 📁 إعدادات الملفات - File Settings
# ═══════════════════════════════════════════════════════════════════

LICENSES_FILE = "licenses.json"
APP_VERSION = "2.0.0"
APP_TITLE = "🔐 License Manager - مدير التراخيص"

# ═══════════════════════════════════════════════════════════════════
# 🎨 الألوان والتنسيقات - Colors & Styles
# ═══════════════════════════════════════════════════════════════════

COLORS = {
    'primary': '#2c3e50',      # أزرق داكن
    'success': '#27ae60',      # أخضر
    'warning': '#f39c12',      # برتقالي
    'danger': '#e74c3c',       # أحمر
    'info': '#3498db',         # أزرق فاتح
    'suspended': '#9b59b6',    # بنفسجي
    'bg_light': '#ecf0f1',     # خلفية فاتحة
    'bg_dark': '#34495e',      # خلفية داكنة
    'text_dark': '#2c3e50',    # نص داكن
    'text_light': '#ffffff',   # نص فاتح
}

# ═══════════════════════════════════════════════════════════════════
# 🔧 دوال المساعدة - Helper Functions
# ═══════════════════════════════════════════════════════════════════

def load_licenses():
    """تحميل التراخيص من الملف"""
    if not os.path.exists(LICENSES_FILE):
        return []
    try:
        with open(LICENSES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_licenses(licenses):
    """حفظ التراخيص في الملف"""
    try:
        with open(LICENSES_FILE, 'w', encoding='utf-8') as f:
            json.dump(licenses, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def generate_license_key():
    """توليد مفتاح ترخيص فريد"""
    return str(uuid.uuid4()).upper()

def calculate_days_remaining(expiry_date_str):
    """حساب الأيام المتبقية"""
    try:
        expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d")
        today = datetime.now()
        delta = expiry_date - today
        return delta.days
    except:
        return 0

def get_status_color(days_remaining, status):
    """الحصول على لون الحالة"""
    if status == "suspended":
        return COLORS['suspended']
    elif days_remaining < 0:
        return COLORS['danger']
    elif days_remaining < 7:
        return COLORS['danger']
    elif days_remaining < 30:
        return COLORS['warning']
    else:
        return COLORS['success']

def format_date(date_str):
    """تنسيق التاريخ"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%Y/%m/%d")
    except:
        return date_str

# ═══════════════════════════════════════════════════════════════════
# 🖥️ التطبيق الرئيسي - Main Application
# ═══════════════════════════════════════════════════════════════════

class LicenseManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1400x800")
        self.root.configure(bg=COLORS['bg_light'])
        
        # تحميل التراخيص
        self.licenses = load_licenses()
        
        # إنشاء الواجهة
        self.create_ui()
        
        # تحديث القائمة
        self.refresh_list()
    
    def create_ui(self):
        """إنشاء واجهة المستخدم"""
        # العنوان الرئيسي
        self.create_header()

        # الحاوية الرئيسية
        main_container = tk.Frame(self.root, bg=COLORS['bg_light'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # القسم الأيسر - الأوامر
        self.create_commands_panel(main_container)

        # القسم الأيمن - القائمة
        self.create_list_panel(main_container)

        # شريط الحالة
        self.create_status_bar()

    def create_header(self):
        """إنشاء العنوان الرئيسي"""
        header = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # العنوان
        title_label = tk.Label(
            header,
            text="🔐 License Manager - مدير التراخيص",
            font=("Arial", 24, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['text_light']
        )
        title_label.pack(pady=15)

        # الإصدار
        version_label = tk.Label(
            header,
            text=f"v{APP_VERSION} | Professional Edition",
            font=("Arial", 10),
            bg=COLORS['primary'],
            fg=COLORS['text_light']
        )
        version_label.pack()

    def create_commands_panel(self, parent):
        """إنشاء لوحة الأوامر"""
        commands_frame = tk.Frame(parent, bg=COLORS['bg_light'], width=300)
        commands_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        commands_frame.pack_propagate(False)

        # عنوان القسم
        title = tk.Label(
            commands_frame,
            text="⚡ الأوامر السريعة - Quick Commands",
            font=("Arial", 14, "bold"),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark']
        )
        title.pack(pady=(0, 20))

        # الأزرار
        buttons = [
            ("➕ إنشاء ترخيص جديد", self.create_license, COLORS['success']),
            ("🔍 البحث عن ترخيص", self.search_license, COLORS['info']),
            ("✅ تفعيل ترخيص", self.activate_license, COLORS['success']),
            ("⏸️ تعليق ترخيص", self.suspend_license, COLORS['warning']),
            ("❌ حذف ترخيص", self.delete_license, COLORS['danger']),
            ("📊 عرض الإحصائيات", self.show_statistics, COLORS['info']),
            ("🔄 تحديث القائمة", self.refresh_list, COLORS['primary']),
            ("📤 تصدير التراخيص", self.export_licenses, COLORS['info']),
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                commands_frame,
                text=text,
                command=command,
                font=("Arial", 11, "bold"),
                bg=color,
                fg=COLORS['text_light'],
                relief=tk.FLAT,
                cursor="hand2",
                padx=20,
                pady=12
            )
            btn.pack(fill=tk.X, pady=5)

            # تأثير hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(relief=tk.RAISED))
            btn.bind("<Leave>", lambda e, b=btn: b.config(relief=tk.FLAT))

    def create_list_panel(self, parent):
        """إنشاء لوحة القائمة"""
        list_frame = tk.Frame(parent, bg=COLORS['bg_light'])
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # عنوان القسم
        title = tk.Label(
            list_frame,
            text="📋 قائمة التراخيص - Licenses List",
            font=("Arial", 14, "bold"),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark']
        )
        title.pack(pady=(0, 10))

        # إنشاء Treeview
        columns = ("company", "key", "created", "expiry", "days", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)

        # تعريف الأعمدة
        self.tree.heading("company", text="الشركة - Company")
        self.tree.heading("key", text="المفتاح - Key")
        self.tree.heading("created", text="تاريخ الإنشاء - Created")
        self.tree.heading("expiry", text="تاريخ الانتهاء - Expiry")
        self.tree.heading("days", text="الأيام المتبقية - Days Left")
        self.tree.heading("status", text="الحالة - Status")

        # عرض الأعمدة
        self.tree.column("company", width=200)
        self.tree.column("key", width=300)
        self.tree.column("created", width=120)
        self.tree.column("expiry", width=120)
        self.tree.column("days", width=150)
        self.tree.column("status", width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # التعبئة
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # تنسيق الألوان
        self.tree.tag_configure('active', background='#d5f4e6')
        self.tree.tag_configure('warning', background='#fff3cd')
        self.tree.tag_configure('danger', background='#f8d7da')
        self.tree.tag_configure('suspended', background='#e8daef')

    def create_status_bar(self):
        """إنشاء شريط الحالة"""
        self.status_bar = tk.Label(
            self.root,
            text="جاهز - Ready",
            font=("Arial", 10),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_light'],
            anchor=tk.W,
            padx=10
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # ═══════════════════════════════════════════════════════════════════
    # 🔧 الدوال الوظيفية - Functional Methods
    # ═══════════════════════════════════════════════════════════════════

    def refresh_list(self):
        """تحديث قائمة التراخيص"""
        # مسح القائمة
        for item in self.tree.get_children():
            self.tree.delete(item)

        # إعادة تحميل التراخيص
        self.licenses = load_licenses()

        # إضافة التراخيص
        for license in self.licenses:
            days_remaining = calculate_days_remaining(license['expiry_date'])
            status = license.get('status', 'active')

            # تحديد اللون
            if status == "suspended":
                tag = 'suspended'
                status_text = "معلق - Suspended"
            elif days_remaining < 0:
                tag = 'danger'
                status_text = "منتهي - Expired"
            elif days_remaining < 7:
                tag = 'danger'
                status_text = "خطر - Critical"
            elif days_remaining < 30:
                tag = 'warning'
                status_text = "تحذير - Warning"
            else:
                tag = 'active'
                status_text = "نشط - Active"

            # إضافة الصف
            self.tree.insert(
                "",
                tk.END,
                values=(
                    license['company_name'],
                    license['license_key'],
                    format_date(license['created_date']),
                    format_date(license['expiry_date']),
                    f"{days_remaining} يوم - days",
                    status_text
                ),
                tags=(tag,)
            )

        # تحديث شريط الحالة
        self.update_status(f"تم تحديث القائمة - {len(self.licenses)} ترخيص")

    def update_status(self, message):
        """تحديث شريط الحالة"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()

    def create_license(self):
        """إنشاء ترخيص جديد"""
        # نافذة الإدخال
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ إنشاء ترخيص جديد - Create New License")
        dialog.geometry("500x300")
        dialog.configure(bg=COLORS['bg_light'])
        dialog.transient(self.root)
        dialog.grab_set()

        # العنوان
        title = tk.Label(
            dialog,
            text="➕ إنشاء ترخيص جديد",
            font=("Arial", 16, "bold"),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark']
        )
        title.pack(pady=20)

        # اسم الشركة
        tk.Label(dialog, text="اسم الشركة - Company Name:", bg=COLORS['bg_light']).pack(pady=5)
        company_entry = tk.Entry(dialog, font=("Arial", 12), width=40)
        company_entry.pack(pady=5)
        company_entry.focus()

        # المدة
        tk.Label(dialog, text="المدة (بالأيام) - Duration (days):", bg=COLORS['bg_light']).pack(pady=5)
        duration_entry = tk.Entry(dialog, font=("Arial", 12), width=40)
        duration_entry.pack(pady=5)
        duration_entry.insert(0, "365")

        def submit():
            company_name = company_entry.get().strip()
            duration_str = duration_entry.get().strip()

            if not company_name:
                messagebox.showerror("خطأ - Error", "الرجاء إدخال اسم الشركة")
                return

            try:
                duration = int(duration_str)
                if duration <= 0:
                    raise ValueError()
            except:
                messagebox.showerror("خطأ - Error", "الرجاء إدخال مدة صحيحة")
                return

            # إنشاء الترخيص
            license_key = generate_license_key()
            created_date = datetime.now().strftime("%Y-%m-%d")
            expiry_date = (datetime.now() + timedelta(days=duration)).strftime("%Y-%m-%d")

            new_license = {
                "license_key": license_key,
                "company_name": company_name,
                "created_date": created_date,
                "expiry_date": expiry_date,
                "status": "active"
            }

            self.licenses.append(new_license)
            save_licenses(self.licenses)

            # حفظ في ملف منفصل
            filename = f"License_{company_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("╔══════════════════════════════════════════════════════════════════╗\n")
                f.write("║                                                                  ║\n")
                f.write("║           🔐 License Manager - مدير التراخيص                    ║\n")
                f.write("║                                                                  ║\n")
                f.write("╚══════════════════════════════════════════════════════════════════╝\n\n")
                f.write(f"الشركة - Company: {company_name}\n")
                f.write(f"مفتاح الترخيص - License Key:\n{license_key}\n\n")
                f.write(f"تاريخ الإنشاء - Created: {format_date(created_date)}\n")
                f.write(f"تاريخ الانتهاء - Expiry: {format_date(expiry_date)}\n")
                f.write(f"المدة - Duration: {duration} يوم - days\n\n")
                f.write("═══════════════════════════════════════════════════════════════════\n")
                f.write(f"تم الإنشاء بواسطة License Manager v{APP_VERSION}\n")

            messagebox.showinfo(
                "نجح - Success",
                f"تم إنشاء الترخيص بنجاح!\n\nالمفتاح:\n{license_key}\n\nتم حفظ الملف:\n{filename}"
            )

            dialog.destroy()
            self.refresh_list()

        # الأزرار
        btn_frame = tk.Frame(dialog, bg=COLORS['bg_light'])
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="✅ إنشاء - Create",
            command=submit,
            font=("Arial", 12, "bold"),
            bg=COLORS['success'],
            fg=COLORS['text_light'],
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="❌ إلغاء - Cancel",
            command=dialog.destroy,
            font=("Arial", 12, "bold"),
            bg=COLORS['danger'],
            fg=COLORS['text_light'],
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

    def search_license(self):
        """البحث عن ترخيص"""
        search_term = simpledialog.askstring(
            "🔍 البحث - Search",
            "أدخل مفتاح الترخيص أو اسم الشركة:\nEnter license key or company name:"
        )

        if not search_term:
            return

        search_term = search_term.strip().lower()
        found = []

        for license in self.licenses:
            if (search_term in license['license_key'].lower() or
                search_term in license['company_name'].lower()):
                found.append(license)

        if not found:
            messagebox.showinfo("🔍 البحث - Search", "لم يتم العثور على نتائج\nNo results found")
            return

        # عرض النتائج
        result_window = tk.Toplevel(self.root)
        result_window.title("🔍 نتائج البحث - Search Results")
        result_window.geometry("800x400")
        result_window.configure(bg=COLORS['bg_light'])

        title = tk.Label(
            result_window,
            text=f"🔍 نتائج البحث - Found {len(found)} result(s)",
            font=("Arial", 14, "bold"),
            bg=COLORS['bg_light']
        )
        title.pack(pady=10)

        text = scrolledtext.ScrolledText(result_window, font=("Courier", 10), wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for license in found:
            days_remaining = calculate_days_remaining(license['expiry_date'])
            status = license.get('status', 'active')

            text.insert(tk.END, "═" * 80 + "\n")
            text.insert(tk.END, f"الشركة - Company: {license['company_name']}\n")
            text.insert(tk.END, f"المفتاح - Key: {license['license_key']}\n")
            text.insert(tk.END, f"تاريخ الإنشاء - Created: {format_date(license['created_date'])}\n")
            text.insert(tk.END, f"تاريخ الانتهاء - Expiry: {format_date(license['expiry_date'])}\n")
            text.insert(tk.END, f"الأيام المتبقية - Days Left: {days_remaining}\n")
            text.insert(tk.END, f"الحالة - Status: {status}\n")
            text.insert(tk.END, "═" * 80 + "\n\n")

        text.config(state=tk.DISABLED)

    def activate_license(self):
        """تفعيل ترخيص"""
        license_key = simpledialog.askstring(
            "✅ تفعيل ترخيص - Activate License",
            "أدخل مفتاح الترخيص:\nEnter license key:"
        )

        if not license_key:
            return

        license_key = license_key.strip().upper()

        for license in self.licenses:
            if license['license_key'] == license_key:
                license['status'] = 'active'
                save_licenses(self.licenses)
                messagebox.showinfo("✅ نجح - Success", "تم تفعيل الترخيص بنجاح")
                self.refresh_list()
                return

        messagebox.showerror("❌ خطأ - Error", "الترخيص غير موجود")

    def suspend_license(self):
        """تعليق ترخيص"""
        license_key = simpledialog.askstring(
            "⏸️ تعليق ترخيص - Suspend License",
            "أدخل مفتاح الترخيص:\nEnter license key:"
        )

        if not license_key:
            return

        license_key = license_key.strip().upper()

        for license in self.licenses:
            if license['license_key'] == license_key:
                license['status'] = 'suspended'
                save_licenses(self.licenses)
                messagebox.showinfo("⏸️ نجح - Success", "تم تعليق الترخيص بنجاح")
                self.refresh_list()
                return

        messagebox.showerror("❌ خطأ - Error", "الترخيص غير موجود")

    def delete_license(self):
        """حذف ترخيص"""
        license_key = simpledialog.askstring(
            "❌ حذف ترخيص - Delete License",
            "أدخل مفتاح الترخيص:\nEnter license key:"
        )

        if not license_key:
            return

        license_key = license_key.strip().upper()

        for i, license in enumerate(self.licenses):
            if license['license_key'] == license_key:
                confirm = messagebox.askyesno(
                    "❌ تأكيد الحذف - Confirm Delete",
                    f"هل أنت متأكد من حذف ترخيص:\n{license['company_name']}؟"
                )

                if confirm:
                    self.licenses.pop(i)
                    save_licenses(self.licenses)
                    messagebox.showinfo("✅ نجح - Success", "تم حذف الترخيص بنجاح")
                    self.refresh_list()
                return

        messagebox.showerror("❌ خطأ - Error", "الترخيص غير موجود")

    def show_statistics(self):
        """عرض الإحصائيات"""
        total = len(self.licenses)
        active = sum(1 for l in self.licenses if l.get('status', 'active') == 'active' and calculate_days_remaining(l['expiry_date']) >= 0)
        suspended = sum(1 for l in self.licenses if l.get('status', 'active') == 'suspended')
        expired = sum(1 for l in self.licenses if calculate_days_remaining(l['expiry_date']) < 0)
        warnings = sum(1 for l in self.licenses if 0 <= calculate_days_remaining(l['expiry_date']) < 30 and l.get('status', 'active') == 'active')

        # نافذة الإحصائيات
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 الإحصائيات - Statistics")
        stats_window.geometry("600x500")
        stats_window.configure(bg=COLORS['bg_light'])
        stats_window.transient(self.root)

        title = tk.Label(
            stats_window,
            text="📊 إحصائيات التراخيص - License Statistics",
            font=("Arial", 16, "bold"),
            bg=COLORS['bg_light']
        )
        title.pack(pady=20)

        # البطاقات
        cards_frame = tk.Frame(stats_window, bg=COLORS['bg_light'])
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        stats = [
            ("📊 إجمالي التراخيص\nTotal Licenses", total, COLORS['primary']),
            ("✅ التراخيص النشطة\nActive Licenses", active, COLORS['success']),
            ("⏸️ التراخيص المعلقة\nSuspended Licenses", suspended, COLORS['suspended']),
            ("❌ التراخيص المنتهية\nExpired Licenses", expired, COLORS['danger']),
            ("⚠️ تحذيرات (< 30 يوم)\nWarnings (< 30 days)", warnings, COLORS['warning']),
        ]

        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(cards_frame, bg=color, relief=tk.RAISED, borderwidth=2)
            card.pack(fill=tk.X, pady=10)

            tk.Label(
                card,
                text=str(value),
                font=("Arial", 32, "bold"),
                bg=color,
                fg=COLORS['text_light']
            ).pack(pady=10)

            tk.Label(
                card,
                text=label,
                font=("Arial", 12),
                bg=color,
                fg=COLORS['text_light']
            ).pack(pady=5)

    def export_licenses(self):
        """تصدير التراخيص"""
        if not self.licenses:
            messagebox.showinfo("📤 تصدير - Export", "لا توجد تراخيص للتصدير")
            return

        filename = f"Licenses_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("╔══════════════════════════════════════════════════════════════════╗\n")
                f.write("║                                                                  ║\n")
                f.write("║           🔐 License Manager - مدير التراخيص                    ║\n")
                f.write("║                                                                  ║\n")
                f.write("║                    تقرير التراخيص - Licenses Report            ║\n")
                f.write("║                                                                  ║\n")
                f.write("╚══════════════════════════════════════════════════════════════════╝\n\n")
                f.write(f"تاريخ التصدير - Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"إجمالي التراخيص - Total Licenses: {len(self.licenses)}\n\n")
                f.write("═" * 80 + "\n\n")

                for i, license in enumerate(self.licenses, 1):
                    days_remaining = calculate_days_remaining(license['expiry_date'])
                    status = license.get('status', 'active')

                    f.write(f"[{i}] {license['company_name']}\n")
                    f.write("─" * 80 + "\n")
                    f.write(f"المفتاح - License Key:\n{license['license_key']}\n\n")
                    f.write(f"تاريخ الإنشاء - Created: {format_date(license['created_date'])}\n")
                    f.write(f"تاريخ الانتهاء - Expiry: {format_date(license['expiry_date'])}\n")
                    f.write(f"الأيام المتبقية - Days Left: {days_remaining} يوم - days\n")
                    f.write(f"الحالة - Status: {status}\n")
                    f.write("═" * 80 + "\n\n")

                f.write("\n")
                f.write("═" * 80 + "\n")
                f.write(f"تم التصدير بواسطة License Manager v{APP_VERSION}\n")
                f.write(f"Made with ❤️ by DED Team\n")
                f.write("═" * 80 + "\n")

            # فتح الملف
            os.startfile(filename)

            messagebox.showinfo(
                "✅ نجح - Success",
                f"تم تصدير {len(self.licenses)} ترخيص بنجاح!\n\nالملف:\n{filename}"
            )

        except Exception as e:
            messagebox.showerror("❌ خطأ - Error", f"فشل التصدير:\n{str(e)}")

# ═══════════════════════════════════════════════════════════════════
# 🚀 تشغيل التطبيق - Run Application
# ═══════════════════════════════════════════════════════════════════

def main():
    """الدالة الرئيسية"""
    root = tk.Tk()
    app = LicenseManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


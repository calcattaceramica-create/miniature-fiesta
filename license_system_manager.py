#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
License System Manager - مدير نظام التراخيص
نظام متكامل لإدارة تراخيص العملاء
"""

from app import create_app, db
from app.license_manager import LicenseManager
from app.models_license import License
from app.models import User, Role
from werkzeug.security import generate_password_hash
import sys
import getpass
from datetime import datetime
from tabulate import tabulate

class LicenseSystemManager:
    """مدير نظام التراخيص"""
    
    def __init__(self):
        self.app = create_app()
    
    def create_license(self):
        """Create New License"""
        print("\n" + "=" * 80)
        print("Create New License")
        print("=" * 80)

        with self.app.app_context():
            # Client Information
            print("\nClient Information:")
            client_name = input("  Client Name: ").strip()
            if not client_name:
                print("  ERROR: Client Name is required!")
                return

            client_company = input("  Company [optional]: ").strip() or None
            client_email = input("  Email [optional]: ").strip() or None
            client_phone = input("  Phone [optional]: ").strip() or None

            # Admin Information
            print("\nAdmin Information:")
            admin_username = input("  Username: ").strip()
            if not admin_username:
                print("  ERROR: Username is required!")
                return

            admin_password = getpass.getpass("  Password: ")
            if not admin_password:
                print("  ERROR: Password is required!")
                return

            # License Type
            print("\nLicense Type:")
            print("  1. Trial - 30 days")
            print("  2. Monthly - 30 days")
            print("  3. Quarterly - 90 days")
            print("  4. Semi-Annual - 180 days")
            print("  5. Yearly - 365 days")
            print("  6. Lifetime")

            choice = input("\n  Choose (1-6): ").strip()
            
            types = {
                '1': ('trial', 30),
                '2': ('monthly', 30),
                '3': ('quarterly', 90),
                '4': ('semi_annual', 180),
                '5': ('yearly', 365),
                '6': ('lifetime', None)
            }
            
            if choice not in types:
                print("  ERROR: Invalid choice!")
                return

            license_type, duration = types[choice]

            # License Limits
            print("\nLicense Limits:")
            max_users = input("  Max Users [5]: ").strip()
            max_users = int(max_users) if max_users.isdigit() else 5

            max_branches = input("  Max Branches [1]: ").strip()
            max_branches = int(max_branches) if max_branches.isdigit() else 1

            notes = input("\nNotes [optional]: ").strip() or None
            
            # إنشاء الترخيص
            try:
                license = LicenseManager.create_license(
                    client_name=client_name,
                    admin_username=admin_username,
                    admin_password=admin_password,
                    license_type=license_type,
                    duration_days=duration,
                    max_users=max_users,
                    max_branches=max_branches,
                    client_email=client_email,
                    client_phone=client_phone,
                    client_company=client_company,
                    notes=notes
                )
                
                # إنشاء مستخدم المدير
                admin_role = Role.query.filter_by(name='admin').first()
                if not admin_role:
                    admin_role = Role(name='admin', name_ar='مدير النظام')
                    db.session.add(admin_role)
                    db.session.commit()
                
                admin_user = User(
                    username=admin_username,
                    email=client_email or f"{admin_username}@client.com",
                    password_hash=generate_password_hash(admin_password),
                    role_id=admin_role.id,
                    license_id=license.id,
                    is_active=True
                )
                db.session.add(admin_user)
                db.session.commit()
                
                # Display Information
                print("\n" + "=" * 80)
                print("SUCCESS: License created successfully!")
                print("=" * 80)

                self._display_license_info(license)

                # Save to file
                self._save_license_to_file(license, admin_username, admin_password)

            except Exception as e:
                print(f"\nERROR: {str(e)}")
                import traceback
                traceback.print_exc()
    
    def _display_license_info(self, license):
        """Display License Information"""
        print(f"\nLicense Key: {license.license_key}")
        print(f"Client: {license.client_name}")
        if license.client_company:
            print(f"Company: {license.client_company}")
        print(f"Type: {license.license_type}")
        print(f"Max Users: {license.max_users}")
        print(f"Max Branches: {license.max_branches}")

        if license.expires_at:
            print(f"Expires: {license.expires_at.strftime('%Y-%m-%d')}")
            print(f"Days Remaining: {license.days_remaining()} days")
        else:
            print(f"Validity: Lifetime")
    
    def _save_license_to_file(self, license, username, password):
        """حفظ معلومات الترخيص في ملف"""
        filename = f"license_{license.license_key.replace('-', '_')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("معلومات الترخيص - License Information\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"مفتاح الترخيص (License Key): {license.license_key}\n")
            f.write(f"العميل (Client): {license.client_name}\n")
            if license.client_company:
                f.write(f"الشركة (Company): {license.client_company}\n")
            f.write(f"النوع (Type): {license.license_type}\n")
            f.write(f"المستخدمين (Max Users): {license.max_users}\n")
            f.write(f"الفروع (Max Branches): {license.max_branches}\n")
            
            if license.expires_at:
                f.write(f"تاريخ الانتهاء (Expires): {license.expires_at.strftime('%Y-%m-%d')}\n")
            else:
                f.write(f"الصلاحية (Validity): مدى الحياة (Lifetime)\n")
            
            f.write(f"\nاسم المستخدم (Username): {username}\n")
            f.write(f"كلمة المرور (Password): {password}\n")
            f.write("\n" + "=" * 80 + "\n")
            f.write("⚠️  احفظ هذا الملف في مكان آمن!\n")
            f.write("=" * 80 + "\n")
        
        print(f"\n💾 تم حفظ المعلومات في: {filename}")

def main():
    """القائمة الرئيسية"""
    manager = LicenseSystemManager()

    while True:
        print("\n" + "=" * 80)
        print("License Manager - License Management System")
        print("=" * 80)
        print("\n1. Create New License")
        print("2. List All Licenses")
        print("3. Search License")
        print("4. Extend License")
        print("5. Suspend License")
        print("6. Unsuspend License")
        print("0. Exit")

        choice = input("\nChoose (0-6): ").strip()

        if choice == '1':
            manager.create_license()
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("\nComing soon...")

if __name__ == '__main__':
    main()


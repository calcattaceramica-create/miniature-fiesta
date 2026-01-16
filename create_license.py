#!/usr/bin/env python
"""
Create License Script
سكريبت إنشاء ترخيص جديد
"""
import sys
from app import create_app, db
from app.license_manager import LicenseManager
from datetime import datetime

def create_trial_license():
    """Create a trial license"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("إنشاء ترخيص تجريبي - Create Trial License")
        print("=" * 60)
        
        # Get license details
        client_name = input("\nاسم العميل - Client Name: ").strip()
        if not client_name:
            client_name = "Trial User"
        
        admin_username = input("اسم المستخدم للمدير - Admin Username: ").strip()
        if not admin_username:
            admin_username = "admin"
        
        admin_password = input("كلمة المرور للمدير - Admin Password: ").strip()
        if not admin_password:
            admin_password = "admin123"
        
        client_email = input("البريد الإلكتروني - Email (optional): ").strip() or None
        client_phone = input("رقم الهاتف - Phone (optional): ").strip() or None
        client_company = input("اسم الشركة - Company (optional): ").strip() or None
        
        # License type
        print("\nنوع الترخيص - License Type:")
        print("1. Trial (30 days)")
        print("2. Monthly (30 days)")
        print("3. Yearly (365 days)")
        print("4. Lifetime (no expiry)")
        
        choice = input("اختر - Choose [1-4]: ").strip()
        
        license_types = {
            '1': ('trial', 30),
            '2': ('monthly', 30),
            '3': ('yearly', 365),
            '4': ('lifetime', None)
        }
        
        license_type, duration_days = license_types.get(choice, ('trial', 30))
        
        # Max users
        max_users_input = input("\nالحد الأقصى للمستخدمين - Max Users [default: 5]: ").strip()
        max_users = int(max_users_input) if max_users_input.isdigit() else 5
        
        # Max branches
        max_branches_input = input("الحد الأقصى للفروع - Max Branches [default: 1]: ").strip()
        max_branches = int(max_branches_input) if max_branches_input.isdigit() else 1
        
        notes = input("ملاحظات - Notes (optional): ").strip() or None
        
        print("\n" + "=" * 60)
        print("جاري إنشاء الترخيص - Creating License...")
        print("=" * 60)
        
        try:
            # Create license
            license = LicenseManager.create_license(
                client_name=client_name,
                admin_username=admin_username,
                admin_password=admin_password,
                license_type=license_type,
                duration_days=duration_days,
                max_users=max_users,
                max_branches=max_branches,
                client_email=client_email,
                client_phone=client_phone,
                client_company=client_company,
                notes=notes
            )
            
            print("\n✅ تم إنشاء الترخيص بنجاح - License Created Successfully!")
            print("=" * 60)
            print(f"مفتاح الترخيص - License Key: {license.license_key}")
            print(f"اسم العميل - Client Name: {license.client_name}")
            print(f"نوع الترخيص - License Type: {license.license_type}")
            print(f"تاريخ الإنشاء - Created: {license.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if license.expires_at:
                print(f"تاريخ الانتهاء - Expires: {license.expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"الأيام المتبقية - Days Remaining: {license.days_remaining()}")
            else:
                print("تاريخ الانتهاء - Expires: دائم - Lifetime")
            
            print(f"الحد الأقصى للمستخدمين - Max Users: {license.max_users}")
            print(f"الحد الأقصى للفروع - Max Branches: {license.max_branches}")
            print("=" * 60)
            
            print("\n⚠️ احفظ مفتاح الترخيص في مكان آمن!")
            print("⚠️ Save the license key in a safe place!")
            
        except Exception as e:
            print(f"\n❌ خطأ - Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        
        return True

def list_licenses():
    """List all licenses"""
    app = create_app()
    
    with app.app_context():
        licenses = LicenseManager.get_all_licenses()
        
        if not licenses:
            print("\n⚠️ لا توجد تراخيص - No licenses found")
            return
        
        print("\n" + "=" * 80)
        print("قائمة التراخيص - Licenses List")
        print("=" * 80)
        
        for license in licenses:
            is_valid, message = license.is_valid()
            status_icon = "✅" if is_valid else "❌"
            
            print(f"\n{status_icon} License ID: {license.id}")
            print(f"   Key: {license.license_key}")
            print(f"   Client: {license.client_name}")
            print(f"   Type: {license.license_type}")
            print(f"   Status: {message}")
            print(f"   Created: {license.created_at.strftime('%Y-%m-%d')}")
            
            if license.expires_at:
                print(f"   Expires: {license.expires_at.strftime('%Y-%m-%d')} ({license.days_remaining()} days)")
            else:
                print(f"   Expires: Lifetime")
            
            print(f"   Max Users: {license.max_users}, Max Branches: {license.max_branches}")
        
        print("=" * 80)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        list_licenses()
    else:
        create_trial_license()


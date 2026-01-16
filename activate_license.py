#!/usr/bin/env python
"""
Activate License Script - Auto Create Trial License
سكريبت تفعيل الترخيص التلقائي
"""
from app import create_app, db
from app.license_manager import LicenseManager
from datetime import datetime

def activate_default_license():
    """Create and activate a default trial license"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("تفعيل الترخيص التلقائي - Auto License Activation")
        print("=" * 60)
        
        # Check if license already exists
        existing_licenses = LicenseManager.get_all_licenses()
        if existing_licenses:
            print("\n⚠️ يوجد ترخيص مفعّل بالفعل - License already exists!")
            for license in existing_licenses:
                is_valid, message = license.is_valid()
                print(f"\nLicense Key: {license.license_key}")
                print(f"Status: {message}")
                print(f"Client: {license.client_name}")
                if license.expires_at:
                    print(f"Expires: {license.expires_at.strftime('%Y-%m-%d')} ({license.days_remaining()} days)")
                else:
                    print("Expires: Lifetime")
            return
        
        print("\nجاري إنشاء ترخيص تجريبي - Creating trial license...")
        
        try:
            # Create a trial license with default values
            license = LicenseManager.create_license(
                client_name="DED ERP System",
                admin_username="admin",
                admin_password="admin123",
                license_type="trial",
                duration_days=365,  # 1 year trial
                max_users=10,
                max_branches=5,
                client_email="info@ded-erp.com",
                client_phone="+966-XXX-XXXX",
                client_company="DED Company",
                notes="Auto-generated trial license"
            )
            
            print("\n✅ تم إنشاء وتفعيل الترخيص بنجاح!")
            print("✅ License Created and Activated Successfully!")
            print("=" * 60)
            print(f"🔑 مفتاح الترخيص - License Key:")
            print(f"   {license.license_key}")
            print("=" * 60)
            print(f"📋 تفاصيل الترخيص - License Details:")
            print(f"   اسم العميل - Client: {license.client_name}")
            print(f"   نوع الترخيص - Type: {license.license_type.upper()}")
            print(f"   تاريخ الإنشاء - Created: {license.created_at.strftime('%Y-%m-%d')}")
            
            if license.expires_at:
                print(f"   تاريخ الانتهاء - Expires: {license.expires_at.strftime('%Y-%m-%d')}")
                print(f"   الأيام المتبقية - Days Remaining: {license.days_remaining()} days")
            else:
                print("   تاريخ الانتهاء - Expires: دائم - Lifetime")
            
            print(f"   الحد الأقصى للمستخدمين - Max Users: {license.max_users}")
            print(f"   الحد الأقصى للفروع - Max Branches: {license.max_branches}")
            print("=" * 60)
            
            print("\n👤 بيانات تسجيل الدخول - Login Credentials:")
            print(f"   Username: admin")
            print(f"   Password: admin123")
            print("=" * 60)
            
            print("\n✅ يمكنك الآن تشغيل النظام!")
            print("✅ You can now run the system!")
            print("\n💡 لعرض معلومات الترخيص، قم بتسجيل الدخول وانتقل إلى:")
            print("💡 To view license info, login and go to:")
            print("   http://127.0.0.1:5000/license-info")
            
        except Exception as e:
            print(f"\n❌ خطأ - Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        
        return True

if __name__ == '__main__':
    activate_default_license()


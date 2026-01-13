#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create Client License
إنشاء ترخيص لعميل جديد
"""
import sys
from app import create_app, db
from app.models_license import License
from app.license_manager import LicenseManager

def create_client():
    """Create a new client license"""
    print("=" * 70)
    print("🔑 إنشاء ترخيص لعميل جديد - Create New Client License")
    print("=" * 70)
    print()
    
    # Get client information
    print("📋 معلومات العميل - Client Information:")
    print("-" * 70)
    client_name = input("اسم العميل - Client Name: ").strip()
    if not client_name:
        print("❌ اسم العميل مطلوب!")
        return
    
    client_company = input("اسم الشركة - Company Name (اختياري): ").strip() or None
    client_email = input("البريد الإلكتروني - Email (اختياري): ").strip() or None
    client_phone = input("رقم الهاتف - Phone (اختياري): ").strip() or None
    
    print()
    print("👤 معلومات المستخدم الإداري - Admin User Information:")
    print("-" * 70)
    admin_username = input("اسم المستخدم - Username: ").strip()
    if not admin_username:
        print("❌ اسم المستخدم مطلوب!")
        return
    
    admin_password = input("كلمة المرور - Password: ").strip()
    if not admin_password:
        print("❌ كلمة المرور مطلوبة!")
        return
    
    print()
    print("📅 نوع الترخيص - License Type:")
    print("-" * 70)
    print("1. تجريبي - Trial (30 يوم)")
    print("2. شهري - Monthly (30 يوم)")
    print("3. سنوي - Yearly (365 يوم)")
    print("4. دائم - Lifetime (بدون انتهاء)")
    
    license_type_choice = input("اختر نوع الترخيص (1-4): ").strip()
    
    license_types = {
        '1': ('trial', 30),
        '2': ('monthly', 30),
        '3': ('yearly', 365),
        '4': ('lifetime', None)
    }
    
    if license_type_choice not in license_types:
        print("❌ اختيار غير صحيح!")
        return
    
    license_type, duration_days = license_types[license_type_choice]
    
    print()
    print("⚙️ إعدادات الترخيص - License Settings:")
    print("-" * 70)
    
    try:
        max_users = int(input("الحد الأقصى للمستخدمين - Max Users (افتراضي: 5): ").strip() or "5")
        max_branches = int(input("الحد الأقصى للفروع - Max Branches (افتراضي: 3): ").strip() or "3")
    except ValueError:
        print("❌ يجب إدخال أرقام صحيحة!")
        return
    
    notes = input("ملاحظات - Notes (اختياري): ").strip() or None
    
    print()
    print("=" * 70)
    print("📝 ملخص الترخيص - License Summary:")
    print("=" * 70)
    print(f"العميل: {client_name}")
    if client_company:
        print(f"الشركة: {client_company}")
    if client_email:
        print(f"البريد: {client_email}")
    if client_phone:
        print(f"الهاتف: {client_phone}")
    print(f"اسم المستخدم: {admin_username}")
    print(f"نوع الترخيص: {license_type}")
    if duration_days:
        print(f"المدة: {duration_days} يوم")
    else:
        print(f"المدة: دائم")
    print(f"عدد المستخدمين: {max_users}")
    print(f"عدد الفروع: {max_branches}")
    print("=" * 70)
    
    confirm = input("\n✅ هل تريد إنشاء الترخيص؟ (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ تم الإلغاء")
        return
    
    # Create license
    app = create_app()
    with app.app_context():
        try:
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
            
            print()
            print("=" * 70)
            print("✅ تم إنشاء الترخيص بنجاح! - License Created Successfully!")
            print("=" * 70)
            print()
            print("🔑 مفتاح الترخيص - License Key:")
            print(f"   {license.license_key}")
            print()
            print("👤 معلومات الدخول - Login Information:")
            print(f"   اسم المستخدم - Username: {admin_username}")
            print(f"   كلمة المرور - Password: {admin_password}")
            print()
            if license.expires_at:
                print(f"📅 تاريخ الانتهاء - Expiration Date: {license.expires_at.strftime('%Y-%m-%d %H:%M')}")
                print(f"⏰ الأيام المتبقية - Days Remaining: {license.days_remaining()}")
            else:
                print("📅 الترخيص دائم - Lifetime License")
            print()
            print("=" * 70)
            print("⚠️  احفظ هذه المعلومات وأرسلها للعميل!")
            print("=" * 70)
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء الترخيص: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_client()


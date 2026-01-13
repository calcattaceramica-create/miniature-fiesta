#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Manage Licenses
إدارة التراخيص - تعليق، إلغاء، تمديد
"""
from app import create_app, db
from app.models_license import License
from app.license_manager import LicenseManager
from datetime import datetime

def show_all_licenses():
    """Show all licenses"""
    licenses = LicenseManager.get_all_licenses()
    
    if not licenses:
        print("❌ لا توجد تراخيص")
        return None
    
    print()
    print("=" * 100)
    print("📋 قائمة التراخيص - Licenses List")
    print("=" * 100)
    print(f"{'ID':<5} {'العميل':<20} {'المفتاح':<20} {'النوع':<10} {'الحالة':<15} {'الانتهاء':<20}")
    print("-" * 100)
    
    for lic in licenses:
        status = "✅ نشط" if lic.is_active else "❌ معطل"
        if lic.is_suspended:
            status = "⏸️ معلق"
        
        expiry = "دائم" if not lic.expires_at else lic.expires_at.strftime('%Y-%m-%d')
        
        print(f"{lic.id:<5} {lic.client_name:<20} {lic.license_key:<20} {lic.license_type:<10} {status:<15} {expiry:<20}")
    
    print("=" * 100)
    return licenses

def suspend_license():
    """Suspend a license"""
    licenses = show_all_licenses()
    if not licenses:
        return
    
    print()
    license_id = input("أدخل رقم الترخيص للتعليق - Enter License ID to suspend: ").strip()
    
    try:
        license_id = int(license_id)
    except ValueError:
        print("❌ رقم غير صحيح!")
        return
    
    reason = input("سبب التعليق - Suspension Reason: ").strip()
    
    if LicenseManager.suspend_license(license_id, reason):
        print(f"✅ تم تعليق الترخيص #{license_id}")
    else:
        print(f"❌ فشل تعليق الترخيص #{license_id}")

def unsuspend_license():
    """Unsuspend a license"""
    licenses = show_all_licenses()
    if not licenses:
        return
    
    print()
    license_id = input("أدخل رقم الترخيص لإلغاء التعليق - Enter License ID to unsuspend: ").strip()
    
    try:
        license_id = int(license_id)
    except ValueError:
        print("❌ رقم غير صحيح!")
        return
    
    if LicenseManager.unsuspend_license(license_id):
        print(f"✅ تم إلغاء تعليق الترخيص #{license_id}")
    else:
        print(f"❌ فشل إلغاء تعليق الترخيص #{license_id}")

def deactivate_license():
    """Deactivate a license permanently"""
    licenses = show_all_licenses()
    if not licenses:
        return
    
    print()
    license_id = input("أدخل رقم الترخيص للإلغاء النهائي - Enter License ID to deactivate: ").strip()
    
    try:
        license_id = int(license_id)
    except ValueError:
        print("❌ رقم غير صحيح!")
        return
    
    confirm = input("⚠️  هل أنت متأكد من إلغاء الترخيص نهائياً؟ (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ تم الإلغاء")
        return
    
    if LicenseManager.deactivate_license(license_id):
        print(f"✅ تم إلغاء الترخيص #{license_id} نهائياً")
    else:
        print(f"❌ فشل إلغاء الترخيص #{license_id}")

def extend_license():
    """Extend license duration"""
    licenses = show_all_licenses()
    if not licenses:
        return
    
    print()
    license_id = input("أدخل رقم الترخيص للتمديد - Enter License ID to extend: ").strip()
    
    try:
        license_id = int(license_id)
    except ValueError:
        print("❌ رقم غير صحيح!")
        return
    
    days = input("عدد الأيام للتمديد - Days to extend: ").strip()
    
    try:
        days = int(days)
    except ValueError:
        print("❌ رقم غير صحيح!")
        return
    
    if LicenseManager.extend_license(license_id, days):
        print(f"✅ تم تمديد الترخيص #{license_id} لمدة {days} يوم")
    else:
        print(f"❌ فشل تمديد الترخيص #{license_id}")

def view_license_details():
    """View detailed license information"""
    licenses = show_all_licenses()
    if not licenses:
        return
    
    print()
    license_id = input("أدخل رقم الترخيص لعرض التفاصيل - Enter License ID for details: ").strip()
    
    try:
        license_id = int(license_id)
    except ValueError:
        print("❌ رقم غير صحيح!")
        return
    
    info = LicenseManager.get_license_info(license_id)
    if not info:
        print(f"❌ الترخيص #{license_id} غير موجود")
        return
    
    lic = info['license']
    
    print()
    print("=" * 70)
    print(f"📋 تفاصيل الترخيص #{lic.id}")
    print("=" * 70)
    print(f"🔑 المفتاح: {lic.license_key}")
    print(f"👤 العميل: {lic.client_name}")
    if lic.client_company:
        print(f"🏢 الشركة: {lic.client_company}")
    if lic.client_email:
        print(f"📧 البريد: {lic.client_email}")
    if lic.client_phone:
        print(f"📱 الهاتف: {lic.client_phone}")
    print(f"📦 النوع: {lic.license_type}")
    print(f"👥 عدد المستخدمين: {lic.max_users}")
    print(f"🏪 عدد الفروع: {lic.max_branches}")
    print(f"✅ نشط: {'نعم' if lic.is_active else 'لا'}")
    print(f"⏸️  معلق: {'نعم' if lic.is_suspended else 'لا'}")
    if lic.is_suspended:
        print(f"   السبب: {lic.suspension_reason}")
    print(f"📅 تاريخ الإنشاء: {lic.created_at.strftime('%Y-%m-%d %H:%M')}")
    if lic.expires_at:
        print(f"📅 تاريخ الانتهاء: {lic.expires_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"⏰ الأيام المتبقية: {info['days_remaining']}")
    else:
        print(f"📅 الترخيص: دائم")
    if lic.last_check:
        print(f"🔍 آخر فحص: {lic.last_check.strftime('%Y-%m-%d %H:%M')}")
    print(f"📊 عدد الفحوصات: {info['checks_count']}")
    print(f"🔐 اسم المستخدم: {lic.admin_username}")
    if lic.notes:
        print(f"📝 ملاحظات: {lic.notes}")
    print("=" * 70)

def main_menu():
    """Main menu"""
    app = create_app()
    
    with app.app_context():
        while True:
            print()
            print("=" * 70)
            print("🔐 إدارة التراخيص - License Management")
            print("=" * 70)
            print("1. عرض جميع التراخيص - Show All Licenses")
            print("2. عرض تفاصيل ترخيص - View License Details")
            print("3. تعليق ترخيص - Suspend License")
            print("4. إلغاء تعليق ترخيص - Unsuspend License")
            print("5. إلغاء ترخيص نهائياً - Deactivate License")
            print("6. تمديد ترخيص - Extend License")
            print("0. خروج - Exit")
            print("=" * 70)
            
            choice = input("اختر (0-6): ").strip()
            
            if choice == '1':
                show_all_licenses()
            elif choice == '2':
                view_license_details()
            elif choice == '3':
                suspend_license()
            elif choice == '4':
                unsuspend_license()
            elif choice == '5':
                deactivate_license()
            elif choice == '6':
                extend_license()
            elif choice == '0':
                print("👋 وداعاً!")
                break
            else:
                print("❌ اختيار غير صحيح!")

if __name__ == '__main__':
    main_menu()


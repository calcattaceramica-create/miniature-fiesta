#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Add License Tables to Database
إضافة جداول التراخيص إلى قاعدة البيانات
"""
from app import create_app, db
from app.models_license import License, LicenseCheck

def add_license_tables():
    """Add license tables to existing database"""
    print("=" * 70)
    print("🔧 إضافة جداول التراخيص - Adding License Tables")
    print("=" * 70)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create license tables
            print("📊 إنشاء جداول التراخيص...")
            db.create_all()
            
            print("✅ تم إنشاء الجداول بنجاح!")
            print()
            print("الجداول المضافة:")
            print("  - licenses (جدول التراخيص)")
            print("  - license_checks (جدول فحوصات التراخيص)")
            print()
            print("=" * 70)
            print("✅ اكتمل التحديث بنجاح!")
            print("=" * 70)
            print()
            print("الخطوات التالية:")
            print("1. قم بإنشاء ترخيص جديد باستخدام: python create_client_license.py")
            print("2. قم بإدارة التراخيص باستخدام: python manage_licenses.py")
            print("3. لتفعيل فحص الترخيص، قم بإلغاء التعليق في app/__init__.py")
            print()
            
        except Exception as e:
            print(f"❌ خطأ: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    add_license_tables()


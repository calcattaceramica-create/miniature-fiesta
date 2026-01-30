#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
تفعيل ترخيص مدى الحياة
Activate Lifetime License
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models_license import License
from datetime import datetime

def activate_lifetime_license():
    """تفعيل ترخيص مدى الحياة"""
    
    app = create_app('development')
    
    with app.app_context():
        # البحث عن الترخيص بالمفتاح
        license_key = "9813-26D0-F98D-741C"
        
        print("=" * 70)
        print("🔍 البحث عن الترخيص...")
        print(f"   المفتاح: {license_key}")
        print("=" * 70)
        
        license = License.query.filter_by(license_key=license_key).first()
        
        if not license:
            print("❌ الترخيص غير موجود!")
            print("\n💡 جاري إنشاء ترخيص جديد مدى الحياة...")
            
            # إنشاء ترخيص جديد مدى الحياة
            from app.license_manager import LicenseManager
            
            license = LicenseManager.create_license(
                client_name="DED ERP System",
                client_email="admin@ded-erp.com",
                client_phone="+966-XXX-XXXX",
                client_company="DED Company",
                license_type="lifetime",
                max_users=999,
                max_branches=999,
                duration_days=None,  # مدى الحياة
                admin_username="admin",
                admin_password="admin123",
                notes="Lifetime License - Full Access"
            )
            
            # تحديث المفتاح إلى المفتاح المطلوب
            license.license_key = license_key
            license.license_hash = License.hash_license_key(license_key)
            db.session.commit()
            
            print("✅ تم إنشاء الترخيص بنجاح!")
        
        # تفعيل الترخيص
        print("\n🔄 جاري تفعيل الترخيص...")
        
        # إلغاء تفعيل جميع التراخيص الأخرى
        License.query.filter(License.id != license.id).update({
            'is_active': False
        })
        
        # تفعيل هذا الترخيص
        license.is_active = True
        license.is_suspended = False
        license.activated_at = datetime.utcnow()
        license.expires_at = None  # مدى الحياة
        license.license_type = "lifetime"
        license.max_users = 999
        license.max_branches = 999
        
        db.session.commit()
        
        print("\n" + "=" * 70)
        print("✅ تم تفعيل الترخيص بنجاح!")
        print("=" * 70)
        print(f"\n🔑 مفتاح الترخيص: {license.license_key}")
        print(f"👤 العميل: {license.client_name}")
        print(f"🏢 الشركة: {license.client_company}")
        print(f"📧 البريد: {license.client_email}")
        print(f"📞 الهاتف: {license.client_phone}")
        print(f"📊 النوع: {license.license_type.upper()}")
        print(f"👥 الحد الأقصى للمستخدمين: {license.max_users}")
        print(f"🏪 الحد الأقصى للفروع: {license.max_branches}")
        print(f"📅 تاريخ التفعيل: {license.activated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏰ تاريخ الانتهاء: {'مدى الحياة ∞' if not license.expires_at else license.expires_at.strftime('%Y-%m-%d')}")
        print(f"✅ الحالة: {'نشط' if license.is_active else 'غير نشط'}")
        print(f"⏸️ موقوف: {'نعم' if license.is_suspended else 'لا'}")
        print("\n" + "=" * 70)
        print("🎉 الترخيص جاهز للاستخدام!")
        print("=" * 70)
        
        return license

if __name__ == '__main__':
    try:
        activate_lifetime_license()
        print("\n✅ تم التفعيل بنجاح!")
        print("\n🚀 يمكنك الآن تشغيل النظام:")
        print("   python start.py")
        print("\n🌐 ثم افتح المتصفح على:")
        print("   http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ حدث خطأ: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


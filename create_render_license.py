#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
إنشاء ترخيص مدى الحياة على Render
Create Lifetime License on Render
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models_license import License
from datetime import datetime

def create_lifetime_license():
    """إنشاء ترخيص مدى الحياة"""
    
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("🔑 إنشاء ترخيص مدى الحياة")
        print("=" * 70)
        
        # Check if license already exists
        existing_license = License.query.filter_by(license_key="9813-26D0-F98D-741C").first()
        
        if existing_license:
            print("\n✅ الترخيص موجود بالفعل!")
            print(f"   المفتاح: {existing_license.license_key}")
            print(f"   العميل: {existing_license.client_name}")
            print(f"   الحالة: {'مفعّل' if existing_license.is_active else 'غير مفعّل'}")
            
            # Update to make sure it's active
            existing_license.is_active = True
            existing_license.is_suspended = False
            existing_license.license_type = 'lifetime'
            existing_license.max_users = 999
            existing_license.max_branches = 999
            existing_license.expires_at = None
            
            db.session.commit()
            print("\n✅ تم تحديث الترخيص بنجاح!")
            
        else:
            print("\n📝 إنشاء ترخيص جديد...")
            
            # Create new license
            license = License(
                license_key="9813-26D0-F98D-741C",
                license_hash=License.hash_license_key("9813-26D0-F98D-741C"),
                client_name="DED ERP System",
                client_email="admin@ded-erp.com",
                client_phone="+966-XXX-XXXX",
                client_company="DED Company",
                license_type="lifetime",
                max_users=999,
                max_branches=999,
                is_active=True,
                is_suspended=False,
                created_at=datetime.utcnow(),
                activated_at=datetime.utcnow(),
                expires_at=None,  # Lifetime
                admin_username="admin",
                notes="Lifetime License - Full Access - Created on Render"
            )
            
            db.session.add(license)
            db.session.commit()
            
            print("\n✅ تم إنشاء الترخيص بنجاح!")
            print(f"   المفتاح: {license.license_key}")
            print(f"   العميل: {license.client_name}")
            print(f"   النوع: {license.license_type}")
            print(f"   الحد الأقصى للمستخدمين: {license.max_users}")
            print(f"   الحد الأقصى للفروع: {license.max_branches}")
        
        print("\n" + "=" * 70)
        print("✅ العملية اكتملت بنجاح!")
        print("=" * 70)
        print("\n📝 يمكنك الآن استخدام مفتاح الترخيص:")
        print("   9813-26D0-F98D-741C")
        print("\n🌐 على الرابط:")
        print("   https://ded-inventory-system.onrender.com/license-activation")
        print("=" * 70)

if __name__ == '__main__':
    create_lifetime_license()


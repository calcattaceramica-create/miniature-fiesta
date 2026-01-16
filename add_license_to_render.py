#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Add License Tables to Render Database
إضافة جداول التراخيص إلى قاعدة بيانات Render
"""

import os
import sys

# Set environment to production
os.environ['FLASK_ENV'] = 'production'

print("=" * 80)
print("🔧 ADDING LICENSE TABLES TO RENDER DATABASE")
print("=" * 80)

from app import create_app, db
from app.models_license import License, LicenseCheck
from app.license_manager import LicenseManager
from datetime import datetime, timedelta

app = create_app('production')

with app.app_context():
    try:
        print("\n1️⃣ Creating license tables...")
        
        # Create tables
        db.create_all()
        
        print("   ✅ Tables created successfully!")
        
        # Check if license already exists
        existing_license = License.query.first()
        
        if existing_license:
            print(f"\n2️⃣ License already exists:")
            print(f"   License Key: {existing_license.license_key}")
            print(f"   Client: {existing_license.client_name}")
            print(f"   Type: {existing_license.license_type}")
            
            is_valid, message = existing_license.is_valid()
            print(f"   Status: {message}")
            
            if existing_license.expires_at:
                days_remaining = existing_license.days_remaining()
                print(f"   Expires: {existing_license.expires_at.strftime('%Y-%m-%d')} ({days_remaining} days)")
            else:
                print(f"   Expires: Lifetime")
        else:
            print("\n2️⃣ Creating trial license...")
            
            # Create trial license
            license = LicenseManager.create_license(
                client_name='DED ERP System',
                admin_username='admin',
                admin_password='admin123',
                license_type='trial',
                duration_days=365,  # 1 year trial
                max_users=10,
                max_branches=5,
                client_email='admin@ded.com',
                client_company='DED ERP',
                notes='Auto-generated trial license for Render deployment'
            )
            
            print(f"   ✅ License created successfully!")
            print(f"   License Key: {license.license_key}")
            print(f"   Valid for: 365 days")
        
        print("\n" + "=" * 80)
        print("✅ SUCCESS! License system is ready on Render!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


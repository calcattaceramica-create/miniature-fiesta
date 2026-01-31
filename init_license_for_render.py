#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialize License for Render Deployment
إنشاء الترخيص لنشر Render
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models_license import License
from datetime import datetime

def init_license():
    """إنشاء الترخيص الأساسي"""
    
    # Use production config for Render
    app = create_app('production')
    
    with app.app_context():
        print("=" * 70)
        print("🚀 Initializing License for Render Deployment")
        print("=" * 70)
        print()
        
        # Check if license already exists
        license_key = "9813-26D0-F98D-741C"
        
        print(f"🔍 Checking for license: {license_key}")
        license = License.query.filter_by(license_key=license_key).first()
        
        if license:
            print(f"✅ License already exists!")
            print(f"   Client: {license.client_name}")
            print(f"   Type: {license.license_type}")
            print(f"   Active: {license.is_active}")
            return
        
        print("💡 Creating new lifetime license...")
        print()
        
        # Create new license directly
        license = License(
            license_key=license_key,
            license_hash=License.hash_license_key(license_key),
            client_name='DED ERP System',
            client_company='DED Company',
            client_email='admin@ded-erp.com',
            client_phone='+966-XXX-XXXX',
            license_type='lifetime',
            max_users=999,
            max_branches=999,
            is_active=True,
            is_suspended=False,
            activated_at=datetime.utcnow(),
            expires_at=None,  # Lifetime license
            admin_username='admin',
            notes='Lifetime License - Render Deployment'
        )
        
        # Set admin password
        from werkzeug.security import generate_password_hash
        license.admin_password_hash = generate_password_hash('admin123')
        
        db.session.add(license)
        db.session.commit()
        
        print("✅ License created successfully!")
        print()
        print("=" * 70)
        print("📋 License Details:")
        print("=" * 70)
        print(f"🔑 License Key: {license.license_key}")
        print(f"👤 Client: {license.client_name}")
        print(f"🏢 Company: {license.client_company}")
        print(f"📊 Type: {license.license_type.upper()}")
        print(f"👥 Max Users: {license.max_users}")
        print(f"🏪 Max Branches: {license.max_branches}")
        print(f"✅ Active: {license.is_active}")
        print()
        print("=" * 70)
        print("🎉 Ready to use!")
        print("=" * 70)
        print()
        print("📝 Login Credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print()

if __name__ == "__main__":
    init_license()


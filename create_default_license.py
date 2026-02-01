#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create Default License - Emergency Script
إنشاء الترخيص الافتراضي - سكريبت طوارئ
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app, db
from app.models_license import License

def create_default_license():
    """Create the default production license"""
    
    print("=" * 70)
    print("🔧 Creating Default Production License")
    print("=" * 70)
    print()
    
    app = create_app()
    
    with app.app_context():
        try:
            default_license_key = "RENDER-2026-PROD-LIVE"
            
            # Check if license already exists
            existing_license = License.query.filter_by(license_key=default_license_key).first()
            
            if existing_license:
                print(f"✅ License already exists: {default_license_key}")
                print(f"   Status: {'Active' if existing_license.is_active else 'Inactive'}")
                print(f"   Suspended: {'Yes' if existing_license.is_suspended else 'No'}")
                print()
                
                # Update if needed
                if not existing_license.is_active or existing_license.is_suspended:
                    print("🔧 Updating license status...")
                    existing_license.is_active = True
                    existing_license.is_suspended = False
                    existing_license.activated_at = datetime.utcnow()
                    db.session.commit()
                    print("✅ License updated successfully!")
                
            else:
                print("Creating new license...")
                license = License(
                    license_key=default_license_key,
                    license_hash=hashlib.sha256(default_license_key.encode()).hexdigest(),
                    client_name="DED ERP System - Production",
                    client_email="admin@ded-erp.com",
                    client_company="DED Company",
                    license_type="lifetime",
                    max_users=100,
                    max_branches=10,
                    is_active=True,
                    is_suspended=False,
                    created_at=datetime.utcnow(),
                    activated_at=datetime.utcnow(),
                    expires_at=None,  # Lifetime
                    admin_username="admin",
                    admin_password_hash=generate_password_hash("admin123"),
                    notes="Production license for Render deployment"
                )
                
                db.session.add(license)
                db.session.commit()
                
                print("=" * 70)
                print("✅ License Created Successfully!")
                print("=" * 70)
            
            print()
            print("📋 License Details:")
            print(f"   🔑 License Key: {default_license_key}")
            print(f"   👤 Username: admin")
            print(f"   🔒 Password: admin123")
            print(f"   📅 Type: Lifetime")
            print(f"   👥 Max Users: 100")
            print(f"   🏢 Max Branches: 10")
            print("=" * 70)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = create_default_license()
    sys.exit(0 if success else 1)


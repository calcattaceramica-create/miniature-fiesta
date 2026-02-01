#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create Licenses for Render Deployment
إنشاء التراخيص لنشر Render
"""
import sys
import os
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app, db
from app.models_license import License
from app.models import User, Role, Branch
from werkzeug.security import generate_password_hash

def create_licenses():
    """Create all licenses for Render"""
    
    print("=" * 80)
    print("🚀 Creating Licenses for Render")
    print("=" * 80)
    print()
    
    app = create_app()
    
    with app.app_context():
        try:
            # License data
            licenses_data = [
                {
                    'license_key': '9813-26D0-F98D-741C',
                    'client_name': 'DED ERP System',
                    'client_company': 'DED Company',
                    'client_email': 'admin@ded-erp.com',
                    'client_phone': '+966-XXX-XXXX',
                    'license_type': 'lifetime',
                    'max_users': 999,
                    'max_branches': 999,
                },
                {
                    'license_key': 'CE9B-0DD8-90B7-B59B',
                    'client_name': 'mohamed',
                    'client_company': 'calcatta bahtrooms and tile',
                    'client_email': 'calcatta.ceramica@gmail.com',
                    'client_phone': '99000142',
                    'license_type': 'lifetime',
                    'max_users': 20,
                    'max_branches': 5,
                },
                {
                    'license_key': 'B31B-B06A-202A-5298',
                    'client_name': 'mohamed',
                    'client_company': 'calca',
                    'client_email': 'calca@g',
                    'client_phone': '99000140',
                    'license_type': 'lifetime',
                    'max_users': 99,
                    'max_branches': 5,
                }
            ]
            
            for lic_data in licenses_data:
                # Check if license already exists
                existing = License.query.filter_by(license_key=lic_data['license_key']).first()
                
                if existing:
                    print(f"⚠️  License {lic_data['license_key']} already exists - skipping")
                    continue
                
                # Create license
                license = License(
                    license_key=lic_data['license_key'],
                    client_name=lic_data['client_name'],
                    client_company=lic_data['client_company'],
                    client_email=lic_data['client_email'],
                    client_phone=lic_data['client_phone'],
                    license_type=lic_data['license_type'],
                    max_users=lic_data['max_users'],
                    max_branches=lic_data['max_branches'],
                    is_active=True,
                    is_suspended=False,
                    admin_username='admin',
                    admin_password_hash=generate_password_hash('admin123'),
                    activated_at=datetime.utcnow()
                )
                
                db.session.add(license)
                print(f"✅ Created license: {lic_data['license_key']}")
            
            db.session.commit()
            
            print()
            print("=" * 80)
            print("✅ All licenses created successfully!")
            print("=" * 80)
            print()
            print("📝 You can now login with:")
            print("   License Key: 9813-26D0-F98D-741C (or any other)")
            print("   Username: admin")
            print("   Password: admin123")
            print()
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = create_licenses()
    sys.exit(0 if success else 1)


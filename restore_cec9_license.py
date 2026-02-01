#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Restore CEC9 License
استعادة ترخيص CEC9
"""
import sys
import os
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app, db
from app.models_license import License
from werkzeug.security import generate_password_hash
import hashlib

def restore_license():
    """Restore CEC9 license"""
    
    print("=" * 80)
    print("🔄 Restoring License: CEC9-79EE-C42F-2DAD")
    print("=" * 80)
    print()
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if license already exists
            existing = License.query.filter_by(license_key='CEC9-79EE-C42F-2DAD').first()
            
            if existing:
                print(f"⚠️  License already exists!")
                print(f"   Client: {existing.client_name}")
                print(f"   Active: {existing.is_active}")
                return True
            
            # Generate license hash
            license_key = 'CEC9-79EE-C42F-2DAD'
            license_hash = hashlib.sha256(license_key.encode()).hexdigest()

            # Create license
            license = License(
                license_key=license_key,
                license_hash=license_hash,
                client_name='mohamed',
                client_company='calcatta ceramica',
                client_email='calcatta.ceramica@gmail.com',
                client_phone='99000142',
                license_type='lifetime',
                max_users=20,
                max_branches=5,
                is_active=True,
                is_suspended=False,
                admin_username='admin',
                admin_password_hash=generate_password_hash('admin123'),
                activated_at=datetime.utcnow()
            )
            
            db.session.add(license)
            db.session.commit()
            
            print("✅ License restored successfully!")
            print()
            print(f"🔑 License Key: CEC9-79EE-C42F-2DAD")
            print(f"👤 Username: admin")
            print(f"🔒 Password: admin123")
            print()
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = restore_license()
    sys.exit(0 if success else 1)


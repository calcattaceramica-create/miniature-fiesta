#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fix Admin Password and License ID
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User
from app.models_license import License
from app.tenant_manager import TenantManager

def fix_admin_password():
    """Fix admin password and license ID"""
    
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    print("=" * 80)
    print("🔧 Fixing Admin Password and License ID")
    print("=" * 80)
    print()
    
    # Create app
    app = create_app()
    
    # Step 1: Get license ID from master database
    with app.app_context():
        master_db_uri = f'sqlite:///{TenantManager.get_master_db_path()}'
        app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri
        db.engine.dispose()
        
        print(f"📋 Getting license from master database...")
        license = License.query.filter_by(license_key=license_key).first()
        
        if not license:
            print(f"❌ License not found!")
            return
        
        license_id = license.id
        print(f"✅ License ID: {license_id}")
        print()
    
    # Step 2: Fix users in tenant database
    with app.app_context():
        # Switch to tenant database
        tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
        app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
        db.engine.dispose()
        
        print(f"📋 Fixing users in tenant database...")
        print()
        
        # Get all users
        users = User.query.all()
        
        for user in users:
            print(f"👤 User: {user.username}")
            
            # Fix license_id
            if user.license_id != license_id:
                user.license_id = license_id
                print(f"   ✅ Updated license_id to {license_id}")
            
            # Fix admin password
            if user.username == 'admin':
                user.set_password('admin123')
                print(f"   ✅ Reset password to 'admin123'")
                
                # Test password
                if user.check_password('admin123'):
                    print(f"   ✅ Password verification successful!")
                else:
                    print(f"   ❌ Password verification failed!")
        
        db.session.commit()
        
        print()
        print("=" * 80)
        print("✅ All users fixed!")
        print("=" * 80)
        print()
        
        # Show all users
        print("📋 Updated Users:")
        users = User.query.all()
        
        for user in users:
            print(f"\n   👤 {user.username}")
            print(f"      Full Name: {user.full_name}")
            print(f"      Email: {user.email}")
            print(f"      Active: {user.is_active}")
            print(f"      Role ID: {user.role_id}")
            print(f"      License ID: {user.license_id}")

if __name__ == '__main__':
    fix_admin_password()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create License: CEC9-79EE-C42F-2DAD
This script creates the license and sets up the tenant database
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app, db
from app.models_license import License
from app.models import User, Role, Branch, Permission
from app.tenant_manager import TenantManager
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import hashlib

def create_license_and_setup():
    """Create license CEC9-79EE-C42F-2DAD and setup tenant database"""
    
    app = create_app()
    
    with app.app_context():
        try:
            # Step 1: Switch to master database
            print("=" * 60)
            print("🔧 Step 1: Connecting to Master Database")
            print("=" * 60)
            
            master_db_path = TenantManager.get_master_db_path()
            master_db_uri = f'sqlite:///{master_db_path}'
            app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri
            
            # Dispose old engine
            if hasattr(db, 'engine'):
                db.engine.dispose()
            if hasattr(db, '_engine'):
                db._engine = None
            
            print(f"✅ Connected to master database: {master_db_path}")
            
            # Step 2: Check if license already exists
            print("\n" + "=" * 60)
            print("🔍 Step 2: Checking if License Exists")
            print("=" * 60)
            
            license_key = "CEC9-79EE-C42F-2DAD"
            existing_license = License.query.filter_by(license_key=license_key).first()
            
            if existing_license:
                print(f"⚠️  License {license_key} already exists!")
                print(f"   Client: {existing_license.client_name}")
                print(f"   Type: {existing_license.license_type}")
                print(f"   Active: {existing_license.is_active}")
                print(f"   Suspended: {existing_license.is_suspended}")
                
                # Update license to be active
                existing_license.is_active = True
                existing_license.is_suspended = False
                existing_license.suspension_reason = None
                db.session.commit()
                print("✅ License reactivated!")
                license = existing_license
            else:
                # Step 3: Create new license
                print("\n" + "=" * 60)
                print("🆕 Step 3: Creating New License")
                print("=" * 60)
                
                license = License(
                    license_key=license_key,
                    license_hash=hashlib.sha256(license_key.encode()).hexdigest(),
                    client_name="DED System",
                    client_email="admin@ded.local",
                    client_phone="",
                    client_company="DED Company",
                    license_type="lifetime",
                    max_users=999,
                    max_branches=999,
                    is_active=True,
                    is_suspended=False,
                    created_at=datetime.utcnow(),
                    activated_at=datetime.utcnow(),
                    expires_at=None,  # Lifetime license
                    admin_username="admin",
                    admin_password_hash=generate_password_hash("admin"),
                    notes="Lifetime license for DED System"
                )
                
                db.session.add(license)
                db.session.commit()
                
                print(f"✅ License created successfully!")
                print(f"   License Key: {license_key}")
                print(f"   Type: lifetime")
                print(f"   Max Users: 999")
                print(f"   Max Branches: 999")
            
            # Step 4: Create tenant database
            print("\n" + "=" * 60)
            print("🗄️  Step 4: Creating Tenant Database")
            print("=" * 60)
            
            tenant_db_path = TenantManager.get_tenant_db_path(license_key)
            
            if os.path.exists(tenant_db_path):
                print(f"⚠️  Tenant database already exists: {tenant_db_path}")
                print("   Skipping database creation...")
            else:
                # Switch to tenant database
                tenant_db_uri = f'sqlite:///{tenant_db_path}'
                app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
                
                # Dispose old engine
                if hasattr(db, 'engine'):
                    db.engine.dispose()
                if hasattr(db, '_engine'):
                    db._engine = None
                
                # Create all tables
                db.create_all()
                
                print(f"✅ Tenant database created: {tenant_db_path}")
                
                # Step 5: Create admin user in tenant database
                print("\n" + "=" * 60)
                print("👤 Step 5: Creating Admin User")
                print("=" * 60)
                
                # Create System Administrator role
                admin_role = Role(
                    name='System Administrator',
                    name_ar='مدير النظام',
                    description='Full system access',
                    description_ar='صلاحيات كاملة للنظام'
                )
                db.session.add(admin_role)
                db.session.flush()
                
                # Create main branch
                main_branch = Branch(
                    name='Main Branch',
                    name_ar='الفرع الرئيسي',
                    code='MAIN',
                    is_active=True
                )
                db.session.add(main_branch)
                db.session.flush()
                
                # Create admin user
                admin_user = User(
                    username='admin',
                    email='admin@ded.local',
                    full_name='System Administrator',
                    password_hash=generate_password_hash('admin'),
                    role_id=admin_role.id,
                    branch_id=main_branch.id,
                    is_admin=True,
                    is_active=True,
                    language='ar'
                )
                db.session.add(admin_user)
                db.session.commit()
                
                print(f"✅ Admin user created!")
                print(f"   Username: admin")
                print(f"   Password: admin")
                print(f"   Role: System Administrator")
                print(f"   Branch: Main Branch")
            
            # Final Summary
            print("\n" + "=" * 60)
            print("✅ SETUP COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"License Key: {license_key}")
            print(f"Username: admin")
            print(f"Password: admin")
            print(f"Database: {tenant_db_path}")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = create_license_and_setup()
    sys.exit(0 if success else 1)


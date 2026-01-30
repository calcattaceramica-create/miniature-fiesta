#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fix Admin Role - إصلاح دور المدير
Creates admin role in tenant database
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Role, User
from app.models_license import License
from app.tenant_manager import TenantManager
from werkzeug.security import generate_password_hash

def fix_admin_role():
    """Create admin role and user in tenant database"""

    app = create_app()

    # License key to use
    license_key = 'CEC9-79EE-C42F-2DAD'

    print("=" * 70)
    print("🔧 إصلاح دور المدير - Fixing Admin Role")
    print("=" * 70)
    print()

    with app.app_context():
        # Step 1: Get license from master database
        print("📋 Step 1: Getting license from master database...")

        license = License.query.filter_by(license_key=license_key).first()

        if not license:
            print(f"❌ License not found: {license_key}")
            return

        print(f"✅ Found license: {license.client_name}")
        print()

        # Step 2: Switch to tenant database
        print("📋 Step 2: Switching to tenant database...")
        tenant_db_path = TenantManager.get_tenant_db_path(license_key)
        tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)

        if not os.path.exists(tenant_db_path):
            print(f"❌ Tenant database not found: {tenant_db_path}")
            print("   Creating tenant database...")
            TenantManager.create_tenant_database(license_key, app)

        app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
        db.engine.dispose()

        print(f"✅ Switched to: {tenant_db_uri}")
        print()
        
        # Step 3: Check if admin role exists
        print("📋 Step 3: Checking admin role...")
        admin_role = Role.query.filter_by(name='admin').first()

        if admin_role:
            print(f"✅ Admin role already exists: {admin_role.name}")
        else:
            print("⚠️  Admin role not found. Creating...")
            admin_role = Role(
                name='admin',
                name_ar='مدير النظام',
                description='System Administrator with full access'
            )
            db.session.add(admin_role)
            db.session.commit()
            print("✅ Admin role created successfully!")

        print()

        # Step 4: Check other roles
        print("📋 Step 4: Checking other roles...")

        roles_to_create = [
            {
                'name': 'manager',
                'name_ar': 'مدير',
                'description': 'Manager with elevated privileges'
            },
            {
                'name': 'employee',
                'name_ar': 'موظف',
                'description': 'Regular employee'
            },
            {
                'name': 'viewer',
                'name_ar': 'مشاهد',
                'description': 'View-only access'
            }
        ]

        for role_data in roles_to_create:
            role = Role.query.filter_by(name=role_data['name']).first()
            if not role:
                role = Role(**role_data)
                db.session.add(role)
                print(f"   ✅ Created role: {role_data['name_ar']}")
            else:
                print(f"   ℹ️  Role exists: {role_data['name_ar']}")

        db.session.commit()
        print()
        
        # Step 5: Check admin user
        print("📋 Step 5: Checking admin user...")
        admin_user = User.query.filter_by(username='admin').first()
        
        if admin_user:
            print(f"✅ Admin user exists: {admin_user.username}")

            # Make sure admin has admin role
            if admin_user.role_id != admin_role.id:
                admin_user.role_id = admin_role.id
                db.session.commit()
                print("   ✅ Updated admin user role")

            # Update password to admin123
            admin_user.password_hash = generate_password_hash('admin123')
            admin_user.is_active = True
            db.session.commit()
            print("   ✅ Updated admin password to: admin123")
        else:
            print("⚠️  Admin user not found. Creating...")
            admin_user = User(
                username='admin',
                email='admin@ded.local',
                full_name='System Administrator',
                password_hash=generate_password_hash('admin123'),
                is_active=True,
                language='ar',
                role_id=admin_role.id  # Assign role_id directly
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Admin user created successfully!")
            print("   Username: admin")
            print("   Password: admin123")
        
        print()
        print("=" * 70)
        print("✅ تم إصلاح دور المدير بنجاح!")
        print("✅ Admin role fixed successfully!")
        print("=" * 70)
        print()
        print("📝 Login credentials:")
        print(f"   License Key: {license_key}")
        print("   Username: admin")
        print("   Password: admin123")
        print()

if __name__ == '__main__':
    fix_admin_role()


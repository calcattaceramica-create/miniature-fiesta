#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Add Sales Cancel Permission
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Permission, Role
from app.tenant_manager import TenantManager

def add_permission():
    """Add sales.cancel permission"""
    
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    print("=" * 80)
    print("➕ Adding Sales Cancel Permission")
    print("=" * 80)
    print()
    
    # Create app
    app = create_app()
    
    with app.app_context():
        # Switch to tenant database
        tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
        app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
        db.engine.dispose()
        
        print(f"✅ Connected to: {tenant_db_uri}")
        print()
        
        # Check if permission already exists
        perm = Permission.query.filter_by(name='sales.cancel').first()
        
        if perm:
            print(f"⚠️  Permission 'sales.cancel' already exists!")
            print(f"   ID: {perm.id}")
            print(f"   Name: {perm.name}")
            print(f"   Arabic: {perm.name_ar}")
        else:
            # Create new permission
            new_perm = Permission(
                name='sales.cancel',
                name_ar='إلغاء فاتورة مبيعات',
                module='sales'
            )
            db.session.add(new_perm)
            db.session.commit()
            
            print(f"✅ Created permission 'sales.cancel'")
            print(f"   ID: {new_perm.id}")
            print(f"   Name: {new_perm.name}")
            print(f"   Arabic: {new_perm.name_ar}")
            
            # Add to admin role
            admin_role = Role.query.filter_by(name='admin').first()
            
            if admin_role:
                admin_role.permissions.append(new_perm)
                db.session.commit()
                print(f"✅ Added permission to admin role")
                print(f"   Admin now has {len(admin_role.permissions)} permissions")
            else:
                print(f"⚠️  Admin role not found!")
        
        print()
        print("=" * 80)
        print("✅ Complete!")
        print("=" * 80)

if __name__ == '__main__':
    add_permission()


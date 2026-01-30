#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check Admin POS Permissions
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Role, Permission
from app.tenant_manager import TenantManager

def check_permissions():
    """Check admin user POS permissions"""
    
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    print("=" * 80)
    print("🔍 Checking Admin POS Permissions")
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
        
        # Get admin user
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("❌ Admin user not found!")
            return
        
        print(f"👤 User: {admin.username} ({admin.full_name})")
        print(f"   Role ID: {admin.role_id}")
        print()
        
        # Get role
        if admin.role:
            print(f"🔐 Role: {admin.role.name} ({admin.role.name_ar})")
            print(f"   Permissions: {len(admin.role.permissions)}")
            print()
            
            # Check POS permissions
            print("📋 POS Permissions:")
            pos_perms = [p for p in admin.role.permissions if 'pos' in p.name.lower()]
            
            if pos_perms:
                for perm in pos_perms:
                    print(f"   ✅ {perm.name} - {perm.name_ar}")
            else:
                print("   ❌ No POS permissions found!")
            print()
            
            # Check all permissions
            print("📋 All Permissions:")
            for perm in admin.role.permissions[:10]:
                print(f"   - {perm.name} ({perm.module})")
            
            if len(admin.role.permissions) > 10:
                print(f"   ... and {len(admin.role.permissions) - 10} more")
        else:
            print("❌ User has no role!")
        
        print()
        print("=" * 80)
        print("✅ Check Complete!")
        print("=" * 80)

if __name__ == '__main__':
    check_permissions()


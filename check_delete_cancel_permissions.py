#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check Delete and Cancel Permissions
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Permission, Role
from app.tenant_manager import TenantManager

def check_permissions():
    """Check delete and cancel permissions"""
    
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    print("=" * 80)
    print("🔍 Checking Delete and Cancel Permissions")
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
        
        # Check required permissions
        required_permissions = [
            'sales.delete',
            'sales.cancel',
            'purchases.delete',
            'purchases.cancel'
        ]
        
        print("📋 Required Permissions:")
        for perm_name in required_permissions:
            perm = Permission.query.filter_by(name=perm_name).first()
            if perm:
                print(f"   ✅ {perm_name} - {perm.name_ar}")
            else:
                print(f"   ❌ {perm_name} - NOT FOUND!")
        
        print()
        
        # Check admin role permissions
        admin_role = Role.query.filter_by(name='admin').first()
        
        if admin_role:
            print(f"📋 Admin Role Permissions:")
            print(f"   Total: {len(admin_role.permissions)}")
            
            # Check if admin has delete/cancel permissions
            for perm_name in required_permissions:
                has_perm = any(p.name == perm_name for p in admin_role.permissions)
                if has_perm:
                    print(f"   ✅ {perm_name}")
                else:
                    print(f"   ❌ {perm_name} - MISSING!")
        
        print()
        print("=" * 80)
        print("✅ Check Complete!")
        print("=" * 80)

if __name__ == '__main__':
    check_permissions()


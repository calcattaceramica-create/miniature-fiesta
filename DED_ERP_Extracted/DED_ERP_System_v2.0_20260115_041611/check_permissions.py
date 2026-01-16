#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
فحص صلاحيات المستخدم
"""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User, Role, Permission

def check_permissions():
    """Check user permissions"""
    print("\n" + "=" * 80)
    print("🔐 Checking User Permissions")
    print("=" * 80)
    
    app = create_app()
    
    with app.app_context():
        # Get admin user
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("\n❌ Admin user not found!")
            return
        
        print(f"\n👤 User: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Active: {admin.is_active}")
        print(f"   Admin: {admin.is_admin}")
        
        # Get user role
        if admin.role:
            print(f"\n📋 Role: {admin.role.name}")
            print(f"   Permissions: {len(admin.role.permissions) if admin.role.permissions else 0}")
        else:
            print(f"\n📋 No role assigned")

        # Check specific permission
        permission_code = 'inventory.products.delete'
        print(f"\n🔍 Checking permission: {permission_code}")

        # Check if user has permission
        has_permission = False

        if admin.is_admin:
            print(f"   ✅ User is admin - has all permissions")
            has_permission = True
        else:
            if admin.role and admin.role.permissions:
                for perm in admin.role.permissions:
                    if perm.name == permission_code or perm.module == 'inventory':
                        print(f"   ✅ Found permission: {perm.name}")
                        has_permission = True
                        break
        
        if not has_permission:
            print(f"   ❌ Permission NOT found!")

        # List all permissions
        print(f"\n📦 All Permissions:")
        all_perms = Permission.query.all()
        for perm in all_perms:
            print(f"   - {perm.name} (Module: {perm.module})")

def main():
    """Run the check"""
    print("\n" + "=" * 80)
    print("🚀 Permission Check")
    print("=" * 80)
    
    check_permissions()
    
    print("\n" + "=" * 80)
    print("✅ Check Completed!")
    print("=" * 80 + "\n")

if __name__ == '__main__':
    main()


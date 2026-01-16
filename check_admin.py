#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check admin user configuration
"""
from app import create_app
from app.models import User, Role, Permission

app = create_app()

with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        print("ERROR: Admin user not found!")
    else:
        print("=" * 70)
        print("Admin User Information:")
        print("=" * 70)
        print(f"ID: {admin.id}")
        print(f"Username: {admin.username}")
        print(f"is_admin: {admin.is_admin}")
        print(f"role_id: {admin.role_id}")
        print(f"role: {admin.role}")
        
        if admin.role:
            print(f"role.name: {admin.role.name}")
            print(f"permissions count: {len(admin.role.permissions)}")
            print("\nFirst 5 permissions:")
            for i, perm in enumerate(admin.role.permissions[:5]):
                print(f"  {i+1}. {perm.name}")
        else:
            print("\nWARNING: Admin has no role assigned!")
        
        print("\n" + "=" * 70)
        print("Testing has_permission():")
        print("=" * 70)
        
        test_permissions = [
            'inventory.products.view',
            'inventory.products.create',
            'inventory.transfer.view',
            'sales.invoices.view'
        ]
        
        for perm in test_permissions:
            result = admin.has_permission(perm)
            print(f"{perm}: {result}")
        
        print("=" * 70)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Grant Inventory Permissions to Admin User
"""

from app import db, create_app
from app.models import User, Role, Permission

app = create_app()

with app.app_context():
    try:
        # Get admin user (usually ID 1 or username 'admin')
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            # Try to get first user
            admin = User.query.first()
        
        if not admin:
            print("❌ No users found in database")
            exit(1)
        
        print(f"✅ Found user: {admin.username} (ID: {admin.id})")
        
        # Get or create admin role
        admin_role = Role.query.filter_by(name='Admin').first()
        
        if not admin_role:
            print("❌ Admin role not found. Creating it...")
            admin_role = Role(
                name='Admin',
                description='Administrator with full access'
            )
            db.session.add(admin_role)
            db.session.flush()
        
        # Assign admin role to user
        if admin.role_id != admin_role.id:
            admin.role_id = admin_role.id
            print(f"✅ Assigned Admin role to {admin.username}")

        # Also set is_admin flag
        if not admin.is_admin:
            admin.is_admin = True
            print(f"✅ Set is_admin flag for {admin.username}")
        
        # List of required permissions for inventory
        required_permissions = [
            'inventory.view',
            'inventory.products.view',
            'inventory.products.add',
            'inventory.products.edit',
            'inventory.products.delete',
            'inventory.categories.manage',
            'inventory.warehouses.view',
            'inventory.warehouses.manage',
            'inventory.stock.view',
            'inventory.stock.edit',
            'inventory.stock.delete',
            'inventory.stock.transfer',
        ]
        
        # Add permissions to admin role
        for perm_name in required_permissions:
            perm = Permission.query.filter_by(name=perm_name).first()
            
            if not perm:
                print(f"⚠️  Creating permission: {perm_name}")
                perm = Permission(
                    name=perm_name,
                    module='inventory'
                )
                db.session.add(perm)
                db.session.flush()
            
            if perm not in admin_role.permissions:
                admin_role.permissions.append(perm)
                print(f"✅ Added permission: {perm_name}")
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("✅ SUCCESS! Permissions granted successfully!")
        print("="*50)
        print(f"\nUser: {admin.username}")
        print(f"Role: {admin_role.name}")
        print(f"Total Permissions: {len(admin_role.permissions)}")
        print("\n✅ You can now access all inventory features including damaged inventory!")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


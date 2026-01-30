#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Grant supplier permissions to admin user
"""

from app import create_app, db
from app.models import User, Role, Permission

def grant_permissions():
    """Grant supplier permissions"""
    app = create_app()
    
    with app.app_context():
        # Get admin user
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("❌ Admin user not found")
            return
        
        print(f"✅ Found user: {admin.username} (ID: {admin.id})")
        
        # Get or create Admin role
        admin_role = Role.query.filter_by(name='Admin').first()
        
        if not admin_role:
            print("❌ Admin role not found. Creating it...")
            admin_role = Role(
                name='Admin',
                description='Administrator with full access'
            )
            db.session.add(admin_role)
            db.session.flush()
        
        # Assign role to admin
        admin.role_id = admin_role.id
        admin.is_admin = True
        db.session.flush()
        
        print(f"✅ Assigned Admin role to {admin.username}")
        
        # Supplier permissions to add
        supplier_permissions = [
            'suppliers.view',
            'suppliers.add',
            'suppliers.edit',
            'suppliers.delete',
        ]
        
        for perm_name in supplier_permissions:
            # Check if permission exists
            permission = Permission.query.filter_by(name=perm_name).first()
            
            if not permission:
                print(f"⚠️  Creating permission: {perm_name}")
                permission = Permission(
                    name=perm_name,
                    module='suppliers'
                )
                db.session.add(permission)
                db.session.flush()
            
            # Check if role already has this permission
            if permission not in admin_role.permissions:
                admin_role.permissions.append(permission)
                print(f"✅ Added permission: {perm_name}")
            else:
                print(f"ℹ️  Permission already exists: {perm_name}")
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("✅ SUCCESS! Permissions granted successfully!")
        print("="*50)
        
        # Verify
        admin = User.query.filter_by(username='admin').first()
        print(f"\nUser: {admin.username}")
        print(f"Role: {admin.role.name if admin.role else 'None'}")
        print(f"Total Permissions: {len(admin.role.permissions) if admin.role else 0}")
        
        print("\n✅ You can now delete suppliers!")

if __name__ == '__main__':
    grant_permissions()


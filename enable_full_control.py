#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Enable full control and delete permissions for admin user
"""
from app import create_app
from app.models import User, Role, Permission, db

app = create_app()

with app.app_context():
    print("=" * 80)
    print("🔧 تفعيل التحكم الكامل وصلاحيات الحذف")
    print("=" * 80)
    
    # Get admin user
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        print("❌ ERROR: Admin user not found!")
        exit(1)
    
    print(f"\n✓ Found admin user: {admin.username}")
    print(f"  is_admin: {admin.is_admin}")
    print(f"  role: {admin.role.name if admin.role else 'None'}")
    
    # Get admin role
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        print("❌ ERROR: Admin role not found!")
        exit(1)
    
    print(f"\n✓ Found admin role: {admin_role.name}")
    print(f"  Current permissions: {len(admin_role.permissions)}")
    
    # Get all permissions
    all_permissions = Permission.query.all()
    print(f"\n✓ Total permissions in system: {len(all_permissions)}")
    
    # Add all permissions to admin role
    print("\n📋 Adding all permissions to admin role...")
    added_count = 0
    
    for perm in all_permissions:
        if perm not in admin_role.permissions:
            admin_role.permissions.append(perm)
            added_count += 1
            print(f"  + Added: {perm.name}")
    
    if added_count > 0:
        db.session.commit()
        print(f"\n✅ Added {added_count} new permissions!")
    else:
        print(f"\n✓ Admin already has all permissions!")
    
    # Verify delete permissions
    print("\n" + "=" * 80)
    print("🗑️  Verifying Delete Permissions")
    print("=" * 80)
    
    delete_permissions = [
        'inventory.products.delete',
        'inventory.categories.delete',
        'inventory.warehouses.delete',
        'sales.delete',
        'sales.quotations',  # includes delete
        'purchases.delete',
        'customers.delete',
        'suppliers.delete',
        'settings.users.delete',
        'settings.roles.delete',
    ]
    
    print("\nChecking critical delete permissions:")
    for perm_name in delete_permissions:
        has_perm = admin.has_permission(perm_name)
        status = "✅" if has_perm else "❌"
        print(f"  {status} {perm_name}: {has_perm}")
    
    # Verify admin status
    print("\n" + "=" * 80)
    print("👑 Admin Status")
    print("=" * 80)
    print(f"  Username: {admin.username}")
    print(f"  is_admin: {admin.is_admin}")
    print(f"  is_active: {admin.is_active}")
    print(f"  Role: {admin.role.name if admin.role else 'None'}")
    print(f"  Total permissions: {len(admin.role.permissions) if admin.role else 0}")
    
    # List all modules with permissions
    print("\n" + "=" * 80)
    print("📦 Permissions by Module")
    print("=" * 80)
    
    modules = {}
    for perm in admin.role.permissions:
        module = perm.module or 'general'
        if module not in modules:
            modules[module] = []
        modules[module].append(perm.name)
    
    for module, perms in sorted(modules.items()):
        print(f"\n  📁 {module.upper()} ({len(perms)} permissions)")
        for perm in sorted(perms)[:5]:  # Show first 5
            print(f"     • {perm}")
        if len(perms) > 5:
            print(f"     ... and {len(perms) - 5} more")
    
    print("\n" + "=" * 80)
    print("✅ Full Control Enabled Successfully!")
    print("=" * 80)
    print("\nYou now have:")
    print("  ✓ Full admin access")
    print("  ✓ All delete permissions")
    print("  ✓ All create/edit permissions")
    print("  ✓ All view permissions")
    print("  ✓ Complete system control")
    print("\n" + "=" * 80)


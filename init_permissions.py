#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialize Permissions and Roles
تهيئة الصلاحيات والأدوار في قاعدة البيانات
"""

from app import create_app, db
from app.models import Permission, Role, RolePermission
from permissions_config import PERMISSIONS, DEFAULT_ROLES

def init_permissions():
    """Initialize all permissions in database"""
    print("🔧 تهيئة الصلاحيات...")
    
    added_count = 0
    updated_count = 0
    
    for module, permissions in PERMISSIONS.items():
        for perm_data in permissions:
            # Check if permission exists
            permission = Permission.query.filter_by(name=perm_data['name']).first()
            
            if permission:
                # Update existing permission
                permission.name_ar = perm_data['name_ar']
                permission.module = perm_data['module']
                updated_count += 1
                print(f"  ✓ تحديث: {perm_data['name_ar']} ({perm_data['name']})")
            else:
                # Create new permission
                permission = Permission(
                    name=perm_data['name'],
                    name_ar=perm_data['name_ar'],
                    module=perm_data['module']
                )
                db.session.add(permission)
                added_count += 1
                print(f"  + إضافة: {perm_data['name_ar']} ({perm_data['name']})")
    
    db.session.commit()
    print(f"\n✅ تم إضافة {added_count} صلاحية جديدة وتحديث {updated_count} صلاحية موجودة")
    return added_count, updated_count

def init_roles():
    """Initialize default roles in database"""
    print("\n🔧 تهيئة الأدوار...")
    
    added_count = 0
    updated_count = 0
    
    for role_data in DEFAULT_ROLES:
        # Check if role exists
        role = Role.query.filter_by(name=role_data['name']).first()
        
        if not role:
            # Create new role
            role = Role(
                name=role_data['name'],
                name_ar=role_data['name_ar'],
                description=role_data['description']
            )
            db.session.add(role)
            db.session.flush()  # Get role ID
            added_count += 1
            print(f"  + إضافة دور: {role_data['name_ar']} ({role_data['name']})")
        else:
            # Update existing role
            role.name_ar = role_data['name_ar']
            role.description = role_data['description']
            # Clear existing permissions
            RolePermission.query.filter_by(role_id=role.id).delete()
            updated_count += 1
            print(f"  ✓ تحديث دور: {role_data['name_ar']} ({role_data['name']})")
        
        # Add permissions to role
        if role_data['permissions'] == 'all':
            # Add all permissions
            all_permissions = Permission.query.all()
            for perm in all_permissions:
                role_perm = RolePermission(role_id=role.id, permission_id=perm.id)
                db.session.add(role_perm)
            print(f"    → تم إضافة جميع الصلاحيات ({len(all_permissions)} صلاحية)")
        else:
            # Add specific permissions
            perm_count = 0
            for perm_name in role_data['permissions']:
                permission = Permission.query.filter_by(name=perm_name).first()
                if permission:
                    role_perm = RolePermission(role_id=role.id, permission_id=permission.id)
                    db.session.add(role_perm)
                    perm_count += 1
                else:
                    print(f"    ⚠️  تحذير: الصلاحية '{perm_name}' غير موجودة")
            print(f"    → تم إضافة {perm_count} صلاحية")
    
    db.session.commit()
    print(f"\n✅ تم إضافة {added_count} دور جديد وتحديث {updated_count} دور موجود")
    return added_count, updated_count

def main():
    """Main function"""
    print("=" * 60)
    print("تهيئة نظام الصلاحيات والأدوار")
    print("Initializing Permissions and Roles System")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Initialize permissions
            perm_added, perm_updated = init_permissions()
            
            # Initialize roles
            roles_added, roles_updated = init_roles()
            
            print("\n" + "=" * 60)
            print("✅ تمت التهيئة بنجاح!")
            print(f"   الصلاحيات: {perm_added} جديدة، {perm_updated} محدثة")
            print(f"   الأدوار: {roles_added} جديدة، {roles_updated} محدثة")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ حدث خطأ: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    main()


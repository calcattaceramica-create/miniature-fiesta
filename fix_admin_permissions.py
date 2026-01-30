#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fix Admin Permissions - إصلاح صلاحيات المدير
Add all permissions to admin role
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Role, Permission, RolePermission
from app.tenant_manager import TenantManager

def fix_admin_permissions():
    """Add all permissions to admin role"""
    
    app = create_app()
    
    # License key to use
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    print("=" * 70)
    print("🔧 إصلاح صلاحيات المدير - Fixing Admin Permissions")
    print("=" * 70)
    print()
    
    with app.app_context():
        # Switch to tenant database
        print("📋 Step 1: Switching to tenant database...")
        tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
        
        app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
        db.engine.dispose()
        
        print(f"✅ Switched to: {tenant_db_uri}")
        print()
        
        # Get admin role
        print("📋 Step 2: Getting admin role...")
        admin_role = Role.query.filter_by(name='admin').first()
        
        if not admin_role:
            print("❌ Admin role not found!")
            return
        
        print(f"✅ Found admin role: {admin_role.name}")
        print()
        
        # Create all permissions
        print("📋 Step 3: Creating permissions...")
        
        permissions_data = [
            # Dashboard
            {'name': 'dashboard.view', 'name_ar': 'عرض لوحة التحكم', 'module': 'dashboard'},
            
            # Inventory
            {'name': 'inventory.view', 'name_ar': 'عرض المخزون', 'module': 'inventory'},
            {'name': 'inventory.create', 'name_ar': 'إضافة منتج', 'module': 'inventory'},
            {'name': 'inventory.edit', 'name_ar': 'تعديل منتج', 'module': 'inventory'},
            {'name': 'inventory.delete', 'name_ar': 'حذف منتج', 'module': 'inventory'},
            
            # Sales
            {'name': 'sales.view', 'name_ar': 'عرض المبيعات', 'module': 'sales'},
            {'name': 'sales.create', 'name_ar': 'إنشاء فاتورة مبيعات', 'module': 'sales'},
            {'name': 'sales.edit', 'name_ar': 'تعديل فاتورة مبيعات', 'module': 'sales'},
            {'name': 'sales.delete', 'name_ar': 'حذف فاتورة مبيعات', 'module': 'sales'},
            
            # Purchases
            {'name': 'purchases.view', 'name_ar': 'عرض المشتريات', 'module': 'purchases'},
            {'name': 'purchases.create', 'name_ar': 'إنشاء فاتورة مشتريات', 'module': 'purchases'},
            {'name': 'purchases.edit', 'name_ar': 'تعديل فاتورة مشتريات', 'module': 'purchases'},
            {'name': 'purchases.delete', 'name_ar': 'حذف فاتورة مشتريات', 'module': 'purchases'},
            
            # Accounting
            {'name': 'accounting.view', 'name_ar': 'عرض الحسابات', 'module': 'accounting'},
            {'name': 'accounting.create', 'name_ar': 'إنشاء قيد محاسبي', 'module': 'accounting'},
            {'name': 'accounting.edit', 'name_ar': 'تعديل قيد محاسبي', 'module': 'accounting'},
            {'name': 'accounting.delete', 'name_ar': 'حذف قيد محاسبي', 'module': 'accounting'},
            
            # CRM
            {'name': 'crm.view', 'name_ar': 'عرض العملاء', 'module': 'crm'},
            {'name': 'crm.create', 'name_ar': 'إضافة عميل', 'module': 'crm'},
            {'name': 'crm.edit', 'name_ar': 'تعديل عميل', 'module': 'crm'},
            {'name': 'crm.delete', 'name_ar': 'حذف عميل', 'module': 'crm'},
            
            # HR
            {'name': 'hr.view', 'name_ar': 'عرض الموظفين', 'module': 'hr'},
            {'name': 'hr.create', 'name_ar': 'إضافة موظف', 'module': 'hr'},
            {'name': 'hr.edit', 'name_ar': 'تعديل موظف', 'module': 'hr'},
            {'name': 'hr.delete', 'name_ar': 'حذف موظف', 'module': 'hr'},
            
            # Settings
            {'name': 'settings.view', 'name_ar': 'عرض الإعدادات', 'module': 'settings'},
            {'name': 'settings.edit', 'name_ar': 'تعديل الإعدادات', 'module': 'settings'},
            
            # Users
            {'name': 'users.view', 'name_ar': 'عرض المستخدمين', 'module': 'users'},
            {'name': 'users.create', 'name_ar': 'إضافة مستخدم', 'module': 'users'},
            {'name': 'users.edit', 'name_ar': 'تعديل مستخدم', 'module': 'users'},
            {'name': 'users.delete', 'name_ar': 'حذف مستخدم', 'module': 'users'},
            
            # Reports
            {'name': 'reports.view', 'name_ar': 'عرض التقارير', 'module': 'reports'},
        ]
        
        created_permissions = []
        
        for perm_data in permissions_data:
            perm = Permission.query.filter_by(name=perm_data['name']).first()
            if not perm:
                perm = Permission(**perm_data)
                db.session.add(perm)
                created_permissions.append(perm)
                print(f"   ✅ Created permission: {perm_data['name_ar']}")
            else:
                created_permissions.append(perm)
                print(f"   ℹ️  Permission exists: {perm_data['name_ar']}")
        
        db.session.commit()
        print()
        
        # Assign all permissions to admin role
        print("📋 Step 4: Assigning permissions to admin role...")
        
        for perm in created_permissions:
            # Check if permission already assigned
            role_perm = RolePermission.query.filter_by(
                role_id=admin_role.id,
                permission_id=perm.id
            ).first()
            
            if not role_perm:
                role_perm = RolePermission(
                    role_id=admin_role.id,
                    permission_id=perm.id
                )
                db.session.add(role_perm)
        
        db.session.commit()
        print(f"✅ Assigned {len(created_permissions)} permissions to admin role")
        print()
        
        print("=" * 70)
        print("✅ تم إصلاح صلاحيات المدير بنجاح!")
        print("✅ Admin permissions fixed successfully!")
        print("=" * 70)
        print()
        print("📝 Now try logging in again:")
        print("   License Key: CEC9-79EE-C42F-2DAD")
        print("   Username: admin")
        print("   Password: admin123")
        print()

if __name__ == '__main__':
    fix_admin_permissions()


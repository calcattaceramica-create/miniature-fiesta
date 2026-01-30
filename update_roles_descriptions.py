#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to add description_en column to roles table and update existing roles
"""

from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Add column to database
    try:
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE roles ADD COLUMN description_en VARCHAR(256)'))
            conn.commit()
        print("✅ Column description_en added successfully!")
    except Exception as e:
        print(f"⚠️ Column might already exist: {e}")

    # Update existing roles with English descriptions
    roles_data = {
        'admin': {
            'description': 'مدير النظام بصلاحيات كاملة',
            'description_en': 'System Administrator with full access'
        },
        'manager': {
            'description': 'مدير بصلاحيات مرتفعة',
            'description_en': 'Manager with elevated privileges'
        },
        'user': {
            'description': 'مستخدم عادي بصلاحيات محدودة',
            'description_en': 'Regular user with limited permissions'
        },
        'employee': {
            'description': 'موظف عادي',
            'description_en': 'Regular employee'
        },
        'viewer': {
            'description': 'صلاحيات عرض فقط',
            'description_en': 'View-only access'
        },
        'sales_employee': {
            'description': 'صلاحيات إجراء عمليات البيع',
            'description_en': 'Sales operations permissions'
        },
        'purchases_manager': {
            'description': 'صلاحيات إدارة المشتريات والموردين',
            'description_en': 'Purchases and suppliers management permissions'
        },
        'inventory_manager': {
            'description': 'صلاحيات إدارة المخزون والمنتجات',
            'description_en': 'Inventory and products management permissions'
        },
        'accountant': {
            'description': 'صلاحيات المحاسبة والتقارير المالية',
            'description_en': 'Accounting and financial reports permissions'
        },
        'cashier': {
            'description': 'صلاحيات نقاط البيع والمدفوعات',
            'description_en': 'Point of sale and payments permissions'
        },
        'hr_manager': {
            'description': 'صلاحيات إدارة الموارد البشرية',
            'description_en': 'Human resources management permissions'
        }
    }

    # Update using raw SQL to avoid model issues
    with db.engine.connect() as conn:
        for role_name, descriptions in roles_data.items():
            conn.execute(
                text("UPDATE roles SET description = :desc, description_en = :desc_en WHERE name = :name"),
                {"desc": descriptions['description'], "desc_en": descriptions['description_en'], "name": role_name}
            )
            print(f"✅ Updated role: {role_name}")
        conn.commit()

    print("\n🎉 All roles updated successfully!")

    # Display updated roles
    print("\n📋 Current roles:")
    with db.engine.connect() as conn:
        result = conn.execute(text("SELECT name, name_ar, description, description_en FROM roles"))
        for row in result:
            print(f"  - {row[0]} ({row[1]})")
            print(f"    AR: {row[2]}")
            print(f"    EN: {row[3]}")


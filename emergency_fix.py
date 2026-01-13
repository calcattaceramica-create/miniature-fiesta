#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Emergency database fix - Works with SQLite or PostgreSQL
Run this immediately to fix the database issue
"""

import os
import sys

print("=" * 70)
print("🚨 EMERGENCY DATABASE FIX")
print("=" * 70)

# Set environment to use local SQLite if DATABASE_URL not found
if not os.getenv('DATABASE_URL'):
    print("\n⚠️  DATABASE_URL not found - using SQLite")
    os.environ['FLASK_ENV'] = 'development'
else:
    print("\n✅ DATABASE_URL found - using PostgreSQL")

# Import app
print("\n📦 Loading application...")
try:
    from run import app, db
    print("✅ Application loaded")
except Exception as e:
    print(f"❌ Failed to load app: {e}")
    sys.exit(1)

# Create database
print("\n🔨 Creating database...")
try:
    with app.app_context():
        # Import all models first
        from models import (
            User, Role, Branch, License, Category, Product,
            Supplier, Customer, PurchaseOrder, SaleOrder,
            Inventory, StockMovement, Payment, Expense
        )
        
        print("📋 Dropping old tables...")
        db.drop_all()
        
        print("🏗️  Creating new tables...")
        db.create_all()
        
        print("✅ Tables created successfully!")
        
        # Create default data
        print("\n📝 Creating default data...")
        
        # License
        license = License(
            license_key='FREE-TRIAL-2024',
            company_name='DED Company',
            max_users=10,
            max_branches=3,
            is_active=True
        )
        db.session.add(license)
        db.session.flush()
        
        # Branch
        branch = Branch(
            name='Main Branch',
            name_ar='الفرع الرئيسي',
            code='MAIN',
            is_active=True,
            license_id=license.id
        )
        db.session.add(branch)
        db.session.flush()
        
        # Admin Role
        admin_role = Role(
            name='admin',
            name_ar='مدير النظام',
            description='Full system access',
            description_ar='صلاحيات كاملة'
        )
        db.session.add(admin_role)
        db.session.flush()
        
        # Admin User
        admin = User(
            username='admin',
            email='admin@ded.com',
            full_name='System Administrator',
            is_active=True,
            is_admin=True,
            must_change_password=True,
            branch_id=branch.id,
            role_id=admin_role.id,
            license_id=license.id
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Commit
        db.session.commit()
        
        print("✅ Default data created!")
        
        # Verify
        print("\n✅ Database verification:")
        print(f"   Users: {User.query.count()}")
        print(f"   Roles: {Role.query.count()}")
        print(f"   Branches: {Branch.query.count()}")
        print(f"   Licenses: {License.query.count()}")
        
        print("\n" + "=" * 70)
        print("🎉 DATABASE FIXED SUCCESSFULLY!")
        print("=" * 70)
        print("\n📝 Login credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n⚠️  CHANGE PASSWORD AFTER LOGIN!")
        print("=" * 70)
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


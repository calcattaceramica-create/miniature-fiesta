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

# Check DATABASE_URL
db_url = os.getenv('DATABASE_URL')
if not db_url:
    print("\n⚠️  DATABASE_URL not found - using SQLite")
    print("⚠️  For production, you MUST create PostgreSQL database!")
else:
    print(f"\n✅ DATABASE_URL found")
    # Fix Render PostgreSQL URL
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
        os.environ['DATABASE_URL'] = db_url
        print("✅ Fixed PostgreSQL URL format")

# Import app
print("\n📦 Loading application...")
try:
    from app import create_app, db
    app = create_app(os.getenv('FLASK_ENV') or 'production')
    print("✅ Application loaded")
except Exception as e:
    print(f"❌ Failed to load app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Create database
print("\n🔨 Creating database...")
try:
    with app.app_context():
        # Import all models
        from app.models import User, Role, Company, Branch
        print("✅ Models imported")

        print("📋 Dropping old tables...")
        db.drop_all()

        print("🏗️  Creating new tables...")
        db.create_all()

        print("✅ Tables created successfully!")

        # Create default data
        print("\n📝 Creating default data...")

        # Company
        company = Company(
            name='شركة DED',
            name_en='DED Company',
            tax_number='123456789',
            city='الرياض',
            country='السعودية',
            currency='SAR',
            tax_rate=15.0
        )
        db.session.add(company)
        db.session.flush()
        print("✅ Company created")

        # Branch
        branch = Branch(
            name='الفرع الرئيسي',
            name_en='Main Branch',
            code='BR001',
            company_id=company.id,
            city='الرياض',
            is_active=True
        )
        db.session.add(branch)
        db.session.flush()
        print("✅ Branch created")

        # Admin Role
        admin_role = Role(
            name='admin',
            name_ar='مدير النظام',
            description='Full system access'
        )
        db.session.add(admin_role)
        db.session.flush()
        print("✅ Admin role created")

        # Admin User
        admin = User(
            username='admin',
            email='admin@ded.com',
            full_name='System Administrator',
            is_active=True,
            is_admin=True,
            language='ar',
            branch_id=branch.id,
            role_id=admin_role.id
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("✅ Admin user created")

        # Commit
        db.session.commit()
        print("✅ All data committed!")

        # Verify
        print("\n✅ Database verification:")
        print(f"   Companies: {Company.query.count()}")
        print(f"   Branches: {Branch.query.count()}")
        print(f"   Roles: {Role.query.count()}")
        print(f"   Users: {User.query.count()}")

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


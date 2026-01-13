#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick fix script to initialize database on Render
Run this from Render Shell: python fix_database.py
"""

import os
import sys

def main():
    print("=" * 60)
    print("🔧 DED ERP - Database Initialization Script")
    print("=" * 60)

    # Check DATABASE_URL
    db_url = os.getenv('DATABASE_URL')

    print("\n📊 Environment Check:")
    print(f"   FLASK_ENV: {os.getenv('FLASK_ENV', 'not set')}")
    print(f"   DATABASE_URL: {'✅ Found' if db_url else '❌ Not found'}")

    if db_url:
        # Hide password in output
        if '@' in db_url:
            parts = db_url.split('@')
            safe_url = parts[0].split(':')[0] + ':***@' + parts[1]
            print(f"   Database: {safe_url}")
        else:
            print(f"   Database: {db_url[:50]}...")
    else:
        print("   ⚠️ WARNING: Using SQLite fallback")
        print("   This means DATABASE_URL is not configured in Render!")

    # Import app
    print("\n📦 Loading application...")
    try:
        from run import app, db
        print("   ✅ Application loaded successfully")
    except ImportError:
        try:
            # Try alternative import
            import sys
            sys.path.insert(0, os.path.dirname(__file__))
            from run import app, db
            print("   ✅ Application loaded successfully")
        except Exception as e:
            print(f"   ❌ Failed to import app: {e}")
            print("\n💡 Troubleshooting:")
            print("   1. Make sure you're in the correct directory")
            print("   2. Check that run.py exists")
            print("   3. Verify all dependencies are installed")
            return 1

    # Create tables
    print("\n🔨 Creating database tables...")
    try:
        with app.app_context():
            # Drop all tables first (fresh start)
            print("   🗑️ Dropping existing tables...")
            db.drop_all()

            # Create all tables
            print("   🏗️ Creating new tables...")
            db.create_all()
            print("   ✅ All tables created successfully!")

            # Import models
            from models import User, Role, Branch, License

            # Create default license
            print("\n📜 Creating default license...")
            license = License(
                license_key='FREE-TRIAL-2024',
                company_name='DED Company',
                max_users=10,
                max_branches=3,
                is_active=True
            )
            db.session.add(license)
            db.session.flush()
            print("   ✅ License created")

            # Create main branch
            print("\n🏢 Creating main branch...")
            branch = Branch(
                name='Main Branch',
                name_ar='الفرع الرئيسي',
                code='MAIN',
                is_active=True,
                license_id=license.id
            )
            db.session.add(branch)
            db.session.flush()
            print("   ✅ Branch created")

            # Create admin role
            print("\n👑 Creating admin role...")
            admin_role = Role(
                name='admin',
                name_ar='مدير النظام',
                description='Full system access',
                description_ar='صلاحيات كاملة للنظام'
            )
            db.session.add(admin_role)
            db.session.flush()
            print("   ✅ Admin role created")

            # Create admin user
            print("\n👤 Creating admin user...")
            admin_user = User(
                username='admin',
                email='admin@ded-erp.com',
                full_name='System Administrator',
                is_active=True,
                is_admin=True,
                must_change_password=True,
                branch_id=branch.id,
                role_id=admin_role.id,
                license_id=license.id
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)

            # Commit all changes
            db.session.commit()

            print("   ✅ Admin user created successfully!")

            # Verify
            print("\n✅ Verification:")
            user_count = User.query.count()
            role_count = Role.query.count()
            branch_count = Branch.query.count()
            license_count = License.query.count()

            print(f"   Users: {user_count}")
            print(f"   Roles: {role_count}")
            print(f"   Branches: {branch_count}")
            print(f"   Licenses: {license_count}")

            print("\n" + "=" * 60)
            print("🎉 Database initialization completed successfully!")
            print("=" * 60)
            print("\n📝 Login Credentials:")
            print("   👤 Username: admin")
            print("   🔑 Password: admin123")
            print("\n⚠️  IMPORTANT: Change the password immediately after login!")
            print("\n🌐 Next steps:")
            print("   1. Go to your Render app URL")
            print("   2. Login with the credentials above")
            print("   3. Change your password")
            print("   4. Start using the system!")
            print("=" * 60)

            return 0

    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        print("\n📋 Full error details:")
        traceback.print_exc()
        print("\n💡 Common solutions:")
        print("   1. Check DATABASE_URL is set in Render Environment")
        print("   2. Make sure PostgreSQL database is created")
        print("   3. Verify database connection is working")
        print("   4. Check all dependencies are installed")
        return 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user")
        sys.exit(1)


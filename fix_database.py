#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick fix script to initialize database on Render
Run this from Render Shell if database is not initialized
"""

import os
import sys

def main():
    print("🔧 Starting database fix...")
    
    # Check if we have DATABASE_URL
    db_url = os.getenv('DATABASE_URL')
    
    if not db_url:
        print("⚠️ WARNING: DATABASE_URL not found!")
        print("Using SQLite as fallback...")
    else:
        print(f"✅ Found DATABASE_URL: {db_url[:30]}...")
    
    # Import app
    try:
        from app import app, db
        print("✅ App imported successfully")
    except Exception as e:
        print(f"❌ Failed to import app: {e}")
        return 1
    
    # Create tables
    try:
        with app.app_context():
            print("🔨 Creating database tables...")
            db.create_all()
            print("✅ Tables created successfully!")
            
            # Check if admin exists
            from models import User
            admin = User.query.filter_by(username='admin').first()
            
            if admin:
                print("✅ Admin user already exists")
            else:
                print("👤 Creating admin user...")
                from models import Role
                
                # Create admin role
                admin_role = Role.query.filter_by(name='admin').first()
                if not admin_role:
                    admin_role = Role(
                        name='admin',
                        name_ar='مدير النظام',
                        description='Full system access'
                    )
                    db.session.add(admin_role)
                
                # Create admin user
                admin_user = User(
                    username='admin',
                    email='admin@ded-erp.com',
                    full_name='System Administrator',
                    is_active=True,
                    must_change_password=True
                )
                admin_user.set_password('admin123')
                if admin_role:
                    admin_user.roles.append(admin_role)
                
                db.session.add(admin_user)
                db.session.commit()
                
                print("✅ Admin user created!")
                print("   Username: admin")
                print("   Password: admin123")
                print("   ⚠️ CHANGE PASSWORD IMMEDIATELY!")
            
            print("\n🎉 Database fix completed successfully!")
            print("\n📝 Next steps:")
            print("   1. Refresh your browser")
            print("   2. Login with admin/admin123")
            print("   3. Change the password!")
            
            return 0
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())


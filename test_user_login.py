#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test User Login
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User
from app.tenant_manager import TenantManager
from werkzeug.security import check_password_hash

def test_user_login():
    """Test user login"""
    
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    print("=" * 80)
    print("🔍 Testing User Login")
    print("=" * 80)
    print()
    
    # Create app
    app = create_app()
    
    with app.app_context():
        # Switch to tenant database
        tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
        app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
        db.engine.dispose()
        
        print(f"✅ Connected to: {tenant_db_uri}")
        print()
        
        # Get all users
        print("📋 All Users:")
        users = User.query.all()
        
        for user in users:
            print(f"\n   👤 User: {user.username}")
            print(f"      Full Name: {user.full_name}")
            print(f"      Email: {user.email}")
            print(f"      Active: {user.is_active}")
            print(f"      Password Hash: {user.password_hash[:50]}..." if user.password_hash else "      Password Hash: None")
            print(f"      Role ID: {user.role_id}")
            print(f"      License ID: {user.license_id}")
            
            # Test password
            test_passwords = ['admin123', 'Admin123', '12345678', 'password']
            
            print(f"      Testing passwords:")
            for pwd in test_passwords:
                if user.password_hash:
                    result = check_password_hash(user.password_hash, pwd)
                    if result:
                        print(f"         ✅ '{pwd}' - CORRECT!")
                    else:
                        print(f"         ❌ '{pwd}' - wrong")
                else:
                    print(f"         ⚠️ No password hash set!")
        
        print()
        print("=" * 80)
        print("✅ Test Complete!")
        print("=" * 80)
        print()
        
        # Ask user to create a test user
        print("💡 Do you want to create a test user? (yes/no)")
        response = input("> ").strip().lower()
        
        if response in ['yes', 'y', 'نعم']:
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            full_name = input("Enter full name: ").strip()
            email = input("Enter email: ").strip()
            
            # Check if user exists
            existing_user = User.query.filter_by(username=username).first()
            
            if existing_user:
                print(f"\n⚠️ User '{username}' already exists!")
                print("Do you want to update the password? (yes/no)")
                update_response = input("> ").strip().lower()
                
                if update_response in ['yes', 'y', 'نعم']:
                    existing_user.set_password(password)
                    db.session.commit()
                    print(f"\n✅ Password updated for user '{username}'!")
                    
                    # Test the new password
                    if existing_user.check_password(password):
                        print(f"✅ Password verification successful!")
                    else:
                        print(f"❌ Password verification failed!")
            else:
                # Create new user
                new_user = User(
                    username=username,
                    email=email,
                    full_name=full_name,
                    is_active=True,
                    role_id=1  # Admin role
                )
                new_user.set_password(password)
                
                db.session.add(new_user)
                db.session.commit()
                
                print(f"\n✅ User '{username}' created successfully!")
                
                # Test the password
                if new_user.check_password(password):
                    print(f"✅ Password verification successful!")
                else:
                    print(f"❌ Password verification failed!")

if __name__ == '__main__':
    test_user_login()


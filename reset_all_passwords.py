#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Reset All User Passwords
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User
from app.tenant_manager import TenantManager

def reset_all_passwords():
    """Reset all user passwords to default"""
    
    license_key = 'CEC9-79EE-C42F-2DAD'
    default_password = 'Admin@123'  # Strong default password
    
    print("=" * 80)
    print("🔧 Resetting All User Passwords")
    print("=" * 80)
    print()
    
    # Create app
    app = create_app()
    
    with app.app_context():
        # Switch to tenant database
        tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
        app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
        db.engine.dispose()
        
        print(f"📋 Resetting passwords for all users...")
        print(f"   Default password: {default_password}")
        print()
        
        # Get all users
        users = User.query.all()
        
        for user in users:
            print(f"👤 User: {user.username}")
            
            # Reset password
            user.set_password(default_password)
            
            # Test password
            if user.check_password(default_password):
                print(f"   ✅ Password reset successful!")
            else:
                print(f"   ❌ Password reset failed!")
        
        db.session.commit()
        
        print()
        print("=" * 80)
        print("✅ All passwords reset!")
        print("=" * 80)
        print()
        
        print("📋 Login Credentials:")
        print()
        
        for user in users:
            print(f"   👤 Username: {user.username}")
            print(f"      Password: {default_password}")
            print(f"      Full Name: {user.full_name}")
            print()

if __name__ == '__main__':
    reset_all_passwords()


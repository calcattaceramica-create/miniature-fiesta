#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verify Login Functionality
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.auth.multi_tenant_login import authenticate_with_license

def verify_login():
    """Verify login functionality"""
    
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    print("=" * 80)
    print("🔍 Verifying Login Functionality")
    print("=" * 80)
    print()
    
    # Create app
    app = create_app()
    
    # Test admin login
    print(f"📋 Testing admin login")
    print(f"   Username: admin")
    print(f"   Password: admin123")
    print(f"   License: {license_key}")
    
    success, message, user = authenticate_with_license(
        'admin', 'admin123', license_key, app
    )
    
    if success:
        print(f"   ✅ SUCCESS: {message}")
        print(f"   User: {user.full_name} ({user.username})")
        print(f"   License ID: {user.license_id}")
    else:
        print(f"   ❌ FAILED: {message}")
    
    print()
    print("=" * 80)

if __name__ == '__main__':
    verify_login()


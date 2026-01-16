#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verify License System
التحقق من نظام التراخيص
"""

import os
import sys

# Set environment
os.environ['FLASK_ENV'] = 'production'

print("=" * 80)
print("🔍 VERIFYING LICENSE SYSTEM - التحقق من نظام التراخيص")
print("=" * 80)

from app import create_app, db
from app.models_license import License, LicenseCheck
from app.license_manager import LicenseManager

app = create_app('production')

def verify_system():
    """Verify license system is working"""
    
    with app.app_context():
        print("\n1️⃣ Checking database tables...")
        
        try:
            # Check if tables exist
            license_count = License.query.count()
            check_count = LicenseCheck.query.count()
            
            print(f"   ✅ License table exists ({license_count} licenses)")
            print(f"   ✅ LicenseCheck table exists ({check_count} checks)")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print("\n   💡 Solution: Run 'python add_license_to_render.py'")
            return False
        
        print("\n2️⃣ Checking active licenses...")
        
        licenses = License.query.filter_by(is_active=True).all()
        
        if not licenses:
            print("   ⚠️  No active licenses found!")
            print("\n   💡 Solution: Run 'python create_license.py'")
            return False
        
        print(f"   ✅ Found {len(licenses)} active license(s)")
        
        print("\n3️⃣ Verifying license validity...")
        
        for license in licenses:
            is_valid, message = license.is_valid()
            
            status_icon = "✅" if is_valid else "❌"
            print(f"\n   {status_icon} License: {license.license_key}")
            print(f"      Client: {license.client_name}")
            print(f"      Type: {license.license_type}")
            print(f"      Status: {message}")
            
            if license.expires_at:
                days_remaining = license.days_remaining()
                print(f"      Expires: {license.expires_at.strftime('%Y-%m-%d')} ({days_remaining} days)")
            else:
                print(f"      Expires: Lifetime")
            
            print(f"      Max Users: {license.max_users}")
            print(f"      Max Branches: {license.max_branches}")
        
        print("\n4️⃣ Testing license verification...")
        
        try:
            is_valid, message, license = LicenseManager.verify_license()
            
            if is_valid:
                print(f"   ✅ License verification successful!")
                print(f"      Message: {message}")
            else:
                print(f"   ❌ License verification failed!")
                print(f"      Message: {message}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error during verification: {e}")
            return False
        
        print("\n5️⃣ Checking middleware integration...")
        
        try:
            from app.license_middleware import check_license_validity
            
            is_valid, message, license = check_license_validity()
            
            if is_valid:
                print(f"   ✅ Middleware is working correctly!")
            else:
                print(f"   ⚠️  Middleware returned: {message}")
                
        except Exception as e:
            print(f"   ❌ Middleware error: {e}")
            return False
        
        print("\n" + "=" * 80)
        print("✅ LICENSE SYSTEM VERIFICATION COMPLETE!")
        print("=" * 80)
        print("\n📊 Summary:")
        print(f"   • Total Licenses: {license_count}")
        print(f"   • Active Licenses: {len(licenses)}")
        print(f"   • Total Checks: {check_count}")
        print(f"   • System Status: OPERATIONAL ✅")
        print("\n🎉 The license system is ready to use!")
        print("=" * 80)
        
        return True

if __name__ == '__main__':
    try:
        success = verify_system()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


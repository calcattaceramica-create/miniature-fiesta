#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check Licenses on Render
فحص التراخيص على Render
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app, db
from app.models_license import License

def check_licenses():
    """Check all licenses in the database"""
    
    print("=" * 80)
    print("🔍 Checking Licenses in Database")
    print("=" * 80)
    print()
    
    app = create_app()
    
    with app.app_context():
        try:
            licenses = License.query.all()
            
            if not licenses:
                print("❌ No licenses found in database!")
                print()
                print("💡 You need to create a license first.")
                print("   Run: python create_default_license.py")
                return False
            
            print(f"✅ Found {len(licenses)} license(s):")
            print()
            
            for i, lic in enumerate(licenses, 1):
                print(f"📋 License #{i}:")
                print(f"   🔑 License Key: {lic.license_key}")
                print(f"   👤 Client: {lic.client_name}")
                print(f"   🏢 Company: {lic.client_company}")
                print(f"   📧 Email: {lic.client_email}")
                print(f"   📱 Phone: {lic.client_phone}")
                print(f"   📅 Type: {lic.license_type}")
                print(f"   👥 Max Users: {lic.max_users}")
                print(f"   🏢 Max Branches: {lic.max_branches}")
                print(f"   ✅ Active: {lic.is_active}")
                print(f"   ⏸️  Suspended: {lic.is_suspended}")
                print(f"   🔐 Admin Username: {lic.admin_username}")
                print(f"   📅 Created: {lic.created_at}")
                print(f"   📅 Activated: {lic.activated_at}")
                print(f"   📅 Expires: {lic.expires_at if lic.expires_at else 'Never (Lifetime)'}")
                print()
                print("-" * 80)
                print()
            
            # Show active licenses
            active_licenses = [lic for lic in licenses if lic.is_active and not lic.is_suspended]
            
            if active_licenses:
                print("=" * 80)
                print("✅ ACTIVE LICENSES (Ready to use):")
                print("=" * 80)
                print()
                
                for lic in active_licenses:
                    print(f"🔑 License Key: {lic.license_key}")
                    print(f"👤 Username: {lic.admin_username}")
                    print(f"🔒 Password: admin123 (default)")
                    print()
                    print("📝 Login URL:")
                    print("   https://ded-inventory-system-1zec.onrender.com/auth/login")
                    print()
                    print("-" * 80)
                    print()
            else:
                print("=" * 80)
                print("⚠️  WARNING: No active licenses found!")
                print("=" * 80)
                print()
                print("All licenses are either inactive or suspended.")
                print("You need to activate a license first.")
                print()
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = check_licenses()
    sys.exit(0 if success else 1)


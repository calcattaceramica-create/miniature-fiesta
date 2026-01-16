"""
Script to update old licenses to new format
تحديث التراخيص القديمة للصيغة الجديدة
"""

import json
import os
from datetime import datetime

def update_licenses():
    """Update old license format to new format"""
    
    license_file = 'licenses.json'
    
    if not os.path.exists(license_file):
        print("❌ ملف التراخيص غير موجود - License file not found")
        return
    
    # Load licenses
    with open(license_file, 'r', encoding='utf-8') as f:
        licenses = json.load(f)
    
    print(f"📋 Found {len(licenses)} license(s)")
    
    updated_count = 0
    
    for key, lic in licenses.items():
        updated = False
        
        # Add missing 'phone' field
        if 'phone' not in lic:
            lic['phone'] = lic.get('contact_phone', '')
            updated = True
            print(f"  ✅ Added 'phone' field to {lic.get('company', 'Unknown')}")
        
        # Add missing 'created_at' field
        if 'created_at' not in lic:
            # Use 'created' if exists, otherwise use current date
            lic['created_at'] = lic.get('created', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            updated = True
            print(f"  ✅ Added 'created_at' field to {lic.get('company', 'Unknown')}")
        
        # Ensure 'status' field exists
        if 'status' not in lic:
            lic['status'] = 'active'
            updated = True
            print(f"  ✅ Added 'status' field to {lic.get('company', 'Unknown')}")
        
        if updated:
            updated_count += 1
    
    # Save updated licenses
    if updated_count > 0:
        # Backup old file
        backup_file = f'licenses_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(licenses, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Backup saved to: {backup_file}")
        
        # Save updated licenses
        with open(license_file, 'w', encoding='utf-8') as f:
            json.dump(licenses, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Updated {updated_count} license(s) successfully!")
        print(f"📁 Updated file: {license_file}")
    else:
        print("\n✅ All licenses are already up to date!")
    
    # Display updated licenses
    print("\n" + "="*60)
    print("📋 Updated Licenses:")
    print("="*60)
    
    for key, lic in licenses.items():
        print(f"\n🔑 Key: {key}")
        print(f"   🏢 Company: {lic.get('company')}")
        print(f"   👤 Username: {lic.get('username')}")
        print(f"   📱 Phone: {lic.get('phone', 'N/A')}")
        print(f"   📅 Created: {lic.get('created_at', 'N/A')}")
        print(f"   ⏰ Expiry: {lic.get('expiry')}")
        print(f"   📊 Status: {lic.get('status', 'active')}")

if __name__ == "__main__":
    print("🔧 Updating old licenses to new format...")
    print("="*60)
    update_licenses()
    print("\n✅ Done!")


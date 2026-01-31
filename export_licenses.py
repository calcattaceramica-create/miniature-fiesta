#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
تصدير التراخيص من قاعدة البيانات المحلية
Export Licenses from Local Database
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models_license import License, LicenseCheck
import json
from datetime import datetime

def export_licenses_to_json():
    """تصدير التراخيص إلى ملف JSON"""
    
    app = create_app('development')
    
    with app.app_context():
        print("=" * 70)
        print("📦 تصدير التراخيص من قاعدة البيانات المحلية")
        print("=" * 70)
        
        # Get all licenses
        licenses = License.query.all()
        
        if not licenses:
            print("❌ لا توجد تراخيص في قاعدة البيانات!")
            return
        
        print(f"\n✅ تم العثور على {len(licenses)} ترخيص")
        
        # Convert to JSON-serializable format
        licenses_data = []
        
        for license in licenses:
            license_dict = {
                'license_key': license.license_key,
                'license_hash': license.license_hash,
                'client_name': license.client_name,
                'client_email': license.client_email,
                'client_phone': license.client_phone,
                'client_company': license.client_company,
                'license_type': license.license_type,
                'max_users': license.max_users,
                'max_branches': license.max_branches,
                'is_active': license.is_active,
                'is_suspended': license.is_suspended,
                'suspension_reason': license.suspension_reason,
                'created_at': license.created_at.isoformat() if license.created_at else None,
                'activated_at': license.activated_at.isoformat() if license.activated_at else None,
                'expires_at': license.expires_at.isoformat() if license.expires_at else None,
                'last_check': license.last_check.isoformat() if license.last_check else None,
                'machine_id': license.machine_id,
                'ip_address': license.ip_address,
                'admin_username': license.admin_username,
                'admin_password_hash': license.admin_password_hash,
                'notes': license.notes
            }
            
            licenses_data.append(license_dict)
            
            print(f"\n📄 الترخيص: {license.license_key}")
            print(f"   العميل: {license.client_name}")
            print(f"   النوع: {license.license_type}")
            print(f"   الحالة: {'مفعّل' if license.is_active else 'غير مفعّل'}")
        
        # Save to JSON file
        output_file = 'licenses_export.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(licenses_data, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 70)
        print(f"✅ تم تصدير التراخيص بنجاح إلى: {output_file}")
        print("=" * 70)
        
        # Also create SQL insert statements
        sql_file = 'licenses_export.sql'
        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write("-- تصدير التراخيص\n")
            f.write("-- Export Licenses\n\n")
            
            for license in licenses:
                # Escape single quotes in strings
                def escape_sql(value):
                    if value is None:
                        return 'NULL'
                    if isinstance(value, bool):
                        return 'TRUE' if value else 'FALSE'
                    if isinstance(value, (int, float)):
                        return str(value)
                    if isinstance(value, datetime):
                        return f"'{value.isoformat()}'"
                    # String - escape single quotes
                    return f"'{str(value).replace(chr(39), chr(39)+chr(39))}'"
                
                sql = f"""INSERT INTO license (
    license_key, license_hash, client_name, client_email, client_phone, 
    client_company, license_type, max_users, max_branches, is_active, 
    is_suspended, suspension_reason, created_at, activated_at, expires_at, 
    last_check, machine_id, ip_address, admin_username, admin_password_hash, notes
) VALUES (
    {escape_sql(license.license_key)}, {escape_sql(license.license_hash)}, 
    {escape_sql(license.client_name)}, {escape_sql(license.client_email)}, 
    {escape_sql(license.client_phone)}, {escape_sql(license.client_company)}, 
    {escape_sql(license.license_type)}, {escape_sql(license.max_users)}, 
    {escape_sql(license.max_branches)}, {escape_sql(license.is_active)}, 
    {escape_sql(license.is_suspended)}, {escape_sql(license.suspension_reason)}, 
    {escape_sql(license.created_at)}, {escape_sql(license.activated_at)}, 
    {escape_sql(license.expires_at)}, {escape_sql(license.last_check)}, 
    {escape_sql(license.machine_id)}, {escape_sql(license.ip_address)}, 
    {escape_sql(license.admin_username)}, {escape_sql(license.admin_password_hash)}, 
    {escape_sql(license.notes)}
);

"""
                f.write(sql)
        
        print(f"✅ تم إنشاء ملف SQL: {sql_file}")
        print("\n📝 الخطوات التالية:")
        print("   1. ارفع ملف licenses_export.sql إلى المشروع")
        print("   2. سيتم تنفيذه تلقائياً على Render")
        print("=" * 70)

if __name__ == '__main__':
    export_licenses_to_json()


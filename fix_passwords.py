"""
Fix Passwords in Master and Tenant Databases
إصلاح كلمات المرور في قواعد البيانات
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash

# New password for all users
new_password = 'admin123'
new_hash = generate_password_hash(new_password)

print("=" * 70)
print("🔧 Fixing Passwords")
print("=" * 70)
print(f"New password: {new_password}")
print(f"New hash: {new_hash[:50]}...")
print()

# Fix master database
print("📦 Fixing Master Database...")
conn = sqlite3.connect('licenses_master.db')
cursor = conn.cursor()

cursor.execute("SELECT license_key, admin_username FROM licenses WHERE is_active = 1")
licenses = cursor.fetchall()

for license_key, username in licenses:
    cursor.execute("UPDATE licenses SET admin_password_hash = ? WHERE license_key = ?", 
                   (new_hash, license_key))
    print(f"  ✅ Updated {license_key} - {username}")

conn.commit()
conn.close()

print()
print("📁 Fixing Tenant Databases...")

for license_key, username in licenses:
    tenant_db = f"tenant_databases/tenant_{license_key.replace('-', '_')}.db"
    
    if os.path.exists(tenant_db):
        conn = sqlite3.connect(tenant_db)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", 
                       (new_hash, username))
        conn.commit()
        conn.close()
        
        print(f"  ✅ Updated {tenant_db} - {username}")
    else:
        print(f"  ⚠️ Database not found: {tenant_db}")

print()
print("=" * 70)
print("✅ All passwords fixed!")
print("=" * 70)
print(f"All users can now login with password: {new_password}")


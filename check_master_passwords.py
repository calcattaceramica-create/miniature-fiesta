"""
Check Passwords in Master Database
التحقق من كلمات المرور في قاعدة البيانات الرئيسية
"""
import sqlite3
from werkzeug.security import check_password_hash

conn = sqlite3.connect('licenses_master.db')
cursor = conn.cursor()

cursor.execute("SELECT license_key, admin_username, admin_password_hash FROM licenses WHERE is_active = 1")
results = cursor.fetchall()

print("=" * 70)
print("🔍 Checking Master Database Passwords")
print("=" * 70)

for license_key, username, password_hash in results:
    is_valid = check_password_hash(password_hash, 'admin123')
    print(f"\n{license_key} - {username}:")
    print(f"  Password 'admin123': {'✅ Valid' if is_valid else '❌ Invalid'}")
    print(f"  Hash: {password_hash[:50]}...")

conn.close()


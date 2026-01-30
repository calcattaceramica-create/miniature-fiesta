"""
Check Passwords in Tenant Databases
التحقق من كلمات المرور في قواعد بيانات التراخيص
"""
import sqlite3
import os
from werkzeug.security import check_password_hash

licenses = [
    ('CEC9-79EE-C42F-2DAD', 'admin'),
    ('6356-6964-93AE-B60D', 'admin1'),
    ('F730-BD34-0A48-A98B', 'admin2'),
]

for license_key, username in licenses:
    tenant_db = f"tenant_databases/tenant_{license_key.replace('-', '_')}.db"
    
    if os.path.exists(tenant_db):
        conn = sqlite3.connect(tenant_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT username, password_hash FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if result:
            user, password_hash = result
            # Test password
            is_valid = check_password_hash(password_hash, 'admin123')
            print(f"{license_key} - {user}: {'✅ Valid' if is_valid else '❌ Invalid'}")
            print(f"  Hash: {password_hash[:50]}...")
        else:
            print(f"{license_key} - {username}: ❌ User not found")
        
        conn.close()
    else:
        print(f"{license_key}: ❌ Database not found")


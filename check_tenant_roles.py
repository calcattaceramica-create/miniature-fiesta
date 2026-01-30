"""
Check Roles in Tenant Databases
التحقق من الأدوار في قواعد بيانات التراخيص
"""
import sqlite3
import os

tenant_db = "tenant_databases/tenant_CEC9_79EE_C42F_2DAD.db"

if os.path.exists(tenant_db):
    conn = sqlite3.connect(tenant_db)
    cursor = conn.cursor()
    
    print(f"Checking: {tenant_db}")
    print("=" * 70)
    
    # Check roles
    cursor.execute("SELECT id, name, name_ar FROM roles")
    roles = cursor.fetchall()
    
    print(f"Roles count: {len(roles)}")
    for role in roles:
        print(f"  - {role[1]} ({role[2]}) - ID: {role[0]}")
    
    print()
    
    # Check users
    cursor.execute("SELECT id, username, full_name, role_id FROM users")
    users = cursor.fetchall()
    
    print(f"Users count: {len(users)}")
    for user in users:
        print(f"  - {user[1]} ({user[2]}) - Role ID: {user[3]}")
    
    conn.close()
else:
    print(f"Database not found: {tenant_db}")


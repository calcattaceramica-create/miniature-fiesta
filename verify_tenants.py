#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verify Tenant Databases
"""

import sqlite3
import os

def verify_tenant_databases():
    """Verify all tenant databases"""
    
    databases = [
        ('CEC9-79EE-C42F-2DAD', 'tenant_CEC9_79EE_C42F_2DAD.db', 'admin'),
        ('9813-26D0-F98D-741C', 'tenant_9813_26D0_F98D_741C.db', 'mohammed'),
        ('5FB2-D77F-D1C2-B045', 'tenant_5FB2_D77F_D1C2_B045.db', 'raef'),
        ('50F5-D5C4-C516-DB59', 'tenant_50F5_D5C4_C516_DB59.db', 'HHH')
    ]
    
    print("="*70)
    print("TENANT DATABASES VERIFICATION")
    print("="*70)
    print()
    
    for license_key, db_file, expected_admin in databases:
        db_path = os.path.join('tenant_databases', db_file)
        
        if not os.path.exists(db_path):
            print(f"License: {license_key}")
            print(f"  ERROR: Database file not found!")
            print()
            continue
        
        print(f"License: {license_key}")
        print(f"  Expected Admin: {expected_admin}")
        print(f"  Database: {db_file}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check users
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        print(f"  Users: {user_count}")
        
        if user_count > 0:
            cursor.execute('SELECT username, email, full_name, is_admin FROM users')
            for row in cursor.fetchall():
                admin_flag = 'ADMIN' if row[3] else 'USER'
                print(f"    - {row[0]} | {row[1]} | {row[2]} | {admin_flag}")
        
        # Check roles
        cursor.execute('SELECT COUNT(*) FROM roles')
        role_count = cursor.fetchone()[0]
        print(f"  Roles: {role_count}")
        
        # Check branches
        cursor.execute('SELECT COUNT(*) FROM branches')
        branch_count = cursor.fetchone()[0]
        print(f"  Branches: {branch_count}")
        
        # Check accounts
        cursor.execute('SELECT COUNT(*) FROM accounts')
        account_count = cursor.fetchone()[0]
        print(f"  Accounts: {account_count}")
        
        if account_count > 0:
            cursor.execute('SELECT code, name FROM accounts LIMIT 5')
            for row in cursor.fetchall():
                print(f"    - {row[0]} | {row[1]}")
        
        conn.close()
        print()
    
    print("="*70)
    print("VERIFICATION COMPLETE!")
    print("="*70)

if __name__ == '__main__':
    verify_tenant_databases()


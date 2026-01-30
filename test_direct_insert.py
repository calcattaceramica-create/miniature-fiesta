#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Direct Data Insertion
"""

import sqlite3
import os

def test_direct_insertion():
    """Test inserting data directly into tenant database"""
    
    db_path = r'C:\Users\DELL\DED\tenant_databases\tenant_CEC9_79EE_C42F_2DAD.db'
    
    print(f"Testing direct insertion into: {db_path}")
    print(f"File exists: {os.path.exists(db_path)}")
    print()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check current data
    cursor.execute('SELECT COUNT(*) FROM roles')
    print(f"Roles before: {cursor.fetchone()[0]}")
    
    # Insert a test role
    cursor.execute("INSERT INTO roles (name, name_ar, description) VALUES (?, ?, ?)", 
                   ('test_direct', 'دور مباشر', 'Direct test role'))
    conn.commit()
    
    # Check after insertion
    cursor.execute('SELECT COUNT(*) FROM roles')
    print(f"Roles after: {cursor.fetchone()[0]}")
    
    # List all roles
    cursor.execute('SELECT name, name_ar FROM roles')
    print("\nAll roles:")
    for row in cursor.fetchall():
        print(f"  - {row[0]} | {row[1]}")
    
    conn.close()
    
    print("\n" + "="*70)
    print("DIRECT INSERTION TEST COMPLETED!")
    print("="*70)

if __name__ == '__main__':
    test_direct_insertion()


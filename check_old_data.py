#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check Old Data - التحقق من البيانات القديمة
"""

import os
import sys
import sqlite3

def check_old_database():
    """Check what data exists in old erp_system.db"""
    
    db_path = 'erp_system.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    print("=" * 70)
    print("🔍 التحقق من البيانات القديمة - Checking Old Data")
    print("=" * 70)
    print()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check Products
    print("📦 Products:")
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    print(f"   Total: {count}")
    
    if count > 0:
        cursor.execute("SELECT name, sku FROM products LIMIT 5")
        for row in cursor.fetchall():
            print(f"   - {row[0]} ({row[1]})")
        if count > 5:
            print(f"   ... and {count - 5} more")
    print()
    
    # Check Categories
    print("📂 Categories:")
    cursor.execute("SELECT COUNT(*) FROM categories")
    count = cursor.fetchone()[0]
    print(f"   Total: {count}")
    
    if count > 0:
        cursor.execute("SELECT name FROM categories LIMIT 5")
        for row in cursor.fetchall():
            print(f"   - {row[0]}")
    print()
    
    # Check Warehouses
    print("🏪 Warehouses:")
    cursor.execute("SELECT COUNT(*) FROM warehouses")
    count = cursor.fetchone()[0]
    print(f"   Total: {count}")
    
    if count > 0:
        cursor.execute("SELECT name FROM warehouses")
        for row in cursor.fetchall():
            print(f"   - {row[0]}")
    print()
    
    # Check Customers
    print("👤 Customers:")
    cursor.execute("SELECT COUNT(*) FROM customers")
    count = cursor.fetchone()[0]
    print(f"   Total: {count}")
    
    if count > 0:
        cursor.execute("SELECT name FROM customers LIMIT 5")
        for row in cursor.fetchall():
            print(f"   - {row[0]}")
    print()
    
    # Check Suppliers
    print("🏭 Suppliers:")
    cursor.execute("SELECT COUNT(*) FROM suppliers")
    count = cursor.fetchone()[0]
    print(f"   Total: {count}")
    
    if count > 0:
        cursor.execute("SELECT name FROM suppliers LIMIT 5")
        for row in cursor.fetchall():
            print(f"   - {row[0]}")
    print()
    
    # Check Sales
    print("💰 Sales Invoices:")
    try:
        cursor.execute("SELECT COUNT(*) FROM sales_invoices")
        count = cursor.fetchone()[0]
        print(f"   Total: {count}")
    except:
        print("   Table not found")
    print()
    
    # Check Purchases
    print("🛒 Purchase Invoices:")
    try:
        cursor.execute("SELECT COUNT(*) FROM purchase_invoices")
        count = cursor.fetchone()[0]
        print(f"   Total: {count}")
    except:
        print("   Table not found")
    print()
    
    conn.close()
    
    print("=" * 70)
    print("✅ Old data check complete!")
    print("=" * 70)
    print()
    print("💡 Do you want to restore this data to the new tenant database?")
    print("   If yes, I can create a migration script.")

if __name__ == '__main__':
    check_old_database()


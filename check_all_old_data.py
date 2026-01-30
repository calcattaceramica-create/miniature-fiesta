#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check All Old Data - التحقق من جميع البيانات القديمة بالتفصيل
"""

import os
import sys
import sqlite3

def check_all_tables():
    """Check all tables in old erp_system.db"""
    
    db_path = 'erp_system.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    print("=" * 70)
    print("🔍 التحقق من جميع البيانات القديمة - Checking All Old Data")
    print("=" * 70)
    print()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print("📋 All Tables in Database:")
    print("-" * 70)
    
    for table in tables:
        table_name = table[0]
        
        # Skip system tables
        if table_name.startswith('sqlite_'):
            continue
        
        # Count rows
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        
        print(f"\n📊 {table_name}: {count} rows")
        
        if count > 0 and count <= 10:
            # Show sample data for small tables
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
            rows = cursor.fetchall()
            
            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            
            print(f"   Columns: {', '.join(columns)}")
            print(f"   Sample data:")
            for row in rows:
                print(f"   - {row}")
    
    print()
    print("=" * 70)
    print("✅ Complete table check done!")
    print("=" * 70)
    
    # Detailed check for important tables
    print()
    print("=" * 70)
    print("📊 DETAILED DATA CHECK")
    print("=" * 70)
    print()
    
    # Check sales_invoice_items
    print("🔍 Sales Invoice Items:")
    cursor.execute("SELECT COUNT(*) FROM sales_invoice_items")
    count = cursor.fetchone()[0]
    print(f"   Total: {count}")
    
    if count > 0:
        cursor.execute("""
            SELECT sii.id, si.invoice_number, p.name, sii.quantity, sii.total_amount
            FROM sales_invoice_items sii
            JOIN sales_invoices si ON sii.invoice_id = si.id
            JOIN products p ON sii.product_id = p.id
            LIMIT 10
        """)
        print("   Sample items:")
        for row in cursor.fetchall():
            print(f"   - Item {row[0]}: Invoice {row[1]}, Product: {row[2]}, Qty: {row[3]}, Total: {row[4]}")
    print()
    
    # Check stock movements
    try:
        cursor.execute("SELECT COUNT(*) FROM stock_movements")
        count = cursor.fetchone()[0]
        print(f"📦 Stock Movements: {count}")
        
        if count > 0:
            cursor.execute("""
                SELECT sm.id, sm.movement_type, p.name, sm.quantity, sm.created_at
                FROM stock_movements sm
                JOIN products p ON sm.product_id = p.id
                LIMIT 10
            """)
            print("   Sample movements:")
            for row in cursor.fetchall():
                print(f"   - {row[1]}: {row[2]}, Qty: {row[3]}, Date: {row[4]}")
    except:
        print("📦 Stock Movements: Table not found")
    print()
    
    # Check branches
    try:
        cursor.execute("SELECT COUNT(*) FROM branches")
        count = cursor.fetchone()[0]
        print(f"🏢 Branches: {count}")
        
        if count > 0:
            cursor.execute("SELECT id, name FROM branches")
            for row in cursor.fetchall():
                print(f"   - {row[1]}")
    except:
        print("🏢 Branches: Table not found")
    print()
    
    # Check users
    try:
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"👥 Users: {count}")
        
        if count > 0:
            cursor.execute("SELECT id, username, email FROM users")
            for row in cursor.fetchall():
                print(f"   - {row[1]} ({row[2]})")
    except:
        print("👥 Users: Table not found")
    print()
    
    conn.close()

if __name__ == '__main__':
    check_all_tables()


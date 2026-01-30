#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update all tenant databases to add description_en column to roles table
تحديث جميع قواعد بيانات المستأجرين لإضافة عمود description_en إلى جدول roles
"""

import sqlite3
import os
from pathlib import Path

def update_tenant_database(db_path):
    """Update a single tenant database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(roles)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'description_en' not in columns:
            # Add the column
            cursor.execute("ALTER TABLE roles ADD COLUMN description_en VARCHAR(256)")
            conn.commit()
            print(f"✅ Updated: {os.path.basename(db_path)}")
            return True
        else:
            print(f"⏭️  Skipped (already has column): {os.path.basename(db_path)}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {os.path.basename(db_path)}: {e}")
        return False
    finally:
        conn.close()

def main():
    """Update all tenant databases"""
    print("=" * 70)
    print("🔧 Updating all tenant databases")
    print("=" * 70)
    print()
    
    # Find all tenant databases
    tenant_dir = Path('tenant_databases')
    if not tenant_dir.exists():
        print("❌ tenant_databases directory not found!")
        return
    
    db_files = list(tenant_dir.glob('*.db'))
    
    if not db_files:
        print("❌ No tenant databases found!")
        return
    
    print(f"Found {len(db_files)} tenant databases")
    print()
    
    updated_count = 0
    for db_file in db_files:
        if update_tenant_database(str(db_file)):
            updated_count += 1
    
    print()
    print("=" * 70)
    print(f"✅ Updated {updated_count} databases")
    print(f"⏭️  Skipped {len(db_files) - updated_count} databases (already up-to-date)")
    print("=" * 70)

if __name__ == '__main__':
    main()


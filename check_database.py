"""
Quick script to check database status
"""
import sqlite3
from pathlib import Path

db_path = Path("erp_system.db")

print("=" * 60)
print("🔍 DATABASE CHECK")
print("=" * 60)
print()

if not db_path.exists():
    print("❌ Database not found!")
    exit(1)

print(f"✅ Database found: {db_path}")
print(f"📊 Database size: {db_path.stat().st_size} bytes")
print()

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Check tables
print("📋 Tables in database:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
for table in tables:
    print(f"  ✓ {table[0]}")
print()

# Check if licenses table exists
if ('licenses',) in tables:
    print("✅ Licenses table exists")
    cursor.execute("SELECT COUNT(*) FROM licenses")
    count = cursor.fetchone()[0]
    print(f"   📊 Number of licenses: {count}")
    print()
else:
    print("❌ Licenses table NOT found!")
    print()

# Check if users table has license_id column
if ('users',) in tables:
    print("✅ Users table exists")
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    if 'license_id' in column_names:
        print("   ✅ license_id column exists")
    else:
        print("   ❌ license_id column NOT found!")
    
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    print(f"   📊 Number of users: {count}")
    print()
else:
    print("❌ Users table NOT found!")
    print()

conn.close()

print("=" * 60)
print("✅ DATABASE CHECK COMPLETED")
print("=" * 60)


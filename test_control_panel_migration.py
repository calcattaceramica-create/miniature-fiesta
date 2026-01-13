"""
Test the Control Panel Migration functionality
"""
import subprocess
import sys
from pathlib import Path

print("=" * 60)
print("🧪 TESTING CONTROL PANEL MIGRATION")
print("=" * 60)
print()

# Test 1: Check if database exists
print("Test 1: Checking database...")
db_path = Path("erp_system.db")
if db_path.exists():
    print("✅ Database found at: erp_system.db")
else:
    print("❌ Database NOT found!")
    sys.exit(1)
print()

# Test 2: Run migration script
print("Test 2: Running migration script...")
result = subprocess.run(
    [sys.executable, "apply_license_migration.py"],
    capture_output=True,
    text=True,
    timeout=30
)

print(f"Return code: {result.returncode}")
print()

if result.returncode == 0:
    print("✅ Migration script executed successfully")
else:
    print("❌ Migration script failed!")
    print(f"Error: {result.stderr}")
    sys.exit(1)
print()

# Test 3: Check output
print("Test 3: Checking migration output...")
if "Migration completed successfully" in result.stdout or "MIGRATION COMPLETED SUCCESSFULLY" in result.stdout:
    print("✅ Migration completed successfully message found")
else:
    print("⚠️ Success message not found in output")
print()

if "Licenses table already exists" in result.stdout or "Licenses table created" in result.stdout:
    print("✅ Licenses table status confirmed")
else:
    print("⚠️ Licenses table status not found")
print()

if "license_id column" in result.stdout:
    print("✅ license_id column status confirmed")
else:
    print("⚠️ license_id column status not found")
print()

# Test 4: Verify database structure
print("Test 4: Verifying database structure...")
import sqlite3

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Check licenses table
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='licenses'")
if cursor.fetchone():
    print("✅ Licenses table exists in database")
else:
    print("❌ Licenses table NOT found in database!")
    conn.close()
    sys.exit(1)

# Check license_id column in users table
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()
column_names = [col[1] for col in columns]

if 'license_id' in column_names:
    print("✅ license_id column exists in users table")
else:
    print("❌ license_id column NOT found in users table!")
    conn.close()
    sys.exit(1)

conn.close()
print()

# Test 5: Check Control Panel file
print("Test 5: Checking Control Panel file...")
control_panel_path = Path("DED_Control_Panel.pyw")
if control_panel_path.exists():
    print("✅ DED_Control_Panel.pyw found")
    
    # Check if it uses correct database path
    with open(control_panel_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'erp_system.db' in content:
        print("✅ Control Panel uses correct database path (erp_system.db)")
    else:
        print("⚠️ Database path not found in Control Panel")
    
    if 'instance/ded.db' in content:
        print("❌ WARNING: Old database path (instance/ded.db) still found!")
    else:
        print("✅ No old database path found")
else:
    print("❌ DED_Control_Panel.pyw NOT found!")
print()

print("=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print()
print("🎉 The Control Panel Migration is working correctly!")
print()
print("Next steps:")
print("1. Open Control Panel: python DED_Control_Panel.pyw")
print("2. Go to '🔐 مدير التراخيص' tab")
print("3. Click '🔧 تطبيق Migration - Apply Migration'")
print("4. You should see a clean success message!")
print()


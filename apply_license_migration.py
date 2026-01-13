# -*- coding: utf-8 -*-
"""
Script to apply license system migration to existing database
"""
import sqlite3
from pathlib import Path
from datetime import datetime
import sys

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def apply_migration():
    db_path = Path("erp_system.db")

    if not db_path.exists():
        print("=" * 60)
        print("❌ DATABASE NOT FOUND!")
        print("=" * 60)
        print()
        print("⚠️  The database file does not exist at:")
        print(f"   {db_path.absolute()}")
        print()
        print("📋 To fix this issue:")
        print("   1. Go to 'App Control' tab in the Control Panel")
        print("   2. Click 'Start Application' button")
        print("   3. Wait for the application to start")
        print("   4. The database will be created automatically")
        print("   5. Then try applying the migration again")
        print()
        print("=" * 60)
        return False

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Check if licenses table exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='licenses'
        """)

        if cursor.fetchone():
            print("✅ Licenses table already exists")
        else:
            print("🔧 Creating licenses table...")

            # Create licenses table
            cursor.execute("""
                CREATE TABLE licenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    license_key VARCHAR(64) NOT NULL UNIQUE,
                    company_name VARCHAR(128) NOT NULL,
                    machine_id VARCHAR(32),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    expiry_date DATETIME NOT NULL,
                    duration_days INTEGER DEFAULT 365,
                    license_type VARCHAR(32) DEFAULT 'Standard',
                    max_users INTEGER DEFAULT 10,
                    features TEXT DEFAULT 'all',
                    status VARCHAR(20) DEFAULT 'active',
                    activation_count INTEGER DEFAULT 0,
                    last_check DATETIME,
                    contact_email VARCHAR(120),
                    contact_phone VARCHAR(20),
                    notes TEXT
                )
            """)

            # Create index
            cursor.execute("""
                CREATE UNIQUE INDEX ix_licenses_license_key
                ON licenses (license_key)
            """)

            print("✅ Licenses table created successfully")

        # Check if users table has license_id column
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]

        if 'license_id' in columns:
            print("✅ Users table already has license_id column")
        else:
            print("🔧 Adding license_id column to users table...")

            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN license_id INTEGER
                REFERENCES licenses(id)
            """)

            print("✅ license_id column added to users table successfully")

        conn.commit()
        conn.close()

        print()
        print("=" * 60)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("📋 What was done:")
        print("   ✓ Licenses table created/verified")
        print("   ✓ Users table updated with license_id column")
        print()
        print("🎉 You can now use the license system!")
        print("=" * 60)
        return True

    except Exception as e:
        print()
        print("=" * 60)
        print("❌ MIGRATION FAILED!")
        print("=" * 60)
        print()
        print(f"Error: {e}")
        print()
        import traceback
        traceback.print_exc()
        print()
        print("=" * 60)
        return False

if __name__ == "__main__":
    print()
    print("=" * 60)
    print("🚀 LICENSE SYSTEM MIGRATION")
    print("=" * 60)
    print()

    success = apply_migration()

    if not success:
        print()
        print("💡 Need help? Check the instructions above.")
        print()


"""
Test script for the integrated license system
Tests database integration and user creation
"""
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

def test_license_system():
    """Test the license system integration"""

    print("=" * 60)
    print("🧪 Testing Integrated License System")
    print("=" * 60)
    print()

    db_path = Path("erp_system.db")

    if not db_path.exists():
        print("❌ Database not found. Please run the app first.")
        return False
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Test 1: Check if licenses table exists
        print("📝 Test 1: Checking licenses table...")
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='licenses'
        """)
        if cursor.fetchone():
            print("✅ Licenses table exists")
        else:
            print("❌ Licenses table not found")
            return False
        
        # Test 2: Check if users table has license_id column
        print("\n📝 Test 2: Checking users table structure...")
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'license_id' in columns:
            print("✅ Users table has license_id column")
        else:
            print("❌ Users table missing license_id column")
            return False
        
        # Test 3: Count licenses
        print("\n📝 Test 3: Counting licenses...")
        cursor.execute("SELECT COUNT(*) FROM licenses")
        license_count = cursor.fetchone()[0]
        print(f"✅ Found {license_count} license(s)")
        
        # Test 4: Count users with licenses
        print("\n📝 Test 4: Counting users with licenses...")
        cursor.execute("SELECT COUNT(*) FROM users WHERE license_id IS NOT NULL")
        users_with_license = cursor.fetchone()[0]
        print(f"✅ Found {users_with_license} user(s) with license")
        
        # Test 5: Show sample data
        if license_count > 0:
            print("\n📝 Test 5: Sample license data...")
            cursor.execute("""
                SELECT l.company_name, l.status, l.expiry_date, u.username
                FROM licenses l
                LEFT JOIN users u ON u.license_id = l.id
                LIMIT 3
            """)
            for row in cursor.fetchall():
                company, status, expiry, username = row
                print(f"  - Company: {company}")
                print(f"    Status: {status}")
                print(f"    Expiry: {expiry}")
                print(f"    User: {username or 'No user'}")
                print()
        
        # Test 6: Check for expired licenses
        print("📝 Test 6: Checking for expired licenses...")
        cursor.execute("""
            SELECT COUNT(*) FROM licenses 
            WHERE expiry_date < datetime('now')
        """)
        expired_count = cursor.fetchone()[0]
        if expired_count > 0:
            print(f"⚠️  Found {expired_count} expired license(s)")
        else:
            print("✅ No expired licenses")
        
        # Test 7: Check for active licenses
        print("\n📝 Test 7: Checking for active licenses...")
        cursor.execute("""
            SELECT COUNT(*) FROM licenses 
            WHERE status = 'active' AND expiry_date > datetime('now')
        """)
        active_count = cursor.fetchone()[0]
        print(f"✅ Found {active_count} active license(s)")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_license_system()


"""
Detailed Multi-Tenant Testing Script
اختبار شامل لنظام Multi-Tenancy
"""
from app import create_app, db
from app.models import User
from app.models_license import License
from flask import session
import sys

def test_login_with_license(app, username, password, license_key):
    """Test login with specific license"""
    with app.test_client() as client:

        # Step 1: Logout first
        print(f"\n{'='*60}")
        print(f"🔄 Logging out first...")
        logout_response = client.get('/auth/logout', follow_redirects=True)
        print(f"✅ Logout status: {logout_response.status_code}")

        # Step 2: Login
        print(f"\n🔐 Logging in with:")
        print(f"   Username: {username}")
        print(f"   License: {license_key}")

        login_data = {
            'username': username,
            'password': password,
            'license_key': license_key,
            'remember': False
        }

        login_response = client.post(
            '/auth/login',
            data=login_data,
            follow_redirects=True
        )

        print(f"✅ Login status: {login_response.status_code}")

        if login_response.status_code != 200:
            print(f"❌ Login failed!")
            return False

        # Step 3: Check what's in session
        with client.session_transaction() as sess:
            tenant_key = sess.get('tenant_license_key')
            print(f"\n🔍 Session tenant_license_key: {tenant_key}")
            if tenant_key == license_key:
                print(f"✅ Session has CORRECT license key!")
            else:
                print(f"❌ Session has WRONG license key! Expected: {license_key}, Got: {tenant_key}")

        # Step 4: Check database URI
        print(f"\n💾 Current database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
        expected_uri = f"sqlite:///C:\\Users\\DELL\\DED\\tenant_databases\\tenant_{license_key.replace('-', '_')}.db"
        if expected_uri in app.config.get('SQLALCHEMY_DATABASE_URI', ''):
            print(f"✅ Database URI is CORRECT!")
        else:
            print(f"❌ Database URI is WRONG!")
            print(f"   Expected: {expected_uri}")

        # Step 5: Check license status page
        print(f"\n📋 Checking license status page...")
        license_response = client.get('/security/license', follow_redirects=True)

        if license_response.status_code == 200:
            response_text = license_response.data.decode('utf-8')
            if license_key in response_text:
                print(f"✅ License page shows CORRECT license: {license_key}")
            else:
                print(f"❌ License page does NOT show license: {license_key}")
                if "CEC9-79EE-C42F-2DAD" in response_text:
                    print(f"⚠️  Found license: CEC9-79EE-C42F-2DAD")
                if "260D-F983-F5D0-73E4" in response_text:
                    print(f"⚠️  Found license: 260D-F983-F5D0-73E4")
        else:
            print(f"❌ License page failed: {license_response.status_code}")

        # Step 6: Query users directly from database
        print(f"\n👥 Querying users from database...")
        users = User.query.all()
        print(f"✅ Found {len(users)} users in current database")
        for user in users[:3]:  # Show first 3 users
            print(f"   - {user.username} (ID: {user.id})")

        return True

def main():
    print("="*60)
    print("🧪 MULTI-TENANT TESTING SCRIPT")
    print("="*60)

    # Create app
    app = create_app()

    with app.app_context():
        # Test 1: Login with first license
        print("\n\n" + "="*60)
        print("TEST 1: Login with License CEC9-79EE-C42F-2DAD")
        print("="*60)
        result1 = test_login_with_license(app, "admin", "admin123", "CEC9-79EE-C42F-2DAD")

        # Test 2: Login with second license
        print("\n\n" + "="*60)
        print("TEST 2: Login with License 260D-F983-F5D0-73E4")
        print("="*60)
        result2 = test_login_with_license(app, "admin", "admin123", "260D-F983-F5D0-73E4")

        # Test 3: Login back to first license
        print("\n\n" + "="*60)
        print("TEST 3: Login BACK to License CEC9-79EE-C42F-2DAD")
        print("="*60)
        result3 = test_login_with_license(app, "admin", "admin123", "CEC9-79EE-C42F-2DAD")

        print("\n\n" + "="*60)
        print("🏁 TESTING COMPLETE")
        print("="*60)
        print("\n📊 Summary:")
        if result1 and result2 and result3:
            print("   ✅ All tests completed!")
        else:
            print("   ❌ Some tests failed!")
        print("   - Check the output above for details")
        print("="*60)

if __name__ == "__main__":
    main()


"""
Quick script to test license login
"""
from app import create_app, db
from app.models_license import License
from app.models import User
from werkzeug.security import check_password_hash

app = create_app('development')

with app.app_context():
    # Test data
    license_key = "9813-26D0-F98D-741C"
    username = "mohammed"
    password = "121212"
    
    print("=" * 60)
    print("TESTING LICENSE LOGIN")
    print("=" * 60)
    
    # Step 1: Find license
    print(f"\n1. Looking for license: {license_key}")
    license = License.query.filter_by(license_key=license_key).first()
    
    if not license:
        print("   ❌ License NOT FOUND!")
    else:
        print(f"   ✅ License FOUND!")
        print(f"   - Client: {license.client_name}")
        print(f"   - Admin Username: {license.admin_username}")
        print(f"   - Is Active: {license.is_active}")
        print(f"   - Expires: {license.expires_at}")
        
        # Step 2: Check validity
        print(f"\n2. Checking license validity...")
        is_valid, message = license.is_valid()
        print(f"   - Valid: {is_valid}")
        print(f"   - Message: {message}")
        
        # Step 3: Check username match
        print(f"\n3. Checking username match...")
        print(f"   - Provided username: {username}")
        print(f"   - License admin username: {license.admin_username}")
        if username == license.admin_username:
            print(f"   ✅ Username MATCHES!")
        else:
            print(f"   ❌ Username DOES NOT MATCH!")
        
        # Step 4: Check if user exists
        print(f"\n4. Checking if user exists...")
        user = User.query.filter_by(username=username).first()
        if user:
            print(f"   ✅ User EXISTS in database")
            print(f"   - User ID: {user.id}")
            print(f"   - Full Name: {user.full_name}")
            print(f"   - Is Active: {user.is_active}")
            print(f"   - Is Admin: {user.is_admin}")
            
            # Check password
            print(f"\n5. Checking password...")
            if user.check_password(password):
                print(f"   ✅ Password CORRECT!")
            else:
                print(f"   ❌ Password INCORRECT!")
        else:
            print(f"   ℹ️  User DOES NOT EXIST (will be created on first login)")
            
            # Check password against license
            print(f"\n5. Checking password against license...")
            if check_password_hash(license.admin_password_hash, password):
                print(f"   ✅ Password MATCHES license admin password!")
            else:
                print(f"   ❌ Password DOES NOT MATCH license admin password!")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


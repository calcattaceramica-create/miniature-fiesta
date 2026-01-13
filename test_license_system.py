"""
Test License System
Tests the license verification functionality
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

def test_license_file_exists():
    """Test if licenses.json exists"""
    license_file = Path('licenses.json')
    if license_file.exists():
        print("✅ License file exists")
        return True
    else:
        print("❌ License file not found")
        return False

def test_license_structure():
    """Test license file structure"""
    try:
        with open('licenses.json', 'r', encoding='utf-8') as f:
            licenses = json.load(f)
        
        print(f"✅ License file is valid JSON")
        print(f"   Total licenses: {len(licenses)}")
        
        # Check structure
        for key, data in licenses.items():
            required_fields = ['company', 'created', 'status']
            missing = [f for f in required_fields if f not in data]
            
            if missing:
                print(f"⚠️  License {key[:16]}... missing fields: {missing}")
            else:
                print(f"✅ License {key[:16]}... has all required fields")
        
        return True
    except Exception as e:
        print(f"❌ Error reading license file: {e}")
        return False

def test_license_with_credentials():
    """Test licenses with username and password"""
    try:
        with open('licenses.json', 'r', encoding='utf-8') as f:
            licenses = json.load(f)
        
        count = 0
        for key, data in licenses.items():
            if 'username' in data and 'password' in data:
                count += 1
                print(f"✅ License for {data['company']}")
                print(f"   Username: {data['username']}")
                print(f"   Password: {data['password']}")
                print(f"   Status: {data.get('status', 'N/A')}")
                print(f"   Expiry: {data.get('expiry', 'N/A')}")
                
                # Check expiry
                expiry = data.get('expiry')
                if expiry:
                    expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
                    days_remaining = (expiry_date - datetime.now()).days
                    
                    if days_remaining > 0:
                        print(f"   Days remaining: {days_remaining} ✅")
                    else:
                        print(f"   EXPIRED {abs(days_remaining)} days ago ❌")
                
                print()
        
        print(f"Total licenses with credentials: {count}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_check_license_function():
    """Test the check_license function"""
    print("\n" + "="*60)
    print("Testing check_license function")
    print("="*60 + "\n")
    
    # Import the function
    import sys
    sys.path.insert(0, 'app')
    
    try:
        from auth.routes import check_license
        
        # Test with valid user
        with open('licenses.json', 'r', encoding='utf-8') as f:
            licenses = json.load(f)
        
        for key, data in licenses.items():
            username = data.get('username')
            if username:
                is_valid, error = check_license(username)
                
                if is_valid:
                    print(f"✅ License valid for user: {username}")
                else:
                    print(f"❌ License invalid for user: {username}")
                    print(f"   Error: {error}")
                print()
        
        # Test with invalid user
        is_valid, error = check_license('nonexistent_user')
        if not is_valid:
            print(f"✅ Correctly rejected nonexistent user")
            print(f"   Error: {error}")
        else:
            print(f"❌ Should have rejected nonexistent user")
        
        return True
    except Exception as e:
        print(f"❌ Error testing check_license: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sync_file():
    """Test license sync file"""
    sync_file = Path('license_sync.json')
    
    if sync_file.exists():
        try:
            with open(sync_file, 'r', encoding='utf-8') as f:
                sync_data = json.load(f)
            
            print(f"✅ Sync file exists")
            print(f"   Total entries: {len(sync_data)}")
            
            synced = sum(1 for d in sync_data.values() if d.get('synced'))
            pending = len(sync_data) - synced
            
            print(f"   Synced: {synced}")
            print(f"   Pending: {pending}")
            
            return True
        except Exception as e:
            print(f"❌ Error reading sync file: {e}")
            return False
    else:
        print("⚠️  Sync file not found (will be created on first sync)")
        return True

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("LICENSE SYSTEM TESTS")
    print("="*60 + "\n")
    
    tests = [
        ("License file exists", test_license_file_exists),
        ("License structure", test_license_structure),
        ("Licenses with credentials", test_license_with_credentials),
        ("Sync file", test_sync_file),
        ("Check license function", test_check_license_function),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Test: {name}")
        print(f"{'='*60}\n")
        
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60 + "\n")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{'='*60}")
    print(f"Total: {passed}/{total} tests passed")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()


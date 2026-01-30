"""Quick test for supplier reports after permission fix"""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

app = create_app()

with app.test_client() as client:
    print("=" * 70)
    print("🧪 Quick Test - Supplier Reports Permission Fix")
    print("=" * 70)
    
    # Login
    print("\n🔐 Logging in...")
    response = client.post('/auth/login', data={
        'license_key': 'CEC9-79EE-C42F-2DAD',
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)
    
    if response.status_code == 200:
        print("✅ Login successful")
    else:
        print(f"❌ Login failed with status {response.status_code}")
        sys.exit(1)
    
    # Test each supplier report
    reports = [
        ('/reports/suppliers', 'Suppliers List'),
        ('/reports/suppliers/top', 'Top Suppliers'),
        ('/reports/suppliers/balances', 'Supplier Balances'),
        ('/reports/suppliers/history/1', 'Supplier History')
    ]
    
    all_passed = True
    
    for url, name in reports:
        print(f"\n📊 Testing {name}...")
        response = client.get(url)
        
        if response.status_code == 200:
            print(f"✅ {name} - Status: 200 OK")
        elif response.status_code == 403:
            print(f"❌ {name} - Status: 403 Forbidden (Permission denied)")
            all_passed = False
        else:
            print(f"⚠️  {name} - Status: {response.status_code}")
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    print("=" * 70)


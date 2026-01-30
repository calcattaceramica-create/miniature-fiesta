"""Test Monthly Purchases Report with CSS"""
import sys
from app import create_app

print("=" * 70)
print("🧪 Testing Monthly Purchases Report with CSS")
print("=" * 70)

app = create_app()

with app.test_client() as client:
    # Login first
    print("\n🔐 Logging in...")
    response = client.post('/auth/login', data={
        'username': 'admin',
        'password': 'admin123',
        'license_key': 'CEC9-79EE-C42F-2DAD'
    }, follow_redirects=True)
    
    if response.status_code == 200:
        print("✅ Login successful")
    else:
        print(f"❌ Login failed: {response.status_code}")
        sys.exit(1)
    
    # Test the monthly report
    print("\n📊 Testing Monthly Purchases Report...")
    response = client.get('/reports/purchases-monthly')
    
    print(f"\nStatus code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCESS - Report is working!")
        
        html = response.data.decode('utf-8')
        
        # Check for CSS
        print("\n🎨 Checking CSS:")
        print("-" * 70)
        if 'bg-gradient-primary' in html:
            print("✅ bg-gradient-primary CSS: Found")
        else:
            print("❌ bg-gradient-primary CSS: NOT FOUND")
        
        if 'bg-gradient-success' in html:
            print("✅ bg-gradient-success CSS: Found")
        else:
            print("❌ bg-gradient-success CSS: NOT FOUND")
        
        if 'bg-gradient-info' in html:
            print("✅ bg-gradient-info CSS: Found")
        else:
            print("❌ bg-gradient-info CSS: NOT FOUND")
        
        if 'linear-gradient' in html:
            print("✅ linear-gradient: Found")
        else:
            print("❌ linear-gradient: NOT FOUND")
        
        # Check for data
        print("\n📊 Checking Data:")
        print("-" * 70)
        if 'إجمالي الفواتير' in html or 'Total Invoices' in html:
            print("✅ Total Invoices label: Found")
        else:
            print("❌ Total Invoices label: NOT FOUND")
        
        if 'إجمالي المشتريات' in html or 'Total Purchases' in html:
            print("✅ Total Purchases label: Found")
        else:
            print("❌ Total Purchases label: NOT FOUND")
        
        if 'إجمالي الضريبة' in html or 'Total Tax' in html:
            print("✅ Total Tax label: Found")
        else:
            print("❌ Total Tax label: NOT FOUND")
        
        if '€' in html or 'EUR' in html:
            print("✅ EUR currency symbol: Found")
        else:
            print("❌ EUR currency symbol: NOT FOUND")
        
        # Check for icons
        print("\n🎨 Checking Icons:")
        print("-" * 70)
        if 'fa-file-invoice' in html:
            print("✅ Invoice icon: Found")
        else:
            print("❌ Invoice icon: NOT FOUND")
        
        if 'fa-shopping-cart' in html:
            print("✅ Shopping cart icon: Found")
        else:
            print("❌ Shopping cart icon: NOT FOUND")
        
        if 'fa-percentage' in html:
            print("✅ Percentage icon: Found")
        else:
            print("❌ Percentage icon: NOT FOUND")
        
    else:
        print(f"❌ FAILED - Status code: {response.status_code}")

print("\n" + "=" * 70)
print("✅ Test Complete!")
print("=" * 70)


"""
Test script for supplier reports
"""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Supplier, PurchaseInvoice
from flask import url_for

def test_supplier_reports():
    """Test all supplier reports"""
    app = create_app()
    
    with app.app_context():
        with app.test_client() as client:
            print("=" * 70)
            print("🧪 Testing Supplier Reports")
            print("=" * 70)
            
            # Login first
            print("\n🔐 Logging in...")
            response = client.post('/auth/login', data={
                'license_key': 'CEC9-79EE-C42F-2DAD',
                'username': 'admin',
                'password': 'admin123'
            }, follow_redirects=True)
            
            if response.status_code == 200:
                print("✅ Login successful")
            else:
                print(f"❌ Login failed with status code: {response.status_code}")
                return
            
            # Test 1: Suppliers List Report
            print("\n📊 Testing Suppliers List Report...")
            response = client.get('/reports/suppliers')
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                html = response.data.decode('utf-8')
                
                # Check for key elements
                checks = {
                    'Total Suppliers card': 'Total Suppliers' in html or 'إجمالي الموردين' in html,
                    'Total Balance card': 'Total Balance' in html or 'إجمالي الأرصدة' in html,
                    'Active Suppliers card': 'Active Suppliers' in html or 'الموردين النشطين' in html,
                    'EUR currency symbol': '€' in html,
                    'Gradient CSS': 'bg-gradient-primary' in html,
                    'Truck icon': 'fa-truck' in html,
                    'Suppliers table': 'table' in html,
                }
                
                print("\n🎨 Checking elements:")
                print("-" * 70)
                for check_name, result in checks.items():
                    status = "✅" if result else "❌"
                    print(f"{status} {check_name}: {'Found' if result else 'Not found'}")
                
                if all(checks.values()):
                    print("\n✅ SUCCESS - Suppliers List Report is working!")
                else:
                    print("\n⚠️  WARNING - Some elements are missing")
            else:
                print(f"❌ FAILED - Status code: {response.status_code}")
            
            # Test 2: Top Suppliers Report
            print("\n📊 Testing Top Suppliers Report...")
            response = client.get('/reports/suppliers/top')
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                html = response.data.decode('utf-8')
                
                checks = {
                    'Total Suppliers card': 'Total Suppliers' in html or 'إجمالي الموردين' in html,
                    'Total Purchases card': 'Total Purchases' in html or 'إجمالي المشتريات' in html,
                    'EUR currency symbol': '€' in html,
                    'Trophy icon': 'fa-trophy' in html,
                    'Rank badges': 'rank-badge' in html or 'badge' in html,
                    'Progress bar': 'progress-bar' in html,
                }
                
                print("\n🎨 Checking elements:")
                print("-" * 70)
                for check_name, result in checks.items():
                    status = "✅" if result else "❌"
                    print(f"{status} {check_name}: {'Found' if result else 'Not found'}")
                
                if all(checks.values()):
                    print("\n✅ SUCCESS - Top Suppliers Report is working!")
                else:
                    print("\n⚠️  WARNING - Some elements are missing")
            else:
                print(f"❌ FAILED - Status code: {response.status_code}")
            
            # Test 3: Supplier Balances Report
            print("\n📊 Testing Supplier Balances Report...")
            response = client.get('/reports/suppliers/balances')
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                html = response.data.decode('utf-8')
                
                checks = {
                    'Total Payable card': 'Total Payable' in html or 'إجمالي المستحق' in html,
                    'Total Receivable card': 'Total Receivable' in html or 'إجمالي المدين' in html,
                    'Net Balance card': 'Net Balance' in html or 'صافي الرصيد' in html,
                    'EUR currency symbol': '€' in html,
                    'Balance scale icon': 'fa-balance-scale' in html,
                    'Status badges': 'badge' in html,
                }
                
                print("\n🎨 Checking elements:")
                print("-" * 70)
                for check_name, result in checks.items():
                    status = "✅" if result else "❌"
                    print(f"{status} {check_name}: {'Found' if result else 'Not found'}")
                
                if all(checks.values()):
                    print("\n✅ SUCCESS - Supplier Balances Report is working!")
                else:
                    print("\n⚠️  WARNING - Some elements are missing")
            else:
                print(f"❌ FAILED - Status code: {response.status_code}")
            
            # Test 4: Check if we have suppliers in database
            print("\n📊 Checking database for suppliers...")
            suppliers = Supplier.query.filter_by(is_active=True).all()
            print(f"Found {len(suppliers)} active suppliers in database")
            
            if suppliers:
                # Test Supplier History Report with first supplier
                supplier_id = suppliers[0].id
                print(f"\n📊 Testing Supplier History Report for supplier ID {supplier_id}...")
                response = client.get(f'/reports/suppliers/history/{supplier_id}')
                print(f"Status code: {response.status_code}")
                
                if response.status_code == 200:
                    html = response.data.decode('utf-8')
                    
                    checks = {
                        'Total Invoices card': 'Total Invoices' in html or 'إجمالي الفواتير' in html,
                        'Total Purchases card': 'Total Purchases' in html or 'إجمالي المشتريات' in html,
                        'Total Paid card': 'Total Paid' in html or 'إجمالي المدفوع' in html,
                        'EUR currency symbol': '€' in html,
                        'Supplier info': 'supplier-info' in html,
                        'History icon': 'fa-history' in html,
                    }
                    
                    print("\n🎨 Checking elements:")
                    print("-" * 70)
                    for check_name, result in checks.items():
                        status = "✅" if result else "❌"
                        print(f"{status} {check_name}: {'Found' if result else 'Not found'}")
                    
                    if all(checks.values()):
                        print("\n✅ SUCCESS - Supplier History Report is working!")
                    else:
                        print("\n⚠️  WARNING - Some elements are missing")
                else:
                    print(f"❌ FAILED - Status code: {response.status_code}")
            else:
                print("⚠️  No suppliers found in database - skipping history report test")
            
            print("\n" + "=" * 70)
            print("✅ Test Complete!")
            print("=" * 70)

if __name__ == '__main__':
    test_supplier_reports()


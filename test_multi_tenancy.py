"""
Test Multi-Tenancy System
اختبار نظام Multi-Tenancy

هذا السكريبت يقوم بإنشاء ترخيصين واختبار العزل بينهما
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models_license import License
from app.models import User, Product
from app.tenant_manager import TenantManager
from app.license_manager import LicenseManager

def test_multi_tenancy():
    """Test multi-tenancy system"""
    
    print("=" * 70)
    print("🧪 Testing Multi-Tenancy System")
    print("=" * 70)
    print()
    
    # Create app
    app = create_app()
    
    # Switch to master database
    master_db_uri = f'sqlite:///{TenantManager.get_master_db_path()}'
    app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri
    
    with app.app_context():
        # Create two test licenses
        print("📝 Creating test licenses...")
        print()
        
        # License 1
        license1 = LicenseManager.create_license(
            client_name="Test Client 1",
            client_email="client1@test.com",
            client_phone="1234567890",
            client_company="Test Company 1",
            license_type="trial",
            max_users=5,
            max_branches=2,
            duration_days=30,
            admin_username="admin1",
            admin_password="password1"
        )
        print(f"✅ License 1 created: {license1.license_key}")
        
        # Create tenant database for license 1
        TenantManager.create_tenant_database(license1.license_key, app)
        TenantManager.initialize_tenant_data(license1.license_key, app, license1)
        print(f"   🗄️  Tenant database created and initialized")
        print()
        
        # License 2
        license2 = LicenseManager.create_license(
            client_name="Test Client 2",
            client_email="client2@test.com",
            client_phone="0987654321",
            client_company="Test Company 2",
            license_type="monthly",
            max_users=10,
            max_branches=3,
            duration_days=30,
            admin_username="admin2",
            admin_password="password2"
        )
        print(f"✅ License 2 created: {license2.license_key}")
        
        # Create tenant database for license 2
        TenantManager.create_tenant_database(license2.license_key, app)
        TenantManager.initialize_tenant_data(license2.license_key, app, license2)
        print(f"   🗄️  Tenant database created and initialized")
        print()
        
        # Test isolation
        print("=" * 70)
        print("🔍 Testing Data Isolation")
        print("=" * 70)
        print()
        
        # Add product to license 1
        print(f"📦 Adding product to License 1 ({license1.license_key})...")
        TenantManager.switch_tenant_database(app, license1.license_key)
        
        with app.app_context():
            product1 = Product(
                name="Product from License 1",
                sku="PROD-L1-001",
                barcode="123456789",
                category="Test Category",
                unit="piece",
                cost_price=10.0,
                selling_price=15.0,
                stock_quantity=100
            )
            db.session.add(product1)
            db.session.commit()
            
            count1 = Product.query.count()
            print(f"   ✅ Product added. Total products in License 1: {count1}")
        print()
        
        # Check products in license 2
        print(f"🔍 Checking products in License 2 ({license2.license_key})...")
        TenantManager.switch_tenant_database(app, license2.license_key)
        
        with app.app_context():
            count2 = Product.query.count()
            print(f"   📊 Total products in License 2: {count2}")
            
            if count2 == 0:
                print(f"   ✅ SUCCESS! License 2 has no products (isolated from License 1)")
            else:
                print(f"   ❌ FAILED! License 2 has {count2} products (should be 0)")
        print()
        
        # Summary
        print("=" * 70)
        print("📊 Test Summary")
        print("=" * 70)
        print(f"License 1: {license1.license_key}")
        print(f"   Client: {license1.client_name}")
        print(f"   Admin: {license1.admin_username}")
        print(f"   Database: tenant_{license1.license_key.replace('-', '_')}.db")
        print()
        print(f"License 2: {license2.license_key}")
        print(f"   Client: {license2.client_name}")
        print(f"   Admin: {license2.admin_username}")
        print(f"   Database: tenant_{license2.license_key.replace('-', '_')}.db")
        print()
        
        if count2 == 0:
            print("🎉 Multi-Tenancy is working correctly!")
            print("   Each license has its own isolated database.")
        else:
            print("⚠️  Multi-Tenancy test failed!")
            print("   Licenses are sharing data.")
        
        print()
        print("=" * 70)

if __name__ == '__main__':
    try:
        test_multi_tenancy()
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERROR:")
        print("=" * 70)
        print(str(e))
        print()
        import traceback
        traceback.print_exc()
        print()
        print("=" * 70)


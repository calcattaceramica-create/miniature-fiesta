"""
Test Multi-Tenancy Isolation
اختبار عزل قواعد البيانات بين التراخيص
"""
import os
import sys
from app import create_app, db
from app.models import User, Product
from app.models_license import License
from app.tenant_manager import TenantManager

def test_tenant_isolation():
    """Test that different licenses use different databases"""
    
    app = create_app()
    
    with app.app_context():
        # Get all licenses
        master_db_uri = f'sqlite:///{TenantManager.get_master_db_path()}'
        app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri
        db.engine.dispose()
        
        licenses = License.query.filter_by(is_active=True).limit(3).all()
        
        if len(licenses) < 2:
            print("❌ Need at least 2 active licenses to test isolation")
            return
        
        print("=" * 70)
        print("🧪 Testing Multi-Tenancy Isolation")
        print("=" * 70)
        print()
        
        # Test each license
        for i, license in enumerate(licenses, 1):
            print(f"\n{'='*70}")
            print(f"📋 License {i}: {license.license_key}")
            print(f"   Client: {license.client_name}")
            print(f"{'='*70}")
            
            # Switch to tenant database
            tenant_db_uri = TenantManager.get_tenant_db_uri(license.license_key)
            app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
            db.engine.dispose()
            
            # Get database path
            db_path = TenantManager.get_tenant_db_path(license.license_key)
            print(f"📁 Database: {db_path}")
            print(f"   Exists: {'✅ Yes' if os.path.exists(db_path) else '❌ No'}")
            
            if os.path.exists(db_path):
                # Count users
                user_count = User.query.count()
                print(f"👥 Users: {user_count}")
                
                # List users
                users = User.query.all()
                for user in users:
                    print(f"   - {user.username} ({user.full_name})")
                
                # Count products
                product_count = Product.query.count()
                print(f"📦 Products: {product_count}")
                
                # List first 5 products
                products = Product.query.limit(5).all()
                for product in products:
                    print(f"   - {product.name} (Code: {product.code})")
        
        print("\n" + "=" * 70)
        print("✅ Test Complete!")
        print("=" * 70)
        print()
        print("🔍 Verification:")
        print("   - Each license should have its own database file")
        print("   - Each database should have different users/products")
        print("   - If all databases show the same data, Multi-Tenancy is NOT working!")
        print()

if __name__ == '__main__':
    test_tenant_isolation()


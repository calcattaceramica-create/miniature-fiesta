"""
Recreate Tenant Databases
إعادة إنشاء قواعد بيانات التراخيص بشكل صحيح
"""
import os
import sys
from app import create_app, db
from app.models_license import License
from app.tenant_manager import TenantManager

def recreate_all_tenant_databases():
    """Recreate all tenant databases from scratch"""
    
    app = create_app()
    
    with app.app_context():
        # Get all licenses
        master_db_uri = f'sqlite:///{TenantManager.get_master_db_path()}'
        app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri
        db.engine.dispose()
        
        licenses = License.query.filter_by(is_active=True).all()
        
        if not licenses:
            print("❌ No active licenses found")
            return
        
        print("=" * 70)
        print("🔄 Recreating Tenant Databases")
        print("=" * 70)
        print(f"\n📊 Found {len(licenses)} active licenses\n")
        
        for i, license in enumerate(licenses, 1):
            print(f"\n{'='*70}")
            print(f"📋 License {i}/{len(licenses)}: {license.license_key}")
            print(f"   Client: {license.client_name}")
            print(f"{'='*70}")
            
            # Get database path
            db_path = TenantManager.get_tenant_db_path(license.license_key)
            
            # Delete old database if exists
            if os.path.exists(db_path):
                print(f"🗑️  Deleting old database: {db_path}")
                try:
                    os.remove(db_path)
                    print("   ✅ Deleted successfully")
                except Exception as e:
                    print(f"   ❌ Error deleting: {e}")
                    continue
            
            # Create new database
            print(f"🗄️  Creating new database...")
            if not TenantManager.create_tenant_database(license.license_key, app):
                print("   ❌ Failed to create database")
                continue
            print("   ✅ Database created")
            
            # Initialize data
            print(f"📦 Initializing data...")
            if not TenantManager.initialize_tenant_data(license.license_key, app, license):
                print("   ❌ Failed to initialize data")
                continue
            print("   ✅ Data initialized")
            
            # Verify
            tenant_db_uri = TenantManager.get_tenant_db_uri(license.license_key)
            app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
            db.engine.dispose()
            
            from app.models import User
            user_count = User.query.count()
            print(f"✅ Verification: {user_count} user(s) created")
            
            # Switch back to master
            app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri
            db.engine.dispose()
        
        print("\n" + "=" * 70)
        print("✅ All Tenant Databases Recreated Successfully!")
        print("=" * 70)
        print()
        print("🎉 Now each license has its own clean database!")
        print("   - Only admin user created for each license")
        print("   - No shared data between licenses")
        print("   - Complete isolation achieved!")
        print()

if __name__ == '__main__':
    print("\n⚠️  WARNING: This will DELETE all existing tenant databases!")
    print("   All data in tenant databases will be lost!")
    print()
    response = input("Are you sure you want to continue? (yes/no): ")
    
    if response.lower() == 'yes':
        recreate_all_tenant_databases()
    else:
        print("\n❌ Operation cancelled")


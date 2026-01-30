"""
Create Tenant Databases for Existing Licenses
إنشاء قواعد بيانات منفصلة للتراخيص الموجودة

هذا السكريبت يقوم بإنشاء قواعد بيانات منفصلة لجميع التراخيص
الموجودة في licenses_master.db والتي لا تملك قواعد بيانات منفصلة.
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models_license import License
from app.tenant_manager import TenantManager

def create_tenant_databases():
    """Create tenant databases for all existing licenses"""
    
    print("=" * 70)
    print("🗄️  Creating Tenant Databases for Existing Licenses")
    print("=" * 70)
    print()
    
    # Create app
    app = create_app()
    
    # Switch to master database
    master_db_uri = f'sqlite:///{TenantManager.get_master_db_path()}'
    app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri
    
    with app.app_context():
        # Get all licenses
        licenses = License.query.all()
        
        if not licenses:
            print("⚠️  No licenses found in master database!")
            return
        
        print(f"📊 Found {len(licenses)} license(s)")
        print()
        
        created_count = 0
        skipped_count = 0
        failed_count = 0
        
        for i, license in enumerate(licenses, 1):
            print(f"[{i}/{len(licenses)}] Processing license: {license.license_key}")
            print(f"   👤 Client: {license.client_name}")
            print(f"   🏢 Company: {license.client_company or 'N/A'}")
            
            # Check if tenant database already exists
            tenant_db_path = TenantManager.get_tenant_db_path(license.license_key)
            
            if os.path.exists(tenant_db_path):
                print(f"   ⏭️  Skipped - Database already exists")
                skipped_count += 1
            else:
                # Create tenant database
                print(f"   🔧 Creating tenant database...")
                
                db_created = TenantManager.create_tenant_database(license.license_key, app)
                
                if not db_created:
                    print(f"   ❌ Failed to create database!")
                    failed_count += 1
                    print()
                    continue
                
                # Initialize tenant data
                print(f"   📦 Initializing tenant data...")
                
                data_initialized = TenantManager.initialize_tenant_data(
                    license.license_key, 
                    app, 
                    license
                )
                
                if not data_initialized:
                    print(f"   ⚠️  Database created but failed to initialize data")
                else:
                    print(f"   ✅ Success!")
                    created_count += 1
            
            print()
        
        # Summary
        print("=" * 70)
        print("📊 Summary:")
        print("=" * 70)
        print(f"✅ Created: {created_count}")
        print(f"⏭️  Skipped: {skipped_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"📊 Total: {len(licenses)}")
        print()
        
        if created_count > 0:
            print("🎉 Tenant databases created successfully!")
        elif skipped_count == len(licenses):
            print("ℹ️  All licenses already have tenant databases")
        else:
            print("⚠️  Some operations failed. Check the output above.")
        
        print()
        print("=" * 70)

if __name__ == '__main__':
    try:
        create_tenant_databases()
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


"""
Create tenant databases for licenses that don't have one
إنشاء قواعد بيانات منفصلة للتراخيص التي لا تملك قاعدة بيانات
"""
from app import create_app, db
from app.models_license import License
from app.tenant_manager import TenantManager
import os

app = create_app()

with app.app_context():
    # Get all licenses
    licenses = License.query.all()
    
    print(f"\n{'='*80}")
    print(f"  Creating Missing Tenant Databases")
    print(f"  إنشاء قواعد البيانات المنفصلة المفقودة")
    print(f"{'='*80}\n")
    
    created_count = 0
    skipped_count = 0
    failed_count = 0
    
    for license in licenses:
        print(f"\n📋 License: {license.license_key} - {license.client_name}")
        
        # Check if tenant database exists
        tenant_db_path = TenantManager.get_tenant_db_path(license.license_key)
        
        if os.path.exists(tenant_db_path):
            print(f"   ✅ Tenant database already exists - SKIPPING")
            skipped_count += 1
            continue
        
        print(f"   ⚠️  Tenant database NOT found - CREATING...")
        
        # Create tenant database
        success = TenantManager.create_tenant_database(license.license_key, app)
        
        if success:
            print(f"   ✅ Tenant database created successfully!")
            
            # Initialize tenant data
            print(f"   🔧 Initializing tenant data...")
            init_success = TenantManager.initialize_tenant_data(license.license_key, app, license)
            
            if init_success:
                print(f"   ✅ Tenant data initialized successfully!")
                created_count += 1
            else:
                print(f"   ❌ Failed to initialize tenant data")
                failed_count += 1
        else:
            print(f"   ❌ Failed to create tenant database")
            failed_count += 1
    
    print(f"\n{'='*80}")
    print(f"  Summary - الملخص")
    print(f"{'='*80}")
    print(f"  ✅ Created: {created_count}")
    print(f"  ⏭️  Skipped (already exists): {skipped_count}")
    print(f"  ❌ Failed: {failed_count}")
    print(f"  📊 Total licenses: {len(licenses)}")
    print(f"{'='*80}\n")


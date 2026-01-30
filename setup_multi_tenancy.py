"""
Setup Multi-Tenancy System
إعداد نظام التعددية - تحويل النظام الحالي إلى نظام متعدد التراخيص
"""
import os
import sys
import shutil
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models_license import License
from app.models import User
from app.tenant_manager import TenantManager
from config import Config

def setup_master_database(app):
    """
    Create master database for licenses only
    """
    print("\n" + "="*70)
    print("STEP 1: Creating Master Database")
    print("="*70)
    
    master_db_path = TenantManager.get_master_db_path()
    
    # Backup existing database if it exists
    if os.path.exists(master_db_path):
        backup_path = master_db_path + f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        shutil.copy2(master_db_path, backup_path)
        print(f"SUCCESS: Backed up existing master database to: {backup_path}")

    # Set master database URI
    master_db_uri = f'sqlite:///{master_db_path}'
    app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri

    with app.app_context():
        # Create only License table
        db.create_all()
        print(f"SUCCESS: Created master database at: {master_db_path}")
    
    return True

def migrate_existing_licenses(app):
    """
    Migrate existing licenses from old database to master database
    """
    print("\n" + "="*70)
    print("STEP 2: Migrating Existing Licenses")
    print("="*70)
    
    # Get old database path
    old_db_path = os.path.join(os.path.dirname(__file__), 'erp_system.db')
    
    if not os.path.exists(old_db_path):
        print("⚠️  No existing database found. Skipping migration.")
        return []
    
    # Read licenses from old database
    old_db_uri = f'sqlite:///{old_db_path}'
    app.config['SQLALCHEMY_DATABASE_URI'] = old_db_uri
    
    licenses_data = []
    
    with app.app_context():
        licenses = License.query.all()
        
        if not licenses:
            print("WARNING: No licenses found in old database.")
            return []

        print(f"Found {len(licenses)} license(s) in old database")
        
        # Extract license data
        for license in licenses:
            license_data = {
                'license_key': license.license_key,
                'license_hash': license.license_hash,
                'client_name': license.client_name,
                'client_email': license.client_email,
                'client_phone': license.client_phone,
                'client_company': license.client_company,
                'license_type': license.license_type,
                'max_users': license.max_users,
                'max_branches': license.max_branches,
                'is_active': license.is_active,
                'is_suspended': license.is_suspended,
                'suspension_reason': license.suspension_reason,
                'created_at': license.created_at,
                'activated_at': license.activated_at,
                'expires_at': license.expires_at,
                'admin_username': license.admin_username,
                'admin_password_hash': license.admin_password_hash,
                'notes': license.notes
            }
            licenses_data.append(license_data)
            print(f"   SUCCESS: {license.license_key} - {license.client_name}")
    
    # Write licenses to master database
    master_db_uri = f'sqlite:///{TenantManager.get_master_db_path()}'
    app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri
    
    with app.app_context():
        for license_data in licenses_data:
            # Check if license already exists
            existing = License.query.filter_by(license_key=license_data['license_key']).first()
            
            if existing:
                print(f"   WARNING: License {license_data['license_key']} already exists in master database")
                continue
            
            # Create new license
            new_license = License(**license_data)
            db.session.add(new_license)

        db.session.commit()
        print(f"SUCCESS: Migrated {len(licenses_data)} license(s) to master database")
    
    return licenses_data

def create_tenant_databases(app, licenses_data):
    """
    Create tenant databases for all licenses
    """
    print("\n" + "="*70)
    print("STEP 3: Creating Tenant Databases")
    print("="*70)
    
    master_db_uri = f'sqlite:///{TenantManager.get_master_db_path()}'
    
    with app.app_context():
        for license_data in licenses_data:
            license_key = license_data['license_key']
            print(f"\nProcessing license: {license_key}")

            # Get license object from master database
            app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri
            db.engine.dispose()

            license = License.query.filter_by(license_key=license_key).first()

            if not license:
                print(f"   ERROR: License not found in master database")
                continue

            # Create tenant database
            if TenantManager.create_tenant_database(license_key, app):
                print(f"   SUCCESS: Created tenant database")

                # Initialize tenant data
                if TenantManager.initialize_tenant_data(license_key, app, license):
                    print(f"   SUCCESS: Initialized tenant data")
                else:
                    print(f"   ERROR: Failed to initialize tenant data")
            else:
                print(f"   ERROR: Failed to create tenant database")

    print("\nTenant databases creation completed")

def main():
    """Main setup function"""
    print("\n" + "="*70)
    print("MULTI-TENANCY SETUP")
    print("   Setup Multi-Tenancy System")
    print("="*70)
    
    # Create app
    app = create_app('default')
    
    # Step 1: Create master database
    if not setup_master_database(app):
        print("❌ Failed to create master database")
        return
    
    # Step 2: Migrate existing licenses
    licenses_data = migrate_existing_licenses(app)
    
    # Step 3: Create tenant databases
    if licenses_data:
        create_tenant_databases(app, licenses_data)
    
    print("\n" + "="*70)
    print("MULTI-TENANCY SETUP COMPLETED!")
    print("="*70)
    print("\nSummary:")
    print(f"   - Master Database: {TenantManager.get_master_db_path()}")
    print(f"   - Tenant Databases: {TenantManager.get_tenants_dir()}")
    print(f"   - Total Licenses: {len(licenses_data)}")
    print("\nSystem is now ready for multi-tenancy!")
    print("\n")

if __name__ == '__main__':
    main()


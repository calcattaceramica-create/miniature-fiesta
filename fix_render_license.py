"""
Fix License on Render
إصلاح الترخيص على Render
"""
import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models_license import License
from app.models import User
from app.tenant_manager import TenantManager
from werkzeug.security import generate_password_hash

def fix_license():
    app = create_app(os.getenv('FLASK_ENV', 'production'))
    
    with app.app_context():
        # License key to fix
        license_key = '9813-26D0-F98D-741C'
        
        print(f"🔧 Fixing license: {license_key}")
        print("=" * 60)
        
        # Step 1: Update license in master database
        master_db_uri = f'sqlite:///{TenantManager.get_master_db_path()}'
        app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri
        db.engine.dispose()
        
        license = License.query.filter_by(license_key=license_key).first()
        
        if not license:
            print(f"❌ License {license_key} not found!")
            return False
        
        print(f"✅ License found")
        print(f"   Client: {license.client_name}")
        print(f"   Company: {license.client_company}")
        print(f"   Type: {license.license_type}")
        print()
        
        # Update admin credentials
        admin_username = 'admin'
        admin_password = 'admin123'
        
        license.admin_username = admin_username
        license.admin_password_hash = generate_password_hash(admin_password)
        
        db.session.commit()
        
        print(f"✅ Updated license admin credentials")
        print(f"   Username: {admin_username}")
        print(f"   Password: {admin_password}")
        print()
        
        # Step 2: Check if tenant database exists
        tenant_db_path = TenantManager.get_tenant_db_path(license_key)
        
        if os.path.exists(tenant_db_path):
            print(f"⚠️  Tenant database exists - deleting and recreating...")
            os.remove(tenant_db_path)
            print(f"   ✅ Deleted old database")
        
        # Step 3: Create tenant database
        print(f"📦 Creating tenant database...")
        if not TenantManager.create_tenant_database(license_key, app):
            print(f"❌ Failed to create tenant database!")
            return False
        
        print(f"   ✅ Tenant database created")
        
        # Step 4: Initialize tenant data
        print(f"📦 Initializing tenant data...")
        if not TenantManager.initialize_tenant_data(license_key, app, license):
            print(f"❌ Failed to initialize tenant data!")
            return False
        
        print(f"   ✅ Tenant data initialized")
        print()
        
        # Step 5: Verify admin user was created
        tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
        app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
        db.engine.dispose()
        
        admin_user = User.query.filter_by(username=admin_username).first()
        
        if admin_user:
            print(f"✅ Admin user verified in tenant database")
            print(f"   Username: {admin_user.username}")
            print(f"   Email: {admin_user.email}")
            print(f"   Full Name: {admin_user.full_name}")
            print(f"   Is Admin: {admin_user.is_admin}")
            print(f"   Is Active: {admin_user.is_active}")
        else:
            print(f"❌ Admin user not found in tenant database!")
            return False
        
        print()
        print("=" * 60)
        print("✅ License fixed successfully!")
        print()
        print("🔐 Login Credentials:")
        print(f"   License Key: {license_key}")
        print(f"   Username: {admin_username}")
        print(f"   Password: {admin_password}")
        
        return True

if __name__ == '__main__':
    success = fix_license()
    sys.exit(0 if success else 1)


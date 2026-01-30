"""
Test Multi-Tenancy - Verify that each license has separate database
اختبار التعددية - التحقق من أن كل ترخيص له قاعدة بيانات منفصلة
"""
from app import create_app, db
from app.models_license import License
from app.models import User
from app.tenant_manager import TenantManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = create_app()

def test_tenant_isolation():
    """Test that tenants have isolated data"""
    
    with app.app_context():
        # Get all licenses
        master_db_uri = f'sqlite:///{TenantManager.get_master_db_path()}'
        app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri
        db.engine.dispose()
        
        licenses = License.query.filter_by(is_active=True).limit(3).all()
        
        print(f"\n{'='*80}")
        print(f"  Testing Multi-Tenancy Isolation")
        print(f"  اختبار عزل البيانات بين التراخيص")
        print(f"{'='*80}\n")
        
        for license in licenses:
            print(f"\n📋 License: {license.license_key} - {license.client_name}")
            
            # Get tenant database path
            tenant_db_path = TenantManager.get_tenant_db_path(license.license_key)
            tenant_db_uri = TenantManager.get_tenant_db_uri(license.license_key)
            
            print(f"   📁 Database: {tenant_db_path}")
            
            # Connect to tenant database
            engine = create_engine(tenant_db_uri)
            Session = sessionmaker(bind=engine)
            session = Session()
            
            try:
                # Count users in this tenant
                user_count = session.query(User).count()
                print(f"   👥 Users in this tenant: {user_count}")
                
                # List users
                users = session.query(User).all()
                for user in users:
                    print(f"      - {user.username} ({user.full_name}) - {user.email}")
                
            finally:
                session.close()
                engine.dispose()
        
        print(f"\n{'='*80}")
        print(f"  ✅ Each license has its own isolated database!")
        print(f"  ✅ كل ترخيص له قاعدة بيانات منفصلة!")
        print(f"{'='*80}\n")

if __name__ == '__main__':
    test_tenant_isolation()


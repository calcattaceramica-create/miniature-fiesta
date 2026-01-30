"""
Debug Initialize Tenant Data
تتبع تهيئة بيانات الترخيص
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app import create_app, db
from app.models import User, Role, Branch
from app.models_license import License
from app.tenant_manager import TenantManager

def debug_initialize_data():
    """Debug the data initialization process"""
    
    app = create_app()
    
    # Test license key
    test_license = "TEST-1234-5678-9ABC"
    
    with app.app_context():
        print("=" * 70)
        print("🔍 Debugging Data Initialization")
        print("=" * 70)
        print()
        
        # Get a real license for testing
        master_db_uri = f'sqlite:///{TenantManager.get_master_db_path()}'
        app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri
        db.engine.dispose()
        
        license = License.query.filter_by(is_active=True).first()
        
        if not license:
            print("❌ No active license found")
            return
        
        print(f"Using license: {license.license_key}")
        print(f"   Client: {license.client_name}")
        print(f"   Admin: {license.admin_username}")
        print()
        
        # Create tenant database
        db_path = TenantManager.get_tenant_db_path(test_license)
        if os.path.exists(db_path):
            os.remove(db_path)
        
        TenantManager.create_tenant_database(test_license, app)
        print(f"✅ Database created: {db_path}")
        print()
        
        # Now initialize data
        print("Initializing data...")
        print()
        
        # Create engine for tenant database
        tenant_db_uri = TenantManager.get_tenant_db_uri(test_license)
        print(f"Tenant DB URI: {tenant_db_uri}")
        
        engine = create_engine(tenant_db_uri)
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        
        print(f"Session engine: {session.bind}")
        print(f"Session engine URL: {session.bind.url}")
        print()
        
        # Check users before
        user_count_before = session.query(User).count()
        print(f"Users BEFORE initialization: {user_count_before}")
        print()
        
        # Create admin role
        admin_role = session.query(Role).filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', name_ar='مدير النظام', description='Full system access')
            session.add(admin_role)
            session.flush()
            print(f"✅ Created admin role (ID: {admin_role.id})")
        else:
            print(f"⚠️  Admin role already exists (ID: {admin_role.id})")
        
        # Create main branch
        main_branch = session.query(Branch).filter_by(code='MAIN').first()
        if not main_branch:
            main_branch = Branch(
                name='الفرع الرئيسي',
                name_en='Main Branch',
                code='MAIN',
                is_active=True
            )
            session.add(main_branch)
            session.flush()
            print(f"✅ Created main branch (ID: {main_branch.id})")
        else:
            print(f"⚠️  Main branch already exists (ID: {main_branch.id})")
        
        # Create admin user
        admin_user = session.query(User).filter_by(username=license.admin_username).first()
        if not admin_user:
            admin_user = User(
                username=license.admin_username,
                email=f"{license.admin_username}@test.com",
                full_name=license.client_name,
                is_active=True,
                is_admin=True,
                role_id=admin_role.id,
                branch_id=main_branch.id
            )
            admin_user.password_hash = license.admin_password_hash
            session.add(admin_user)
            session.flush()
            print(f"✅ Created admin user: {admin_user.username} (ID: {admin_user.id})")
        else:
            print(f"⚠️  Admin user already exists: {admin_user.username} (ID: {admin_user.id})")
        
        session.commit()
        print()
        
        # Check users after
        user_count_after = session.query(User).count()
        print(f"Users AFTER initialization: {user_count_after}")
        
        if user_count_after > 1:
            print(f"❌ ERROR: Too many users! Expected 1, got {user_count_after}")
            users = session.query(User).all()
            for user in users:
                print(f"   - {user.username} (ID: {user.id})")
        else:
            print(f"✅ SUCCESS: Correct number of users!")
        
        session.close()
        engine.dispose()
        
        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"\n✅ Cleaned up test database")

if __name__ == '__main__':
    debug_initialize_data()


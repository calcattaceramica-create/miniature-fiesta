"""
Create admin user for a specific license
إنشاء مستخدم admin لترخيص محدد
"""
from app import create_app, db
from app.models import User, Role
from app.tenant_manager import TenantManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys

def create_admin_user(license_key, username="admin", password="admin123", full_name="Administrator"):
    """Create admin user for a specific license"""
    
    app = create_app()
    
    with app.app_context():
        # Get tenant database path
        tenant_db_path = TenantManager.get_tenant_db_path(license_key)
        tenant_db_uri = f'sqlite:///{tenant_db_path}'
        
        print(f"📦 Creating admin user for license: {license_key}")
        print(f"💾 Database: {tenant_db_uri}")
        
        # Create engine for tenant database
        engine = create_engine(tenant_db_uri)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        try:
            # Check if user already exists
            existing_user = session.query(User).filter_by(username=username).first()
            
            if existing_user:
                print(f"⚠️  User '{username}' already exists in this license!")
                print(f"   ID: {existing_user.id}")
                print(f"   Full Name: {existing_user.full_name}")
                print(f"   Email: {existing_user.email}")
                return False
            
            # Get admin role
            admin_role = session.query(Role).filter_by(name='admin').first()
            
            if not admin_role:
                print(f"❌ Admin role not found! Creating it...")
                admin_role = Role(
                    name='admin',
                    name_ar='مدير النظام',
                    description='System Administrator',
                    description_en='System Administrator'
                )
                session.add(admin_role)
                session.flush()
            
            # Create admin user
            admin_user = User(
                username=username,
                email=f"{username}@example.com",
                full_name=full_name,
                is_active=True,
                is_admin=True,
                language='ar',
                role_id=admin_role.id
            )
            admin_user.set_password(password)
            
            session.add(admin_user)
            session.commit()
            
            print(f"✅ Admin user created successfully!")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
            print(f"   Full Name: {full_name}")
            print(f"   ID: {admin_user.id}")
            
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error creating admin user: {e}")
            return False
            
        finally:
            session.close()
            engine.dispose()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_admin_for_license.py <license_key> [username] [password] [full_name]")
        print("\nExample:")
        print("  python create_admin_for_license.py 260D-F983-F5D0-73E4")
        print("  python create_admin_for_license.py 260D-F983-F5D0-73E4 admin admin123 'Administrator'")
        sys.exit(1)
    
    license_key = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else "admin"
    password = sys.argv[3] if len(sys.argv) > 3 else "admin123"
    full_name = sys.argv[4] if len(sys.argv) > 4 else "Administrator"
    
    create_admin_user(license_key, username, password, full_name)


"""
Check users for a specific license
التحقق من المستخدمين في ترخيص محدد
"""
from app import create_app, db
from app.models import User
from app.tenant_manager import TenantManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys

def check_users(license_key):
    """Check users for a specific license"""
    
    app = create_app()
    
    with app.app_context():
        # Get tenant database path
        tenant_db_path = TenantManager.get_tenant_db_path(license_key)
        tenant_db_uri = f'sqlite:///{tenant_db_path}'
        
        print(f"📦 Checking users for license: {license_key}")
        print(f"💾 Database: {tenant_db_uri}")
        print(f"{'='*60}")
        
        # Create engine for tenant database
        engine = create_engine(tenant_db_uri)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        try:
            # Get all users
            users = session.query(User).all()
            
            if not users:
                print(f"❌ No users found in this license!")
                return
            
            print(f"\n✅ Found {len(users)} user(s):\n")
            
            for user in users:
                print(f"{'='*60}")
                print(f"👤 Username: {user.username}")
                print(f"   Full Name: {user.full_name}")
                print(f"   Email: {user.email}")
                print(f"   Is Active: {'✅ Yes' if user.is_active else '❌ No'}")
                print(f"   Is Admin: {'✅ Yes' if user.is_admin else '❌ No'}")
                print(f"   Language: {user.language}")
                print(f"   ID: {user.id}")
                print(f"   Created: {user.created_at}")
                if user.last_login:
                    print(f"   Last Login: {user.last_login}")
            
            print(f"\n{'='*60}")
            print(f"\n💡 Default password for admin users: admin123")
            print(f"{'='*60}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
        finally:
            session.close()
            engine.dispose()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_license_users.py <license_key>")
        print("\nExample:")
        print("  python check_license_users.py 260D-F983-F5D0-73E4")
        sys.exit(1)
    
    license_key = sys.argv[1]
    check_users(license_key)


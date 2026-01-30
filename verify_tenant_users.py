"""
Verify Tenant Users
التحقق من المستخدمين في قواعد بيانات التراخيص
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User

def verify_tenant_users():
    """Verify users in tenant databases"""
    
    tenant_dbs = [
        ('CEC9-79EE-C42F-2DAD', 'admin'),
        ('6356-6964-93AE-B60D', 'admin1'),
        ('F730-BD34-0A48-A98B', 'admin2'),
        ('E972-34E5-2BAF-0AA9', 'ali'),
        ('67A7-AADF-40E8-6D3A', 'admin6'),
    ]
    
    print("=" * 70)
    print("🔍 Verifying Tenant Users")
    print("=" * 70)
    print()
    
    for license_key, expected_username in tenant_dbs:
        db_name = license_key.replace('-', '_')
        db_path = f'C:/Users/DELL/DED/tenant_databases/tenant_{db_name}.db'
        db_uri = f'sqlite:///{db_path}'
        
        engine = create_engine(db_uri)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        user_count = session.query(User).count()
        users = session.query(User).all()
        
        print(f"License: {license_key}")
        print(f"   Expected user: {expected_username}")
        print(f"   User count: {user_count}")
        
        if users:
            for user in users:
                print(f"   - {user.username} ({user.full_name}) - Admin: {user.is_admin}")
        else:
            print(f"   ❌ NO USERS FOUND!")
        
        print()
        
        session.close()
        engine.dispose()

if __name__ == '__main__':
    verify_tenant_users()


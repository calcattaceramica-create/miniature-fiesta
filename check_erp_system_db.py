"""
Check erp_system.db contents
فحص محتويات قاعدة البيانات القديمة
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User

def check_erp_system_db():
    """Check what's in erp_system.db"""
    
    db_uri = 'sqlite:///C:/Users/DELL/DED/erp_system.db'
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("=" * 70)
    print("🔍 Checking erp_system.db")
    print("=" * 70)
    print()
    
    user_count = session.query(User).count()
    print(f"Total users: {user_count}")
    print()
    
    users = session.query(User).all()
    for user in users:
        print(f"   - {user.username} ({user.full_name}) - Admin: {user.is_admin}")
    
    session.close()
    engine.dispose()

if __name__ == '__main__':
    check_erp_system_db()


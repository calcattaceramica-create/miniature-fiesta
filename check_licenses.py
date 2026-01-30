"""
Check License Details
فحص تفاصيل التراخيص
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models_license import License

def check_licenses():
    """Check license details"""
    
    db_uri = 'sqlite:///C:/Users/DELL/DED/licenses_master.db'
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("=" * 70)
    print("🔍 Checking Licenses")
    print("=" * 70)
    print()
    
    licenses = session.query(License).all()
    
    for lic in licenses:
        print(f"License: {lic.license_key}")
        print(f"   Client: {lic.client_name}")
        print(f"   Admin Username: {lic.admin_username}")
        print(f"   Admin Password Hash: {lic.admin_password_hash[:20] if lic.admin_password_hash else 'None'}...")
        print(f"   Is Active: {lic.is_active}")
        print()
    
    session.close()
    engine.dispose()

if __name__ == '__main__':
    check_licenses()


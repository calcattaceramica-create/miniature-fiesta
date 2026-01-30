"""
Migrate Licenses from erp_system.db to licenses_master.db
نقل التراخيص من قاعدة البيانات القديمة إلى قاعدة البيانات الرئيسية
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models_license import License

def migrate_licenses():
    """Migrate licenses from old database to master database"""
    
    print("=" * 70)
    print("🔄 Migrating Licenses")
    print("=" * 70)
    print()
    
    # Connect to old database
    old_db_uri = 'sqlite:///C:/Users/DELL/DED/erp_system.db'
    old_engine = create_engine(old_db_uri)
    OldSession = sessionmaker(bind=old_engine)
    old_session = OldSession()
    
    # Connect to new master database
    new_db_uri = 'sqlite:///C:/Users/DELL/DED/licenses_master.db'
    new_engine = create_engine(new_db_uri)
    NewSession = sessionmaker(bind=new_engine)
    new_session = NewSession()
    
    try:
        # Get all licenses from old database
        old_licenses = old_session.query(License).all()
        print(f"Found {len(old_licenses)} licenses in erp_system.db")
        print()
        
        if not old_licenses:
            print("❌ No licenses found in old database")
            return
        
        # Copy to new database
        for old_license in old_licenses:
            # Check if already exists
            existing = new_session.query(License).filter_by(
                license_key=old_license.license_key
            ).first()
            
            if existing:
                print(f"⚠️  License {old_license.license_key} already exists - skipping")
                continue
            
            # Create new license
            new_license = License(
                license_key=old_license.license_key,
                license_hash=old_license.license_hash,
                client_name=old_license.client_name,
                client_email=old_license.client_email,
                client_phone=old_license.client_phone,
                client_company=old_license.client_company,
                license_type=old_license.license_type,
                max_users=old_license.max_users,
                max_branches=old_license.max_branches,
                is_active=old_license.is_active,
                is_suspended=old_license.is_suspended,
                suspension_reason=old_license.suspension_reason,
                created_at=old_license.created_at,
                activated_at=old_license.activated_at,
                expires_at=old_license.expires_at,
                last_check=old_license.last_check,
                machine_id=old_license.machine_id,
                ip_address=old_license.ip_address,
                admin_username=old_license.admin_username,
                admin_password_hash=old_license.admin_password_hash,
                notes=old_license.notes
            )
            
            new_session.add(new_license)
            print(f"✅ Migrated: {old_license.license_key} ({old_license.client_name})")
        
        new_session.commit()
        print()
        print("=" * 70)
        print("✅ Migration Complete!")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        new_session.rollback()
    
    finally:
        old_session.close()
        new_session.close()
        old_engine.dispose()
        new_engine.dispose()

if __name__ == '__main__':
    migrate_licenses()


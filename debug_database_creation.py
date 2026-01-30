"""
Debug Database Creation
تتبع إنشاء قاعدة البيانات خطوة بخطوة
"""
import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app import create_app, db
from app.models import User
from app.tenant_manager import TenantManager

def debug_database_creation():
    """Debug the database creation process"""
    
    app = create_app()
    
    # Test license key
    test_license = "TEST-1234-5678-9ABC"
    
    with app.app_context():
        print("=" * 70)
        print("🔍 Debugging Database Creation")
        print("=" * 70)
        print()
        
        # Step 1: Check current database
        print("Step 1: Current database connection")
        print(f"   URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        user_count = User.query.count()
        print(f"   Users in current DB: {user_count}")
        print()
        
        # Step 2: Create tenant database path
        db_path = TenantManager.get_tenant_db_path(test_license)
        print(f"Step 2: Tenant database path")
        print(f"   Path: {db_path}")
        
        # Delete if exists
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"   Deleted existing database")
        print()
        
        # Step 3: Create engine for new database
        db_uri = TenantManager.get_tenant_db_uri(test_license)
        print(f"Step 3: Create engine")
        print(f"   URI: {db_uri}")
        engine = create_engine(db_uri)
        print(f"   Engine created: {engine}")
        print()
        
        # Step 4: Create tables using db.metadata
        print(f"Step 4: Create tables using db.metadata")
        print(f"   db object: {db}")
        print(f"   db.metadata: {db.metadata}")
        print(f"   db.engine: {db.engine}")
        print(f"   db.engine.url: {db.engine.url}")
        
        # Import models
        import app.models
        import app.models_inventory
        
        print(f"   Tables in metadata: {len(db.metadata.tables)}")
        for table_name in list(db.metadata.tables.keys())[:5]:
            print(f"      - {table_name}")
        print(f"      ... and {len(db.metadata.tables) - 5} more")
        print()
        
        # Create tables
        print(f"Step 5: Creating tables in new database...")
        db.metadata.create_all(engine)
        print(f"   ✅ Tables created")
        print()
        
        # Step 6: Check if data was copied
        print(f"Step 6: Check if data was copied")
        Session = sessionmaker(bind=engine)
        session = Session()
        
        user_count_new = session.query(User).count()
        print(f"   Users in new DB: {user_count_new}")
        
        if user_count_new > 0:
            print(f"   ❌ ERROR: Data was copied! This should be 0!")
            users = session.query(User).all()
            for user in users[:5]:
                print(f"      - {user.username}")
        else:
            print(f"   ✅ SUCCESS: No data copied!")
        
        session.close()
        engine.dispose()
        
        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"\n   Cleaned up test database")

if __name__ == '__main__':
    debug_database_creation()


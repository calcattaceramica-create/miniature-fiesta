"""
Initialize Master Database
تهيئة قاعدة البيانات الرئيسية للتراخيص
"""
import os
from sqlalchemy import create_engine
from app import create_app, db
from app.models_license import License, LicenseCheck

def initialize_master_database():
    """Initialize the master database with license tables"""
    
    print("=" * 70)
    print("🔧 Initializing Master Database")
    print("=" * 70)
    print()
    
    app = create_app()
    
    with app.app_context():
        # The config now points to licenses_master.db
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print()
        
        # Create all tables
        print("Creating tables...")
        db.create_all()
        print("✅ Tables created successfully!")
        print()
        
        # Verify
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"📋 Tables in master database: {len(tables)}")
        for table in tables:
            print(f"   - {table}")
        
        print()
        print("=" * 70)
        print("✅ Master Database Initialized Successfully!")
        print("=" * 70)

if __name__ == '__main__':
    initialize_master_database()


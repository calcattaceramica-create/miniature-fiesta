#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialize Master Database for Production Deployment
تهيئة قاعدة البيانات الرئيسية للنشر على Render
"""
import sys
import os
from pathlib import Path
from sqlalchemy import create_engine, inspect
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app, db
from app.models_license import License, LicenseCheck
from app.models import User, Role, Branch, Company

def initialize_master_database():
    """Initialize the master database with license tables and default data"""

    print("=" * 70)
    print("🔧 Initializing Master Database for Production")
    print("=" * 70)
    print()

    app = create_app()

    with app.app_context():
        try:
            # The config now points to licenses_master.db
            print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            print()

            # Create all tables
            print("Creating tables...")
            db.create_all()
            print("✅ Tables created successfully!")
            print()

            # Verify tables
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()

            print(f"📋 Tables in master database: {len(tables)}")
            for table in tables:
                print(f"   - {table}")
            print()

            # Create default production license
            default_license_key = "RENDER-2026-PROD-LIVE"
            existing_license = License.query.filter_by(license_key=default_license_key).first()

            if existing_license:
                print(f"✅ Default license already exists: {default_license_key}")
            else:
                print("Creating default production license...")
                license = License(
                    license_key=default_license_key,
                    license_hash=hashlib.sha256(default_license_key.encode()).hexdigest(),
                    client_name="DED ERP System - Production",
                    client_email="admin@ded-erp.com",
                    client_company="DED Company",
                    license_type="lifetime",
                    max_users=100,
                    max_branches=10,
                    is_active=True,
                    is_suspended=False,
                    created_at=datetime.utcnow(),
                    activated_at=datetime.utcnow(),
                    expires_at=None,  # Lifetime
                    admin_username="admin",
                    admin_password_hash=generate_password_hash("admin123"),
                    notes="Production license for Render deployment"
                )

                db.session.add(license)
                db.session.commit()

                print("=" * 70)
                print("✅ Default License Created Successfully!")
                print("=" * 70)
                print(f"🔑 License Key: {default_license_key}")
                print(f"👤 Username: admin")
                print(f"🔒 Password: admin123")
                print(f"📅 Type: Lifetime")
                print("=" * 70)

            print()
            print("=" * 70)
            print("✅ Master Database Initialized Successfully!")
            print("=" * 70)

            return True

        except Exception as e:
            print(f"\n❌ Error initializing database: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = initialize_master_database()
    sys.exit(0 if success else 1)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple database initialization script
Run this in Render Shell: python init_database.py
"""

import os
import sys

print("=" * 70)
print("DATABASE INITIALIZATION")
print("=" * 70)

# Check environment
print("\nEnvironment:")
print(f"  FLASK_ENV: {os.getenv('FLASK_ENV', 'not set')}")
print(f"  DATABASE_URL: {'set' if os.getenv('DATABASE_URL') else 'NOT SET'}")

# Fix PostgreSQL URL if needed
db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith('postgres://'):
    os.environ['DATABASE_URL'] = db_url.replace('postgres://', 'postgresql://', 1)
    print("  Fixed PostgreSQL URL")

# Import Flask app
print("\nLoading application...")
from app import create_app, db
app = create_app('production')
print("  App loaded!")

# Create database
print("\nInitializing database...")
with app.app_context():
    # Import models
    from app.models import User, Role, Company, Branch
    
    # Drop and create all tables
    print("  Dropping old tables...")
    db.drop_all()
    
    print("  Creating new tables...")
    db.create_all()
    
    print("  Creating default data...")
    
    # Company
    company = Company(
        name='شركة DED',
        name_en='DED Company',
        tax_number='123456789',
        city='الرياض',
        country='السعودية',
        currency='SAR',
        tax_rate=15.0
    )
    db.session.add(company)
    db.session.flush()
    
    # Branch
    branch = Branch(
        name='الفرع الرئيسي',
        name_en='Main Branch',
        code='BR001',
        company_id=company.id,
        city='الرياض',
        is_active=True
    )
    db.session.add(branch)
    db.session.flush()
    
    # Role
    role = Role(
        name='admin',
        name_ar='مدير النظام',
        description='Full system access'
    )
    db.session.add(role)
    db.session.flush()
    
    # Admin user
    admin = User(
        username='admin',
        email='admin@ded.com',
        full_name='System Administrator',
        is_active=True,
        is_admin=True,
        language='ar',
        branch_id=branch.id,
        role_id=role.id
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Commit
    db.session.commit()

    # Create trial license
    print("\n  Creating trial license...")
    from app.models_license import License
    from werkzeug.security import generate_password_hash
    from datetime import datetime, timedelta

    if not License.query.first():
        license_key = License.generate_license_key()
        license_hash = License.hash_license_key(license_key)

        trial_license = License(
            license_key=license_key,
            license_hash=license_hash,
            client_name='Trial User',
            client_email='trial@ded.com',
            client_company='DED Trial',
            license_type='trial',
            max_users=5,
            max_branches=2,
            is_active=True,
            activated_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=30),
            admin_username='admin',
            admin_password_hash=generate_password_hash('admin123'),
            notes='Auto-generated trial license - 30 days'
        )
        db.session.add(trial_license)
        db.session.commit()

        print(f"  ✅ Trial License Created!")
        print(f"  License Key: {license_key}")
        print(f"  Valid for: 30 days")

    print("\n" + "=" * 70)
    print("SUCCESS!")
    print("=" * 70)
    print("\nLogin with:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nCHANGE PASSWORD AFTER LOGIN!")
    print("=" * 70)


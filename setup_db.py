#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Minimal database setup for Render.com
"""
import os
import sys

# Fix PostgreSQL URL
db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith('postgres://'):
    os.environ['DATABASE_URL'] = db_url.replace('postgres://', 'postgresql://', 1)

print("Starting database setup...")

try:
    from app import create_app, db
    from app.models import User, Role, Company, Branch
    from app.models_license import License
    from werkzeug.security import generate_password_hash
    from datetime import datetime, timedelta
    
    app = create_app('production')
    
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        
        # Check if already initialized
        if Company.query.first():
            print("Database already initialized!")
            sys.exit(0)
        
        print("Adding default data...")
        
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
        db.session.commit()
        
        # License
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
            notes='Trial license - 30 days'
        )
        db.session.add(trial_license)
        db.session.commit()
        
        print("SUCCESS!")
        print(f"License: {license_key}")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


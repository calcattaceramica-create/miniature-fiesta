#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Tenant Data Insertion
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User, Role, Branch
from app.models_accounting import Account
from app.models_license import License
from app.tenant_manager import TenantManager

def test_tenant_data_insertion():
    """Test inserting data into a tenant database"""
    
    app = create_app('default')
    
    # Use the first tenant database
    license_key = 'CEC9-79EE-C42F-2DAD'
    tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
    
    print(f"Testing data insertion for license: {license_key}")
    print(f"Tenant DB URI: {tenant_db_uri}")
    print()
    
    # Switch to tenant database
    app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
    
    with app.app_context():
        # Dispose engine to force reconnection
        db.engine.dispose()
        
        print("Creating test role...")
        test_role = Role(name='test_role', name_ar='دور اختبار', description='Test role')
        db.session.add(test_role)
        db.session.commit()
        print("  Committed!")
        
        # Query to verify
        roles = Role.query.all()
        print(f"  Roles in database: {len(roles)}")
        for role in roles:
            print(f"    - {role.name}")
        
        print()
        print("Creating test branch...")
        test_branch = Branch(
            name='فرع اختبار',
            name_en='Test Branch',
            code='TEST',
            is_active=True
        )
        db.session.add(test_branch)
        db.session.commit()
        print("  Committed!")
        
        # Query to verify
        branches = Branch.query.all()
        print(f"  Branches in database: {len(branches)}")
        for branch in branches:
            print(f"    - {branch.code} | {branch.name}")
        
        print()
        print("Creating test account...")
        test_account = Account(
            code='9999',
            name='حساب اختبار',
            name_en='Test Account',
            account_type='asset',
            is_system=False
        )
        db.session.add(test_account)
        db.session.commit()
        print("  Committed!")
        
        # Query to verify
        accounts = Account.query.all()
        print(f"  Accounts in database: {len(accounts)}")
        for account in accounts:
            print(f"    - {account.code} | {account.name}")
        
        print()
        print("="*70)
        print("TEST COMPLETED SUCCESSFULLY!")
        print("="*70)

if __name__ == '__main__':
    test_tenant_data_insertion()


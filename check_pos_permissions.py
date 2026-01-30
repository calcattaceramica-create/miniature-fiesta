#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check POS Permissions
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Permission
from app.tenant_manager import TenantManager

def check_permissions():
    """Check POS permissions"""
    
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    print("=" * 80)
    print("🔍 Checking POS Permissions in Database")
    print("=" * 80)
    print()
    
    # Create app
    app = create_app()
    
    with app.app_context():
        # Switch to tenant database
        tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
        app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
        db.engine.dispose()
        
        print(f"✅ Connected to: {tenant_db_uri}")
        print()
        
        # Get all POS permissions
        print("📋 All POS Permissions:")
        pos_perms = Permission.query.filter(Permission.name.like('pos.%')).all()
        
        for perm in pos_perms:
            print(f"   - {perm.name} ({perm.name_ar})")
        
        print()
        print(f"Total: {len(pos_perms)} permissions")
        print()
        
        # Check if pos.view exists
        pos_view = Permission.query.filter_by(name='pos.view').first()
        
        if pos_view:
            print("✅ pos.view permission exists")
        else:
            print("❌ pos.view permission NOT found!")
            print("   Need to add this permission")
        
        print()
        print("=" * 80)
        print("✅ Check Complete!")
        print("=" * 80)

if __name__ == '__main__':
    check_permissions()


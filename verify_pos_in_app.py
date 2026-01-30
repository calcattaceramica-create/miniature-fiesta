#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verify POS Data through Flask App
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models_pos import POSSession, POSOrder
from app.models_sales import Quotation
from app.tenant_manager import TenantManager

def verify_pos_data():
    """Verify POS data in tenant database"""
    
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    print("=" * 80)
    print("🔍 Verifying POS Data in Application")
    print("=" * 80)
    print()
    
    # Create app
    app = create_app()
    
    with app.app_context():
        # Switch to tenant database
        print(f"📋 Switching to tenant database for license: {license_key}")
        
        # Manually set the database URI
        tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
        app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
        
        # Recreate the engine
        db.engine.dispose()
        
        print(f"✅ Connected to: {tenant_db_uri}")
        print()
        
        # Query POS Sessions
        print("📋 POS Sessions:")
        sessions = POSSession.query.all()
        print(f"   Total Sessions: {len(sessions)}")
        
        if sessions:
            print(f"\n   First 5 Sessions:")
            for session in sessions[:5]:
                print(f"   - ID: {session.id}, Number: {session.session_number}, Status: {session.status}")
        print()
        
        # Query POS Orders
        print("📋 POS Orders:")
        orders = POSOrder.query.all()
        print(f"   Total Orders: {len(orders)}")
        
        if orders:
            print(f"\n   First 5 Orders:")
            for order in orders[:5]:
                print(f"   - ID: {order.id}, Number: {order.order_number}, Total: {order.total_amount}")
        print()
        
        # Query Quotations
        print("📋 Quotations:")
        quotations = Quotation.query.all()
        print(f"   Total Quotations: {len(quotations)}")
        
        if quotations:
            print(f"\n   First 5 Quotations:")
            for quot in quotations[:5]:
                print(f"   - ID: {quot.id}, Number: {quot.quotation_number}, Total: {quot.total_amount}")
        print()
        
        print("=" * 80)
        print("✅ Verification Complete!")
        print("=" * 80)

if __name__ == '__main__':
    verify_pos_data()


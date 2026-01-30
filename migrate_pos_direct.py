#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Direct POS Data Migration using SQLAlchemy
"""

import os
import sys
import sqlite3
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models_pos import POSSession, POSOrder, POSOrderItem
from app.models_sales import Quotation, QuotationItem
from app.tenant_manager import TenantManager

def safe_date(date_str):
    """Safely convert date string to datetime"""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str)
    except:
        return None

def migrate_pos_data():
    """Migrate POS data directly"""
    
    old_db_path = 'erp_system.db'
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    if not os.path.exists(old_db_path):
        print(f"❌ Old database not found: {old_db_path}")
        return
    
    print("=" * 80)
    print("🔄 نقل بيانات نقاط البيع - POS DATA MIGRATION")
    print("=" * 80)
    print()
    
    # Create direct SQLAlchemy engine for tenant database
    print(f"📋 Step 1: Connecting to tenant database...")
    tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
    tenant_db_path = TenantManager.get_tenant_db_path(license_key)
    
    print(f"   Database URI: {tenant_db_uri}")
    print(f"   Database Path: {tenant_db_path}")
    
    # Create engine and session
    engine = create_engine(tenant_db_uri, echo=True)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    
    print(f"✅ Connected to tenant database")
    print()
    
    # Connect to old database
    print(f"📋 Step 2: Connecting to old database...")
    old_conn = sqlite3.connect(old_db_path)
    old_conn.row_factory = sqlite3.Row
    old_cursor = old_conn.cursor()
    print(f"✅ Connected to: {old_db_path}")
    print()
    
    try:
        # ========== MIGRATE QUOTATIONS ==========
        print("📋 Step 3: Migrating Quotations...")
        
        # Delete existing quotations
        session.query(Quotation).delete()
        session.commit()
        
        old_cursor.execute("SELECT * FROM quotations")
        migrated_quot = 0

        for row in old_cursor.fetchall():
            quot = Quotation(
                id=row['id'],
                quotation_number=row['quotation_number'],
                quotation_date=safe_date(row['quotation_date']) or datetime.utcnow(),
                valid_until=safe_date(row['valid_until']),
                customer_id=row['customer_id'],
                subtotal=row['subtotal'],
                discount_amount=row['discount_amount'],
                tax_amount=row['tax_amount'],
                total_amount=row['total_amount'],
                status=row['status'],
                notes=row['notes'],
                user_id=row['user_id'],
                created_at=safe_date(row['created_at']) or datetime.utcnow()
            )
            session.add(quot)
            migrated_quot += 1

        session.commit()
        print(f"✅ Migrated {migrated_quot} quotations")
        print()

        # ========== MIGRATE POS SESSIONS ==========
        print("📋 Step 4: Migrating POS Sessions...")
        
        # Delete existing sessions
        session.query(POSSession).delete()
        session.commit()
        
        old_cursor.execute("SELECT * FROM pos_sessions")
        migrated_sessions = 0

        for row in old_cursor.fetchall():
            pos_session = POSSession(
                id=row['id'],
                session_number=row['session_number'],
                cashier_id=row['cashier_id'],
                warehouse_id=row['warehouse_id'],
                opening_time=safe_date(row['opening_time']) or datetime.utcnow(),
                closing_time=safe_date(row['closing_time']),
                opening_balance=row['opening_balance'],
                closing_balance=row['closing_balance'],
                total_sales=row['total_sales'],
                total_cash=row['total_cash'],
                total_card=row['total_card'],
                status=row['status'],
                notes=row['notes'],
                created_at=safe_date(row['created_at']) or datetime.utcnow()
            )
            session.add(pos_session)
            migrated_sessions += 1

        session.commit()
        print(f"✅ Migrated {migrated_sessions} POS sessions")
        print()

        # ========== MIGRATE POS ORDERS ==========
        print("📋 Step 5: Migrating POS Orders...")
        
        # Delete existing orders
        session.query(POSOrder).delete()
        session.commit()
        
        old_cursor.execute("SELECT * FROM pos_orders")
        migrated_orders = 0

        for row in old_cursor.fetchall():
            pos_order = POSOrder(
                id=row['id'],
                order_number=row['order_number'],
                order_date=safe_date(row['order_date']) or datetime.utcnow(),
                session_id=row['session_id'],
                customer_id=row['customer_id'],
                subtotal=row['subtotal'],
                discount_amount=row['discount_amount'],
                tax_amount=row['tax_amount'],
                total_amount=row['total_amount'],
                payment_method=row['payment_method'],
                cash_amount=row['cash_amount'],
                card_amount=row['card_amount'],
                change_amount=row['change_amount'],
                status=row['status'],
                notes=row['notes'],
                created_at=safe_date(row['created_at']) or datetime.utcnow()
            )
            session.add(pos_order)
            migrated_orders += 1

        session.commit()
        print(f"✅ Migrated {migrated_orders} POS orders")
        print()

        print("=" * 80)
        print("🎉 نقل بيانات نقاط البيع اكتمل بنجاح!")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        session.rollback()
    finally:
        old_conn.close()
        session.close()

if __name__ == '__main__':
    migrate_pos_data()


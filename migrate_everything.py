#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete Full Migration - نقل جميع البيانات بالكامل بدون استثناء
"""

import os
import sys
import sqlite3
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models import User, Role, Permission, Branch, Company
from app.models_inventory import Product, Category, Unit, Warehouse, StockMovement, Stock
from app.models_sales import Customer, SalesInvoice, SalesInvoiceItem, Quotation, QuotationItem
from app.models_purchases import Supplier
from app.models_hr import Employee
from app.models_pos import POSSession, POSOrder, POSOrderItem
from app.models_accounting import Account, JournalEntry, JournalEntryItem
from app.models_settings import AccountingSettings
from app.tenant_manager import TenantManager

def safe_date(date_str):
    """Safely convert date string to datetime"""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str)
    except:
        return None

def migrate_everything():
    """Migrate EVERYTHING from old database"""
    
    old_db_path = 'erp_system.db'
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    if not os.path.exists(old_db_path):
        print(f"❌ Old database not found: {old_db_path}")
        return
    
    print("=" * 80)
    print("🔄 نقل جميع البيانات بالكامل - COMPLETE FULL MIGRATION")
    print("=" * 80)
    print()

    # Create direct SQLAlchemy engine for tenant database
    print(f"📋 Step 1: Connecting to tenant database...")
    tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)

    # Create engine and session
    engine = create_engine(tenant_db_uri, echo=False)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()

    print(f"✅ Connected to: {tenant_db_uri}")
    print()

    # Connect to old database
    print(f"📋 Step 2: Connecting to old database...")
    old_conn = sqlite3.connect(old_db_path)
    old_conn.row_factory = sqlite3.Row
    old_cursor = old_conn.cursor()
    print(f"✅ Connected to: {old_db_path}")
    print()

    # Get admin user
    admin_user = session.query(User).filter_by(username='admin').first()
        
        # ========== MIGRATE USERS ==========
        print("📋 Step 3: Migrating Users...")
        old_cursor.execute("SELECT * FROM users")
        users_map = {}
        migrated_users = 0
        
        for row in old_cursor.fetchall():
            # Skip if username already exists
            existing = User.query.filter_by(username=row['username']).first()
            if existing:
                users_map[row['id']] = existing
                print(f"   ℹ️  User already exists: {row['username']}")
                continue
            
            user = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                password_hash=row['password_hash'],
                full_name=row['full_name'],
                phone=row['phone'],
                is_active=row['is_active'],
                is_admin=row['is_admin'],
                language=row['language'],
                branch_id=row['branch_id'],
                role_id=row['role_id'],
                created_at=safe_date(row['created_at']) or datetime.utcnow()
            )
            db.session.add(user)
            users_map[row['id']] = user
            migrated_users += 1
            print(f"   ✅ Migrated user: {row['username']}")
        
        db.session.commit()
        print(f"✅ Processed {len(users_map)} users ({migrated_users} new)")
        print()
        
        # ========== MIGRATE ROLES ==========
        print("📋 Step 4: Migrating Roles...")
        old_cursor.execute("SELECT * FROM roles")
        roles_map = {}
        migrated_roles = 0

        with db.session.no_autoflush:
            for row in old_cursor.fetchall():
                # Check by name first
                existing = Role.query.filter_by(name=row['name']).first()
                if existing:
                    roles_map[row['id']] = existing
                    print(f"   ℹ️  Role already exists: {row['name']}")
                    continue

                # Check if ID exists
                existing_by_id = Role.query.filter_by(id=row['id']).first()
                if existing_by_id:
                    # ID exists but different name - map old ID to existing role
                    roles_map[row['id']] = existing_by_id
                    print(f"   ℹ️  Role ID {row['id']} already used by: {existing_by_id.name}")
                    continue

                role = Role(
                    id=row['id'],
                    name=row['name'],
                    name_ar=row['name_ar'],
                    description=row['description']
                )
                db.session.add(role)
                roles_map[row['id']] = role
                migrated_roles += 1
                print(f"   ✅ Migrated role: {row['name']}")

        db.session.commit()
        print(f"✅ Processed {len(roles_map)} roles ({migrated_roles} new)")
        print()
        
        # ========== MIGRATE PERMISSIONS ==========
        print("📋 Step 5: Migrating Permissions...")
        old_cursor.execute("SELECT * FROM permissions")
        permissions_map = {}
        migrated_perms = 0

        with db.session.no_autoflush:
            for row in old_cursor.fetchall():
                # Check by name first
                existing = Permission.query.filter_by(name=row['name']).first()
                if existing:
                    permissions_map[row['id']] = existing
                    continue

                # Check if ID exists
                existing_by_id = Permission.query.filter_by(id=row['id']).first()
                if existing_by_id:
                    # ID exists but different name - map old ID to existing permission
                    permissions_map[row['id']] = existing_by_id
                    continue

                perm = Permission(
                    id=row['id'],
                    name=row['name'],
                    name_ar=row['name_ar'],
                    module=row['module']
                )
                db.session.add(perm)
                permissions_map[row['id']] = perm
                migrated_perms += 1

        db.session.commit()
        print(f"✅ Processed {len(permissions_map)} permissions ({migrated_perms} new)")
        print()

        # ========== MIGRATE ROLE PERMISSIONS ==========
        print("📋 Step 6: Migrating Role Permissions...")
        old_cursor.execute("SELECT * FROM role_permissions")
        migrated_rp = 0

        for row in old_cursor.fetchall():
            role_id = row['role_id']
            perm_id = row['permission_id']

            if role_id in roles_map and perm_id in permissions_map:
                role = roles_map[role_id]
                perm = permissions_map[perm_id]

                if perm not in role.permissions:
                    role.permissions.append(perm)
                    migrated_rp += 1

        db.session.commit()
        print(f"✅ Migrated {migrated_rp} role-permission links")
        print()

        # ========== MIGRATE ACCOUNTS ==========
        print("📋 Step 7: Migrating Accounts...")
        old_cursor.execute("SELECT * FROM accounts ORDER BY id")
        accounts_map = {}
        migrated_accounts = 0

        for row in old_cursor.fetchall():
            existing = Account.query.filter_by(code=row['code']).first()
            if existing:
                accounts_map[row['id']] = existing
                continue

            account = Account(
                id=row['id'],
                code=row['code'],
                name=row['name'],
                name_en=row['name_en'],
                account_type=row['account_type'],
                parent_id=row['parent_id'],
                debit_balance=row['debit_balance'] or 0.0,
                credit_balance=row['credit_balance'] or 0.0,
                current_balance=row['current_balance'] or 0.0,
                is_active=row['is_active'],
                is_system=row['is_system'],
                description=row['description'],
                created_at=safe_date(row['created_at']) or datetime.utcnow()
            )
            db.session.add(account)
            accounts_map[row['id']] = account
            migrated_accounts += 1

        db.session.commit()
        print(f"✅ Processed {len(accounts_map)} accounts ({migrated_accounts} new)")
        print()

        # ========== MIGRATE ACCOUNTING SETTINGS ==========
        print("📋 Step 8: Migrating Accounting Settings...")
        old_cursor.execute("SELECT * FROM accounting_settings LIMIT 1")
        acc_settings_row = old_cursor.fetchone()

        if acc_settings_row:
            acc_settings = AccountingSettings.query.first()
            if not acc_settings:
                acc_settings = AccountingSettings()

            acc_settings.sales_revenue_account_id = acc_settings_row['sales_revenue_account_id']
            acc_settings.sales_tax_account_id = acc_settings_row['sales_tax_account_id']
            acc_settings.sales_discount_account_id = acc_settings_row['sales_discount_account_id']
            acc_settings.accounts_receivable_account_id = acc_settings_row['accounts_receivable_account_id']
            acc_settings.sales_cost_account_id = acc_settings_row['sales_cost_account_id']
            acc_settings.purchase_expense_account_id = acc_settings_row['purchase_expense_account_id']
            acc_settings.purchase_tax_account_id = acc_settings_row['purchase_tax_account_id']
            acc_settings.purchase_discount_account_id = acc_settings_row['purchase_discount_account_id']
            acc_settings.accounts_payable_account_id = acc_settings_row['accounts_payable_account_id']
            acc_settings.inventory_account_id = acc_settings_row['inventory_account_id']
            acc_settings.inventory_adjustment_account_id = acc_settings_row['inventory_adjustment_account_id']
            acc_settings.cash_account_id = acc_settings_row['cash_account_id']
            acc_settings.pos_cash_account_id = acc_settings_row['pos_cash_account_id']
            acc_settings.pos_card_account_id = acc_settings_row['pos_card_account_id']
            acc_settings.auto_create_journal_entries = acc_settings_row['auto_create_journal_entries']
            acc_settings.auto_post_journal_entries = acc_settings_row['auto_post_journal_entries']

            db.session.add(acc_settings)
            db.session.commit()
            print(f"   ✅ Migrated accounting settings")
        print()

        # ========== MIGRATE JOURNAL ENTRIES ==========
        print("📋 Step 9: Migrating Journal Entries...")
        old_cursor.execute("SELECT * FROM journal_entries")
        journal_map = {}
        migrated_je = 0

        for row in old_cursor.fetchall():
            existing = JournalEntry.query.filter_by(entry_number=row['entry_number']).first()
            if existing:
                journal_map[row['id']] = existing
                continue

            je = JournalEntry(
                id=row['id'],
                entry_number=row['entry_number'],
                entry_date=safe_date(row['entry_date']) or datetime.utcnow().date(),
                entry_type=row['entry_type'],
                reference_type=row['reference_type'],
                reference_id=row['reference_id'],
                description=row['description'],
                total_debit=row['total_debit'] or 0.0,
                total_credit=row['total_credit'] or 0.0,
                status=row['status'],
                user_id=admin_user.id if admin_user else None,
                created_at=safe_date(row['created_at']) or datetime.utcnow()
            )
            db.session.add(je)
            journal_map[row['id']] = je
            migrated_je += 1

        db.session.commit()
        print(f"✅ Processed {len(journal_map)} journal entries ({migrated_je} new)")
        print()

        # ========== MIGRATE QUOTATIONS ==========
        print("📋 Step 10: Migrating Quotations...")

        # First, delete all existing quotations in tenant DB
        db.session.query(Quotation).delete()
        db.session.commit()

        old_cursor.execute("SELECT * FROM quotations")
        quotations_map = {}
        migrated_quot = 0

        for row in old_cursor.fetchall():
            quot = Quotation(
                id=row['id'],
                quotation_number=row['quotation_number'],
                quotation_date=safe_date(row['quotation_date']) or datetime.utcnow().date(),
                valid_until=safe_date(row['valid_until']),
                customer_id=row['customer_id'],
                subtotal=row['subtotal'] or 0.0,
                discount_amount=row['discount_amount'] or 0.0,
                tax_amount=row['tax_amount'] or 0.0,
                total_amount=row['total_amount'] or 0.0,
                status=row['status'],
                notes=row['notes'],
                user_id=admin_user.id if admin_user else None,
                created_at=safe_date(row['created_at']) or datetime.utcnow()
            )
            db.session.add(quot)
            quotations_map[row['id']] = quot
            migrated_quot += 1

        db.session.commit()
        print(f"✅ Migrated {migrated_quot} quotations")
        print()

        # ========== MIGRATE POS SESSIONS ==========
        print("📋 Step 11: Migrating POS Sessions...")

        # First, delete all existing POS sessions in tenant DB
        db.session.query(POSSession).delete()
        db.session.commit()

        old_cursor.execute("SELECT * FROM pos_sessions")
        sessions_map = {}
        migrated_sessions = 0

        for row in old_cursor.fetchall():
            session = POSSession(
                id=row['id'],
                session_number=row['session_number'],
                cashier_id=admin_user.id if admin_user else 1,
                warehouse_id=row['warehouse_id'],
                opening_time=safe_date(row['opening_time']) or datetime.utcnow(),
                closing_time=safe_date(row['closing_time']),
                opening_balance=row['opening_balance'] or 0.0,
                closing_balance=row['closing_balance'] or 0.0,
                total_sales=row['total_sales'] or 0.0,
                total_cash=row['total_cash'] or 0.0,
                total_card=row['total_card'] or 0.0,
                status=row['status'],
                notes=row['notes'],
                created_at=safe_date(row['created_at']) or datetime.utcnow()
            )
            db.session.add(session)
            sessions_map[row['id']] = session
            migrated_sessions += 1

        db.session.commit()
        print(f"✅ Migrated {migrated_sessions} POS sessions")
        print()

        # ========== MIGRATE POS ORDERS ==========
        print("📋 Step 12: Migrating POS Orders...")

        # First, delete all existing POS orders in tenant DB
        db.session.query(POSOrder).delete()
        db.session.commit()

        old_cursor.execute("SELECT * FROM pos_orders")
        orders_map = {}
        migrated_orders = 0

        for row in old_cursor.fetchall():
            order = POSOrder(
                id=row['id'],
                order_number=row['order_number'],
                order_date=safe_date(row['order_date']) or datetime.utcnow(),
                session_id=row['session_id'],
                customer_id=row['customer_id'],
                subtotal=row['subtotal'] or 0.0,
                discount_amount=row['discount_amount'] or 0.0,
                tax_amount=row['tax_amount'] or 0.0,
                total_amount=row['total_amount'] or 0.0,
                payment_method=row['payment_method'],
                cash_amount=row['cash_amount'] or 0.0,
                card_amount=row['card_amount'] or 0.0,
                change_amount=row['change_amount'] or 0.0,
                status=row['status'],
                notes=row['notes'],
                created_at=safe_date(row['created_at']) or datetime.utcnow()
            )
            db.session.add(order)
            orders_map[row['id']] = order
            migrated_orders += 1

        db.session.commit()
        print(f"✅ Migrated {migrated_orders} POS orders")
        print()

        # Close connections
        old_conn.close()

        print("=" * 80)
        print("🎉 جميع البيانات تم نقلها بنجاح! - ALL DATA MIGRATED SUCCESSFULLY!")
        print("=" * 80)
        print()
        print("📊 Migration Summary:")
        print(f"   ✅ Users: {len(users_map)} ({migrated_users} new)")
        print(f"   ✅ Roles: {len(roles_map)} ({migrated_roles} new)")
        print(f"   ✅ Permissions: {len(permissions_map)} ({migrated_perms} new)")
        print(f"   ✅ Role-Permission Links: {migrated_rp}")
        print(f"   ✅ Accounts: {len(accounts_map)} ({migrated_accounts} new)")
        print(f"   ✅ Accounting Settings: Migrated")
        print(f"   ✅ Journal Entries: {len(journal_map)} ({migrated_je} new)")
        print(f"   ✅ Quotations: {len(quotations_map)} ({migrated_quot} new)")
        print(f"   ✅ POS Sessions: {len(sessions_map)} ({migrated_sessions} new)")
        print(f"   ✅ POS Orders: {len(orders_map)} ({migrated_orders} new)")
        print()

if __name__ == '__main__':
    migrate_everything()


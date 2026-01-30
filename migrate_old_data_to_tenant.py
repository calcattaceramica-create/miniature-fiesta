#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migrate Old Data to Tenant - نقل البيانات القديمة إلى قاعدة بيانات الترخيص
"""

import os
import sys
import sqlite3
from datetime import datetime

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Branch
from app.models_inventory import Product, Category, Unit, Warehouse, StockMovement
from app.models_sales import Customer, SalesInvoice, SalesInvoiceItem
from app.models_purchases import Supplier
from app.tenant_manager import TenantManager

def migrate_data():
    """Migrate data from old database to new tenant database"""
    
    old_db_path = 'erp_system.db'
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    if not os.path.exists(old_db_path):
        print(f"❌ Old database not found: {old_db_path}")
        return
    
    print("=" * 70)
    print("🔄 نقل البيانات - Migrating Data")
    print("=" * 70)
    print()
    
    app = create_app()
    
    with app.app_context():
        # Switch to tenant database
        print(f"📋 Step 1: Connecting to tenant database...")
        tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
        app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
        db.engine.dispose()
        print(f"✅ Connected to: {tenant_db_uri}")
        print()
        
        # Connect to old database
        print(f"📋 Step 2: Connecting to old database...")
        old_conn = sqlite3.connect(old_db_path)
        old_conn.row_factory = sqlite3.Row
        old_cursor = old_conn.cursor()
        print(f"✅ Connected to: {old_db_path}")
        print()
        
        # Get admin user for foreign keys
        admin_user = User.query.filter_by(username='admin').first()
        
        # Migrate Categories
        print("📋 Step 3: Migrating Categories...")
        old_cursor.execute("SELECT * FROM categories")
        categories_map = {}

        for row in old_cursor.fetchall():
            # Check if category already exists
            existing = Category.query.filter_by(id=row['id']).first()
            if existing:
                categories_map[row['id']] = existing
                print(f"   ℹ️  Category already exists: {row['name']}")
                continue

            category = Category(
                id=row['id'],
                name=row['name'],
                name_en=row['name_en'],
                code=row['code'],
                parent_id=row['parent_id'],
                description=row['description'],
                is_active=row['is_active'],
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.utcnow()
            )
            db.session.add(category)
            categories_map[row['id']] = category
            print(f"   ✅ Migrated category: {row['name']}")

        db.session.commit()
        print(f"✅ Processed {len(categories_map)} categories")
        print()
        
        # Migrate Units (create default if not exists)
        print("📋 Step 4: Checking Units...")
        unit = Unit.query.filter_by(symbol='PCS').first()
        if not unit:
            unit = Unit(
                name='قطعة',
                name_en='Piece',
                symbol='PCS',
                is_active=True
            )
            db.session.add(unit)
            db.session.commit()
            print("   ✅ Created default unit: قطعة (PCS)")
        else:
            print("   ℹ️  Default unit already exists")
        print()
        
        # Migrate Warehouses
        print("📋 Step 5: Migrating Warehouses...")
        old_cursor.execute("SELECT * FROM warehouses")
        warehouses_map = {}

        for row in old_cursor.fetchall():
            # Check if warehouse already exists
            existing = Warehouse.query.filter_by(id=row['id']).first()
            if existing:
                warehouses_map[row['id']] = existing
                print(f"   ℹ️  Warehouse already exists: {row['name']}")
                continue

            warehouse = Warehouse(
                id=row['id'],
                name=row['name'],
                name_en=row['name_en'],
                code=row['code'],
                address=row['address'],
                is_active=row['is_active'],
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.utcnow()
            )
            db.session.add(warehouse)
            warehouses_map[row['id']] = warehouse
            print(f"   ✅ Migrated warehouse: {row['name']}")

        db.session.commit()
        print(f"✅ Processed {len(warehouses_map)} warehouses")
        print()

        # Migrate Products
        print("📋 Step 6: Migrating Products...")
        old_cursor.execute("SELECT * FROM products")
        products_map = {}

        for row in old_cursor.fetchall():
            # Check if product already exists
            existing = Product.query.filter_by(id=row['id']).first()
            if existing:
                products_map[row['id']] = existing
                print(f"   ℹ️  Product already exists: {row['name']}")
                continue

            product = Product(
                id=row['id'],
                name=row['name'],
                name_en=row['name_en'],
                code=row['code'],
                barcode=row['barcode'],
                sku=row['sku'],
                category_id=row['category_id'],
                unit_id=unit.id,  # Use default unit
                description=row['description'],
                image=row['image'],
                cost_price=row['cost_price'],
                selling_price=row['selling_price'],
                min_price=row['min_price'],
                min_stock=row['min_stock'],
                max_stock=row['max_stock'],
                reorder_level=row['reorder_level'],
                is_active=row['is_active'],
                is_sellable=row['is_sellable'],
                is_purchasable=row['is_purchasable'],
                track_inventory=row['track_inventory'],
                has_expiry=row['has_expiry'],
                has_serial=row['has_serial'],
                tax_rate=row['tax_rate'],
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.utcnow()
            )
            db.session.add(product)
            products_map[row['id']] = product
            print(f"   ✅ Migrated product: {row['name']}")

        db.session.commit()
        print(f"✅ Processed {len(products_map)} products")
        print()

        # Migrate Customers
        print("📋 Step 7: Migrating Customers...")
        old_cursor.execute("SELECT * FROM customers")
        customers_map = {}

        for row in old_cursor.fetchall():
            # Check if customer already exists
            existing = Customer.query.filter_by(id=row['id']).first()
            if existing:
                customers_map[row['id']] = existing
                print(f"   ℹ️  Customer already exists: {row['name']}")
                continue

            customer = Customer(
                id=row['id'],
                code=row['code'],
                name=row['name'],
                name_en=row['name_en'],
                email=row['email'],
                phone=row['phone'],
                mobile=row['mobile'],
                address=row['address'],
                city=row['city'],
                country=row['country'],
                tax_number=row['tax_number'],
                commercial_register=row['commercial_register'],
                customer_type=row['customer_type'],
                credit_limit=row['credit_limit'],
                current_balance=row['current_balance'],
                payment_terms=row['payment_terms'],
                category=row['category'],
                rating=row['rating'],
                is_active=row['is_active'],
                notes=row['notes'],
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.utcnow()
            )
            db.session.add(customer)
            customers_map[row['id']] = customer
            print(f"   ✅ Migrated customer: {row['name']}")

        db.session.commit()
        print(f"✅ Processed {len(customers_map)} customers")
        print()

        # Migrate Suppliers
        print("📋 Step 8: Migrating Suppliers...")
        old_cursor.execute("SELECT * FROM suppliers")
        suppliers_map = {}

        for row in old_cursor.fetchall():
            # Check if supplier already exists
            existing = Supplier.query.filter_by(id=row['id']).first()
            if existing:
                suppliers_map[row['id']] = existing
                print(f"   ℹ️  Supplier already exists: {row['name']}")
                continue

            supplier = Supplier(
                id=row['id'],
                code=row['code'],
                name=row['name'],
                name_en=row['name_en'],
                email=row['email'],
                phone=row['phone'],
                mobile=row['mobile'],
                address=row['address'],
                city=row['city'],
                country=row['country'],
                tax_number=row['tax_number'],
                commercial_register=row['commercial_register'],
                credit_limit=row['credit_limit'],
                current_balance=row['current_balance'],
                payment_terms=row['payment_terms'],
                category=row['category'],
                rating=row['rating'],
                is_active=row['is_active'],
                notes=row['notes'],
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.utcnow()
            )
            db.session.add(supplier)
            suppliers_map[row['id']] = supplier
            print(f"   ✅ Migrated supplier: {row['name']}")

        db.session.commit()
        print(f"✅ Processed {len(suppliers_map)} suppliers")
        print()

        # Migrate Sales Invoices
        print("📋 Step 9: Migrating Sales Invoices...")
        old_cursor.execute("SELECT * FROM sales_invoices")
        invoices_map = {}

        for row in old_cursor.fetchall():
            # Check if invoice already exists
            existing = SalesInvoice.query.filter_by(id=row['id']).first()
            if existing:
                invoices_map[row['id']] = existing
                print(f"   ℹ️  Invoice already exists: {row['invoice_number']}")
                continue

            invoice = SalesInvoice(
                id=row['id'],
                invoice_number=row['invoice_number'],
                invoice_date=datetime.fromisoformat(row['invoice_date']) if row['invoice_date'] else datetime.utcnow(),
                customer_id=row['customer_id'],
                warehouse_id=row['warehouse_id'],
                user_id=admin_user.id,  # Assign to admin
                subtotal=row['subtotal'],
                tax_amount=row['tax_amount'],
                discount_amount=row['discount_amount'],
                total_amount=row['total_amount'],
                paid_amount=row['paid_amount'],
                remaining_amount=row['remaining_amount'],
                payment_status=row['payment_status'],
                notes=row['notes'],
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.utcnow()
            )
            db.session.add(invoice)
            invoices_map[row['id']] = invoice
            print(f"   ✅ Migrated invoice: {row['invoice_number']}")

        db.session.commit()
        print(f"✅ Processed {len(invoices_map)} sales invoices")
        print()

        # Migrate Sales Invoice Items
        print("📋 Step 10: Migrating Sales Invoice Items...")
        old_cursor.execute("SELECT * FROM sales_invoice_items")
        items_count = 0

        for row in old_cursor.fetchall():
            # Check if item already exists
            existing = SalesInvoiceItem.query.filter_by(id=row['id']).first()
            if existing:
                print(f"   ℹ️  Invoice item already exists: ID {row['id']}")
                items_count += 1
                continue

            item = SalesInvoiceItem(
                id=row['id'],
                invoice_id=row['invoice_id'],
                product_id=row['product_id'],
                quantity=row['quantity'],
                unit_price=row['unit_price'],
                discount_percent=row['discount_percent'],
                discount_amount=row['discount_amount'],
                tax_percent=row['tax_percent'],
                tax_amount=row['tax_amount'],
                total_amount=row['total_amount'],
                notes=row['notes']
            )
            db.session.add(item)
            items_count += 1

        db.session.commit()
        print(f"✅ Processed {items_count} invoice items")
        print()

        # Close old database connection
        old_conn.close()

        print("=" * 70)
        print("🎉 Migration Complete!")
        print("=" * 70)
        print()
        print("📊 Summary:")
        print(f"   ✅ Categories: {len(categories_map)}")
        print(f"   ✅ Warehouses: {len(warehouses_map)}")
        print(f"   ✅ Products: {len(products_map)}")
        print(f"   ✅ Customers: {len(customers_map)}")
        print(f"   ✅ Suppliers: {len(suppliers_map)}")
        print(f"   ✅ Sales Invoices: {len(invoices_map)}")
        print(f"   ✅ Invoice Items: {items_count}")
        print()
        print("🚀 You can now login and see all your data!")

if __name__ == '__main__':
    migrate_data()


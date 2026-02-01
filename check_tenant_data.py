#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check Tenant Database Data
فحص بيانات قاعدة بيانات المستأجر
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app, db
from app.models import User, Product, Customer, Supplier, Stock
from app.models import SalesInvoice, PurchaseInvoice

def check_tenant_data(license_key):
    """Check data in tenant database"""
    
    print("=" * 80)
    print(f"🔍 Checking Data for License: {license_key}")
    print("=" * 80)
    print()
    
    app = create_app()
    
    with app.app_context():
        # Switch to tenant database
        from app.tenant_manager import TenantManager
        tenant_db_path = TenantManager.get_tenant_db_path(license_key)
        
        if not os.path.exists(tenant_db_path):
            print(f"❌ Tenant database not found: {tenant_db_path}")
            return False
        
        print(f"✅ Tenant database found: {tenant_db_path}")
        print()
        
        # Update database URI
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{tenant_db_path}'
        
        # Dispose old engine
        if hasattr(db, 'engine'):
            db.engine.dispose()
        if hasattr(db, '_engine'):
            db._engine = None
        
        try:
            # Check Users
            users = User.query.all()
            print(f"👥 Users: {len(users)}")
            for user in users[:5]:
                print(f"   - {user.username} ({user.full_name})")
            if len(users) > 5:
                print(f"   ... and {len(users) - 5} more")
            print()
            
            # Check Products
            products = Product.query.all()
            print(f"📦 Products: {len(products)}")
            for product in products[:5]:
                print(f"   - {product.name}")
            if len(products) > 5:
                print(f"   ... and {len(products) - 5} more")
            print()
            
            # Check Stock
            stocks = Stock.query.all()
            print(f"📦 Stock Items: {len(stocks)}")
            for stock in stocks[:5]:
                if stock.product:
                    print(f"   - {stock.product.name}: {stock.quantity}")
            if len(stocks) > 5:
                print(f"   ... and {len(stocks) - 5} more")
            print()
            
            # Check Customers
            customers = Customer.query.all()
            print(f"👤 Customers: {len(customers)}")
            for customer in customers[:5]:
                print(f"   - {customer.name}")
            if len(customers) > 5:
                print(f"   ... and {len(customers) - 5} more")
            print()
            
            # Check Suppliers
            suppliers = Supplier.query.all()
            print(f"🏭 Suppliers: {len(suppliers)}")
            for supplier in suppliers[:5]:
                print(f"   - {supplier.name}")
            if len(suppliers) > 5:
                print(f"   ... and {len(suppliers) - 5} more")
            print()
            
            # Check Sales
            sales = SalesInvoice.query.all()
            print(f"💰 Sales Invoices: {len(sales)}")
            print()

            # Check Purchases
            purchases = PurchaseInvoice.query.all()
            print(f"🛒 Purchase Invoices: {len(purchases)}")
            print()
            
            print("=" * 80)
            print("✅ Data check complete!")
            print("=" * 80)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    # Check all three licenses
    licenses = [
        '9813-26D0-F98D-741C',
        'CE9B-0DD8-90B7-B59B',
        'B31B-B06A-202A-5298'
    ]
    
    for license_key in licenses:
        check_tenant_data(license_key)
        print("\n\n")


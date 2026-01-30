#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check Current Data - التحقق من البيانات الحالية
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Role
from app.models_inventory import Product, Category, Warehouse
from app.models_sales import Customer
from app.models_purchases import Supplier
from app.tenant_manager import TenantManager

def check_current_data():
    """Check what data exists in current tenant database"""
    
    app = create_app()
    
    # License key to check
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    print("=" * 70)
    print("🔍 التحقق من البيانات الحالية - Checking Current Data")
    print("=" * 70)
    print()
    
    with app.app_context():
        # Switch to tenant database
        print(f"📋 Switching to tenant database: {license_key}")
        tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
        
        app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
        db.engine.dispose()
        
        print(f"✅ Connected to: {tenant_db_uri}")
        print()
        
        # Check Users
        print("👥 Users:")
        users = User.query.all()
        print(f"   Total: {len(users)}")
        for user in users:
            print(f"   - {user.username} ({user.email}) - Role: {user.role.name if user.role else 'None'}")
        print()
        
        # Check Roles
        print("🔐 Roles:")
        roles = Role.query.all()
        print(f"   Total: {len(roles)}")
        for role in roles:
            print(f"   - {role.name} ({role.name_ar})")
        print()
        
        # Check Products
        print("📦 Products:")
        products = Product.query.all()
        print(f"   Total: {len(products)}")
        if products:
            for product in products[:5]:  # Show first 5
                print(f"   - {product.name} ({product.sku})")
            if len(products) > 5:
                print(f"   ... and {len(products) - 5} more")
        print()
        
        # Check Categories
        print("📂 Categories:")
        categories = Category.query.all()
        print(f"   Total: {len(categories)}")
        if categories:
            for cat in categories[:5]:
                print(f"   - {cat.name}")
        print()
        
        # Check Warehouses
        print("🏪 Warehouses:")
        warehouses = Warehouse.query.all()
        print(f"   Total: {len(warehouses)}")
        if warehouses:
            for wh in warehouses:
                print(f"   - {wh.name}")
        print()
        
        # Check Customers
        print("👤 Customers:")
        customers = Customer.query.all()
        print(f"   Total: {len(customers)}")
        if customers:
            for customer in customers[:5]:
                print(f"   - {customer.name}")
        print()
        
        # Check Suppliers
        print("🏭 Suppliers:")
        suppliers = Supplier.query.all()
        print(f"   Total: {len(suppliers)}")
        if suppliers:
            for supplier in suppliers[:5]:
                print(f"   - {supplier.name}")
        print()
        
        print("=" * 70)
        print("✅ Data check complete!")
        print("=" * 70)

if __name__ == '__main__':
    check_current_data()


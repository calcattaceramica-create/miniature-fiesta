#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verify Migrated Data - التحقق من البيانات المنقولة
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Role, Permission, Branch, Company
from app.models_inventory import Product, Category, Unit, Warehouse, StockMovement, Stock
from app.models_sales import Customer, SalesInvoice
from app.models_purchases import Supplier
from app.models_hr import Employee
from app.tenant_manager import TenantManager

def verify_data():
    """Verify all migrated data"""
    
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    print("=" * 70)
    print("🔍 التحقق من البيانات المنقولة - Verifying Migrated Data")
    print("=" * 70)
    print()
    
    app = create_app()
    
    with app.app_context():
        # Switch to tenant database
        tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
        app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
        db.engine.dispose()
        
        print(f"📊 Current Data in Tenant Database:")
        print("-" * 70)
        
        # Check Company
        company = Company.query.first()
        if company:
            print(f"✅ Company: {company.name}")
        else:
            print("❌ Company: Not found")
        
        # Check Branches
        branches = Branch.query.all()
        print(f"✅ Branches: {len(branches)}")
        for branch in branches:
            print(f"   - {branch.name}")
        
        # Check Units
        units = Unit.query.all()
        print(f"✅ Units: {len(units)}")
        for unit in units:
            print(f"   - {unit.name}")
        
        # Check Categories
        categories = Category.query.all()
        print(f"✅ Categories: {len(categories)}")
        for cat in categories:
            print(f"   - {cat.name}")
        
        # Check Warehouses
        warehouses = Warehouse.query.all()
        print(f"✅ Warehouses: {len(warehouses)}")
        for wh in warehouses:
            print(f"   - {wh.name}")
        
        # Check Products
        products = Product.query.all()
        print(f"✅ Products: {len(products)}")
        for prod in products:
            print(f"   - {prod.name} ({prod.code})")
        
        # Check Customers
        customers = Customer.query.all()
        print(f"✅ Customers: {len(customers)}")
        for cust in customers:
            print(f"   - {cust.name}")
        
        # Check Suppliers
        suppliers = Supplier.query.all()
        print(f"✅ Suppliers: {len(suppliers)}")
        for supp in suppliers:
            print(f"   - {supp.name}")
        
        # Check Employees
        employees = Employee.query.all()
        print(f"✅ Employees: {len(employees)}")
        for emp in employees:
            print(f"   - {emp.first_name} {emp.last_name}")
        
        # Check Sales Invoices
        invoices = SalesInvoice.query.all()
        print(f"✅ Sales Invoices: {len(invoices)}")
        
        # Check Stock Movements
        movements = StockMovement.query.all()
        print(f"✅ Stock Movements: {len(movements)}")
        
        # Check Stocks
        stocks = Stock.query.all()
        print(f"✅ Stocks: {len(stocks)}")
        for stock in stocks:
            print(f"   - Product {stock.product_id}: {stock.quantity} units")
        
        # Check Users
        users = User.query.all()
        print(f"✅ Users: {len(users)}")
        
        # Check Roles
        roles = Role.query.all()
        print(f"✅ Roles: {len(roles)}")
        
        print()
        print("=" * 70)
        print("✅ Verification Complete!")
        print("=" * 70)

if __name__ == '__main__':
    verify_data()


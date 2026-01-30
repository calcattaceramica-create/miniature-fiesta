#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete Data Migration - نقل جميع البيانات بالكامل
"""

import os
import sys
import sqlite3
from datetime import datetime

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Role, Permission, Branch, Company
from app.models_inventory import Product, Category, Unit, Warehouse, StockMovement, Stock
from app.models_sales import Customer, SalesInvoice, SalesInvoiceItem
from app.models_purchases import Supplier
from app.models_hr import Employee
from app.tenant_manager import TenantManager

def migrate_all_data():
    """Migrate ALL data from old database to new tenant database"""
    
    old_db_path = 'erp_system.db'
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    if not os.path.exists(old_db_path):
        print(f"❌ Old database not found: {old_db_path}")
        return
    
    print("=" * 70)
    print("🔄 نقل جميع البيانات بالكامل - Complete Data Migration")
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
        
        # Step 3: Migrate Company
        print("📋 Step 3: Migrating Company...")
        old_cursor.execute("SELECT * FROM companies LIMIT 1")
        company_row = old_cursor.fetchone()
        
        if company_row:
            company = Company.query.first()
            if not company:
                company = Company()
            
            company.name = company_row['name']
            company.name_en = company_row['name_en']
            company.tax_number = company_row['tax_number']
            company.commercial_register = company_row['commercial_register']
            company.address = company_row['address']
            company.city = company_row['city']
            company.country = company_row['country']
            company.phone = company_row['phone']
            company.email = company_row['email']
            company.website = company_row['website']
            company.logo = company_row['logo']
            company.currency = company_row['currency']
            company.tax_rate = company_row['tax_rate']
            
            db.session.add(company)
            db.session.commit()
            print(f"   ✅ Migrated company: {company_row['name']}")
        print()
        
        # Step 4: Migrate Branches
        print("📋 Step 4: Migrating Branches...")
        old_cursor.execute("SELECT * FROM branches")
        branches_map = {}
        
        for row in old_cursor.fetchall():
            existing = Branch.query.filter_by(id=row['id']).first()
            if existing:
                branches_map[row['id']] = existing
                print(f"   ℹ️  Branch already exists: {row['name']}")
                continue
            
            branch = Branch(
                id=row['id'],
                name=row['name'],
                name_en=row['name_en'],
                code=row['code'],
                address=row['address'],
                city=row['city'],
                phone=row['phone'],
                is_active=row['is_active'],
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.utcnow()
            )
            db.session.add(branch)
            branches_map[row['id']] = branch
            print(f"   ✅ Migrated branch: {row['name']}")
        
        db.session.commit()
        print(f"✅ Processed {len(branches_map)} branches")
        print()
        
        # Step 5: Migrate Units
        print("📋 Step 5: Migrating Units...")
        old_cursor.execute("SELECT * FROM units")
        units_map = {}
        
        for row in old_cursor.fetchall():
            existing = Unit.query.filter_by(id=row['id']).first()
            if existing:
                units_map[row['id']] = existing
                print(f"   ℹ️  Unit already exists: {row['name']}")
                continue
            
            unit = Unit(
                id=row['id'],
                name=row['name'],
                name_en=row['name_en'],
                symbol=row['symbol'],
                is_active=row['is_active']
            )
            db.session.add(unit)
            units_map[row['id']] = unit
            print(f"   ✅ Migrated unit: {row['name']}")
        
        db.session.commit()
        print(f"✅ Processed {len(units_map)} units")
        print()

        # Step 6: Migrate Employees
        print("📋 Step 6: Migrating Employees...")
        old_cursor.execute("SELECT * FROM employees")
        employees_map = {}

        for row in old_cursor.fetchall():
            existing = Employee.query.filter_by(id=row['id']).first()
            if existing:
                employees_map[row['id']] = existing
                print(f"   ℹ️  Employee already exists: {row['first_name']}")
                continue

            employee = Employee(
                id=row['id'],
                employee_number=row['employee_number'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                first_name_en=row['first_name_en'],
                last_name_en=row['last_name_en'],
                national_id=row['national_id'],
                passport_number=row['passport_number'],
                date_of_birth=datetime.fromisoformat(row['date_of_birth']) if row['date_of_birth'] else None,
                gender=row['gender'],
                marital_status=row['marital_status'],
                nationality=row['nationality'],
                email=row['email'],
                phone=row['phone'],
                mobile=row['mobile'],
                address=row['address'],
                city=row['city'],
                branch_id=row['branch_id'],
                hire_date=datetime.fromisoformat(row['hire_date']) if row['hire_date'] else None,
                contract_type=row['contract_type'],
                employment_status=row['employment_status'],
                basic_salary=row['basic_salary'],
                is_active=row['is_active'],
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.utcnow()
            )
            db.session.add(employee)
            employees_map[row['id']] = employee
            print(f"   ✅ Migrated employee: {row['first_name']} {row['last_name']}")

        db.session.commit()
        print(f"✅ Processed {len(employees_map)} employees")
        print()

        # Step 7: Migrate Stock Movements
        print("📋 Step 7: Migrating Stock Movements...")
        old_cursor.execute("SELECT * FROM stock_movements")

        for row in old_cursor.fetchall():
            existing = StockMovement.query.filter_by(id=row['id']).first()
            if existing:
                print(f"   ℹ️  Stock movement already exists: {row['id']}")
                continue

            movement = StockMovement(
                id=row['id'],
                product_id=row['product_id'],
                warehouse_id=row['warehouse_id'],
                movement_type=row['movement_type'],
                quantity=row['quantity'],
                reference_type=row['reference_type'],
                reference_id=row['reference_id'],
                notes=row['notes'],
                user_id=admin_user.id if admin_user else None,
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.utcnow()
            )
            db.session.add(movement)
            print(f"   ✅ Migrated stock movement: {row['movement_type']} - {row['quantity']}")

        db.session.commit()
        print("✅ Stock movements migrated")
        print()

        # Step 8: Migrate Stocks
        print("📋 Step 8: Migrating Stocks...")
        old_cursor.execute("SELECT * FROM stocks")

        for row in old_cursor.fetchall():
            existing = Stock.query.filter_by(id=row['id']).first()
            if existing:
                # Update existing stock
                existing.quantity = row['quantity']
                existing.reserved_quantity = row['reserved_quantity']
                existing.available_quantity = row['available_quantity']
                print(f"   ℹ️  Stock updated: Product {row['product_id']}, Qty: {row['quantity']}")
            else:
                stock = Stock(
                    id=row['id'],
                    product_id=row['product_id'],
                    warehouse_id=row['warehouse_id'],
                    quantity=row['quantity'],
                    reserved_quantity=row['reserved_quantity'],
                    available_quantity=row['available_quantity'],
                    last_updated=datetime.fromisoformat(row['last_updated']) if row['last_updated'] else datetime.utcnow()
                )
                db.session.add(stock)
                print(f"   ✅ Migrated stock: Product {row['product_id']}, Qty: {row['quantity']}")

        db.session.commit()
        print("✅ Stocks migrated")
        print()

        # Step 9: Close connections
        old_conn.close()

        print("=" * 70)
        print("🎉 جميع البيانات تم نقلها بنجاح! - All Data Migrated Successfully!")
        print("=" * 70)
        print()
        print("📊 Summary:")
        print(f"   ✅ Company: 1")
        print(f"   ✅ Branches: {len(branches_map)}")
        print(f"   ✅ Units: {len(units_map)}")
        print(f"   ✅ Employees: {len(employees_map)}")
        print(f"   ✅ Stock Movements: Migrated")
        print(f"   ✅ Stocks: Migrated")
        print()

if __name__ == '__main__':
    migrate_all_data()


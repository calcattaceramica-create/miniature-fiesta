"""
Seed database with sample data for testing and demonstration
"""
from app import create_app, db
from app.models import User, Role
from app.models_inventory import Category, Unit, Product, Warehouse, Stock
from app.models_sales import Customer
from app.models_purchases import Supplier
from datetime import datetime, timedelta
import random

def seed_sample_data():
    """Add sample data to database"""
    app = create_app()
    
    with app.app_context():
        print("Adding sample data...")
        
        # Get default warehouse
        warehouse = Warehouse.query.first()
        if not warehouse:
            print("❌ No warehouse found. Run init_db.py first!")
            return
        
        # Get units
        piece_unit = Unit.query.filter_by(name='قطعة').first()
        kg_unit = Unit.query.filter_by(name='كيلوجرام').first()
        
        # Get categories
        electronics = Category.query.filter_by(code='ELEC').first()
        clothing = Category.query.filter_by(code='CLTH').first()
        food = Category.query.filter_by(code='FOOD').first()
        
        # Add sample products
        print("Adding sample products...")
        products_data = [
            # Electronics
            {
                'name': 'لابتوب HP ProBook',
                'name_en': 'HP ProBook Laptop',
                'code': 'PROD-001',
                'barcode': '1234567890001',
                'category_id': electronics.id,
                'unit_id': piece_unit.id,
                'cost_price': 2000.00,
                'selling_price': 2500.00,
                'min_price': 2200.00,
                'tax_rate': 15.0,
                'track_inventory': True,
                'min_stock_level': 5,
                'reorder_point': 10
            },
            {
                'name': 'ماوس لاسلكي Logitech',
                'name_en': 'Logitech Wireless Mouse',
                'code': 'PROD-002',
                'barcode': '1234567890002',
                'category_id': electronics.id,
                'unit_id': piece_unit.id,
                'cost_price': 50.00,
                'selling_price': 75.00,
                'min_price': 60.00,
                'tax_rate': 15.0,
                'track_inventory': True,
                'min_stock_level': 20,
                'reorder_point': 30
            },
            {
                'name': 'لوحة مفاتيح ميكانيكية',
                'name_en': 'Mechanical Keyboard',
                'code': 'PROD-003',
                'barcode': '1234567890003',
                'category_id': electronics.id,
                'unit_id': piece_unit.id,
                'cost_price': 150.00,
                'selling_price': 200.00,
                'min_price': 170.00,
                'tax_rate': 15.0,
                'track_inventory': True,
                'min_stock_level': 10,
                'reorder_point': 15
            },
            # Clothing
            {
                'name': 'قميص رجالي قطن',
                'name_en': 'Men Cotton Shirt',
                'code': 'PROD-004',
                'barcode': '1234567890004',
                'category_id': clothing.id,
                'unit_id': piece_unit.id,
                'cost_price': 80.00,
                'selling_price': 120.00,
                'min_price': 100.00,
                'tax_rate': 15.0,
                'track_inventory': True,
                'min_stock_level': 15,
                'reorder_point': 25
            },
            {
                'name': 'بنطال جينز',
                'name_en': 'Jeans Pants',
                'code': 'PROD-005',
                'barcode': '1234567890005',
                'category_id': clothing.id,
                'unit_id': piece_unit.id,
                'cost_price': 100.00,
                'selling_price': 150.00,
                'min_price': 120.00,
                'tax_rate': 15.0,
                'track_inventory': True,
                'min_stock_level': 20,
                'reorder_point': 30
            },
            # Food
            {
                'name': 'أرز بسمتي',
                'name_en': 'Basmati Rice',
                'code': 'PROD-006',
                'barcode': '1234567890006',
                'category_id': food.id,
                'unit_id': kg_unit.id,
                'cost_price': 8.00,
                'selling_price': 12.00,
                'min_price': 10.00,
                'tax_rate': 0.0,  # Food usually exempt from tax
                'track_inventory': True,
                'min_stock_level': 100,
                'reorder_point': 200
            },
        ]
        
        for product_data in products_data:
            product = Product(**product_data)
            db.session.add(product)
            
            # Add initial stock
            stock = Stock(
                product=product,
                warehouse_id=warehouse.id,
                quantity=random.randint(50, 200),
                reserved_quantity=0
            )
            stock.available_quantity = stock.quantity - stock.reserved_quantity
            db.session.add(stock)
        
        db.session.commit()
        print(f"✅ Added {len(products_data)} sample products")
        
        # Add sample customers
        print("Adding sample customers...")
        customers_data = [
            {
                'code': 'CUST-001',
                'name': 'أحمد محمد السعيد',
                'name_en': 'Ahmed Mohammed Alsaeed',
                'email': 'ahmed@example.com',
                'phone': '+966 50 123 4567',
                'mobile': '+966 50 123 4567',
                'address': 'الرياض، حي النخيل',
                'city': 'الرياض',
                'country': 'المملكة العربية السعودية',
                'customer_type': 'individual',
                'credit_limit': 10000.00,
                'payment_terms': 0,
                'category': 'Regular'
            },
            {
                'code': 'CUST-002',
                'name': 'شركة التقنية المتقدمة',
                'name_en': 'Advanced Technology Company',
                'email': 'info@advtech.com',
                'phone': '+966 11 234 5678',
                'mobile': '+966 50 234 5678',
                'address': 'جدة، حي الروضة',
                'city': 'جدة',
                'country': 'المملكة العربية السعودية',
                'tax_number': '300123456789003',
                'commercial_register': '1234567890',
                'customer_type': 'company',
                'credit_limit': 50000.00,
                'payment_terms': 30,
                'category': 'VIP'
            },
            {
                'code': 'CUST-003',
                'name': 'فاطمة علي الأحمد',
                'name_en': 'Fatima Ali Alahmad',
                'email': 'fatima@example.com',
                'phone': '+966 50 345 6789',
                'mobile': '+966 50 345 6789',
                'address': 'الدمام، حي الفيصلية',
                'city': 'الدمام',
                'country': 'المملكة العربية السعودية',
                'customer_type': 'individual',
                'credit_limit': 5000.00,
                'payment_terms': 0,
                'category': 'Regular'
            },
        ]
        
        for customer_data in customers_data:
            customer = Customer(**customer_data)
            db.session.add(customer)
        
        db.session.commit()
        print(f"✅ Added {len(customers_data)} sample customers")
        
        # Add sample suppliers
        print("Adding sample suppliers...")
        suppliers_data = [
            {
                'code': 'SUPP-001',
                'name': 'شركة الإلكترونيات الحديثة',
                'name_en': 'Modern Electronics Company',
                'email': 'sales@modernelec.com',
                'phone': '+966 11 456 7890',
                'mobile': '+966 50 456 7890',
                'address': 'الرياض، حي العليا',
                'city': 'الرياض',
                'country': 'المملكة العربية السعودية',
                'tax_number': '300234567890003',
                'commercial_register': '2345678901',
                'credit_limit': 100000.00,
                'payment_terms': 30,
                'category': 'Electronics',
                'rating': 5
            },
            {
                'code': 'SUPP-002',
                'name': 'مصنع الملابس الوطني',
                'name_en': 'National Clothing Factory',
                'email': 'orders@nationalclothing.com',
                'phone': '+966 12 567 8901',
                'mobile': '+966 50 567 8901',
                'address': 'جدة، حي الصفا',
                'city': 'جدة',
                'country': 'المملكة العربية السعودية',
                'tax_number': '300345678901003',
                'commercial_register': '3456789012',
                'credit_limit': 75000.00,
                'payment_terms': 45,
                'category': 'Clothing',
                'rating': 4
            },
        ]
        
        for supplier_data in suppliers_data:
            supplier = Supplier(**supplier_data)
            db.session.add(supplier)
        
        db.session.commit()
        print(f"✅ Added {len(suppliers_data)} sample suppliers")
        
        print("\n" + "="*50)
        print("✅ Sample data added successfully!")
        print("="*50)
        print("\nSummary:")
        print(f"  Products: {Product.query.count()}")
        print(f"  Customers: {Customer.query.count()}")
        print(f"  Suppliers: {Supplier.query.count()}")
        print("="*50)

if __name__ == '__main__':
    seed_sample_data()


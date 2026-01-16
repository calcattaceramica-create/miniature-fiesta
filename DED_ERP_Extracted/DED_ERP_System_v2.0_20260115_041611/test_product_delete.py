#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار حذف المنتج نهائياً
"""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import Product
from app.models_sales import SalesInvoiceItem
from app.models_inventory import Stock, StockMovement

def test_product_delete():
    """Test product deletion"""
    print("\n" + "=" * 80)
    print("🧪 Testing Product Delete Functionality")
    print("=" * 80)
    
    app = create_app()
    
    with app.app_context():
        # Get all products
        products = Product.query.all()
        print(f"\n📦 Total products in database: {len(products)}")
        
        if not products:
            print("\n⚠️  No products found. Creating a test product...")
            
            # Create a test product
            test_product = Product(
                name="منتج تجريبي للحذف",
                name_en="Test Product for Deletion",
                code="TEST-DELETE-001",
                barcode="TEST123456",
                cost_price=10.0,
                selling_price=15.0,
                is_active=True
            )
            
            db.session.add(test_product)
            db.session.commit()
            
            print(f"✅ Created test product: {test_product.name} (ID: {test_product.id})")
            product_id = test_product.id
        else:
            # Use the first product
            test_product = products[0]
            product_id = test_product.id
            print(f"\n📦 Using existing product: {test_product.name} (ID: {product_id})")
        
        # Check related records
        print(f"\n🔍 Checking related records for product ID {product_id}:")
        
        sales_items = SalesInvoiceItem.query.filter_by(product_id=product_id).count()
        print(f"   - Sales invoice items: {sales_items}")
        
        stocks = Stock.query.filter_by(product_id=product_id).count()
        print(f"   - Stock records: {stocks}")
        
        movements = StockMovement.query.filter_by(product_id=product_id).count()
        print(f"   - Stock movements: {movements}")
        
        # Try to delete
        print(f"\n🗑️  Attempting to delete product ID {product_id}...")
        
        try:
            # Delete related records first
            deleted_sales = SalesInvoiceItem.query.filter_by(product_id=product_id).delete()
            deleted_stocks = Stock.query.filter_by(product_id=product_id).delete()
            deleted_movements = StockMovement.query.filter_by(product_id=product_id).delete()
            
            print(f"   ✅ Deleted {deleted_sales} sales invoice items")
            print(f"   ✅ Deleted {deleted_stocks} stock records")
            print(f"   ✅ Deleted {deleted_movements} stock movements")
            
            # Delete the product
            product_name = test_product.name
            db.session.delete(test_product)
            db.session.commit()
            
            print(f"\n✅ Successfully deleted product: {product_name}")
            
            # Verify deletion
            check_product = Product.query.get(product_id)
            if check_product is None:
                print(f"✅ Verified: Product ID {product_id} no longer exists in database")
            else:
                print(f"❌ Error: Product ID {product_id} still exists!")
                
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error deleting product: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()

def main():
    """Run the test"""
    print("\n" + "=" * 80)
    print("🚀 Product Delete Test")
    print("=" * 80)
    
    test_product_delete()
    
    print("\n" + "=" * 80)
    print("✅ Test Completed!")
    print("=" * 80 + "\n")

if __name__ == '__main__':
    main()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test products route
"""
from app import create_app
from app.models import User, Product, Category

app = create_app()

with app.app_context():
    print("=" * 70)
    print("Testing Products Route")
    print("=" * 70)
    
    # Get admin user
    admin = User.query.filter_by(username='admin').first()
    print(f"\n1. Admin user: {admin.username}")
    print(f"   is_admin: {admin.is_admin}")
    print(f"   has permission: {admin.has_permission('inventory.products.view')}")
    
    # Test query
    print("\n2. Testing Product query...")
    try:
        query = Product.query
        products = query.order_by(Product.created_at.desc()).paginate(
            page=1, per_page=20, error_out=False
        )
        print(f"   ✓ Products found: {products.total}")
        print(f"   ✓ Pages: {products.pages}")
        print(f"   ✓ Current page items: {len(products.items)}")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    # Test categories
    print("\n3. Testing Category query...")
    try:
        categories = Category.query.filter_by(is_active=True).all()
        print(f"   ✓ Categories found: {len(categories)}")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    # Test template rendering
    print("\n4. Testing template rendering...")
    try:
        with app.test_client() as client:
            # Login first
            with client.session_transaction() as sess:
                sess['_user_id'] = str(admin.id)
            
            # Try to access products page
            response = client.get('/inventory/products')
            print(f"   Status code: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✓ Page loaded successfully!")
            elif response.status_code == 500:
                print("   ✗ Internal Server Error!")
                print(f"   Response: {response.data[:500]}")
            else:
                print(f"   Response: {response.status_code}")
                
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)


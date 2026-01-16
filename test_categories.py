#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the categories page
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_categories_page():
    """Test categories page"""
    
    print("=" * 80)
    print("TESTING CATEGORIES PAGE")
    print("=" * 80)
    
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            # Login
            print("\n1. Logging in...")
            response = client.post('/auth/login', data={
                'username': 'admin',
                'password': 'admin123'
            }, follow_redirects=True)
            
            if response.status_code != 200:
                print(f"❌ Login failed: {response.status_code}")
                return False
            
            print("✅ Logged in successfully")
            
            # Get categories page
            print("\n2. Getting categories page...")
            response = client.get('/inventory/categories')
            
            if response.status_code != 200:
                print(f"❌ Failed to get categories page: {response.status_code}")
                print(f"Response: {response.data.decode('utf-8')[:500]}")
                return False
            
            print("✅ Categories page loaded successfully!")
            
            html = response.data.decode('utf-8')
            
            # Check for key elements
            checks = {
                'Page title': 'التصنيفات' in html,
                'Add button': 'إضافة تصنيف جديد' in html,
                'Table header': '<th>الاسم</th>' in html,
                'Categories route': '/inventory/categories' in html
            }
            
            print("\n" + "=" * 80)
            print("RESULTS:")
            print("=" * 80)
            
            all_found = True
            for name, found in checks.items():
                status = "✅" if found else "❌"
                print(f"{status} {name}: {'Found' if found else 'NOT FOUND'}")
                if not found:
                    all_found = False
            
            print("\n" + "=" * 80)
            
            if all_found:
                print("🎉 SUCCESS! Categories page is working!")
                return True
            else:
                print("❌ FAILED! Some elements are missing")
                return False

if __name__ == '__main__':
    try:
        result = test_categories_page()
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for Purchase Report by Product
Tests that the report works with EUR currency and English translations
"""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

def test_purchases_by_product():
    """Test the purchases by product report"""
    print("=" * 70)
    print("🧪 Testing Purchase Report by Product")
    print("=" * 70)
    print()
    
    app = create_app()
    
    with app.app_context():
        # Get admin user
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("❌ Admin user not found!")
            return
        
        print(f"✅ Admin user found: {admin.username}")
        print()
        
        # Test the route
        with app.test_client() as client:
            # Login
            response = client.post('/auth/login', data={
                'username': 'admin',
                'password': 'admin123'
            }, follow_redirects=True)
            
            if response.status_code == 200:
                print("✅ Login successful")
            else:
                print(f"❌ Login failed: {response.status_code}")
                return
            
            # Test the purchases by product report
            response = client.get('/reports/purchases-by-product')
            
            print()
            print("📊 Testing Purchase Report by Product:")
            print("-" * 70)
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ SUCCESS - Report is working!")
                
                # Check for EUR currency symbol in response
                if '€' in response.data.decode('utf-8'):
                    print("✅ EUR currency symbol (€) found in response")
                else:
                    print("⚠️  EUR currency symbol (€) not found in response")
                
                # Check for English translations
                if 'Purchase Report by Product' in response.data.decode('utf-8'):
                    print("✅ English translation found")
                else:
                    print("⚠️  English translation not found")
                    
            else:
                print(f"❌ FAILED - Status code: {response.status_code}")
                print(response.data.decode('utf-8')[:500])
    
    print()
    print("=" * 70)
    print("✅ Test Complete!")
    print("=" * 70)

if __name__ == '__main__':
    test_purchases_by_product()


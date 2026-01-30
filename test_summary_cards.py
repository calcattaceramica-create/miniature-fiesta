#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify summary cards in Purchase Report by Product
"""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

def test_summary_cards():
    """Test the summary cards in purchases by product report"""
    print("=" * 70)
    print("🧪 Testing Summary Cards in Purchase Report by Product")
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
                
                html = response.data.decode('utf-8')
                
                # Check for summary cards
                checks = [
                    ('Total Products', 'Total Products card'),
                    ('Total Quantity', 'Total Quantity card'),
                    ('Total Amount', 'Total Amount card'),
                    ('bg-primary', 'Primary card style'),
                    ('bg-success', 'Success card style'),
                    ('bg-info', 'Info card style'),
                    ('fa-boxes', 'Boxes icon'),
                    ('fa-cubes', 'Cubes icon'),
                    ('fa-money-bill-wave', 'Money icon'),
                    ('€', 'EUR currency symbol'),
                ]
                
                print()
                print("🔍 Checking Summary Cards Elements:")
                print("-" * 70)
                
                for check_text, description in checks:
                    if check_text in html:
                        print(f"✅ {description}: Found")
                    else:
                        print(f"❌ {description}: NOT FOUND")
                
            else:
                print(f"❌ FAILED - Status code: {response.status_code}")
    
    print()
    print("=" * 70)
    print("✅ Test Complete!")
    print("=" * 70)

if __name__ == '__main__':
    test_summary_cards()


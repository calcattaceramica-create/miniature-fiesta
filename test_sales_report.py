#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script for Sales Report cards"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_sales_report():
    """Test the sales report cards"""
    app = create_app()
    
    with app.test_client() as client:
        print("=" * 70)
        print("🧪 Testing Sales Report Cards")
        print("=" * 70)
        
        # Login first
        print("\n🔐 Logging in...")
        response = client.post('/auth/login', data={
            'license_key': 'CEC9-79EE-C42F-2DAD',
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        
        if response.status_code == 200:
            print("✅ Login successful")
        else:
            print(f"❌ Login failed with status {response.status_code}")
            return
        
        # Test sales report
        print("\n📊 Testing Sales Report...")
        response = client.get('/reports/sales')
        
        print(f"\nStatus code: {response.status_code}")
        
        if response.status_code == 200:
            html = response.data.decode('utf-8')
            
            print("✅ SUCCESS - Report is working!")
            
            # Check CSS
            print("\n🎨 Checking CSS:")
            print("-" * 70)
            checks = {
                'bg-gradient-success CSS': 'bg-gradient-success' in html,
                'bg-gradient-primary CSS': 'bg-gradient-primary' in html,
                'bg-gradient-warning CSS': 'bg-gradient-warning' in html,
                'linear-gradient': 'linear-gradient' in html,
            }
            
            for check, result in checks.items():
                print(f"{'✅' if result else '❌'} {check}: {'Found' if result else 'NOT FOUND'}")
            
            # Check Data
            print("\n📊 Checking Data:")
            print("-" * 70)
            data_checks = {
                'Total Invoices label': 'Total Invoices' in html or 'إجمالي الفواتير' in html,
                'Total Sales label': 'Total Sales' in html or 'إجمالي المبيعات' in html,
                'Total Tax label': 'Total Tax' in html or 'إجمالي الضريبة' in html,
                'EUR currency symbol': '€' in html,
            }
            
            for check, result in data_checks.items():
                print(f"{'✅' if result else '❌'} {check}: {'Found' if result else 'NOT FOUND'}")
            
            # Check Icons
            print("\n🎨 Checking Icons:")
            print("-" * 70)
            icon_checks = {
                'Invoice icon': 'fa-file-invoice' in html,
                'Chart line icon': 'fa-chart-line' in html,
                'Percentage icon': 'fa-percentage' in html,
            }
            
            for check, result in icon_checks.items():
                print(f"{'✅' if result else '❌'} {check}: {'Found' if result else 'NOT FOUND'}")
            
        else:
            print(f"❌ FAILED - Status code: {response.status_code}")
            print(response.data.decode('utf-8')[:500])
        
        print("\n" + "=" * 70)
        print("✅ Test Complete!")
        print("=" * 70)

if __name__ == '__main__':
    test_sales_report()


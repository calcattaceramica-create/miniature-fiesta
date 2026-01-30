#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script for Inventory Report card"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask import url_for

def test_inventory_card():
    """Test the inventory report card"""
    app = create_app()
    
    with app.test_client() as client:
        print("=" * 70)
        print("🧪 Testing Inventory Report Card")
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
        
        # Test inventory report
        print("\n📊 Testing Inventory Report...")
        response = client.get('/reports/inventory')
        
        print(f"\nStatus code: {response.status_code}")
        
        if response.status_code == 200:
            html = response.data.decode('utf-8')
            
            print("✅ SUCCESS - Report is working!")
            
            # Check CSS
            print("\n🎨 Checking CSS:")
            print("-" * 70)
            checks = {
                'bg-gradient-primary CSS': 'bg-gradient-primary' in html,
                'linear-gradient': 'linear-gradient' in html,
                'text-white-50': 'text-white-50' in html,
            }
            
            for check, result in checks.items():
                print(f"{'✅' if result else '❌'} {check}: {'Found' if result else 'NOT FOUND'}")
            
            # Check Data
            print("\n📊 Checking Data:")
            print("-" * 70)
            data_checks = {
                'Total Inventory Value label': 'Total Inventory Value' in html or 'إجمالي قيمة المخزون' in html,
                'EUR currency symbol': '€' in html,
                'Warehouse icon': 'fa-warehouse' in html,
            }
            
            for check, result in data_checks.items():
                print(f"{'✅' if result else '❌'} {check}: {'Found' if result else 'NOT FOUND'}")
            
            # Check card structure
            print("\n🏗️ Checking Card Structure:")
            print("-" * 70)
            structure_checks = {
                'Card with gradient': 'bg-gradient-primary text-white' in html,
                'Display-4 class': 'display-4' in html,
                'Shadow-lg class': 'shadow-lg' in html,
            }
            
            for check, result in structure_checks.items():
                print(f"{'✅' if result else '❌'} {check}: {'Found' if result else 'NOT FOUND'}")
            
        else:
            print(f"❌ FAILED - Status code: {response.status_code}")
            print(response.data.decode('utf-8')[:500])
        
        print("\n" + "=" * 70)
        print("✅ Test Complete!")
        print("=" * 70)

if __name__ == '__main__':
    test_inventory_card()


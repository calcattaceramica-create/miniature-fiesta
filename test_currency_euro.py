#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify EUR currency in Purchase Report by Product
"""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_currency():
    """Test that the default currency is EUR"""
    print("=" * 70)
    print("🧪 Testing Currency Configuration")
    print("=" * 70)
    print()
    
    app = create_app()
    
    with app.app_context():
        default_currency = app.config.get('DEFAULT_CURRENCY')
        currencies = app.config.get('CURRENCIES', {})
        currency_info = currencies.get(default_currency, {})
        
        print(f"📊 Default Currency: {default_currency}")
        print(f"💰 Currency Name: {currency_info.get('name', 'N/A')}")
        print(f"💵 Currency Symbol: {currency_info.get('symbol', 'N/A')}")
        print()
        
        if default_currency == 'EUR':
            print("✅ SUCCESS - Default currency is EUR (Euro)")
            print(f"✅ Symbol: {currency_info.get('symbol', 'N/A')}")
        else:
            print(f"❌ FAILED - Default currency is {default_currency}, not EUR")
        
        print()
        print("📋 Available Currencies:")
        print("-" * 70)
        for code, info in currencies.items():
            marker = "👉" if code == default_currency else "  "
            print(f"{marker} {code}: {info.get('name', 'N/A')} ({info.get('symbol', 'N/A')})")
    
    print()
    print("=" * 70)
    print("✅ Test Complete!")
    print("=" * 70)

if __name__ == '__main__':
    test_currency()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test translations in live Flask app
اختبار الترجمات في تطبيق Flask الحي
"""

from babel.support import Translations

def test_translations():
    """Test translations"""
    print("=" * 70)
    print("🧪 Testing Translations")
    print("=" * 70)
    print()

    if True:
        # Test Arabic translations
        print("📝 Testing Arabic Translations:")
        print("-" * 70)
        
        t = Translations.load('translations', ['ar'])
        
        test_strings = [
            'Cash Flow Report',
            'Accounts Receivable Report',
            'Inventory Value Report',
            'Supplier List',
            'Customer List',
            'Supplier Balances Report',
            'Customer Balances Report',
            'Supplier History Report',
            'Customer History Report',
            'Session',
            'Cashier',
            'Warehouse',
            'Time'
        ]
        
        for string in test_strings:
            translation = t.gettext(string)
            status = "✅" if translation != string else "❌"
            print(f"{status} {string:40} → {translation}")
        
        print()
        print("=" * 70)
        print("✅ Test Complete!")
        print("=" * 70)

if __name__ == '__main__':
    test_translations()


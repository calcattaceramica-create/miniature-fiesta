#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Reports Center translation
اختبار ترجمة مركز التقارير
"""

from app import create_app
from flask_babel import gettext

app = create_app()

with app.app_context():
    print("=" * 70)
    print("🧪 Testing Reports Center Translation")
    print("=" * 70)
    print()
    
    # Test Arabic
    print("📝 Arabic Translations:")
    print("-" * 70)
    
    with app.test_request_context():
        from flask import session
        session['language'] = 'ar'
        
        print(f"Reports Center: {gettext('Reports Center')}")
        print(f"Select the required report: {gettext('Select the required report')}")
        print(f"Sales Reports: {gettext('Sales Reports')}")
        print(f"Detailed Sales Report: {gettext('Detailed Sales Report')}")
        print(f"Sales Report by Product: {gettext('Sales Report by Product')}")
        print(f"Sales Report by Customer: {gettext('Sales Report by Customer')}")
        print(f"Purchase Reports: {gettext('Purchase Reports')}")
        print(f"Inventory Reports: {gettext('Inventory Reports')}")
        print(f"Financial Reports: {gettext('Financial Reports')}")
        print(f"Customer Reports: {gettext('Customer Reports')}")
        print(f"Supplier Reports: {gettext('Supplier Reports')}")
    
    print()
    print("=" * 70)
    print("📝 English Translations:")
    print("-" * 70)

    # Force English locale
    from flask import g
    with app.test_request_context():
        g.locale = 'en'
        session['language'] = 'en'

        # Reimport gettext to get fresh translations
        from flask_babel import gettext as _

        print(f"Reports Center: {_('Reports Center')}")
        print(f"Select the required report: {_('Select the required report')}")
        print(f"Sales Reports: {_('Sales Reports')}")
        print(f"Detailed Sales Report: {_('Detailed Sales Report')}")
        print(f"Sales Report by Product: {_('Sales Report by Product')}")
        print(f"Sales Report by Customer: {_('Sales Report by Customer')}")
        print(f"Purchase Reports: {_('Purchase Reports')}")
        print(f"Inventory Reports: {_('Inventory Reports')}")
        print(f"Financial Reports: {_('Financial Reports')}")
        print(f"Customer Reports: {_('Customer Reports')}")
        print(f"Supplier Reports: {_('Supplier Reports')}")
    
    print()
    print("=" * 70)
    print("✅ Translation test completed!")
    print("=" * 70)


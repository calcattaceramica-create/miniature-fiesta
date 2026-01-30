#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test currency translations"""

from app import create_app, db
from flask import session
from flask_babel import gettext

app = create_app()

with app.app_context():
    # Test Arabic
    with app.test_request_context():
        session['language'] = 'ar'

        # Currency name translations mapping
        currency_names = {
            'SAR': gettext('Saudi Riyal'),
            'USD': gettext('US Dollar'),
            'EUR': gettext('Euro'),
            'AED': gettext('UAE Dirham'),
            'KWD': gettext('Kuwaiti Dinar'),
            'BHD': gettext('Bahraini Dinar'),
            'OMR': gettext('Omani Riyal'),
            'QAR': gettext('Qatari Riyal'),
            'EGP': gettext('Egyptian Pound'),
        }

        print("=" * 60)
        print("Testing Arabic Currency:")
        print("=" * 60)
        print(f"SAR: {currency_names['SAR']}")
        print(f"USD: {currency_names['USD']}")
        print(f"EUR: {currency_names['EUR']}")
        print("=" * 60)

    # Test English
    with app.test_request_context():
        session['language'] = 'en'

        # Currency name translations mapping
        currency_names = {
            'SAR': gettext('Saudi Riyal'),
            'USD': gettext('US Dollar'),
            'EUR': gettext('Euro'),
            'AED': gettext('UAE Dirham'),
            'KWD': gettext('Kuwaiti Dinar'),
            'BHD': gettext('Bahraini Dinar'),
            'OMR': gettext('Omani Riyal'),
            'QAR': gettext('Qatari Riyal'),
            'EGP': gettext('Egyptian Pound'),
        }

        print("\n" + "=" * 60)
        print("Testing English Currency:")
        print("=" * 60)
        print(f"SAR: {currency_names['SAR']}")
        print(f"USD: {currency_names['USD']}")
        print(f"EUR: {currency_names['EUR']}")
        print("=" * 60)


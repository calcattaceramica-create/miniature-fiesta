#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test company page translations"""

from app import create_app, db
from flask_babel import gettext

app = create_app()

with app.app_context():
    # Test Arabic translations
    with app.test_request_context():
        from flask import session
        session['language'] = 'ar'
        
        print("=" * 60)
        print("Testing Arabic Translations:")
        print("=" * 60)
        
        texts = [
            "Company Data and Invoice Settings",
            "Manage company information, logo, and invoice and quotation data",
            "Back to Settings",
            "Invoice Templates",
            "Important Note",
            "The data you enter here will appear on all invoices and quotations printed from the POS and system",
            "Basic Information",
            "Company Name (English)",
            "Company Name (Arabic)",
            "Tax Number",
            "Commercial Register",
            "Phone",
            "Email",
            "Appears on invoices",
            "Tax number registered with the Zakat and Tax Authority"
        ]
        
        for text in texts:
            translated = gettext(text)
            print(f"EN: {text}")
            print(f"AR: {translated}")
            print("-" * 60)
    
    # Test English translations
    with app.test_request_context():
        from flask import session
        session['language'] = 'en'
        
        print("\n" + "=" * 60)
        print("Testing English Translations:")
        print("=" * 60)
        
        for text in texts[:3]:
            translated = gettext(text)
            print(f"Original: {text}")
            print(f"Translated: {translated}")
            print("-" * 60)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup Company Currency
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Company
from app.tenant_manager import TenantManager

def setup_currency():
    """Setup or update company currency"""
    
    license_key = 'CEC9-79EE-C42F-2DAD'
    
    print("=" * 80)
    print("⚙️  إعداد عملة الشركة")
    print("=" * 80)
    print()
    
    # Create app
    app = create_app()
    
    with app.app_context():
        # Switch to tenant database
        tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
        app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri
        db.engine.dispose()
        
        print(f"✅ Connected to: {tenant_db_uri}")
        print()
        
        # Check if company exists
        company = Company.query.first()
        
        if company:
            print(f"📊 الشركة الحالية:")
            print(f"   الاسم: {company.name}")
            print(f"   العملة الحالية: {company.currency}")
            print()
            
            # Ask user if they want to change currency
            print("العملات المتاحة:")
            currencies = app.config['CURRENCIES']
            for code, info in currencies.items():
                print(f"   {code} - {info['name']} ({info['symbol']})")
            print()
            
            new_currency = input("أدخل رمز العملة الجديدة (اضغط Enter للإبقاء على الحالية): ").strip().upper()
            
            if new_currency and new_currency in currencies:
                company.currency = new_currency
                db.session.commit()
                print()
                print(f"✅ تم تحديث العملة إلى: {new_currency} - {currencies[new_currency]['name']}")
            elif new_currency:
                print()
                print(f"⚠️  العملة '{new_currency}' غير متاحة!")
            else:
                print()
                print(f"✅ تم الإبقاء على العملة الحالية: {company.currency}")
        else:
            print("⚠️  لا توجد بيانات شركة!")
            print("سيتم إنشاء شركة جديدة...")
            print()
            
            # Create new company
            company = Company(
                name='شركة تجريبية',
                name_en='Demo Company',
                currency='SAR',
                tax_rate=15.0
            )
            db.session.add(company)
            db.session.commit()
            
            print(f"✅ تم إنشاء شركة جديدة بالعملة: SAR - ريال سعودي")
        
        print()
        print("=" * 80)
        print("✅ اكتمل!")
        print("=" * 80)

if __name__ == '__main__':
    setup_currency()


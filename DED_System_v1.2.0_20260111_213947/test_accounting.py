#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار النظام المحاسبي
"""

from app import create_app, db
from app.models_accounting import Account, JournalEntry, Payment, BankAccount, CostCenter
from jinja2 import TemplateError

def test_app():
    """اختبار التطبيق"""
    print("=" * 60)
    print("🧪 اختبار النظام المحاسبي")
    print("=" * 60)
    
    # إنشاء التطبيق
    app = create_app()
    
    with app.app_context():
        # 1. اختبار قاعدة البيانات
        print("\n1️⃣ اختبار قاعدة البيانات...")
        tables = db.metadata.tables.keys()
        accounting_tables = [
            'accounts', 'journal_entries', 'journal_entry_items',
            'payments', 'bank_accounts', 'cost_centers'
        ]
        
        for table in accounting_tables:
            if table in tables:
                print(f"   ✅ جدول {table} موجود")
            else:
                print(f"   ❌ جدول {table} غير موجود")
        
        # 2. اختبار النماذج
        print("\n2️⃣ اختبار النماذج (Models)...")
        models = [Account, JournalEntry, Payment, BankAccount, CostCenter]
        for model in models:
            print(f"   ✅ نموذج {model.__name__} جاهز")
        
        # 3. اختبار القوالب
        print("\n3️⃣ اختبار القوالب (Templates)...")
        templates = [
            'accounting/dashboard.html',
            'accounting/accounts.html',
            'accounting/add_account.html',
            'accounting/journal_entries.html',
            'accounting/add_journal_entry.html',
            'accounting/payments.html',
            'accounting/reports.html',
        ]
        
        for template in templates:
            try:
                app.jinja_env.get_template(template)
                print(f"   ✅ قالب {template} جاهز")
            except TemplateError as e:
                print(f"   ❌ خطأ في قالب {template}: {e}")
        
        # 4. اختبار المسارات
        print("\n4️⃣ اختبار المسارات (Routes)...")
        with app.test_request_context():
            from flask import url_for
            routes = [
                ('accounting.dashboard', 'لوحة التحكم'),
                ('accounting.accounts', 'دليل الحسابات'),
                ('accounting.add_account', 'إضافة حساب'),
                ('accounting.journal_entries', 'القيود اليومية'),
                ('accounting.add_journal_entry', 'إضافة قيد'),
                ('accounting.payments', 'المدفوعات'),
                ('accounting.reports', 'التقارير'),
            ]
            
            for route, name in routes:
                try:
                    url = url_for(route)
                    print(f"   ✅ مسار {name}: {url}")
                except Exception as e:
                    print(f"   ❌ خطأ في مسار {name}: {e}")
        
        # 5. اختبار البيانات
        print("\n5️⃣ اختبار البيانات...")
        account_count = Account.query.count()
        entry_count = JournalEntry.query.count()
        payment_count = Payment.query.count()
        
        print(f"   📊 عدد الحسابات: {account_count}")
        print(f"   📊 عدد القيود: {entry_count}")
        print(f"   📊 عدد المدفوعات: {payment_count}")
        
    print("\n" + "=" * 60)
    print("✅ اكتمل الاختبار بنجاح!")
    print("=" * 60)
    print("\n🚀 يمكنك الآن تشغيل التطبيق:")
    print("   python run.py")
    print("\n🌐 ثم افتح المتصفح على:")
    print("   http://localhost:5000/accounting/dashboard")
    print("=" * 60)

if __name__ == '__main__':
    test_app()


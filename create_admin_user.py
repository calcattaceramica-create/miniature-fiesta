#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
سكريبت لإنشاء مستخدم مدير افتراضي
يتم تشغيله تلقائياً على Render
"""
import os
import sys
from datetime import datetime

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User, Role, Branch, Company
from werkzeug.security import generate_password_hash

def create_default_admin():
    """إنشاء مستخدم مدير افتراضي"""
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if admin user already exists
            admin_user = User.query.filter_by(username='admin').first()
            if admin_user:
                print("✅ المستخدم 'admin' موجود بالفعل")
                return True
            
            # Get or create default company
            company = Company.query.first()
            if not company:
                company = Company(
                    name='DED ERP',
                    name_ar='شركة DED',
                    tax_number='1234567890',
                    phone='+966-XXX-XXXX',
                    email='info@ded-erp.com',
                    address='الرياض، المملكة العربية السعودية',
                    is_active=True,
                    created_at=datetime.utcnow()
                )
                db.session.add(company)
                db.session.commit()
                print("✅ تم إنشاء الشركة الافتراضية")
            
            # Get or create default branch
            branch = Branch.query.filter_by(company_id=company.id).first()
            if not branch:
                branch = Branch(
                    name='الفرع الرئيسي',
                    company_id=company.id,
                    phone='+966-XXX-XXXX',
                    email='main@ded-erp.com',
                    address='الرياض، المملكة العربية السعودية',
                    is_active=True,
                    is_main=True,
                    created_at=datetime.utcnow()
                )
                db.session.add(branch)
                db.session.commit()
                print("✅ تم إنشاء الفرع الافتراضي")
            
            # Get or create admin role
            admin_role = Role.query.filter_by(name='admin').first()
            if not admin_role:
                admin_role = Role(
                    name='admin',
                    name_ar='مدير النظام',
                    description='System Administrator with full access'
                )
                db.session.add(admin_role)
                db.session.commit()
                print("✅ تم إنشاء دور المدير")
            
            # Create admin user
            admin_user = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                full_name='مدير النظام',
                email='admin@ded-erp.com',
                is_active=True,
                is_admin=True,
                company_id=company.id,
                branch_id=branch.id,
                role_id=admin_role.id,
                created_at=datetime.utcnow()
            )
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("=" * 60)
            print("✅ تم إنشاء المستخدم المدير بنجاح!")
            print("=" * 60)
            print("اسم المستخدم: admin")
            print("كلمة المرور: admin123")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء المستخدم: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("🔑 إنشاء مستخدم مدير افتراضي...")
    create_default_admin()


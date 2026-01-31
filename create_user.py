#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
سكريبت لإنشاء مستخدم جديد في النظام
"""
import os
import sys
from datetime import datetime

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User, Role, Branch, Company
from werkzeug.security import generate_password_hash

def create_user(username, password, full_name, email, is_admin=False):
    """إنشاء مستخدم جديد"""
    
    app = create_app()
    
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"❌ المستخدم '{username}' موجود بالفعل!")
            return False
        
        # Get default company and branch
        company = Company.query.first()
        if not company:
            print("❌ لا توجد شركة في النظام! يجب إنشاء شركة أولاً.")
            return False
        
        branch = Branch.query.filter_by(company_id=company.id).first()
        if not branch:
            print("❌ لا يوجد فرع في النظام! يجب إنشاء فرع أولاً.")
            return False
        
        # Get or create role
        if is_admin:
            role = Role.query.filter_by(name='admin').first()
            if not role:
                role = Role(
                    name='admin',
                    name_ar='مدير النظام',
                    description='System Administrator'
                )
                db.session.add(role)
                db.session.commit()
        else:
            role = Role.query.filter_by(name='user').first()
            if not role:
                role = Role(
                    name='user',
                    name_ar='مستخدم',
                    description='Regular User'
                )
                db.session.add(role)
                db.session.commit()
        
        # Create new user
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            email=email,
            is_active=True,
            is_admin=is_admin,
            company_id=company.id,
            branch_id=branch.id,
            role_id=role.id,
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        print("✅ تم إنشاء المستخدم بنجاح!")
        print(f"   اسم المستخدم: {username}")
        print(f"   كلمة المرور: {password}")
        print(f"   الاسم الكامل: {full_name}")
        print(f"   البريد الإلكتروني: {email}")
        print(f"   مدير النظام: {'نعم' if is_admin else 'لا'}")
        
        return True

if __name__ == '__main__':
    print("=" * 50)
    print("إنشاء مستخدم جديد")
    print("=" * 50)
    
    # Get user input
    username = input("اسم المستخدم (Username): ").strip()
    password = input("كلمة المرور (Password): ").strip()
    full_name = input("الاسم الكامل (Full Name): ").strip()
    email = input("البريد الإلكتروني (Email): ").strip()
    is_admin_input = input("هل هو مدير النظام؟ (y/n): ").strip().lower()
    
    is_admin = is_admin_input in ['y', 'yes', 'نعم', 'ن']
    
    # Validate input
    if not username or not password or not full_name:
        print("❌ يجب إدخال اسم المستخدم وكلمة المرور والاسم الكامل!")
        sys.exit(1)
    
    # Create user
    success = create_user(username, password, full_name, email, is_admin)
    
    if success:
        print("\n✅ تم إنشاء المستخدم بنجاح!")
        print("\nيمكنك الآن تسجيل الدخول باستخدام:")
        print(f"   اسم المستخدم: {username}")
        print(f"   كلمة المرور: {password}")
    else:
        print("\n❌ فشل إنشاء المستخدم!")
        sys.exit(1)


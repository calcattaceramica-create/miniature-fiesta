#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug script to test language settings
"""

from app import create_app, db
from app.models import User
from flask import session

app = create_app()

with app.app_context():
    with app.test_request_context():
        # Get admin user
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print(f"✅ Admin user found")
            print(f"   Username: {admin.username}")
            print(f"   Language in DB: {admin.language}")
            
            # Update admin language to English
            admin.language = 'en'
            db.session.commit()
            print(f"✅ Updated admin language to 'en'")
            
            # Verify
            admin = User.query.filter_by(username='admin').first()
            print(f"✅ Verified - Language in DB: {admin.language}")
        else:
            print("❌ Admin user not found")


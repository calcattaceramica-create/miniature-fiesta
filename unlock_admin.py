#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unlock admin account
"""
from app import create_app
from app.models import User
from datetime import datetime

app = create_app()

with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print("=" * 70)
        print("Unlocking admin account...")
        print("=" * 70)
        
        # Reset failed login attempts
        admin.failed_login_attempts = 0
        admin.account_locked_until = None
        admin.last_failed_login = None
        
        from app import db
        db.session.commit()
        
        print("✓ Admin account unlocked successfully!")
        print(f"  Username: {admin.username}")
        print(f"  Failed attempts: {admin.failed_login_attempts}")
        print(f"  Account locked until: {admin.account_locked_until}")
        print("=" * 70)
        print("\nYou can now login with:")
        print("  Username: admin")
        print("  Password: admin123")
        print("=" * 70)
    else:
        print("ERROR: Admin user not found!")


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Apply Damaged Inventory Migration
"""

from app import db, create_app

app = create_app()

with app.app_context():
    try:
        # Read migration file
        with open('migrations/add_damaged_inventory.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # Split by semicolon and execute each statement
        statements = [s.strip() for s in sql.split(';') if s.strip() and not s.strip().startswith('--')]
        
        for statement in statements:
            if statement:
                print(f"Executing: {statement[:50]}...")
                db.session.execute(db.text(statement))
        
        db.session.commit()
        print("\n✅ Migration applied successfully!")
        print("✅ Added 'damaged_quantity' column to stocks table")
        print("✅ Created 'damaged_inventory' table")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error applying migration: {e}")
        import traceback
        traceback.print_exc()


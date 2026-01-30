#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check and Fix Database Schema
"""

from app import db, create_app

app = create_app()

with app.app_context():
    try:
        # Check if damaged_inventory table exists
        result = db.session.execute(db.text(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='damaged_inventory'"
        ))
        table_exists = bool(list(result))
        
        if not table_exists:
            print("❌ Table 'damaged_inventory' does not exist. Creating it...")
            
            # Create damaged_inventory table
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS damaged_inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                warehouse_id INTEGER NOT NULL,
                quantity REAL NOT NULL,
                reason VARCHAR(200),
                damage_type VARCHAR(50),
                cost_value REAL DEFAULT 0.0,
                notes TEXT,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id),
                FOREIGN KEY (warehouse_id) REFERENCES warehouses (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
            db.session.execute(db.text(create_table_sql))
            db.session.commit()
            print("✅ Table 'damaged_inventory' created successfully!")
        else:
            print("✅ Table 'damaged_inventory' already exists")
        
        # Check if damaged_quantity column exists in stocks table
        result = db.session.execute(db.text("PRAGMA table_info(stocks)"))
        columns = [row[1] for row in result]
        
        if 'damaged_quantity' not in columns:
            print("❌ Column 'damaged_quantity' does not exist in stocks table")
        else:
            print("✅ Column 'damaged_quantity' exists in stocks table")
        
        # Update all existing stocks to have damaged_quantity = 0
        db.session.execute(db.text(
            "UPDATE stocks SET damaged_quantity = 0.0 WHERE damaged_quantity IS NULL"
        ))
        db.session.commit()
        print("✅ Updated existing stocks with damaged_quantity = 0")
        
        print("\n✅ Database schema is ready!")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


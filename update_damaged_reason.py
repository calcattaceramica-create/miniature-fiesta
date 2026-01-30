#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update damaged inventory reason from Arabic to English
"""

from app import create_app, db
from app.models_inventory import DamagedInventory

def update_reasons():
    """Update damaged inventory reasons"""
    app = create_app()
    
    with app.app_context():
        # Translation mapping
        translations = {
            'عند التحميل': 'During Loading',
            'تلف التحميل': 'Loading Damage',
            'تلف أثناء النقل': 'Transport Damage',
            'منتهي الصلاحية': 'Expired',
            'مكسور': 'Broken',
            'معيب': 'Defective',
            'تالف': 'Damaged',
        }
        
        # Get all damaged inventory records
        damaged_items = DamagedInventory.query.all()
        
        updated_count = 0
        for item in damaged_items:
            if item.reason in translations:
                old_reason = item.reason
                item.reason = translations[item.reason]
                print(f"✅ Updated: '{old_reason}' → '{item.reason}'")
                updated_count += 1
        
        if updated_count > 0:
            db.session.commit()
            print(f"\n✅ Successfully updated {updated_count} record(s)")
        else:
            print("\nℹ️  No records to update")

if __name__ == '__main__':
    update_reasons()


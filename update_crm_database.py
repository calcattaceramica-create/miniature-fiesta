#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to update database with CRM tables
"""

from app import create_app, db
from app.models_crm import Lead, Interaction, Opportunity, Task, Campaign, Contact

def update_database():
    """Update database with CRM tables"""
    app = create_app()
    
    with app.app_context():
        print("Starting database update for CRM...")
        
        try:
            # Create all CRM tables
            db.create_all()
            
            print("\n✅ Database updated successfully!")
            print("CRM tables created:")
            print("  - leads")
            print("  - interactions")
            print("  - opportunities")
            print("  - tasks")
            print("  - campaigns")
            print("  - contacts")
            
        except Exception as e:
            print(f"\n❌ Error updating database: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    update_database()


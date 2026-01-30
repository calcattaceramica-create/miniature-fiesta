"""Check user permissions"""
import os
import sys

# Set the working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Role, Permission

app = create_app()

with app.app_context():
    # Get admin user
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print(f"User: {admin.username}")
        print(f"Role: {admin.role.name if admin.role else 'No role'}")
        
        if admin.role:
            print(f"\nRole permissions:")
            for perm in admin.role.permissions:
                print(f"  - {perm.name} ({perm.module})")
        
        # Check specific permission
        print(f"\nHas 'reports.view' permission: {admin.has_permission('reports.view')}")
        print(f"Has 'reports.purchases' permission: {admin.has_permission('reports.purchases')}")
    else:
        print("Admin user not found!")


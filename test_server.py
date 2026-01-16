#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test server startup
"""
import sys
import traceback

try:
    print("=" * 60)
    print("Step 1: Importing modules...")
    from app import create_app
    print("✓ Modules imported successfully")
    
    print("\nStep 2: Creating app...")
    app = create_app()
    print("✓ App created successfully")
    
    print("\nStep 3: Testing models...")
    from app.models import User, Role, Permission
    print("✓ Models imported successfully")
    
    print("\nStep 4: Testing database connection...")
    with app.app_context():
        user_count = User.query.count()
        role_count = Role.query.count()
        permission_count = Permission.query.count()
        print(f"✓ Database connected successfully")
        print(f"  - Users: {user_count}")
        print(f"  - Roles: {role_count}")
        print(f"  - Permissions: {permission_count}")
    
    print("\nStep 5: Starting server...")
    print("=" * 60)
    print("Server URL: http://localhost:5000")
    print("Username: admin")
    print("Password: admin123")
    print("=" * 60)
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    
except Exception as e:
    print("\n" + "=" * 60)
    print("ERROR OCCURRED!")
    print("=" * 60)
    print(f"Error: {str(e)}")
    print("\nFull traceback:")
    traceback.print_exc()
    print("=" * 60)
    sys.exit(1)


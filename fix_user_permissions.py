"""
Fix user permissions for mohammed
"""
from app import create_app, db
from app.models import User, Role, Permission

app = create_app('development')

with app.app_context():
    # Find user
    user = User.query.filter_by(username='mohammed').first()
    
    if not user:
        print("❌ User not found!")
    else:
        print(f"✅ Found user: {user.username}")
        print(f"   Current is_admin: {user.is_admin}")
        print(f"   Current role: {user.role}")
        
        # Set is_admin to True
        user.is_admin = True
        
        # Make sure user has admin role
        admin_role = Role.query.filter_by(name='admin').first()
        if admin_role:
            user.role_id = admin_role.id
            print(f"✅ Set role to: {admin_role.name}")
            print(f"   Role has {len(admin_role.permissions)} permissions")
        
        db.session.commit()
        
        print("\n" + "="*60)
        print("UPDATED USER INFO:")
        print("="*60)
        print(f"Username: {user.username}")
        print(f"Is Admin: {user.is_admin}")
        print(f"Role: {user.role.name if user.role else 'None'}")
        print(f"Has dashboard.view: {user.has_permission('dashboard.view')}")
        print("="*60)
        print("\n✅ User permissions fixed!")


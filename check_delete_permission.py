from app import create_app, db
from app.models import Permission, Role, User

app = create_app()

with app.app_context():
    # Check if suppliers.delete permission exists
    delete_perm = Permission.query.filter_by(name='suppliers.delete').first()
    if not delete_perm:
        delete_perm = Permission(
            name='suppliers.delete',
            description='Delete suppliers'
        )
        db.session.add(delete_perm)
        print("Created suppliers.delete permission")
    else:
        print("suppliers.delete permission exists")
    
    # Get admin role
    admin_role = Role.query.filter_by(name='Admin').first()
    if admin_role:
        if delete_perm not in admin_role.permissions:
            admin_role.permissions.append(delete_perm)
            print("Added suppliers.delete to Admin role")
        else:
            print("Admin already has suppliers.delete permission")
    
    # Check admin user permissions
    admin_user = User.query.filter_by(username='admin').first()
    if admin_user:
        print(f"\nAdmin user permissions:")
        if admin_user.role:
            for perm in admin_user.role.permissions:
                if 'supplier' in perm.name:
                    print(f"  - {perm.name}")
    
    db.session.commit()
    print("\nPermissions checked successfully!")


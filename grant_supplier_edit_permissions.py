from app import create_app, db
from app.models import Permission, Role

app = create_app()

with app.app_context():
    # Check if suppliers.edit permission exists
    edit_perm = Permission.query.filter_by(name='suppliers.edit').first()
    if not edit_perm:
        edit_perm = Permission(
            name='suppliers.edit',
            description='Edit suppliers'
        )
        db.session.add(edit_perm)
        print("Created suppliers.edit permission")
    
    # Get admin role
    admin_role = Role.query.filter_by(name='Admin').first()
    if admin_role:
        if edit_perm not in admin_role.permissions:
            admin_role.permissions.append(edit_perm)
            print("Added suppliers.edit to Admin role")
    
    db.session.commit()
    print("Permissions updated successfully!")


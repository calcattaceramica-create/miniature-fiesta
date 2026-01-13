"""
License Synchronization Script
Syncs licenses from licenses.json to database users
"""

import json
from pathlib import Path
from app import create_app, db
from app.models import User, Role
from datetime import datetime

def sync_licenses_to_database():
    """Sync all licenses to database"""
    app = create_app()
    
    with app.app_context():
        license_file = Path('licenses.json')
        sync_file = Path('license_sync.json')
        
        if not license_file.exists():
            print("❌ License file not found!")
            return
        
        # Load licenses
        with open(license_file, 'r', encoding='utf-8') as f:
            licenses = json.load(f)
        
        # Load sync queue
        sync_queue = {}
        if sync_file.exists():
            with open(sync_file, 'r', encoding='utf-8') as f:
                sync_queue = json.load(f)
        
        # Get or create default role
        default_role = Role.query.filter_by(name='User').first()
        if not default_role:
            default_role = Role(name='User', description='Default user role')
            db.session.add(default_role)
            db.session.commit()
        
        synced_count = 0
        updated_count = 0
        
        for license_key, license_data in licenses.items():
            username = license_data.get('username')
            password = license_data.get('password')
            company = license_data.get('company')
            email = license_data.get('contact_email', '')
            status = license_data.get('status', 'active')
            
            if not username or not password:
                print(f"⚠️  Skipping license {license_key[:16]}... - Missing username or password")
                continue
            
            # Check if user exists
            user = User.query.filter_by(username=username).first()
            
            if user:
                # Update existing user
                user.is_active = (status == 'active')
                user.email = email or user.email
                updated_count += 1
                print(f"✅ Updated user: {username} ({company})")
            else:
                # Create new user
                user = User(
                    username=username,
                    email=email or f"{username}@{company.replace(' ', '').lower()}.com",
                    full_name=company,
                    is_active=(status == 'active'),
                    is_admin=False,
                    role_id=default_role.id,
                    language='ar'
                )
                user.set_password(password)
                db.session.add(user)
                synced_count += 1
                print(f"✨ Created user: {username} ({company})")
            
            # Mark as synced in queue
            if license_key in sync_queue:
                sync_queue[license_key]['synced'] = True
                sync_queue[license_key]['synced_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Commit all changes
        db.session.commit()
        
        # Update sync queue
        if sync_file.exists():
            with open(sync_file, 'w', encoding='utf-8') as f:
                json.dump(sync_queue, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print(f"✅ Sync completed!")
        print(f"   - New users created: {synced_count}")
        print(f"   - Existing users updated: {updated_count}")
        print(f"   - Total licenses: {len(licenses)}")
        print(f"{'='*60}\n")

if __name__ == '__main__':
    print("\n🔄 Starting license synchronization...\n")
    sync_licenses_to_database()


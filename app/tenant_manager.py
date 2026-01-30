"""
Multi-Tenancy Manager
مدير التعددية - كل ترخيص له قاعدة بيانات منفصلة
"""
import os
import shutil
from flask import g, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect
from app.models_license import License

class TenantManager:
    """
    Manages multiple tenant databases - one database per license
    يدير قواعد بيانات متعددة - قاعدة بيانات واحدة لكل ترخيص
    """
    
    # Master database for licenses only
    MASTER_DB = 'licenses_master.db'
    
    # Tenant databases directory
    TENANTS_DIR = 'tenant_databases'
    
    @staticmethod
    def get_master_db_path():
        """Get path to master database (licenses only)"""
        basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(basedir, TenantManager.MASTER_DB)
    
    @staticmethod
    def get_tenants_dir():
        """Get path to tenants directory"""
        basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        tenants_path = os.path.join(basedir, TenantManager.TENANTS_DIR)
        
        # Create directory if it doesn't exist
        if not os.path.exists(tenants_path):
            os.makedirs(tenants_path)
        
        return tenants_path
    
    @staticmethod
    def get_tenant_db_path(license_key):
        """
        Get path to tenant database for a specific license
        
        Args:
            license_key: License key (e.g., '9813-26D0-F98D-741C')
        
        Returns:
            Full path to tenant database file
        """
        # Sanitize license key for filename (remove dashes)
        safe_key = license_key.replace('-', '_')
        db_filename = f"tenant_{safe_key}.db"
        
        return os.path.join(TenantManager.get_tenants_dir(), db_filename)
    
    @staticmethod
    def get_tenant_db_uri(license_key):
        """
        Get SQLAlchemy database URI for a specific tenant
        
        Args:
            license_key: License key
        
        Returns:
            SQLAlchemy database URI string
        """
        db_path = TenantManager.get_tenant_db_path(license_key)
        return f'sqlite:///{db_path}'
    
    @staticmethod
    def create_tenant_database(license_key, app):
        """
        Create a new tenant database for a license
        
        Args:
            license_key: License key
            app: Flask application instance
        
        Returns:
            True if successful, False otherwise
        """
        try:
            db_path = TenantManager.get_tenant_db_path(license_key)
            
            # Check if database already exists
            if os.path.exists(db_path):
                print(f"WARNING: Database already exists for license {license_key}")
                return True
            
            # Create database URI
            db_uri = TenantManager.get_tenant_db_uri(license_key)
            
            # Create engine
            engine = create_engine(db_uri)
            
            # Import all models - just import to register them with SQLAlchemy
            # We don't need to use them directly, just import them
            import app.models
            import app.models_inventory
            import app.models_sales
            import app.models_purchases
            import app.models_accounting
            import app.models_crm
            import app.models_hr
            import app.models_pos
            import app.models_settings
            import app.models_license
            
            # Get metadata from db
            from app import db
            
            # Create all tables
            db.metadata.create_all(engine)

            print(f"SUCCESS: Created tenant database for license {license_key}")
            print(f"   Path: {db_path}")

            return True
            
        except Exception as e:
            print(f"ERROR: Error creating tenant database for {license_key}: {e}")
            return False
    
    @staticmethod
    def initialize_tenant_data(license_key, app, license_obj):
        """
        Initialize tenant database with default data

        Args:
            license_key: License key
            app: Flask application instance
            license_obj: License object from master database
        """
        try:
            # Use direct SQLAlchemy connection instead of Flask-SQLAlchemy
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker, scoped_session

            # Create engine for tenant database
            tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
            engine = create_engine(tenant_db_uri)
            Session = scoped_session(sessionmaker(bind=engine))
            session = Session()

            # Import models
            from app.models import User, Role, Branch
            from app.models_accounting import Account

            # Create default roles (check if they exist first)
            admin_role = session.query(Role).filter_by(name='admin').first()
            if not admin_role:
                admin_role = Role(name='admin', name_ar='مدير النظام', description='Full system access')
                session.add(admin_role)

            manager_role = session.query(Role).filter_by(name='manager').first()
            if not manager_role:
                manager_role = Role(name='manager', name_ar='مدير', description='Manager access')
                session.add(manager_role)

            user_role = session.query(Role).filter_by(name='user').first()
            if not user_role:
                user_role = Role(name='user', name_ar='مستخدم', description='Basic user access')
                session.add(user_role)

            session.flush()

            # Create default branch (check if it exists first)
            main_branch = session.query(Branch).filter_by(code='MAIN').first()
            if not main_branch:
                main_branch = Branch(
                    name='الفرع الرئيسي',
                    name_en='Main Branch',
                    code='MAIN',
                    is_active=True
                )
                session.add(main_branch)
                session.flush()
                
            # Create admin user from license (check if exists first)
            print(f"DEBUG: Checking admin user creation for license {license_key}")
            print(f"DEBUG: admin_username={license_obj.admin_username}, has_password_hash={bool(license_obj.admin_password_hash)}")

            if license_obj.admin_username and license_obj.admin_password_hash:
                # Check if user already exists by username or email
                admin_user = session.query(User).filter_by(username=license_obj.admin_username).first()
                print(f"DEBUG: Existing admin_user by username: {admin_user}")

                # Generate a valid email address
                email = license_obj.client_email
                if not email or '@' not in email:
                    # If email is invalid, generate one from username and company
                    email = f"{license_obj.admin_username}@{license_obj.client_company or 'company'}.com"

                print(f"DEBUG: Generated email: {email}")

                # Check if email already exists
                existing_email_user = session.query(User).filter_by(email=email).first()
                print(f"DEBUG: Existing user by email: {existing_email_user}")

                if not admin_user and not existing_email_user:
                    print(f"DEBUG: Creating new admin user: {license_obj.admin_username}")
                    admin_user = User(
                        username=license_obj.admin_username,
                        email=email,
                        full_name=license_obj.client_name,
                        phone=license_obj.client_phone,
                        is_active=True,
                        is_admin=True,
                        role_id=admin_role.id,
                        branch_id=main_branch.id
                    )
                    admin_user.password_hash = license_obj.admin_password_hash
                    session.add(admin_user)
                    print(f"DEBUG: Admin user added to session")
                else:
                    print(f"DEBUG: Admin user already exists - skipping creation")
            else:
                print(f"DEBUG: Missing admin_username or admin_password_hash - skipping user creation")
                
            # Create default chart of accounts (check if they exist first)
            default_accounts = [
                {'code': '1000', 'name': 'الأصول', 'name_en': 'Assets', 'account_type': 'asset'},
                {'code': '2000', 'name': 'الخصوم', 'name_en': 'Liabilities', 'account_type': 'liability'},
                {'code': '3000', 'name': 'حقوق الملكية', 'name_en': 'Equity', 'account_type': 'equity'},
                {'code': '4000', 'name': 'الإيرادات', 'name_en': 'Revenue', 'account_type': 'revenue'},
                {'code': '5000', 'name': 'المصروفات', 'name_en': 'Expenses', 'account_type': 'expense'},
            ]

            for acc_data in default_accounts:
                existing_account = session.query(Account).filter_by(code=acc_data['code']).first()
                if not existing_account:
                    account = Account(
                        code=acc_data['code'],
                        name=acc_data['name'],
                        name_en=acc_data['name_en'],
                        account_type=acc_data['account_type'],
                        is_system=True
                    )
                    session.add(account)

            # Commit all changes
            session.commit()
            print(f"SUCCESS: Initialized tenant data for license {license_key}")

            # Close session and engine
            session.close()
            engine.dispose()

            return True

        except Exception as e:
            print(f"ERROR: Error initializing tenant data for {license_key}: {e}")
            session.rollback()
            session.close()
            engine.dispose()
            return False

    @staticmethod
    def set_current_tenant(license_key):
        """
        Set current tenant in Flask g object and session

        Args:
            license_key: License key to set as current tenant
        """
        g.tenant_license_key = license_key
        session['tenant_license_key'] = license_key

    @staticmethod
    def get_current_tenant():
        """
        Get current tenant license key

        Returns:
            Current tenant license key or None
        """
        # Try to get from g first (request context)
        if hasattr(g, 'tenant_license_key'):
            return g.tenant_license_key

        # Try to get from session
        return session.get('tenant_license_key')

    @staticmethod
    def switch_tenant_database(app, license_key):
        """
        Switch to a specific tenant database

        Args:
            app: Flask application instance
            license_key: License key to switch to

        Returns:
            True if successful, False otherwise
        """
        try:
            db_uri = TenantManager.get_tenant_db_uri(license_key)

            # Check if database exists
            db_path = TenantManager.get_tenant_db_path(license_key)
            if not os.path.exists(db_path):
                print(f"❌ Tenant database not found for license {license_key}")
                return False

            # Update app config
            app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

            # Set current tenant
            TenantManager.set_current_tenant(license_key)

            print(f"✅ Switched to tenant database: {license_key}")
            return True

        except Exception as e:
            print(f"❌ Error switching to tenant {license_key}: {e}")
            return False

    @staticmethod
    def delete_tenant_database(license_key):
        """
        Delete a tenant database (use with caution!)

        Args:
            license_key: License key

        Returns:
            True if successful, False otherwise
        """
        try:
            db_path = TenantManager.get_tenant_db_path(license_key)

            if os.path.exists(db_path):
                os.remove(db_path)
                print(f"✅ Deleted tenant database for license {license_key}")
                return True
            else:
                print(f"⚠️  Tenant database not found for license {license_key}")
                return False

        except Exception as e:
            print(f"❌ Error deleting tenant database for {license_key}: {e}")
            return False

    @staticmethod
    def backup_tenant_database(license_key, backup_dir=None):
        """
        Backup a tenant database

        Args:
            license_key: License key
            backup_dir: Directory to store backup (optional)

        Returns:
            Path to backup file or None if failed
        """
        try:
            from datetime import datetime

            db_path = TenantManager.get_tenant_db_path(license_key)

            if not os.path.exists(db_path):
                print(f"❌ Tenant database not found for license {license_key}")
                return None

            # Create backup directory
            if backup_dir is None:
                basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
                backup_dir = os.path.join(basedir, 'backups')

            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            # Create backup filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_key = license_key.replace('-', '_')
            backup_filename = f"tenant_{safe_key}_backup_{timestamp}.db"
            backup_path = os.path.join(backup_dir, backup_filename)

            # Copy database file
            shutil.copy2(db_path, backup_path)

            print(f"✅ Backed up tenant database for license {license_key}")
            print(f"   Backup: {backup_path}")

            return backup_path

        except Exception as e:
            print(f"❌ Error backing up tenant database for {license_key}: {e}")
            return None

    @staticmethod
    def list_all_tenants():
        """
        List all tenant databases

        Returns:
            List of license keys that have tenant databases
        """
        try:
            tenants_dir = TenantManager.get_tenants_dir()
            tenant_files = [f for f in os.listdir(tenants_dir) if f.startswith('tenant_') and f.endswith('.db')]

            # Extract license keys from filenames
            license_keys = []
            for filename in tenant_files:
                # Remove 'tenant_' prefix and '.db' suffix
                safe_key = filename[7:-3]  # tenant_XXXX_XXXX_XXXX_XXXX.db
                # Convert back to license key format
                license_key = safe_key.replace('_', '-')
                license_keys.append(license_key)

            return license_keys

        except Exception as e:
            print(f"❌ Error listing tenants: {e}")
            return []


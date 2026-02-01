"""
Multi-Tenancy Middleware
Middleware للتعامل مع قواعد البيانات المتعددة
"""
from flask import request, redirect, url_for, flash, session, g, current_app
from flask_login import current_user
from datetime import datetime
from app.models_license import License
from app.tenant_manager import TenantManager
from app import db

# Routes that don't require tenant database
EXEMPT_ROUTES = [
    '/static/',
    '/auth/login',
    '/auth/logout',
    '/auth/register',
    '/activate-license',
    '/license-activation',
    '/licenses-dashboard',  # License management dashboard
    '/license/',  # All license view/edit/delete routes
    '/create-license',  # Create new license
    '/security/license',  # All license management routes use master database
    '/security/create_license',
    '/_debug_toolbar/',  # Flask Debug Toolbar
    '/favicon.ico',
]

def init_tenant_middleware(app):
    """
    Initialize multi-tenancy middleware
    This middleware switches database based on the current tenant (license)
    """
    
    @app.before_request
    def switch_tenant_database():
        """Switch to appropriate tenant database before each request"""

        # Debug: Print request path
        print(f"DEBUG: Request path: {request.path}")

        # Skip for exempt routes - but reset to master database first!
        for exempt_route in EXEMPT_ROUTES:
            if request.path.startswith(exempt_route):
                print(f"DEBUG: Exempt route detected: {request.path}")

                # CRITICAL: Reset to master database for exempt routes
                # This prevents "no such table" errors when accessing login page
                master_db_uri = f'sqlite:///{TenantManager.get_master_db_path()}'
                app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri

                # Dispose old engine
                if hasattr(db, 'engine'):
                    db.engine.dispose()

                # Remove the engine so Flask-SQLAlchemy will recreate it
                if hasattr(db, '_engine'):
                    db._engine = None

                return None
        
        # Get current tenant from session
        tenant_license_key = session.get('tenant_license_key')

        # If no tenant in session, redirect to login
        if not tenant_license_key:
            if current_user.is_authenticated:
                # User is authenticated but no tenant - logout
                flash('خطأ في تحديد الترخيص. يرجى تسجيل الدخول مرة أخرى.', 'error')
                return redirect(url_for('auth.logout'))
            return redirect(url_for('auth.login'))
        
        # Get master database URI
        master_db_uri = f'sqlite:///{TenantManager.get_master_db_path()}'
        
        # Check license validity in master database
        # Temporarily switch to master database
        original_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        
        try:
            # Switch to master database
            app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri

            # Dispose old engine and let Flask-SQLAlchemy recreate it
            if hasattr(db, 'engine'):
                db.engine.dispose()

            # Remove the engine so Flask-SQLAlchemy will recreate it with new URI
            if hasattr(db, '_engine'):
                db._engine = None

            # Check license (we're already in app context from the request)
            license = License.query.filter_by(
                license_key=tenant_license_key,
                is_active=True,
                is_suspended=False
            ).first()

            if not license:
                flash('الترخيص غير نشط أو معلق. يرجى الاتصال بالدعم.', 'error')
                session.pop('tenant_license_key', None)
                return redirect(url_for('auth.login'))

            # Check if license is expired
            if license.expires_at and license.expires_at < datetime.utcnow():
                flash('انتهت صلاحية الترخيص. يرجى تجديد الترخيص.', 'error')
                session.pop('tenant_license_key', None)
                return redirect(url_for('auth.login'))

            # Store license data (not object) to avoid DetachedInstanceError
            g.license_data = {
                'id': license.id,
                'license_key': license.license_key,
                'client_name': license.client_name,
                'client_email': license.client_email,
                'license_type': license.license_type,
                'expires_at': license.expires_at,
                'is_active': license.is_active,
                'is_suspended': license.is_suspended
            }
            g.tenant_license_key = tenant_license_key

            print(f"DEBUG: Switched to tenant database for license: {tenant_license_key}")

        finally:
            # Switch to tenant database
            tenant_db_uri = TenantManager.get_tenant_db_uri(tenant_license_key)
            app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri

            # Dispose old engine and let Flask-SQLAlchemy recreate it
            if hasattr(db, 'engine'):
                db.engine.dispose()

            # Remove the engine so Flask-SQLAlchemy will recreate it with new URI
            if hasattr(db, '_engine'):
                db._engine = None

            print(f"✅ MIDDLEWARE: Switched to tenant database: {tenant_license_key}")
            print(f"✅ MIDDLEWARE: Database URI: {tenant_db_uri}")

        return None
    
    @app.context_processor
    def inject_license():
        """Inject license information into all templates"""
        # Skip for exempt routes to avoid database queries on login page
        for exempt_route in EXEMPT_ROUTES:
            if request.path.startswith(exempt_route):
                return dict(license=None)

        license_data = getattr(g, 'license_data', None)
        return dict(license=license_data)


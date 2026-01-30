"""
Multi-Tenant Login Handler
معالج تسجيل الدخول للنظام متعدد التراخيص
"""
from flask import session, flash, current_app
from flask_login import login_user
from werkzeug.security import check_password_hash
from datetime import datetime
from app import db
from app.models import User, Role
from app.models_license import License
from app.tenant_manager import TenantManager
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def authenticate_with_license(username, password, license_key, app):
    """
    Authenticate user with multi-tenancy support

    Args:
        username: Username
        password: Password
        license_key: License key
        app: Flask application instance

    Returns:
        (success: bool, message: str, user: User or None)
    """

    # Step 1: Verify license in master database
    master_db_uri = f'sqlite:///{TenantManager.get_master_db_path()}'
    original_uri = app.config.get('SQLALCHEMY_DATABASE_URI')

    with app.app_context():
        try:
            # Switch to master database
            app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri
            db.engine.dispose()

            # Find license
            license = License.query.filter_by(license_key=license_key).first()

            if not license:
                return False, '🔑 مفتاح الترخيص غير صحيح', None

            # Check if license is active
            if not license.is_active:
                return False, '🔑 الترخيص غير نشط', None

            # Check if license is suspended
            if license.is_suspended:
                return False, f'🔑 الترخيص معلق: {license.suspension_reason or "يرجى الاتصال بالدعم"}', None

            # Check if license is expired
            if license.expires_at and license.expires_at < datetime.utcnow():
                return False, '🔑 انتهت صلاحية الترخيص', None

            # Store license info for later use
            license_info = {
                'id': license.id,
                'license_key': license.license_key,
                'client_name': license.client_name,
                'client_email': license.client_email,
                'admin_username': license.admin_username,
                'admin_password_hash': license.admin_password_hash
            }

        finally:
            # Don't switch back yet - we'll switch to tenant database next
            pass

        # Step 2: Check if tenant database exists, create if not
        tenant_db_path = TenantManager.get_tenant_db_path(license_key)

        if not os.path.exists(tenant_db_path):
            # Create tenant database
            print(f"📦 Creating tenant database for license {license_key}...")

            # Switch back to master temporarily to get full license object
            app.config['SQLALCHEMY_DATABASE_URI'] = master_db_uri
            db.engine.dispose()

            license = License.query.filter_by(license_key=license_key).first()

            # Create tenant database
            if not TenantManager.create_tenant_database(license_key, app):
                return False, '❌ فشل إنشاء قاعدة بيانات الترخيص', None

            # Initialize tenant data
            if not TenantManager.initialize_tenant_data(license_key, app, license):
                return False, '❌ فشل تهيئة بيانات الترخيص', None

        # Step 3: Switch to tenant database and authenticate user using direct SQLAlchemy
        tenant_db_path = TenantManager.get_tenant_db_path(license_key)
        tenant_engine = create_engine(f'sqlite:///{tenant_db_path}')
        TenantSession = sessionmaker(bind=tenant_engine)
        tenant_session = TenantSession()

        try:
            # Find user in tenant database using direct SQLAlchemy
            user = tenant_session.query(User).filter_by(username=username).first()

            if not user:
                return False, '❌ اسم المستخدم غير موجود', None

            # Verify password
            if not user.check_password(password):
                return False, '❌ كلمة المرور غير صحيحة', None

            # Check if user is active
            if not user.is_active:
                return False, '❌ الحساب غير نشط', None

            # Store user ID
            user_id = user.id

            # Update last login
            user.last_login = datetime.utcnow()
            tenant_session.commit()

        finally:
            tenant_session.close()
            tenant_engine.dispose()

        # Step 4: Switch Flask-SQLAlchemy to tenant database
        tenant_db_uri = TenantManager.get_tenant_db_uri(license_key)
        app.config['SQLALCHEMY_DATABASE_URI'] = tenant_db_uri

        # Completely recreate the engine
        if hasattr(db, 'engine'):
            db.engine.dispose()

        # Create new engine for tenant database
        from sqlalchemy import create_engine as sa_create_engine
        new_engine = sa_create_engine(tenant_db_uri)
        db.session.bind = new_engine

        # Reload user using direct query on new engine
        TenantSession2 = sessionmaker(bind=new_engine)
        tenant_session2 = TenantSession2()

        try:
            user = tenant_session2.query(User).get(user_id)

            if not user:
                return False, '❌ خطأ في تحميل بيانات المستخدم', None

            # Detach user from session to avoid DetachedInstanceError
            tenant_session2.expunge(user)

        finally:
            tenant_session2.close()

        # Set tenant in session (only if we have a request context)
        try:
            session['tenant_license_key'] = license_key
        except RuntimeError:
            # No request context - this is OK for testing
            pass

        return True, '✅ تم تسجيل الدخول بنجاح', user


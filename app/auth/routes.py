from flask import render_template, redirect, url_for, flash, request, session, current_app, make_response
from flask_login import login_user, logout_user, current_user
from flask_babel import gettext as _
from app import db
from app.auth import bp
from app.models import User, SecurityLog, SessionLog
from app.models_license import License
from app.license_manager import LicenseManager
from app.auth.multi_tenant_login import authenticate_with_license
from datetime import datetime
import uuid
import json
from pathlib import Path

def get_client_ip():
    """Get client IP address"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

def log_security_event(user_id, event_type, details=None, severity='info'):
    """Log security event"""
    try:
        log = SecurityLog(
            user_id=user_id,
            event_type=event_type,
            ip_address=get_client_ip(),
            user_agent=request.headers.get('User-Agent', '')[:256],
            details=details,
            severity=severity
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Error logging security event: {e}")

def check_license(username):
    """Check if user has valid license"""
    try:
        license_file = Path('licenses.json')
        if not license_file.exists():
            return False, "ملف التراخيص غير موجود"

        with open(license_file, 'r', encoding='utf-8') as f:
            licenses = json.load(f)

        # Find license for this username
        for key, data in licenses.items():
            if data.get('username') == username:
                # Check license status
                status = data.get('status', 'inactive')
                if status == 'suspended':
                    return False, "الترخيص موقوف مؤقتاً. يرجى التواصل مع المسؤول"

                if status != 'active':
                    return False, "الترخيص غير نشط. يرجى التواصل مع المسؤول"

                # Check expiry date
                expiry = data.get('expiry')
                if expiry:
                    from datetime import datetime
                    expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
                    if expiry_date < datetime.now():
                        return False, f"الترخيص منتهي الصلاحية منذ {expiry}. يرجى التجديد"

                # License is valid
                return True, None

        # No license found for this username
        return False, "لا يوجد ترخيص مسجل لهذا المستخدم"

    except Exception as e:
        print(f"Error checking license: {e}")
        return False, f"خطأ في التحقق من الترخيص: {str(e)}"

@bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            license_key = request.form.get('license_key')
            remember = request.form.get('remember', False)

            # License key is now required
            if not license_key:
                flash('🔑 يرجى إدخال مفتاح الترخيص', 'danger')
                return redirect(url_for('auth.login'))

            # Use Multi-Tenant authentication
            app = current_app._get_current_object()
            success, message, user = authenticate_with_license(
                username, password, license_key, app
            )

            if not success:
                log_security_event(None, 'failed_login',
                                 f'Failed login: {message}', 'warning')
                flash(message, 'danger')
                return redirect(url_for('auth.login'))

            # CRITICAL: authenticate_with_license has already switched to the correct tenant database
            # DO NOT dispose the engine here as it will reset to the default database!

            # Clear session completely (EXCEPT Flask-Login internal keys)
            # We need to preserve Flask-Login's session management
            keys_to_remove = [key for key in session.keys() if not key.startswith('_')]
            for key in keys_to_remove:
                session.pop(key, None)

            print(f"🔥 LOGIN: Cleared session data (kept Flask-Login internal state)")

            # Set tenant license key BEFORE login_user
            session['tenant_license_key'] = license_key
            print(f"✅ LOGIN: Set tenant_license_key in session: {license_key}")

            # Now login the user - this will set Flask-Login session data
            login_user(user, remember=remember)
            print(f"✅ LOGIN: Logged in user: {user.username}")

            # Create session log
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
            session_log = SessionLog(
                user_id=user.id,
                session_id=session_id,
                ip_address=get_client_ip(),
                user_agent=request.headers.get('User-Agent', '')[:256]
            )
            db.session.add(session_log)
            db.session.commit()

            # Log successful login
            log_security_event(user.id, 'successful_login',
                             f'Successful login from {get_client_ip()} with license {license_key[:4]}****', 'info')

            # Set user language in session
            session['language'] = user.language

            # Check if password change is required
            if user.must_change_password:
                flash('يجب عليك تغيير كلمة المرور', 'warning')
                response = make_response(redirect(url_for('auth.change_password')))
                # Add cache-busting headers
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
                return response

            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')

            flash(f'مرحباً {user.full_name}!', 'success')

            # Create response with cache-busting headers to prevent browser caching
            response = make_response(redirect(next_page))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            print(f"✅ LOGIN: Redirecting to {next_page} with cache-busting headers")
            return response

        return render_template('auth/login.html')

    except Exception as e:
        current_app.logger.error(f"Error in login route: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        flash(f'حدث خطأ: {str(e)}', 'danger')
        return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        # Update session log
        session_id = session.get('session_id')
        if session_id:
            session_log = SessionLog.query.filter_by(session_id=session_id).first()
            if session_log:
                session_log.logout_at = datetime.utcnow()
                session_log.is_active = False
                db.session.commit()

        # Log logout event
        log_security_event(current_user.id, 'logout', 'User logged out', 'info')

        logout_user()

        # CRITICAL: Clear ALL session data including tenant info
        session.clear()
        print(f"🔥 LOGOUT: Cleared all session data including tenant_license_key")

        # Force database engine disposal
        if hasattr(db, 'engine'):
            db.engine.dispose()
            print(f"🔥 LOGOUT: Disposed database engine")

        flash('تم تسجيل الخروج بنجاح', 'info')

    # Create response with cache-busting headers
    response = make_response(redirect(url_for('auth.login')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    print(f"✅ LOGOUT: Redirecting to login with cache-busting headers")
    return response

@bp.route('/fix-render-license')
def fix_render_license():
    """
    🔧 Fix license for Render deployment
    - Updates machine_id
    - Creates admin user if missing
    - Recreates tenant database
    """
    try:
        from werkzeug.security import generate_password_hash
        from app.tenant_manager import TenantManager
        import uuid
        import platform
        import os

        # Get current machine ID
        current_machine_id = str(uuid.UUID(int=uuid.getnode()))

        # Find the license
        license_key = "9813-26D0-F98D-741C"
        license = License.query.filter_by(license_key=license_key).first()

        if not license:
            return f"""
            <html dir="rtl">
            <body style="font-family: Arial; padding: 20px;">
                <h2>❌ الترخيص غير موجود</h2>
                <p>لم يتم العثور على الترخيص: {license_key}</p>
            </body>
            </html>
            """, 404

        old_machine_id = license.machine_id

        # Step 1: Update license with admin credentials
        license.admin_username = 'admin'
        license.admin_password_hash = generate_password_hash('admin123')
        license.machine_id = current_machine_id
        license.is_active = True
        db.session.commit()

        # Step 2: Delete and recreate tenant database
        tenant_db_path = TenantManager.get_tenant_db_path(license_key)
        if os.path.exists(tenant_db_path):
            os.remove(tenant_db_path)

        # Step 3: Create fresh tenant database
        from flask import current_app
        TenantManager.create_tenant_database(license_key, current_app._get_current_object())
        TenantManager.initialize_tenant_data(license_key, current_app._get_current_object(), license)

        return f"""
        <html dir="rtl">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                .container {{
                    background: white;
                    color: #333;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                    max-width: 600px;
                    margin: 0 auto;
                }}
                h1 {{ color: #28a745; }}
                .info {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .success {{ color: #28a745; font-weight: bold; }}
                .credentials {{ background: #fff3cd; border: 2px solid #ffc107; padding: 15px; border-radius: 5px; }}
                a {{
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background: #667eea;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }}
                a:hover {{ background: #764ba2; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✅ تم إصلاح الترخيص بنجاح!</h1>

                <div class="info">
                    <p><strong>مفتاح الترخيص:</strong> {license.license_key}</p>
                    <p><strong>اسم العميل:</strong> {license.client_name}</p>
                    <p><strong>نوع الترخيص:</strong> {license.license_type}</p>
                </div>

                <div class="credentials">
                    <h3>🔐 بيانات تسجيل الدخول:</h3>
                    <p><strong>License Key:</strong> {license_key}</p>
                    <p><strong>Username:</strong> admin</p>
                    <p><strong>Password:</strong> admin123</p>
                </div>

                <div class="info">
                    <p class="success">✅ تم تحديث machine_id</p>
                    <p class="success">✅ تم إنشاء المستخدم admin</p>
                    <p class="success">✅ تم إعادة إنشاء قاعدة البيانات</p>
                </div>

                <p class="success">✅ الآن يمكنك تسجيل الدخول!</p>

                <a href="/auth/login">🔐 الذهاب لصفحة تسجيل الدخول</a>
            </div>
        </body>
        </html>
        """

    except Exception as e:
        import traceback
        return f"""
        <html dir="rtl">
        <body style="font-family: Arial; padding: 20px;">
            <h2>❌ حدث خطأ</h2>
            <p>{str(e)}</p>
            <pre>{traceback.format_exc()}</pre>
        </body>
        </html>
        """, 500

@bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Validate current password
        if not current_user.check_password(current_password):
            flash('كلمة المرور الحالية غير صحيحة', 'danger')
            return redirect(url_for('auth.change_password'))

        # Validate new password
        if len(new_password) < 8:
            flash('كلمة المرور يجب أن تكون 8 أحرف على الأقل', 'danger')
            return redirect(url_for('auth.change_password'))

        if new_password != confirm_password:
            flash('كلمة المرور الجديدة وتأكيد كلمة المرور غير متطابقتين', 'danger')
            return redirect(url_for('auth.change_password'))

        # Check password strength
        if not any(c.isupper() for c in new_password):
            flash('كلمة المرور يجب أن تحتوي على حرف كبير واحد على الأقل', 'danger')
            return redirect(url_for('auth.change_password'))

        if not any(c.isdigit() for c in new_password):
            flash('كلمة المرور يجب أن تحتوي على رقم واحد على الأقل', 'danger')
            return redirect(url_for('auth.change_password'))

        # Update password
        current_user.set_password(new_password)
        current_user.password_changed_at = datetime.utcnow()
        current_user.must_change_password = False
        db.session.commit()

        # Log password change
        log_security_event(current_user.id, 'password_changed',
                         'User changed password', 'info')

        flash('تم تغيير كلمة المرور بنجاح', 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/change_password.html')

@bp.route('/change-language/<lang>')
def change_language(lang):
    if lang in ['ar', 'en']:
        session['language'] = lang
        if current_user.is_authenticated:
            current_user.language = lang
            db.session.commit()
    return redirect(request.referrer or url_for('main.index'))


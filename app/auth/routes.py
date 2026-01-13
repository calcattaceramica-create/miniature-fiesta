from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.models import User, SecurityLog, SessionLog
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
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)

        user = User.query.filter_by(username=username).first()

        # Check if user exists
        if user is None:
            log_security_event(None, 'failed_login_unknown_user',
                             f'Unknown username: {username}', 'warning')
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')
            return redirect(url_for('auth.login'))

        # Check if account is locked
        if user.is_account_locked():
            log_security_event(user.id, 'login_attempt_locked_account',
                             f'Attempt to login to locked account', 'warning')
            flash('حسابك مقفل مؤقتاً بسبب محاولات دخول فاشلة متعددة. يرجى المحاولة لاحقاً', 'danger')
            return redirect(url_for('auth.login'))

        # Check password
        if not user.check_password(password):
            user.record_failed_login()
            log_security_event(user.id, 'failed_login_wrong_password',
                             f'Failed login attempt #{user.failed_login_attempts}', 'warning')

            remaining_attempts = 5 - user.failed_login_attempts
            if remaining_attempts > 0:
                flash(f'اسم المستخدم أو كلمة المرور غير صحيحة. المحاولات المتبقية: {remaining_attempts}', 'danger')
            else:
                flash('تم قفل حسابك لمدة 30 دقيقة بسبب محاولات دخول فاشلة متعددة', 'danger')

            return redirect(url_for('auth.login'))

        # Check if account is active
        if not user.is_active:
            log_security_event(user.id, 'login_attempt_inactive_account',
                             'Attempt to login to inactive account', 'warning')
            flash('حسابك غير مفعل. يرجى التواصل مع المسؤول', 'warning')
            return redirect(url_for('auth.login'))

        # Check license validity (NEW)
        if not user.has_valid_license():
            license_status = user.get_license_status()
            log_security_event(user.id, 'login_attempt_invalid_license',
                             f'License status: {license_status}', 'warning')

            if license_status == 'no_license':
                flash('🔒 لا يوجد ترخيص مرتبط بحسابك. يرجى التواصل مع المسؤول', 'danger')
            elif license_status == 'suspended':
                flash('🔒 تم إيقاف ترخيصك مؤقتاً. يرجى التواصل مع المسؤول', 'danger')
            elif license_status == 'expired':
                flash('🔒 انتهت صلاحية ترخيصك. يرجى التواصل مع المسؤول للتجديد', 'danger')
            else:
                flash('🔒 ترخيصك غير صالح. يرجى التواصل مع المسؤول', 'danger')

            return redirect(url_for('auth.login'))

        # Successful login
        login_user(user, remember=remember)
        user.record_successful_login(get_client_ip())

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
                         f'Successful login from {get_client_ip()}', 'info')

        # Set user language in session
        session['language'] = user.language

        # Check if password change is required
        if user.must_change_password:
            flash('يجب عليك تغيير كلمة المرور', 'warning')
            return redirect(url_for('auth.change_password'))

        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')

        flash(f'مرحباً {user.full_name}!', 'success')
        return redirect(next_page)

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
        flash('تم تسجيل الخروج بنجاح', 'info')

    return redirect(url_for('auth.login'))

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


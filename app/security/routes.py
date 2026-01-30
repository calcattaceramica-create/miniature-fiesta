from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app import db
from app.security import bp
from app.models import SecurityLog, IPWhitelist, SessionLog, User
from app.models_license import License, LicenseCheck
from app.license_manager import LicenseManager
from app.tenant_manager import TenantManager
from app.auth.decorators import admin_required, permission_required
from datetime import datetime, timedelta
from sqlalchemy import func, desc

@bp.route('/dashboard')
@login_required
@permission_required('security.view')
def dashboard():
    """Security dashboard"""
    # Get statistics
    total_logs = SecurityLog.query.count()
    failed_logins_today = SecurityLog.query.filter(
        SecurityLog.event_type == 'failed_login_wrong_password',
        SecurityLog.created_at >= datetime.utcnow().date()
    ).count()
    
    active_sessions = SessionLog.query.filter_by(is_active=True).count()
    locked_accounts = User.query.filter(
        User.account_locked_until != None,
        User.account_locked_until > datetime.utcnow()
    ).count()
    
    # Recent security events
    recent_events = SecurityLog.query.order_by(desc(SecurityLog.created_at)).limit(20).all()
    
    # Failed login attempts by IP
    failed_by_ip = db.session.query(
        SecurityLog.ip_address,
        func.count(SecurityLog.id).label('count')
    ).filter(
        SecurityLog.event_type.in_(['failed_login_wrong_password', 'failed_login_unknown_user']),
        SecurityLog.created_at >= datetime.utcnow() - timedelta(days=7)
    ).group_by(SecurityLog.ip_address).order_by(desc('count')).limit(10).all()
    
    # Active sessions
    active_sessions_list = SessionLog.query.filter_by(is_active=True).order_by(
        desc(SessionLog.last_activity)
    ).limit(10).all()
    
    return render_template('security/dashboard.html',
                         total_logs=total_logs,
                         failed_logins_today=failed_logins_today,
                         active_sessions=active_sessions,
                         locked_accounts=locked_accounts,
                         recent_events=recent_events,
                         failed_by_ip=failed_by_ip,
                         active_sessions_list=active_sessions_list)

@bp.route('/logs')
@login_required
@permission_required('security.view')
def logs():
    """View security logs"""
    page = request.args.get('page', 1, type=int)
    event_type = request.args.get('event_type', '')
    severity = request.args.get('severity', '')
    
    query = SecurityLog.query
    
    if event_type:
        query = query.filter_by(event_type=event_type)
    if severity:
        query = query.filter_by(severity=severity)
    
    logs = query.order_by(desc(SecurityLog.created_at)).paginate(
        page=page, per_page=50, error_out=False
    )
    
    return render_template('security/logs.html', logs=logs)

@bp.route('/ip-whitelist')
@login_required
@permission_required('security.manage')
def ip_whitelist():
    """Manage IP whitelist"""
    ips = IPWhitelist.query.order_by(desc(IPWhitelist.created_at)).all()
    return render_template('security/ip_whitelist.html', ips=ips)

@bp.route('/ip-whitelist/add', methods=['POST'])
@login_required
@permission_required('security.manage')
def add_ip_whitelist():
    """Add IP to whitelist"""
    ip_address = request.form.get('ip_address')
    description = request.form.get('description')
    
    if not ip_address:
        flash('يرجى إدخال عنوان IP', 'danger')
        return redirect(url_for('security.ip_whitelist'))
    
    # Check if IP already exists
    existing = IPWhitelist.query.filter_by(ip_address=ip_address).first()
    if existing:
        flash('عنوان IP موجود بالفعل', 'warning')
        return redirect(url_for('security.ip_whitelist'))
    
    # Add to whitelist
    whitelist = IPWhitelist(
        ip_address=ip_address,
        description=description,
        created_by=current_user.id
    )
    db.session.add(whitelist)
    db.session.commit()
    
    flash('تم إضافة عنوان IP إلى القائمة البيضاء', 'success')
    return redirect(url_for('security.ip_whitelist'))

@bp.route('/ip-whitelist/delete/<int:id>')
@login_required
@permission_required('security.manage')
def delete_ip_whitelist(id):
    """Delete IP from whitelist"""
    whitelist = IPWhitelist.query.get_or_404(id)
    db.session.delete(whitelist)
    db.session.commit()
    
    flash('تم حذف عنوان IP من القائمة البيضاء', 'success')
    return redirect(url_for('security.ip_whitelist'))

@bp.route('/sessions')
@login_required
@permission_required('security.manage')
def sessions():
    """View active sessions"""
    active = SessionLog.query.filter_by(is_active=True).order_by(
        desc(SessionLog.last_activity)
    ).all()
    
    return render_template('security/sessions.html', sessions=active)

@bp.route('/sessions/terminate/<int:id>')
@login_required
@permission_required('security.manage')
def terminate_session(id):
    """Terminate a session"""
    session_log = SessionLog.query.get_or_404(id)
    session_log.is_active = False
    session_log.logout_at = datetime.utcnow()
    db.session.commit()
    
    flash('تم إنهاء الجلسة', 'success')
    return redirect(url_for('security.sessions'))

@bp.route('/users/unlock/<int:id>')
@login_required
@permission_required('security.manage')
def unlock_user(id):
    """Unlock a user account"""
    user = User.query.get_or_404(id)
    user.unlock_account()
    
    flash(f'تم فتح حساب {user.username}', 'success')
    return redirect(url_for('security.dashboard'))

@bp.route('/license')
@login_required
@permission_required('license.view')
def license_info():
    """License information and management"""
    licenses = LicenseManager.get_all_licenses()
    active_license = next((l for l in licenses if l.is_active), None)

    # Get stats for active license (simplified - no user count)
    stats = None
    if active_license:
        stats = {
            'current_users': 0,
            'max_users': active_license.max_users,
            'user_percentage': 0,
            'days_remaining': active_license.days_remaining()
        }

    return render_template('security/license.html',
                         licenses=licenses,
                         active_license=active_license,
                         stats=stats)

@bp.route('/license/activate', methods=['POST'])
@login_required
@permission_required('license.manage')
def activate_license():
    """Activate a new license key"""
    license_key = request.form.get('license_key')
    if not license_key:
        flash('يرجى إدخال مفتاح الترخيص', 'danger')
        return redirect(url_for('security.license_info'))
    
    # In a real system, you would verify this key with a remote server
    # For now, we'll look it up in our DB (offline activation)
    license = License.query.filter_by(license_key=license_key).first()
    
    if not license:
        flash('مفتاح الترخيص غير صالح', 'danger')
        return redirect(url_for('security.license_info'))
    
    # Deactivate other licenses
    License.query.filter(License.id != license.id).update({License.is_active: False})
    
    license.is_active = True
    license.activated_at = datetime.utcnow()
    db.session.commit()
    
    flash('تم تفعيل الترخيص بنجاح', 'success')
    return redirect(url_for('security.license_info'))

@bp.route('/license/users/<int:license_id>')
@login_required
@permission_required('license.view')
def license_users(license_id):
    """View users assigned to a license"""
    license = License.query.get_or_404(license_id)
    users = User.query.filter_by(license_id=license_id).all()
    all_users = User.query.filter(User.is_admin == False).all()

    return render_template('security/license_users.html',
                         license=license,
                         users=users,
                         all_users=all_users)

@bp.route('/license/details/<int:license_id>')
@login_required
@permission_required('license.view')
def license_details(license_id):
    """View detailed license information and statistics"""
    license = License.query.get_or_404(license_id)

    # Get users for this license
    users = User.query.filter_by(license_id=license_id).all()

    # Get statistics
    stats = {
        'total_users': len(users),
        'active_users': len([u for u in users if u.is_active]),
        'max_users': license.max_users,
        'days_remaining': license.days_remaining(),
        'is_expired': license.is_expired() if hasattr(license, 'is_expired') else False,
        'is_expiring_soon': license.days_remaining() <= 7 if license.days_remaining() else False,
    }

    return render_template('security/license_details.html',
                         license=license,
                         users=users,
                         stats=stats)

@bp.route('/license/suspend/<int:license_id>', methods=['POST'])
@login_required
@permission_required('license.manage')
def suspend_license(license_id):
    """Suspend a license"""
    license = License.query.get_or_404(license_id)

    if license.is_suspended:
        flash('الترخيص موقوف بالفعل', 'warning')
    else:
        license.is_suspended = True
        license.suspended_at = datetime.utcnow()
        db.session.commit()

        from app.utils.security_helper import log_security_event
        log_security_event(
            current_user.id,
            'license_suspended',
            f'Suspended license: {license.license_key} for {license.client_name}',
            'warning'
        )

        flash(f'تم توقيف الترخيص {license.license_key} بنجاح', 'success')

    return redirect(url_for('security.license_info'))

@bp.route('/license/reactivate/<int:license_id>', methods=['POST'])
@login_required
@permission_required('license.manage')
def reactivate_license(license_id):
    """Reactivate a suspended license"""
    license = License.query.get_or_404(license_id)

    if not license.is_suspended:
        flash('الترخيص نشط بالفعل', 'warning')
    else:
        license.is_suspended = False
        license.suspended_at = None
        db.session.commit()

        from app.utils.security_helper import log_security_event
        log_security_event(
            current_user.id,
            'license_reactivated',
            f'Reactivated license: {license.license_key} for {license.client_name}',
            'info'
        )

        flash(f'تم تفعيل الترخيص {license.license_key} بنجاح', 'success')

    return redirect(url_for('security.license_info'))

@bp.route('/license/delete/<int:license_id>', methods=['POST'])
@login_required
@permission_required('license.manage')
def delete_license(license_id):
    """Delete a license (soft delete)"""
    license = License.query.get_or_404(license_id)

    users_count = User.query.filter_by(license_id=license_id).count()

    if users_count > 0:
        flash(f'لا يمكن حذف الترخيص. يوجد {users_count} مستخدم مرتبط به. يرجى إزالة المستخدمين أولاً.', 'danger')
        return redirect(url_for('security.license_info'))

    license.is_active = False
    license.is_suspended = True
    license.suspended_at = datetime.utcnow()
    db.session.commit()

    from app.utils.security_helper import log_security_event
    log_security_event(
        current_user.id,
        'license_deleted',
        f'Deleted license: {license.license_key} for {license.client_name}',
        'warning'
    )

    flash(f'تم حذف الترخيص {license.license_key} بنجاح', 'success')
    return redirect(url_for('security.license_info'))

@bp.route('/license/assign-user', methods=['POST'])
@login_required
@permission_required('license.manage')
def assign_user_license():
    """Assign a user to a license"""
    user_id = request.form.get('user_id')
    license_id = request.form.get('license_id')
    
    user = User.query.get_or_404(user_id)
    license = License.query.get_or_404(license_id)
    
    if not license.is_active:
        flash('لا يمكن التخصيص لترخيص غير نشط', 'danger')
        return redirect(url_for('security.license_users', license_id=license_id))
    
    # Check max users
    if not license.can_add_user() and user.license_id != license.id:
        flash(f'تم الوصول للحد الأقصى للمستخدمين لهذا الترخيص ({license.max_users})', 'danger')
        return redirect(url_for('security.license_users', license_id=license_id))
    
    user.license_id = license.id
    db.session.commit()
    
    flash(f'تم ربط المستخدم {user.username} بالترخيص بنجاح', 'success')
    return redirect(url_for('security.license_users', license_id=license_id))

@bp.route('/license/remove-user/<int:user_id>')
@login_required
@permission_required('license.manage')
def remove_user_license(user_id):
    """Remove a user from their license"""
    user = User.query.get_or_404(user_id)
    license_id = user.license_id
    
    user.license_id = None
    db.session.commit()
    
    flash(f'تم فصل المستخدم {user.username} عن الترخيص', 'success')
    return redirect(url_for('security.license_users', license_id=license_id) if license_id else url_for('security.license_info'))

@bp.route('/license/create', methods=['GET', 'POST'])
@login_required
@permission_required('license.manage')
def create_license():
    """Create a new license"""
    if request.method == 'POST':
        try:
            # Get form data
            client_name = request.form.get('client_name')
            client_company = request.form.get('client_company')
            client_email = request.form.get('client_email')
            client_phone = request.form.get('client_phone')
            license_type = request.form.get('license_type', 'trial')
            max_users = int(request.form.get('max_users', 1))
            max_branches = int(request.form.get('max_branches', 1))
            duration_days = request.form.get('duration_days')
            admin_username = request.form.get('admin_username')
            admin_password = request.form.get('admin_password')
            notes = request.form.get('notes')

            # Validate required fields
            if not client_name:
                flash(_('Client name is required'), 'danger')
                return redirect(url_for('security.create_license'))

            # Convert duration_days
            if duration_days:
                duration_days = int(duration_days)
            else:
                duration_days = None

            # Create license using LicenseManager
            license = LicenseManager.create_license(
                client_name=client_name,
                admin_username=admin_username or 'admin',
                admin_password=admin_password or 'admin123',
                license_type=license_type,
                duration_days=duration_days,
                max_users=max_users,
                max_branches=max_branches,
                client_email=client_email,
                client_phone=client_phone,
                client_company=client_company,
                notes=notes
            )

            db.session.add(license)
            db.session.commit()

            # Create tenant database for this license
            print(f"Creating tenant database for license: {license.license_key}")
            tenant_created = TenantManager.create_tenant_database(license.license_key, current_app._get_current_object())

            if tenant_created:
                # Initialize tenant database with default data
                print(f"Initializing tenant data for license: {license.license_key}")
                TenantManager.initialize_tenant_data(license.license_key, current_app._get_current_object(), license)
                flash(_('License created successfully! License Key: {} - Tenant database created').format(license.license_key), 'success')
            else:
                flash(_('License created successfully! License Key: {} - Warning: Tenant database creation failed').format(license.license_key), 'warning')

            return redirect(url_for('security.license_info'))

        except Exception as e:
            db.session.rollback()
            flash(_('Error creating license: {}').format(str(e)), 'danger')
            return redirect(url_for('security.create_license'))

    return render_template('security/create_license.html')


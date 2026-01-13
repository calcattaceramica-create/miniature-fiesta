from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.security import bp
from app.models import SecurityLog, IPWhitelist, SessionLog, User
from app.auth.decorators import admin_required
from datetime import datetime, timedelta
from sqlalchemy import func, desc

@bp.route('/dashboard')
@login_required
@admin_required
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
@admin_required
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
@admin_required
def ip_whitelist():
    """Manage IP whitelist"""
    ips = IPWhitelist.query.order_by(desc(IPWhitelist.created_at)).all()
    return render_template('security/ip_whitelist.html', ips=ips)

@bp.route('/ip-whitelist/add', methods=['POST'])
@login_required
@admin_required
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
@admin_required
def delete_ip_whitelist(id):
    """Delete IP from whitelist"""
    whitelist = IPWhitelist.query.get_or_404(id)
    db.session.delete(whitelist)
    db.session.commit()
    
    flash('تم حذف عنوان IP من القائمة البيضاء', 'success')
    return redirect(url_for('security.ip_whitelist'))

@bp.route('/sessions')
@login_required
@admin_required
def sessions():
    """View active sessions"""
    active = SessionLog.query.filter_by(is_active=True).order_by(
        desc(SessionLog.last_activity)
    ).all()
    
    return render_template('security/sessions.html', sessions=active)

@bp.route('/sessions/terminate/<int:id>')
@login_required
@admin_required
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
@admin_required
def unlock_user(id):
    """Unlock a user account"""
    user = User.query.get_or_404(id)
    user.unlock_account()
    
    flash(f'تم فتح حساب {user.username}', 'success')
    return redirect(url_for('security.dashboard'))


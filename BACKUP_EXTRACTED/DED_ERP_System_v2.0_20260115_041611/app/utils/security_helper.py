"""
Security Helper Functions
Provides security utilities for the application
"""

from functools import wraps
from flask import request, jsonify, session, current_app
from flask_login import current_user
from datetime import datetime, timedelta
from app import db
from app.models import SecurityLog, IPWhitelist, SessionLog
import time

# Rate limiting storage (in-memory, use Redis in production)
_rate_limit_storage = {}

def get_client_ip():
    """Get client IP address"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    return request.remote_addr or '0.0.0.0'

def is_ip_whitelisted(ip_address):
    """Check if IP is in whitelist"""
    whitelist = IPWhitelist.query.filter_by(ip_address=ip_address, is_active=True).first()
    return whitelist is not None

def check_rate_limit(key, max_requests=10, window_seconds=60):
    """
    Check if rate limit is exceeded
    
    Args:
        key: Unique identifier (e.g., IP address, user ID)
        max_requests: Maximum number of requests allowed
        window_seconds: Time window in seconds
    
    Returns:
        tuple: (is_allowed, remaining_requests, reset_time)
    """
    now = time.time()
    window_start = now - window_seconds
    
    # Clean old entries
    if key in _rate_limit_storage:
        _rate_limit_storage[key] = [
            timestamp for timestamp in _rate_limit_storage[key]
            if timestamp > window_start
        ]
    else:
        _rate_limit_storage[key] = []
    
    # Check limit
    current_requests = len(_rate_limit_storage[key])
    
    if current_requests >= max_requests:
        oldest_request = min(_rate_limit_storage[key])
        reset_time = oldest_request + window_seconds
        return False, 0, reset_time
    
    # Add current request
    _rate_limit_storage[key].append(now)
    remaining = max_requests - (current_requests + 1)
    reset_time = now + window_seconds
    
    return True, remaining, reset_time

def rate_limit(max_requests=10, window_seconds=60, by_ip=True):
    """
    Decorator to apply rate limiting to routes
    
    Args:
        max_requests: Maximum number of requests allowed
        window_seconds: Time window in seconds
        by_ip: If True, limit by IP address; if False, limit by user ID
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Determine the key for rate limiting
            if by_ip:
                key = f"ip:{get_client_ip()}"
            else:
                if current_user.is_authenticated:
                    key = f"user:{current_user.id}"
                else:
                    key = f"ip:{get_client_ip()}"
            
            # Check rate limit
            is_allowed, remaining, reset_time = check_rate_limit(
                key, max_requests, window_seconds
            )
            
            if not is_allowed:
                # Log rate limit exceeded
                log_security_event(
                    current_user.id if current_user.is_authenticated else None,
                    'rate_limit_exceeded',
                    f'Rate limit exceeded for {key}',
                    'warning'
                )
                
                return jsonify({
                    'error': 'تم تجاوز الحد المسموح من الطلبات - Rate limit exceeded',
                    'retry_after': int(reset_time - time.time())
                }), 429
            
            # Add rate limit headers
            response = f(*args, **kwargs)
            if hasattr(response, 'headers'):
                response.headers['X-RateLimit-Limit'] = str(max_requests)
                response.headers['X-RateLimit-Remaining'] = str(remaining)
                response.headers['X-RateLimit-Reset'] = str(int(reset_time))
            
            return response
        
        return decorated_function
    return decorator

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

def require_ip_whitelist(f):
    """Decorator to require IP whitelist"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = get_client_ip()
        
        if not is_ip_whitelisted(ip):
            log_security_event(
                current_user.id if current_user.is_authenticated else None,
                'ip_not_whitelisted',
                f'Access denied for IP: {ip}',
                'warning'
            )
            return jsonify({
                'error': 'عنوان IP غير مصرح به - IP address not authorized'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

def check_session_timeout():
    """Check if session has timed out"""
    if 'last_activity' in session:
        last_activity = session['last_activity']
        timeout = current_app.config.get('PERMANENT_SESSION_LIFETIME', timedelta(hours=2))
        
        if datetime.utcnow() - last_activity > timeout:
            return True
    
    session['last_activity'] = datetime.utcnow()
    return False


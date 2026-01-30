"""
License Middleware
فحص الترخيص قبل كل طلب
"""
from flask import request, render_template_string, abort
from app.license_manager import LicenseManager
from datetime import datetime, timedelta

# Routes that don't require license check
EXEMPT_ROUTES = [
    '/static/',
    '/auth/login',
    '/auth/logout',
    '/activate-license',
    '/license-activation',
]

# Last license check time (to avoid checking on every request)
_last_license_check = None
_license_check_interval = timedelta(minutes=5)  # Check every 5 minutes
_license_status = {'is_valid': False, 'message': '', 'license': None}

def check_license_validity():
    """Check if license is valid (with caching)"""
    global _last_license_check, _license_status

    # Check if we need to verify license
    now = datetime.utcnow()
    if _last_license_check and (now - _last_license_check) < _license_check_interval:
        # Use cached result
        return _license_status['is_valid'], _license_status['message'], _license_status['license_data']

    # Verify license
    is_valid, message, license = LicenseManager.verify_license()

    # Extract license data to avoid DetachedInstanceError
    license_data = None
    if license:
        license_data = {
            'id': license.id,
            'client_name': license.client_name,
            'license_key': license.license_key,
            'license_type': license.license_type,
            'expires_at': license.expires_at,
            'days_remaining': license.days_remaining() if license.expires_at else None,
            'is_active': license.is_active
        }

    # Update cache
    _last_license_check = now
    _license_status = {
        'is_valid': is_valid,
        'message': message,
        'license_data': license_data
    }

    return is_valid, message, license_data

def init_license_middleware(app):
    """Initialize license checking middleware"""
    
    @app.before_request
    def check_license():
        """Check license before each request"""
        return None # TEMPORARY DISABLE FOR DEBUGGING
        # Skip license check for exempt routes
        for exempt_route in EXEMPT_ROUTES:
            if request.path.startswith(exempt_route):
                return None

        # Check license
        is_valid, message, license_data = check_license_validity()

        if not is_valid:
            # License is invalid - show error page
            return render_license_error(message, license_data)

        # License is valid - check if expiring soon
        if license_data and license_data.get('expires_at'):
            days_remaining = license_data.get('days_remaining')
            if days_remaining is not None and days_remaining <= 7:
                # Add warning to session (you can display this in the UI)
                from flask import session
                session['license_warning'] = f"⚠️ الترخيص سينتهي خلال {days_remaining} يوم"

        return None

def render_license_error(message, license_data=None):
    """Render license error page"""
    template = """
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>خطأ في الترخيص - License Error</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }

            .error-container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 600px;
                width: 100%;
                padding: 50px;
                text-align: center;
            }

            .error-icon {
                font-size: 80px;
                margin-bottom: 20px;
            }

            h1 {
                color: #333;
                font-size: 32px;
                margin-bottom: 20px;
            }

            .error-message {
                background: #fee;
                border: 2px solid #fcc;
                border-radius: 10px;
                padding: 20px;
                margin: 30px 0;
                color: #c33;
                font-size: 18px;
                font-weight: bold;
            }

            .info-box {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                text-align: right;
            }

            .info-row {
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #dee2e6;
            }

            .info-row:last-child {
                border-bottom: none;
            }

            .info-label {
                font-weight: bold;
                color: #666;
            }

            .info-value {
                color: #333;
            }

            .contact-info {
                margin-top: 30px;
                padding: 20px;
                background: #e3f2fd;
                border-radius: 10px;
                color: #1976d2;
            }

            .contact-info h3 {
                margin-bottom: 15px;
                color: #1565c0;
            }

            .contact-info p {
                margin: 10px 0;
                font-size: 16px;
            }

            .btn {
                display: inline-block;
                padding: 12px 30px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 25px;
                margin-top: 20px;
                font-weight: bold;
                transition: all 0.3s;
            }

            .btn:hover {
                background: #764ba2;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            }
        </style>
    </head>
    <body>
        <div class="error-container">
            <div class="error-icon">🔒</div>
            <h1>خطأ في الترخيص</h1>
            <h2 style="color: #666; font-size: 20px; margin-bottom: 20px;">License Error</h2>

            <div class="error-message">
                {{ message }}
            </div>

            {% if license_data %}
            <div class="info-box">
                <div class="info-row">
                    <span class="info-label">العميل - Client:</span>
                    <span class="info-value">{{ license_data.get('client_name', 'N/A') }}</span>
                </div>
                {% if license_data.get('expires_at') %}
                <div class="info-row">
                    <span class="info-label">تاريخ الانتهاء - Expiration:</span>
                    <span class="info-value">{{ license_data.get('expires_at').strftime('%Y-%m-%d') }}</span>
                </div>
                {% endif %}
                <div class="info-row">
                    <span class="info-label">نوع الترخيص - Type:</span>
                    <span class="info-value">{{ license_data.get('license_type', 'N/A') }}</span>
                </div>
            </div>
            {% endif %}

            <div class="contact-info">
                <h3>📞 للتواصل والتجديد - Contact for Renewal</h3>
                <p>يرجى التواصل مع مزود الخدمة لتجديد الترخيص</p>
                <p>Please contact your service provider to renew the license</p>
            </div>

            <a href="/auth/logout" class="btn">تسجيل الخروج - Logout</a>
        </div>
    </body>
    </html>
    """

    return render_template_string(template, message=message, license_data=license_data), 403


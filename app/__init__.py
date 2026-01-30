from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_babel import Babel
from config import config
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
babel = Babel()

def get_locale():
    """Get user's preferred language from session or default to Arabic"""
    # Try to get language from session
    if 'language' in session:
        return session['language']

    # Try to get from user preferences if logged in
    from flask_login import current_user
    if current_user and current_user.is_authenticated:
        if hasattr(current_user, 'language') and current_user.language:
            return current_user.language

    # Default to Arabic
    return 'ar'

def create_app(config_name='default'):
    """Application factory pattern"""
    # Get the absolute path to the app directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(app_dir, 'templates')
    static_dir = os.path.join(app_dir, 'static')

    # Get the absolute path to the translations directory (one level up from app)
    basedir = os.path.dirname(app_dir)
    translations_dir = os.path.join(basedir, 'translations')

    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Disable template caching for development
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Initialize Babel with absolute path
    app.config['BABEL_DEFAULT_LOCALE'] = 'ar'
    app.config['BABEL_DEFAULT_TIMEZONE'] = 'Asia/Riyadh'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = translations_dir
    babel.init_app(app, locale_selector=get_locale)
    
    # Login manager settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'يرجى تسجيل الدخول للوصول إلى هذه الصفحة'
    login_manager.login_message_category = 'info'
    
    # Create upload folder
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.inventory import bp as inventory_bp
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    
    from app.sales import bp as sales_bp
    app.register_blueprint(sales_bp, url_prefix='/sales')
    
    from app.purchases import bp as purchases_bp
    app.register_blueprint(purchases_bp, url_prefix='/purchases')
    
    from app.accounting import bp as accounting_bp
    app.register_blueprint(accounting_bp, url_prefix='/accounting')
    
    from app.crm import bp as crm_bp
    app.register_blueprint(crm_bp, url_prefix='/crm')
    
    from app.hr import bp as hr_bp
    app.register_blueprint(hr_bp, url_prefix='/hr')
    
    from app.pos import bp as pos_bp
    app.register_blueprint(pos_bp, url_prefix='/pos')
    
    from app.reports import bp as reports_bp
    app.register_blueprint(reports_bp, url_prefix='/reports')
    
    from app.settings import bp as settings_bp
    app.register_blueprint(settings_bp, url_prefix='/settings')

    from app.security import bp as security_bp
    app.register_blueprint(security_bp, url_prefix='/security')

    # Initialize Multi-Tenancy middleware
    from app.tenant_middleware import init_tenant_middleware
    init_tenant_middleware(app)

    # Add context processor for translations and currency
    @app.context_processor
    def inject_locale():
        from flask_babel import get_locale, gettext
        return {
            'get_locale': get_locale,
            'current_locale': str(get_locale()),
            '_': gettext
        }

    # Add context processor for currency
    @app.context_processor
    def inject_currency():
        """Inject currency information into all templates"""
        from app.models import Company
        from flask_babel import gettext

        try:
            company = Company.query.first()
            if company and company.currency:
                currency_code = company.currency
            else:
                currency_code = app.config.get('DEFAULT_CURRENCY', 'SAR')
        except:
            # Fallback if database is not available
            currency_code = 'SAR'

        # Get currency info from config
        currency_info = app.config['CURRENCIES'].get(currency_code, {})
        currency_symbol = currency_info.get('symbol', 'ر.س')

        # Translate currency name based on code
        currency_name_map = {
            'SAR': 'Saudi Riyal',
            'USD': 'US Dollar',
            'EUR': 'Euro',
            'AED': 'UAE Dirham',
            'KWD': 'Kuwaiti Dinar',
            'BHD': 'Bahraini Dinar',
            'OMR': 'Omani Riyal',
            'QAR': 'Qatari Riyal',
            'EGP': 'Egyptian Pound',
        }

        currency_name_key = currency_name_map.get(currency_code, 'Saudi Riyal')
        currency_name = gettext(currency_name_key)

        return {
            'currency_code': currency_code,
            'currency_symbol': currency_symbol,
            'currency_name': currency_name
        }

    # Add template filter for currency formatting
    @app.template_filter('currency')
    def currency_filter(value):
        """Format number with currency symbol"""
        from app.models import Company

        try:
            company = Company.query.first()
            if company and company.currency:
                currency_code = company.currency
                currency_info = app.config['CURRENCIES'].get(currency_code, {})
                currency_symbol = currency_info.get('symbol', 'ر.س')
            else:
                currency_symbol = 'ر.س'
        except:
            currency_symbol = 'ر.س'

        try:
            return f"{float(value):.2f} {currency_symbol}"
        except (ValueError, TypeError):
            return f"0.00 {currency_symbol}"

    return app

from app import models
from app import models_license


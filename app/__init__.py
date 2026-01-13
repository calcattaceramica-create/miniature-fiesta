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

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
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

    # Initialize license middleware (optional - uncomment to enable)
    # from app.license_middleware import init_license_middleware
    # init_license_middleware(app)

    return app

def get_locale():
    """Get user's preferred language"""
    # Try to get language from session
    if 'language' in session:
        return session['language']
    # Try to get from user settings (if logged in)
    # Otherwise use browser's accept language
    return request.accept_languages.best_match(['ar', 'en']) or 'ar'

from app import models
from app import models_license


import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database
    database_url = os.environ.get('DATABASE_URL')
    # Fix for Render.com PostgreSQL URL (postgres:// -> postgresql://)
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    # Multi-Tenancy: Use master database for license management
    # Tenant databases are switched dynamically by tenant_middleware
    SQLALCHEMY_DATABASE_URI = database_url or \
        'sqlite:///' + os.path.join(basedir, 'licenses_master.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Application
    APP_NAME = os.environ.get('APP_NAME') or 'نظام إدارة المخزون المتكامل'
    DEFAULT_LANGUAGE = 'ar'
    BABEL_DEFAULT_LOCALE = 'ar'
    BABEL_DEFAULT_TIMEZONE = 'Asia/Riyadh'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    LANGUAGES = {
        'ar': {'name': 'العربية', 'flag': '🇸🇦', 'dir': 'rtl'},
        'en': {'name': 'English', 'flag': '🇬🇧', 'dir': 'ltr'}
    }

    # Session Security
    SESSION_TYPE = 'null'  # Use default Flask session (signed cookies)
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)  # Session expires after 2 hours
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to cookies
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    SESSION_REFRESH_EACH_REQUEST = True  # Refresh session on each request
    SESSION_PERMANENT = True  # Make sessions permanent (use PERMANENT_SESSION_LIFETIME)

    # Security
    WTF_CSRF_ENABLED = True  # Enable CSRF protection
    WTF_CSRF_TIME_LIMIT = None  # No time limit for CSRF tokens
    MAX_LOGIN_ATTEMPTS = 5  # Maximum failed login attempts before account lock
    ACCOUNT_LOCK_DURATION = 30  # Account lock duration in minutes
    SESSION_TIMEOUT_WARNING = 5  # Show warning 5 minutes before session expires
    PASSWORD_MIN_LENGTH = 8  # Minimum password length
    PASSWORD_REQUIRE_UPPERCASE = True  # Require uppercase letter
    PASSWORD_REQUIRE_DIGIT = True  # Require digit
    PASSWORD_REQUIRE_SPECIAL = False  # Require special character (optional)
    
    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'xls', 'csv'}
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Currency
    DEFAULT_CURRENCY = 'EUR'
    CURRENCIES = {
        'EUR': {'name': 'يورو', 'symbol': '€'},
        'SAR': {'name': 'ريال سعودي', 'symbol': 'ر.س'},
        'USD': {'name': 'دولار أمريكي', 'symbol': '$'},
        'AED': {'name': 'درهم إماراتي', 'symbol': 'د.إ'},
        'KWD': {'name': 'دينار كويتي', 'symbol': 'د.ك'},
        'BHD': {'name': 'دينار بحريني', 'symbol': 'د.ب'},
        'OMR': {'name': 'ريال عماني', 'symbol': 'ر.ع'},
        'QAR': {'name': 'ريال قطري', 'symbol': 'ر.ق'},
        'EGP': {'name': 'جنيه مصري', 'symbol': 'ج.م'},
    }
    
    # Tax
    DEFAULT_TAX_RATE = 15.0  # VAT 15%
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = True  # Temporarily enable for debugging
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


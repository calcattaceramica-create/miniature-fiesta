"""
Translation Helper Functions
Provides easy-to-use translation functions for the application
"""

from flask_babel import gettext, ngettext, lazy_gettext
from flask import session

# Shorthand functions for easier use
_ = gettext  # For regular translations
_n = ngettext  # For plural translations
_l = lazy_gettext  # For lazy translations (e.g., in forms)

def get_current_language():
    """Get the current language code"""
    return session.get('language', 'ar')

def is_rtl():
    """Check if current language is RTL (Right-to-Left)"""
    return get_current_language() in ['ar', 'he', 'fa', 'ur']

def get_language_name(lang_code):
    """Get the display name of a language"""
    languages = {
        'ar': 'العربية',
        'en': 'English',
        'fr': 'Français',
        'es': 'Español',
        'de': 'Deutsch',
    }
    return languages.get(lang_code, lang_code)

def get_language_flag(lang_code):
    """Get the flag emoji for a language"""
    flags = {
        'ar': '🇸🇦',
        'en': '🇬🇧',
        'fr': '🇫🇷',
        'es': '🇪🇸',
        'de': '🇩🇪',
    }
    return flags.get(lang_code, '🌐')

# Common translations dictionary (for quick reference)
COMMON_TRANSLATIONS = {
    'ar': {
        'dashboard': 'لوحة التحكم',
        'home': 'الرئيسية',
        'inventory': 'المخزون',
        'sales': 'المبيعات',
        'purchases': 'المشتريات',
        'pos': 'نقاط البيع',
        'accounting': 'المحاسبة',
        'crm': 'إدارة العملاء',
        'hr': 'الموارد البشرية',
        'reports': 'التقارير',
        'settings': 'الإعدادات',
        'logout': 'تسجيل الخروج',
        'save': 'حفظ',
        'cancel': 'إلغاء',
        'delete': 'حذف',
        'edit': 'تعديل',
        'add': 'إضافة',
        'search': 'بحث',
        'filter': 'تصفية',
        'export': 'تصدير',
        'import': 'استيراد',
        'print': 'طباعة',
    },
    'en': {
        'dashboard': 'Dashboard',
        'home': 'Home',
        'inventory': 'Inventory',
        'sales': 'Sales',
        'purchases': 'Purchases',
        'pos': 'POS',
        'accounting': 'Accounting',
        'crm': 'CRM',
        'hr': 'HR',
        'reports': 'Reports',
        'settings': 'Settings',
        'logout': 'Logout',
        'save': 'Save',
        'cancel': 'Cancel',
        'delete': 'Delete',
        'edit': 'Edit',
        'add': 'Add',
        'search': 'Search',
        'filter': 'Filter',
        'export': 'Export',
        'import': 'Import',
        'print': 'Print',
    }
}

def t(key, default=None):
    """
    Quick translation function
    Usage: t('dashboard') -> returns translation based on current language
    """
    lang = get_current_language()
    translations = COMMON_TRANSLATIONS.get(lang, COMMON_TRANSLATIONS['ar'])
    return translations.get(key.lower(), default or key)

def format_number(number, decimals=2):
    """Format number according to current language"""
    lang = get_current_language()
    
    if lang == 'ar':
        # Arabic number formatting
        formatted = f"{number:,.{decimals}f}"
        # Optionally convert to Arabic-Indic numerals
        # formatted = convert_to_arabic_numerals(formatted)
        return formatted
    else:
        # English number formatting
        return f"{number:,.{decimals}f}"

def format_currency(amount, currency='SAR'):
    """Format currency according to current language"""
    lang = get_current_language()
    formatted_amount = format_number(amount, 2)
    
    currency_symbols = {
        'SAR': 'ر.س',
        'USD': '$',
        'EUR': '€',
        'AED': 'د.إ',
        'KWD': 'د.ك',
        'BHD': 'د.ب',
        'OMR': 'ر.ع',
        'QAR': 'ر.ق',
        'EGP': 'ج.م',
    }
    
    symbol = currency_symbols.get(currency, currency)
    
    if lang == 'ar':
        return f"{formatted_amount} {symbol}"
    else:
        return f"{symbol}{formatted_amount}"

def format_date(date_obj, format='medium'):
    """Format date according to current language"""
    from flask_babel import format_date as babel_format_date
    return babel_format_date(date_obj, format=format)

def format_datetime(datetime_obj, format='medium'):
    """Format datetime according to current language"""
    from flask_babel import format_datetime as babel_format_datetime
    return babel_format_datetime(datetime_obj, format=format)


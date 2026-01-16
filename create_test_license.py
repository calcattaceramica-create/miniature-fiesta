"""
Create a test license with correct format
إنشاء ترخيص تجريبي بالصيغة الصحيحة
"""

import json
import hashlib
import secrets
from datetime import datetime, timedelta

def create_license_key(company):
    """Generate a unique license key"""
    timestamp = datetime.now().isoformat()
    random_part = secrets.token_hex(16)
    data = f"{company}-{timestamp}-{random_part}"
    hash_obj = hashlib.sha256(data.encode())
    return f"DED-{hash_obj.hexdigest()[:32].upper()}"

def create_test_license():
    """Create a test license"""
    
    # License details
    company = "شمه"
    username = "ششش"
    password = "سسسس"
    phone = "+966501234567"
    duration_days = 365
    
    # Generate key
    key = create_license_key(company)
    
    # Calculate expiry
    expiry = (datetime.now() + timedelta(days=duration_days)).strftime("%Y-%m-%d")
    
    # Create license data
    license_data = {
        key: {
            "company": company,
            "username": username,
            "password": password,
            "phone": phone,
            "expiry": expiry,
            "duration_days": duration_days,
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    
    # Save to file
    with open('licenses.json', 'w', encoding='utf-8') as f:
        json.dump(license_data, f, indent=2, ensure_ascii=False)
    
    print("✅ تم إنشاء الترخيص بنجاح!")
    print("="*60)
    print(f"🔑 المفتاح: {key}")
    print(f"🏢 الشركة: {company}")
    print(f"👤 المستخدم: {username}")
    print(f"🔒 كلمة المرور: {password}")
    print(f"📱 الهاتف: {phone}")
    print(f"📅 تاريخ الانتهاء: {expiry}")
    print(f"⏱️ المدة: {duration_days} يوم")
    print("="*60)
    print("\n📋 استخدم هذه البيانات لتسجيل الدخول في تطبيق العملاء")
    
    return key, license_data

if __name__ == "__main__":
    create_test_license()


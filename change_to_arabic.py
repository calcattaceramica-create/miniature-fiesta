"""
Script to change language to Arabic for all users
"""
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Update all users to Arabic
    users = User.query.all()
    for user in users:
        user.language = 'ar'
    
    db.session.commit()
    print(f"✅ تم تغيير لغة {len(users)} مستخدم إلى العربية")
    print("✅ Language changed to Arabic for all users")
    print("\n⚠️ ملاحظة: قد تحتاج إلى:")
    print("1. تسجيل الخروج وتسجيل الدخول مرة أخرى")
    print("2. أو استخدام زر تغيير اللغة في الواجهة")
    print("\n⚠️ Note: You may need to:")
    print("1. Logout and login again")
    print("2. Or use the language switcher in the interface")


"""
Force Arabic language for the application
"""
from app import create_app, db
from app.models import User
from flask import session

app = create_app()

with app.app_context():
    # Update all users to Arabic
    users = User.query.all()
    for user in users:
        user.language = 'ar'
    
    db.session.commit()
    
    print(f"✅ تم تغيير لغة {len(users)} مستخدم إلى العربية")
    print(f"✅ Changed language to Arabic for {len(users)} users")
    
    # Print current users and their languages
    print("\n📋 قائمة المستخدمين:")
    print("📋 Users list:")
    for user in users:
        print(f"   - {user.username}: {user.language}")
    
    print("\n⚠️ الآن افتح المتصفح واضغط على زر '🇸🇦 العربية' في الأعلى")
    print("⚠️ Now open browser and click on '🇸🇦 العربية' button at the top")


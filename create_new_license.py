"""
Create a new license
"""
from app import create_app, db
from app.models_license import License
from datetime import datetime, timedelta
import uuid

app = create_app()

with app.app_context():
    # Generate new license key
    license_key = '-'.join([uuid.uuid4().hex[:4].upper() for _ in range(4)])
    
    # Create new license
    new_license = License(
        license_key=license_key,
        license_hash=License.hash_license_key(license_key),
        client_name='عميل جديد',
        client_company='شركة جديدة',
        client_email='client@example.com',
        client_phone='0500000000',
        license_type='LIFETIME',
        max_users=100,
        max_branches=10,
        is_active=True,
        is_suspended=False,
        activated_at=datetime.now(),
        expires_at=None,  # Lifetime license
        admin_username='admin'
    )

    # Set admin password
    if hasattr(new_license, 'set_admin_password'):
        new_license.set_admin_password('admin123')
    
    db.session.add(new_license)
    db.session.commit()
    
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║              ✅ تم إنشاء ترخيص جديد بنجاح!                                  ║")
    print("║           New License Created Successfully!                                  ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("🔑 معلومات الترخيص الجديد:")
    print("═══════════════════════════════════════════════════════════════════════════════")
    print()
    print(f"┌─────────────────────────┬──────────────────────────────────────┐")
    print(f"│ البيان                  │ القيمة                                │")
    print(f"├─────────────────────────┼──────────────────────────────────────┤")
    print(f"│ 🔑 مفتاح الترخيص        │ {license_key:<36} │")
    print(f"│ 👤 العميل               │ {new_license.client_name:<36} │")
    print(f"│ 🏢 الشركة               │ {new_license.client_company:<36} │")
    print(f"│ 📧 البريد الإلكتروني    │ {new_license.client_email:<36} │")
    print(f"│ 📞 الهاتف               │ {new_license.client_phone:<36} │")
    print(f"│ 📊 نوع الترخيص          │ {new_license.license_type:<36} │")
    print(f"│ 👥 الحد الأقصى للمستخدمين│ {new_license.max_users:<36} │")
    print(f"│ 🏪 الحد الأقصى للفروع   │ {new_license.max_branches:<36} │")
    print(f"│ ✅ الحالة               │ {'نشط' if new_license.is_active else 'غير نشط':<36} │")
    print(f"│ ⏰ تاريخ الانتهاء       │ {'مدى الحياة ∞':<36} │")
    print(f"└─────────────────────────┴──────────────────────────────────────┘")
    print()
    print("═══════════════════════════════════════════════════════════════════════════════")
    print()
    print("✅ يمكنك الآن استخدام هذا الترخيص في النظام")
    print("✅ افتح صفحة التراخيص لرؤية الترخيص الجديد")
    print()
    print(f"🔗 الرابط: http://localhost:5000/security/license")
    print()
    
    # List all licenses
    all_licenses = License.query.all()
    print(f"📋 إجمالي التراخيص في النظام: {len(all_licenses)}")
    print()
    for i, lic in enumerate(all_licenses, 1):
        status = "نشط" if lic.is_active and not lic.is_suspended else "موقوف" if lic.is_suspended else "غير نشط"
        print(f"   {i}. {lic.license_key} - {lic.client_name} - {status}")
    print()


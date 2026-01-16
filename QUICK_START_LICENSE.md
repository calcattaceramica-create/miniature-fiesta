# دليل البدء السريع - Quick Start Guide

## 🎉 تم تفعيل نظام الترخيص بنجاح!

---

## 🔑 معلومات الترخيص الحالي

```
License Key: CEC9-79EE-C42F-2DAD
Status: ✅ Active
Expires: 2027-01-16 (364 days remaining)
Max Users: 10
Max Branches: 5
```

---

## 🚀 البدء السريع

### 1. تشغيل النظام
```bash
python run.py
```

### 2. عرض معلومات الترخيص
افتح المتصفح وانتقل إلى:
```
http://127.0.0.1:5000/license-info
```

---

## 📋 الأوامر المتاحة

### إنشاء ترخيص جديد (تلقائي)
```bash
python activate_license.py
```

### إنشاء ترخيص جديد (يدوي)
```bash
python create_license.py
```

### عرض جميع التراخيص
```bash
python create_license.py list
```

---

## 🛠️ إدارة التراخيص

### تمديد ترخيص
```python
from app import create_app
from app.license_manager import LicenseManager

app = create_app()
with app.app_context():
    LicenseManager.extend_license(license_id=1, days=30)
```

### تعليق ترخيص
```python
LicenseManager.suspend_license(license_id=1, reason="Payment pending")
```

### إلغاء التعليق
```python
LicenseManager.unsuspend_license(license_id=1)
```

---

## 📞 الدعم

للمساعدة أو الاستفسارات:
- Email: info@ded-erp.com
- Phone: +966-XXX-XXXX

---

## ✅ تم!

نظام الترخيص جاهز للاستخدام!


# 📦 DED ERP System - Export Package
# حزمة تصدير نظام DED ERP

## 🎉 تم التصدير بنجاح! - Export Successful!

تم تصدير نظام DED ERP بنجاح مع نظام إدارة التراخيص الكامل.
DED ERP System has been successfully exported with complete license management system.

---

## 📋 محتويات الحزمة - Package Contents

### ✅ الملفات الأساسية - Core Files

- `app/` - التطبيق الرئيسي - Main application
- `migrations/` - ملفات الهجرة - Migration files
- `translations/` - الترجمات - Translations
- `config.py` - الإعدادات - Configuration
- `run.py` - ملف التشغيل - Run file
- `requirements.txt` - المتطلبات - Dependencies

### 🚀 ملفات النشر - Deployment Files

- `render.yaml` - إعدادات Render
- `Procfile` - إعدادات Gunicorn
- `runtime.txt` - إصدار Python
- `initialize_master_database.py` - تهيئة قاعدة البيانات

### 📖 الوثائق - Documentation

- `README.md` - الدليل الرئيسي
- `DEPLOYMENT_GUIDE.md` - دليل النشر
- `LICENSE` - الترخيص

---

## 🔑 نظام التراخيص - License System

### الميزات - Features

✅ **إدارة تراخيص متعددة** - Multiple license management
✅ **أنواع تراخيص مختلفة** - Different license types
✅ **تفعيل/تعليق التراخيص** - Activate/Suspend licenses
✅ **Multi-Tenancy** - عزل البيانات لكل ترخيص
✅ **واجهة إدارة سهلة** - Easy management interface

### أنواع التراخيص - License Types

1. **Lifetime** - مدى الحياة
   - لا ينتهي أبداً
   - مناسب للعملاء الدائمين

2. **Yearly** - سنوي
   - صالح لمدة سنة
   - يمكن تجديده

3. **Monthly** - شهري
   - صالح لمدة شهر
   - للاشتراكات الشهرية

4. **Trial** - تجريبي
   - للتجربة المجانية
   - مدة محدودة

---

## 🌐 النشر على Render - Deploy on Render

### الخطوات السريعة - Quick Steps

```bash
# 1. رفع إلى GitHub - Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_REPO_URL
git push -u origin main

# 2. النشر على Render - Deploy on Render
# اذهب إلى: https://render.com
# انقر: New + → Blueprint
# اختر المستودع - Select repository
# انقر: Apply
```

### الترخيص الافتراضي - Default License

```
License Key: RENDER-2026-PROD-LIVE
Username: admin
Password: admin123
Type: Lifetime
```

---

## 📊 إدارة التراخيص - License Management

### الوصول للوحة التحكم - Access Dashboard

```
https://your-app.onrender.com/security/licenses
```

### إنشاء ترخيص جديد - Create New License

1. اذهب إلى: `/security/create-license`
2. املأ البيانات المطلوبة
3. اختر نوع الترخيص
4. انقر "إنشاء"

### تعديل ترخيص - Edit License

1. اذهب إلى: `/security/licenses`
2. انقر على زر "تعديل" بجانب الترخيص
3. عدل البيانات
4. احفظ التغييرات

### تعليق/تفعيل ترخيص - Suspend/Activate License

- **تعليق**: يوقف الترخيص مؤقتاً
- **تفعيل**: يعيد تفعيل الترخيص

---

## 🔧 التكوين المحلي - Local Configuration

### تشغيل محلي - Run Locally

```bash
# تثبيت المتطلبات - Install dependencies
pip install -r requirements.txt

# تهيئة قاعدة البيانات - Initialize database
python initialize_master_database.py

# تشغيل التطبيق - Run application
python run.py
```

### الوصول المحلي - Local Access

```
http://localhost:5000
```

---

## 📝 ملاحظات مهمة - Important Notes

### قاعدة البيانات - Database

- ✅ SQLite (لا حاجة لـ PostgreSQL)
- ✅ تُنشأ تلقائياً عند أول تشغيل
- ✅ ملف واحد سهل النسخ الاحتياطي

### الأمان - Security

- 🔒 تشفير كلمات المرور
- 🔑 مفاتيح ترخيص فريدة
- 🛡️ عزل بيانات كل ترخيص

### الأداء - Performance

- ⚡ Gunicorn مع 2 workers
- 💾 SQLite محسّن للأداء
- 🔄 Timeout 120 ثانية

---

## 🆘 الدعم - Support

### المشاكل الشائعة - Common Issues

**التطبيق لا يعمل:**
- تحقق من Logs في Render
- تأكد من اكتمال البناء

**خطأ في قاعدة البيانات:**
```bash
python initialize_master_database.py
```

**نسيت كلمة المرور:**
- استخدم الترخيص الافتراضي
- أو أنشئ ترخيص جديد

---

## 📞 الاتصال - Contact

للمساعدة أو الاستفسارات:
For help or inquiries:

- 📧 Email: support@ded-erp.com
- 📖 Docs: DEPLOYMENT_GUIDE.md
- 🐛 Issues: Check application logs

---

## 🎯 الخطوات التالية - Next Steps

1. ✅ راجع `DEPLOYMENT_GUIDE.md`
2. ✅ ارفع إلى GitHub
3. ✅ انشر على Render
4. ✅ سجل دخول بالترخيص الافتراضي
5. ✅ أنشئ تراخيص جديدة لعملائك

---

## 🎉 استمتع! - Enjoy!

الآن لديك نظام ERP كامل مع إدارة تراخيص احترافية!
Now you have a complete ERP system with professional license management!

🚀 **Happy Managing!** 🚀


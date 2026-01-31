# 🚀 DED ERP System - Render Deployment Guide
# دليل نشر نظام DED ERP على Render

## 📋 نظرة عامة - Overview

هذا الدليل يشرح كيفية نشر نظام DED ERP على منصة Render مجاناً.
This guide explains how to deploy DED ERP System on Render platform for free.

---

## ✅ المتطلبات - Prerequisites

1. ✅ حساب GitHub - GitHub Account
2. ✅ حساب Render - Render Account (https://render.com)
3. ✅ Git مثبت على جهازك - Git installed

---

## 🎯 خطوات النشر - Deployment Steps

### 1️⃣ تصدير التطبيق - Export Application

```bash
python export_for_render.py
```

هذا سينشئ ملف ZIP يحتوي على كل ما تحتاجه للنشر.
This will create a ZIP file containing everything needed for deployment.

---

### 2️⃣ رفع إلى GitHub - Push to GitHub

```bash
# فك ضغط الملف - Extract the ZIP
unzip DED_ERP_Render_*.zip
cd DED_ERP_Render_*

# تهيئة Git - Initialize Git
git init
git add .
git commit -m "Initial commit for Render deployment"

# ربط بـ GitHub - Connect to GitHub
git remote add origin YOUR_GITHUB_REPO_URL
git branch -M main
git push -u origin main
```

---

### 3️⃣ النشر على Render - Deploy on Render

1. **افتح Render Dashboard**
   - اذهب إلى: https://dashboard.render.com

2. **أنشئ Web Service جديد**
   - انقر "New +" → "Web Service"
   - اختر "Build and deploy from a Git repository"
   - اختر مستودع GitHub الخاص بك

3. **التكوين التلقائي**
   - Render سيكتشف ملف `render.yaml` تلقائياً
   - سيتم تكوين كل شيء تلقائياً

4. **انقر "Create Web Service"**
   - انتظر حتى يكتمل البناء (5-10 دقائق)

---

## 🔑 بيانات الدخول الافتراضية - Default Credentials

بعد اكتمال النشر، استخدم هذه البيانات للدخول:
After deployment completes, use these credentials to login:

```
🔐 License Key: RENDER-2026-PROD-LIVE
👤 Username: admin
🔒 Password: admin123
```

---

## 🌐 الوصول للتطبيق - Access Application

سيكون التطبيق متاحاً على:
Your application will be available at:

```
https://ded-inventory-system.onrender.com
```

أو الرابط الذي يوفره Render.
Or the URL provided by Render.

---

## 📊 إدارة التراخيص - License Management

### الوصول لصفحة إدارة التراخيص:
Access License Management page:

```
https://your-app.onrender.com/security/licenses
```

### إنشاء ترخيص جديد:
Create new license:

```
https://your-app.onrender.com/security/create-license
```

### أنواع التراخيص المتاحة:
Available license types:

- ✅ **Lifetime** - مدى الحياة
- ✅ **Yearly** - سنوي
- ✅ **Monthly** - شهري
- ✅ **Trial** - تجريبي

---

## 🔧 التكوين - Configuration

### ملف `render.yaml`:

```yaml
services:
  - type: web
    name: ded-inventory-system
    env: python
    plan: free
    region: frankfurt
    runtime: python-3.11.7
```

### المتغيرات البيئية:
Environment Variables:

- `FLASK_APP=run.py`
- `FLASK_ENV=production`
- `SECRET_KEY` (يتم توليده تلقائياً)

---

## 📝 ملاحظات مهمة - Important Notes

### الخطة المجانية - Free Tier:

- ✅ 750 ساعة شهرياً - 750 hours/month
- ⏸️ التطبيق ينام بعد 15 دقيقة من عدم النشاط
- 🔄 أول طلب بعد النوم يأخذ ~30 ثانية
- 💾 قاعدة البيانات تبقى عبر عمليات النشر

### قاعدة البيانات - Database:

- 📦 SQLite (لا حاجة لـ PostgreSQL)
- 💾 تُحفظ في `/opt/render/project/src/`
- 🔄 تُنشأ تلقائياً عند أول تشغيل

---

## 🆘 استكشاف الأخطاء - Troubleshooting

### التطبيق لا يعمل:
Application not working:

1. تحقق من Logs في Render Dashboard
2. تأكد من اكتمال البناء بنجاح
3. تحقق من Environment Variables

### خطأ في قاعدة البيانات:
Database error:

```bash
# في Render Shell
python initialize_master_database.py
```

---

## 📞 الدعم - Support

للمساعدة أو الأسئلة:
For help or questions:

- 📧 Email: support@ded-erp.com
- 📖 Documentation: Check DEPLOYMENT_GUIDE.md
- 🐛 Issues: Check Render logs

---

## 🎉 تم بنجاح! - Success!

الآن لديك نظام DED ERP يعمل على Render!
Now you have DED ERP System running on Render!

استمتع بإدارة أعمالك! 🚀
Enjoy managing your business! 🚀


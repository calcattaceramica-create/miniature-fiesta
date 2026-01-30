# 🚀 دليل نشر نظام DED ERP على Render.com

## 📋 المتطلبات الأساسية

- ✅ حساب GitHub
- ✅ حساب Render.com (مجاني)
- ✅ Repository على GitHub يحتوي على الكود

---

## 🔧 ملفات النشر المطلوبة

### 1️⃣ **render.yaml** - ملف الإعدادات الرئيسي
```yaml
services:
  - type: web
    name: ded-inventory-system
    env: python
    plan: free
    region: frankfurt
    buildCommand: pip install --upgrade pip && pip install -r requirements.txt
    startCommand: gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: ded-database
          property: connectionString

databases:
  - name: ded-database
    plan: free
    region: frankfurt
    databaseName: ded_erp
    user: ded_user
```

### 2️⃣ **requirements.txt** - المكتبات المطلوبة
```
Flask==3.1.2
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
gunicorn==21.2.0
psycopg2-binary==2.9.9
... (باقي المكتبات)
```

### 3️⃣ **runtime.txt** - إصدار Python
```
python-3.11.7
```

### 4️⃣ **Procfile** - أمر التشغيل (اختياري)
```
web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 run:app
```

---

## 📝 خطوات النشر على Render.com

### **الطريقة 1: استخدام render.yaml (موصى بها)**

1. **ارفع الكود إلى GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **اذهب إلى Render Dashboard:**
   - افتح: https://dashboard.render.com
   - اضغط: `New +` → `Blueprint`

3. **اربط Repository:**
   - اختر: `Connect a repository`
   - اختر: `calcattaceramica-create/miniature-fiesta`
   - اضغط: `Connect`

4. **Render سيقرأ `render.yaml` تلقائياً:**
   - سينشئ Web Service
   - سينشئ PostgreSQL Database
   - سيربطهم ببعض

5. **انتظر اكتمال البناء:**
   - راقب الـ Logs
   - انتظر رسالة: `Build successful`

---

### **الطريقة 2: إنشاء Service يدوياً**

1. **اذهب إلى Render Dashboard:**
   - افتح: https://dashboard.render.com

2. **أنشئ PostgreSQL Database:**
   - اضغط: `New +` → `PostgreSQL`
   - **Name:** `ded-database`
   - **Database:** `ded_erp`
   - **User:** `ded_user`
   - **Region:** `Frankfurt (EU Central)`
   - **Plan:** `Free`
   - اضغط: `Create Database`

3. **أنشئ Web Service:**
   - اضغط: `New +` → `Web Service`
   - اختر Repository: `miniature-fiesta`
   - **Name:** `ded-inventory-system`
   - **Region:** `Frankfurt (EU Central)`
   - **Branch:** `main`
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Plan:** `Free`

4. **أضف Environment Variables:**
   - `FLASK_ENV` = `production`
   - `SECRET_KEY` = (اضغط Generate)
   - `DATABASE_URL` = (اختر من Database: `ded-database`)

5. **اضغط:** `Create Web Service`

---

## 🔍 التحقق من النشر

### **1️⃣ تحقق من الـ Logs:**
```
==> Building...
==> Installing dependencies...
==> Build successful
==> Starting service...
==> Deploy live
```

### **2️⃣ افتح التطبيق:**
```
https://ded-inventory-system.onrender.com
```

### **3️⃣ تسجيل الدخول:**
- **Username:** `admin`
- **Password:** `admin123`

---

## ⚠️ ملاحظات مهمة

### **Free Plan Limitations:**
- ✅ **مجاني تماماً**
- ⚠️ **ينام بعد 15 دقيقة** من عدم النشاط
- ⚠️ **يستغرق 50 ثانية** للاستيقاظ
- ✅ **750 ساعة/شهر** مجاناً
- ✅ **PostgreSQL 1GB** مجاناً

### **تحسين الأداء:**
- استخدم `--workers 2` (عدد العمال)
- استخدم `--timeout 120` (وقت الانتظار)
- فعّل `autoDeploy: true` للنشر التلقائي

---

## 🐛 حل المشاكل الشائعة

### **1️⃣ Build Failed:**
```bash
# تحقق من requirements.txt
pip install -r requirements.txt

# تحقق من Python version
python --version  # يجب أن يكون 3.11.7
```

### **2️⃣ Application Error:**
```bash
# تحقق من الـ Logs في Render Dashboard
# تحقق من DATABASE_URL
# تحقق من SECRET_KEY
```

### **3️⃣ Database Connection Error:**
```bash
# تحقق من DATABASE_URL في Environment Variables
# تحقق من أن Database تم إنشاؤه بنجاح
```

---

## 📞 الدعم

- **Render Docs:** https://render.com/docs
- **GitHub Issues:** https://github.com/calcattaceramica-create/miniature-fiesta/issues

---

## ✅ تم بنجاح!

الآن تطبيقك يعمل على الإنترنت! 🎉


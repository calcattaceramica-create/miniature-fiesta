# دليل تصدير المشروع (Export Guide)

هذا الدليل يشرح كيفية تصدير المشروع ونقله إلى جهاز آخر أو مشاركته.

---

## 📦 تصدير المشروع

### الطريقة 1: استخدام Git (موصى به)

#### 1. إنشاء مستودع Git

```bash
# تهيئة Git
git init

# إضافة جميع الملفات
git add .

# إنشاء commit
git commit -m "Initial commit - HR & CRM System v1.2.0"
```

#### 2. رفع المشروع إلى GitHub

```bash
# إنشاء مستودع على GitHub أولاً، ثم:
git remote add origin https://github.com/username/ded-system.git
git branch -M main
git push -u origin main
```

#### 3. استنساخ المشروع على جهاز آخر

```bash
git clone https://github.com/username/ded-system.git
cd ded-system
```

---

### الطريقة 2: ضغط المشروع (ZIP)

#### 1. تنظيف المشروع

قبل الضغط، احذف الملفات غير الضرورية:

```bash
# حذف البيئة الافتراضية
rm -rf venv/

# حذف الملفات المؤقتة
rm -rf __pycache__/
rm -rf app/__pycache__/
rm -rf *.pyc

# حذف قاعدة البيانات (اختياري)
rm -rf instance/
rm -f *.db
```

#### 2. ضغط المشروع

**Windows:**
- انقر بزر الماوس الأيمن على مجلد المشروع
- اختر "Send to" > "Compressed (zipped) folder"

**Linux/Mac:**
```bash
cd ..
tar -czf ded-system.tar.gz DED/
# أو
zip -r ded-system.zip DED/ -x "*/venv/*" "*/__pycache__/*" "*.pyc"
```

#### 3. فك الضغط على جهاز آخر

```bash
# Windows: انقر مرتين على الملف
# Linux/Mac:
tar -xzf ded-system.tar.gz
# أو
unzip ded-system.zip
```

---

## 🔄 إعداد المشروع بعد التصدير

### 1. تثبيت المتطلبات

```bash
cd DED

# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# تثبيت المتطلبات
pip install -r requirements.txt
```

### 2. إعداد قاعدة البيانات

```bash
# إنشاء قاعدة البيانات
python init_db.py

# إنشاء بيانات تجريبية (اختياري)
python seed_data.py
python seed_crm_data.py
```

### 3. تشغيل التطبيق

```bash
python run.py
```

---

## 📋 قائمة الملفات المهمة

### ملفات أساسية (يجب تضمينها)

```
✅ app/                      # مجلد التطبيق الرئيسي
✅ migrations/               # ملفات الهجرة
✅ config.py                # إعدادات التطبيق
✅ run.py                   # نقطة البداية
✅ init_db.py              # إنشاء قاعدة البيانات
✅ seed_data.py            # بيانات تجريبية HR
✅ seed_crm_data.py        # بيانات تجريبية CRM
✅ requirements.txt        # المتطلبات
✅ README.md               # الوثائق الرئيسية
✅ QUICK_START.md          # دليل البدء السريع
✅ DEPLOYMENT.md           # دليل النشر
✅ CHANGELOG.md            # سجل التغييرات
✅ LICENSE                 # الترخيص
✅ .gitignore              # ملفات Git المستبعدة
```

### ملفات يجب استبعادها

```
❌ venv/                    # البيئة الافتراضية
❌ __pycache__/             # ملفات Python المؤقتة
❌ *.pyc                    # ملفات Python المترجمة
❌ instance/                # قاعدة البيانات المحلية
❌ *.db                     # ملفات قاعدة البيانات
❌ .env                     # متغيرات البيئة (تحتوي على أسرار)
❌ *.log                    # ملفات السجلات
❌ uploads/                 # الملفات المرفوعة
```

---

## 🔐 تصدير قاعدة البيانات

### SQLite (قاعدة البيانات الافتراضية)

```bash
# نسخ ملف قاعدة البيانات
cp instance/erp_system.db backup/erp_system_backup.db

# أو تصدير إلى SQL
sqlite3 instance/erp_system.db .dump > database_backup.sql
```

### PostgreSQL

```bash
# تصدير قاعدة البيانات
pg_dump -U ded_user ded_db > database_backup.sql

# استيراد قاعدة البيانات
psql -U ded_user ded_db < database_backup.sql
```

### MySQL

```bash
# تصدير قاعدة البيانات
mysqldump -u ded_user -p ded_db > database_backup.sql

# استيراد قاعدة البيانات
mysql -u ded_user -p ded_db < database_backup.sql
```

---

## 📤 مشاركة المشروع

### 1. إنشاء ملف README للمستلم

أنشئ ملف `SETUP_INSTRUCTIONS.md`:

```markdown
# تعليمات الإعداد

1. فك ضغط الملف
2. افتح Terminal/CMD في مجلد المشروع
3. نفذ الأوامر التالية:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python init_db.py
python seed_data.py
python seed_crm_data.py
python run.py
```

4. افتح المتصفح على: http://127.0.0.1:5000
5. سجل الدخول بـ:
   - اسم المستخدم: admin
   - كلمة المرور: admin123
```

### 2. إنشاء سكريبت تشغيل تلقائي

**Windows (setup.bat):**
```batch
@echo off
echo Installing DED System...
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python seed_data.py
python seed_crm_data.py
echo Setup complete!
echo Run 'python run.py' to start the application
pause
```

**Linux/Mac (setup.sh):**
```bash
#!/bin/bash
echo "Installing DED System..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
python seed_data.py
python seed_crm_data.py
echo "Setup complete!"
echo "Run 'python run.py' to start the application"
```

---

## ✅ قائمة التحقق قبل التصدير

- [ ] تحديث requirements.txt
- [ ] تحديث README.md
- [ ] تحديث CHANGELOG.md
- [ ] حذف ملفات .env (تحتوي على أسرار)
- [ ] حذف قاعدة البيانات (أو تصديرها بشكل منفصل)
- [ ] حذف البيئة الافتراضية (venv/)
- [ ] حذف ملفات __pycache__
- [ ] التأكد من وجود .gitignore
- [ ] اختبار المشروع على جهاز نظيف
- [ ] كتابة تعليمات الإعداد

---

## 🎯 نصائح مهمة

1. **لا تشارك ملف .env** - يحتوي على مفاتيح سرية
2. **استخدم Git** - أفضل طريقة لإدارة الإصدارات
3. **وثق التغييرات** - حدّث CHANGELOG.md دائماً
4. **اختبر قبل التصدير** - تأكد أن كل شيء يعمل
5. **احفظ نسخة احتياطية** - من قاعدة البيانات والملفات المهمة

---

## 📞 الدعم

إذا واجهت مشاكل في التصدير أو الإعداد:
- راجع README.md
- راجع QUICK_START.md
- افتح Issue على GitHub

---

**تم بنجاح! المشروع جاهز للتصدير والمشاركة** 🎉


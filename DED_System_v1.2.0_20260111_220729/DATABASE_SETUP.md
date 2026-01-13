# 🗄️ دليل إعداد قاعدة البيانات (Database Setup Guide)

## نظرة عامة

هذا الدليل يشرح كيفية إعداد قاعدة البيانات للنظام.

---

## 🚀 الطريقة السريعة (للتطوير)

### الخطوة 1: تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

### الخطوة 2: تهيئة قاعدة البيانات

```bash
python init_db.py
```

هذا الأمر سيقوم بـ:
- ✅ إنشاء جميع الجداول
- ✅ إدخال البيانات الافتراضية
- ✅ إنشاء مستخدم admin
- ✅ إنشاء الأدوار الأساسية
- ✅ إنشاء دليل الحسابات

### الخطوة 3: تسجيل الدخول

```
Username: admin
Password: admin123
```

⚠️ **مهم:** غيّر كلمة المرور فوراً!

---

## 🔧 الطريقة المتقدمة (باستخدام Flask-Migrate)

### الخطوة 1: تهيئة الترحيل

```bash
flask db init
```

### الخطوة 2: إنشاء الترحيل الأولي

```bash
flask db migrate -m "Initial migration"
```

### الخطوة 3: تطبيق الترحيل

```bash
flask db upgrade
```

### الخطوة 4: إدخال البيانات الافتراضية

```bash
python seed_data.py
```

---

## 🐘 PostgreSQL (للإنتاج)

### الخطوة 1: تثبيت PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**Windows:**
- حمّل من: https://www.postgresql.org/download/windows/

**macOS:**
```bash
brew install postgresql
```

### الخطوة 2: إنشاء قاعدة البيانات

```bash
# تسجيل الدخول إلى PostgreSQL
sudo -u postgres psql

# إنشاء قاعدة بيانات
CREATE DATABASE erp_system;

# إنشاء مستخدم
CREATE USER erp_user WITH PASSWORD 'your_password';

# منح الصلاحيات
GRANT ALL PRIVILEGES ON DATABASE erp_system TO erp_user;

# الخروج
\q
```

### الخطوة 3: تكوين الاتصال

أنشئ ملف `.env`:

```bash
DATABASE_URL=postgresql://erp_user:your_password@localhost/erp_system
SECRET_KEY=your-secret-key-here
```

### الخطوة 4: تطبيق الترحيل

```bash
flask db upgrade
```

### الخطوة 5: إدخال البيانات

```bash
python init_db.py
```

---

## 🐬 MySQL (بديل)

### الخطوة 1: تثبيت MySQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-server
```

**Windows:**
- حمّل من: https://dev.mysql.com/downloads/installer/

### الخطوة 2: إنشاء قاعدة البيانات

```bash
# تسجيل الدخول
mysql -u root -p

# إنشاء قاعدة بيانات
CREATE DATABASE erp_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# إنشاء مستخدم
CREATE USER 'erp_user'@'localhost' IDENTIFIED BY 'your_password';

# منح الصلاحيات
GRANT ALL PRIVILEGES ON erp_system.* TO 'erp_user'@'localhost';
FLUSH PRIVILEGES;

# الخروج
EXIT;
```

### الخطوة 3: تثبيت المكتبة

```bash
pip install pymysql
```

### الخطوة 4: تكوين الاتصال

في `.env`:

```bash
DATABASE_URL=mysql+pymysql://erp_user:your_password@localhost/erp_system
```

### الخطوة 5: تطبيق الترحيل

```bash
flask db upgrade
python init_db.py
```

---

## 🔄 النسخ الاحتياطي والاستعادة

### SQLite

**النسخ الاحتياطي:**
```bash
# طريقة 1: نسخ الملف
cp erp_system.db erp_system.db.backup

# طريقة 2: باستخدام sqlite3
sqlite3 erp_system.db ".backup 'backup.db'"
```

**الاستعادة:**
```bash
# طريقة 1: نسخ الملف
cp erp_system.db.backup erp_system.db

# طريقة 2: باستخدام sqlite3
sqlite3 erp_system.db ".restore 'backup.db'"
```

---

### PostgreSQL

**النسخ الاحتياطي:**
```bash
# نسخ احتياطي كامل
pg_dump -U erp_user -d erp_system -F c -f backup.dump

# نسخ احتياطي SQL
pg_dump -U erp_user -d erp_system > backup.sql
```

**الاستعادة:**
```bash
# من ملف dump
pg_restore -U erp_user -d erp_system backup.dump

# من ملف SQL
psql -U erp_user -d erp_system < backup.sql
```

---

### MySQL

**النسخ الاحتياطي:**
```bash
mysqldump -u erp_user -p erp_system > backup.sql
```

**الاستعادة:**
```bash
mysql -u erp_user -p erp_system < backup.sql
```

---

## 🔐 الأمان

### 1. تغيير كلمة المرور الافتراضية

```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='admin').first()
    user.set_password('new_secure_password')
    db.session.commit()
```

### 2. تأمين قاعدة البيانات

**PostgreSQL:**
```bash
# تعديل pg_hba.conf
sudo nano /etc/postgresql/*/main/pg_hba.conf

# استخدم md5 بدلاً من trust
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
```

**MySQL:**
```sql
-- حذف المستخدمين المجهولين
DELETE FROM mysql.user WHERE User='';

-- حذف قاعدة البيانات التجريبية
DROP DATABASE IF EXISTS test;

-- تحديث الصلاحيات
FLUSH PRIVILEGES;
```

---

## 📊 التحقق من الإعداد

### 1. التحقق من الجداول

**SQLite:**
```bash
sqlite3 erp_system.db ".tables"
```

**PostgreSQL:**
```bash
psql -U erp_user -d erp_system -c "\dt"
```

**MySQL:**
```bash
mysql -u erp_user -p erp_system -e "SHOW TABLES;"
```

### 2. التحقق من البيانات

```python
from app import create_app, db
from app.models import User, Role, Company

app = create_app()
with app.app_context():
    print(f"Users: {User.query.count()}")
    print(f"Roles: {Role.query.count()}")
    print(f"Companies: {Company.query.count()}")
```

### 3. اختبار الاتصال

```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('✅ Database connection successful!')"
```

---

## 🚨 استكشاف الأخطاء

### خطأ: "No such table"

**الحل:**
```bash
python init_db.py
# أو
flask db upgrade
```

### خطأ: "Connection refused"

**الحل:**
- تأكد من تشغيل خادم قاعدة البيانات
- تحقق من بيانات الاتصال في `.env`

### خطأ: "Access denied"

**الحل:**
- تحقق من اسم المستخدم وكلمة المرور
- تأكد من منح الصلاحيات

---

## 📝 ملاحظات مهمة

1. **SQLite:**
   - ✅ سهل الإعداد
   - ✅ لا يحتاج خادم
   - ❌ غير مناسب للإنتاج
   - ❌ لا يدعم التزامن العالي

2. **PostgreSQL:**
   - ✅ موصى به للإنتاج
   - ✅ يدعم التزامن العالي
   - ✅ ميزات متقدمة
   - ❌ يحتاج إعداد أكثر

3. **MySQL:**
   - ✅ شائع الاستخدام
   - ✅ أداء جيد
   - ✅ سهل الإدارة
   - ⚠️ تأكد من استخدام InnoDB

---

## 🎯 التوصيات

### للتطوير
- استخدم **SQLite**
- البيانات في ملف `erp_system.db`

### للإنتاج
- استخدم **PostgreSQL**
- نسخ احتياطية يومية
- مراقبة الأداء

---

**آخر تحديث:** 2026-01-10


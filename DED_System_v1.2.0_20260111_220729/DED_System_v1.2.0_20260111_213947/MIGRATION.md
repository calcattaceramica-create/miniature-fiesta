# 🔄 دليل الترحيل (Migration Guide)

## نظرة عامة

نستخدم **Flask-Migrate** (Alembic) لإدارة تغييرات قاعدة البيانات.

---

## 📋 الأوامر الأساسية

### 1. تهيئة الترحيل (أول مرة فقط)

```bash
flask db init
```

هذا الأمر ينشئ مجلد `migrations/` الذي يحتوي على:
- `alembic.ini` - ملف التكوين
- `env.py` - بيئة الترحيل
- `versions/` - مجلد إصدارات الترحيل

⚠️ **ملاحظة:** لا تحتاج لتشغيل هذا الأمر إلا مرة واحدة عند بداية المشروع.

---

### 2. إنشاء ترحيل جديد

```bash
flask db migrate -m "وصف التغيير"
```

**مثال:**
```bash
flask db migrate -m "Add customer table"
flask db migrate -m "Add email field to users"
```

هذا الأمر:
- يقارن النماذج الحالية مع قاعدة البيانات
- ينشئ ملف ترحيل جديد في `migrations/versions/`
- يحتوي على دوال `upgrade()` و `downgrade()`

---

### 3. تطبيق الترحيل

```bash
flask db upgrade
```

هذا الأمر:
- يطبق جميع الترحيلات الجديدة
- يحدّث قاعدة البيانات
- يسجل الإصدار الحالي

---

### 4. التراجع عن الترحيل

```bash
# التراجع خطوة واحدة
flask db downgrade

# التراجع إلى إصدار معين
flask db downgrade <revision_id>

# التراجع إلى البداية
flask db downgrade base
```

---

### 5. عرض السجل

```bash
# عرض جميع الترحيلات
flask db history

# عرض الإصدار الحالي
flask db current

# عرض الترحيلات المعلقة
flask db show
```

---

## 🔧 سيناريوهات شائعة

### السيناريو 1: إضافة جدول جديد

**1. أنشئ النموذج:**
```python
# في app/models.py
class NewTable(db.Model):
    __tablename__ = 'new_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
```

**2. أنشئ الترحيل:**
```bash
flask db migrate -m "Add new_table"
```

**3. طبّق الترحيل:**
```bash
flask db upgrade
```

---

### السيناريو 2: إضافة عمود جديد

**1. عدّل النموذج:**
```python
class User(db.Model):
    # ... existing fields
    new_field = db.Column(db.String(64))  # حقل جديد
```

**2. أنشئ الترحيل:**
```bash
flask db migrate -m "Add new_field to users"
```

**3. طبّق الترحيل:**
```bash
flask db upgrade
```

---

### السيناريو 3: تعديل عمود موجود

**1. عدّل النموذج:**
```python
class User(db.Model):
    # قبل: email = db.Column(db.String(120))
    email = db.Column(db.String(256))  # زيادة الحجم
```

**2. أنشئ الترحيل:**
```bash
flask db migrate -m "Increase email field size"
```

**3. راجع ملف الترحيل:**
```python
# في migrations/versions/xxxxx_.py
def upgrade():
    op.alter_column('users', 'email',
                    existing_type=sa.String(length=120),
                    type_=sa.String(length=256))
```

**4. طبّق الترحيل:**
```bash
flask db upgrade
```

---

### السيناريو 4: حذف عمود

**1. احذف من النموذج:**
```python
class User(db.Model):
    # حذف: old_field = db.Column(db.String(64))
    pass
```

**2. أنشئ الترحيل:**
```bash
flask db migrate -m "Remove old_field from users"
```

**3. طبّق الترحيل:**
```bash
flask db upgrade
```

⚠️ **تحذير:** تأكد من عمل نسخة احتياطية قبل حذف الأعمدة!

---

### السيناريو 5: إعادة تسمية عمود

**الطريقة اليدوية (موصى بها):**

**1. أنشئ ترحيل فارغ:**
```bash
flask db revision -m "Rename column"
```

**2. عدّل ملف الترحيل:**
```python
def upgrade():
    op.alter_column('users', 'old_name', new_column_name='new_name')

def downgrade():
    op.alter_column('users', 'new_name', new_column_name='old_name')
```

**3. طبّق الترحيل:**
```bash
flask db upgrade
```

---

## 🚨 استكشاف الأخطاء

### خطأ: "Target database is not up to date"

**الحل:**
```bash
flask db stamp head
```

---

### خطأ: "Can't locate revision identified by"

**الحل:**
```bash
# احذف مجلد migrations
rm -rf migrations/

# أعد التهيئة
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

### خطأ: "Multiple head revisions are present"

**الحل:**
```bash
flask db merge heads -m "Merge heads"
flask db upgrade
```

---

## 📝 أفضل الممارسات

### 1. رسائل وصفية

```bash
# ❌ سيء
flask db migrate -m "update"

# ✅ جيد
flask db migrate -m "Add email verification to users table"
```

---

### 2. راجع ملفات الترحيل

دائماً راجع ملف الترحيل قبل تطبيقه:

```bash
# بعد flask db migrate
cat migrations/versions/xxxxx_.py
```

تأكد من:
- العمليات صحيحة
- لا توجد عمليات غير مرغوبة
- دالة `downgrade()` تعمل بشكل صحيح

---

### 3. نسخ احتياطية

```bash
# قبل التطبيق
cp erp_system.db erp_system.db.backup

# أو
sqlite3 erp_system.db ".backup 'backup.db'"
```

---

### 4. اختبر في بيئة التطوير أولاً

```bash
# في بيئة التطوير
flask db upgrade

# اختبر التطبيق
python -m pytest

# إذا نجح، طبّق في الإنتاج
```

---

### 5. استخدم Transactions

في ملفات الترحيل المعقدة:

```python
def upgrade():
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('new_field', sa.String(64)))
        batch_op.alter_column('old_field', new_column_name='renamed_field')
```

---

## 🔄 سير العمل الموصى به

### للتطوير

```bash
# 1. عدّل النماذج
# 2. أنشئ الترحيل
flask db migrate -m "وصف التغيير"

# 3. راجع الملف
cat migrations/versions/xxxxx_.py

# 4. طبّق
flask db upgrade

# 5. اختبر
python run.py
```

---

### للإنتاج

```bash
# 1. خذ نسخة احتياطية
cp erp_system.db erp_system.db.backup

# 2. طبّق الترحيل
flask db upgrade

# 3. اختبر
# 4. إذا فشل، تراجع
flask db downgrade
```

---

## 📊 مثال كامل

### إضافة ميزة "تفعيل البريد الإلكتروني"

**1. عدّل النموذج:**
```python
class User(db.Model):
    # ... existing fields
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(128))
    email_verification_sent_at = db.Column(db.DateTime)
```

**2. أنشئ الترحيل:**
```bash
flask db migrate -m "Add email verification fields to users"
```

**3. راجع الملف:**
```python
# migrations/versions/xxxxx_add_email_verification.py
def upgrade():
    op.add_column('users', sa.Column('email_verified', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('email_verification_token', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('email_verification_sent_at', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('users', 'email_verification_sent_at')
    op.drop_column('users', 'email_verification_token')
    op.drop_column('users', 'email_verified')
```

**4. طبّق:**
```bash
flask db upgrade
```

**5. تحقق:**
```bash
flask db current
```

---

## 🎯 نصائح إضافية

1. **لا تعدّل ملفات الترحيل المطبقة**
2. **احتفظ بملفات الترحيل في Git**
3. **استخدم أسماء وصفية**
4. **اختبر دالة downgrade()**
5. **خذ نسخ احتياطية دائماً**

---

## 📚 مراجع

- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

**آخر تحديث:** 2026-01-10


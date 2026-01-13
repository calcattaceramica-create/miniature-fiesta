# سياسة الأمان (Security Policy)

## الإصدارات المدعومة

نحن نوفر تحديثات الأمان للإصدارات التالية:

| الإصدار | مدعوم          |
| ------- | -------------- |
| 1.0.x   | ✅ نعم         |
| < 1.0   | ❌ لا          |

---

## الإبلاغ عن ثغرة أمنية

### كيفية الإبلاغ

إذا اكتشفت ثغرة أمنية، يرجى **عدم** فتح Issue عام. بدلاً من ذلك:

1. **أرسل بريد إلكتروني إلى:** security@erpsystem.com
2. **قدم المعلومات التالية:**
   - وصف الثغرة
   - خطوات إعادة الإنتاج
   - التأثير المحتمل
   - الإصدار المتأثر
   - أي معلومات إضافية مفيدة

### ما يمكن توقعه

- **الرد الأولي:** خلال 48 ساعة
- **التحديث:** خلال 7 أيام
- **الإصلاح:** حسب خطورة الثغرة
  - حرجة: خلال 24-48 ساعة
  - عالية: خلال 7 أيام
  - متوسطة: خلال 30 يوم
  - منخفضة: في الإصدار التالي

### سياسة الإفصاح

- سنعمل معك لفهم وحل المشكلة
- سنبقي المعلومات سرية حتى يتم الإصلاح
- سنذكر اسمك (إذا رغبت) في الشكر والتقدير

---

## أفضل الممارسات الأمنية

### للمطورين

#### 1. كلمات المرور
```python
# ✅ صحيح - استخدام تشفير قوي
from werkzeug.security import generate_password_hash
password_hash = generate_password_hash(password, method='pbkdf2:sha256')

# ❌ خطأ - تخزين كلمات مرور نصية
password = "admin123"  # لا تفعل هذا!
```

#### 2. SQL Injection
```python
# ✅ صحيح - استخدام ORM
user = User.query.filter_by(username=username).first()

# ❌ خطأ - استعلامات SQL مباشرة
cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
```

#### 3. XSS Protection
```html
<!-- ✅ صحيح - استخدام escape تلقائي -->
{{ user.name }}

<!-- ❌ خطأ - HTML غير آمن -->
{{ user.name|safe }}  <!-- استخدم فقط عند الضرورة -->
```

#### 4. CSRF Protection
```python
# ✅ صحيح - تفعيل CSRF
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

### للمستخدمين

#### 1. كلمات المرور القوية
- **الحد الأدنى:** 8 أحرف
- **يجب أن تحتوي على:**
  - أحرف كبيرة (A-Z)
  - أحرف صغيرة (a-z)
  - أرقام (0-9)
  - رموز خاصة (!@#$%)

**مثال على كلمة مرور قوية:** `MyP@ssw0rd2026!`

#### 2. تغيير كلمة المرور الافتراضية
```bash
# ⚠️ مهم جداً!
# غيّر كلمة المرور فوراً بعد التثبيت
Username: admin
Password: admin123  # غيّرها فوراً!
```

#### 3. تحديث النظام
```bash
# تحقق من التحديثات بانتظام
git pull origin main
pip install -r requirements.txt --upgrade
```

#### 4. النسخ الاحتياطي
```bash
# خذ نسخة احتياطية يومياً
cp erp_system.db backups/backup_$(date +%Y%m%d).db
```

---

## إعدادات الأمان الموصى بها

### 1. ملف .env

```bash
# ✅ الإنتاج
FLASK_ENV=production
DEBUG=False
SECRET_KEY=<generate-strong-random-key>
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True

# ❌ التطوير فقط
FLASK_ENV=development
DEBUG=True
```

### 2. توليد مفتاح سري قوي

```python
import secrets
print(secrets.token_hex(32))
# مثال: 8f42a73054b1749f8f58848be5e6502c2e0e3e5c7f1c3b4a5d6e7f8a9b0c1d2e
```

### 3. قاعدة البيانات

```bash
# ✅ صحيح - أذونات محدودة
chmod 600 erp_system.db

# ❌ خطأ - أذونات مفتوحة
chmod 777 erp_system.db
```

### 4. HTTPS

```nginx
# ✅ صحيح - إعادة توجيه HTTP إلى HTTPS
server {
    listen 80;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    # ...
}
```

---

## قائمة التحقق الأمنية

### قبل النشر

- [ ] تغيير كلمة المرور الافتراضية
- [ ] توليد SECRET_KEY جديد
- [ ] تعطيل DEBUG mode
- [ ] تفعيل HTTPS
- [ ] تكوين جدار الحماية
- [ ] تحديد أذونات الملفات
- [ ] إعداد النسخ الاحتياطي
- [ ] مراجعة الصلاحيات
- [ ] تحديث جميع المكتبات
- [ ] اختبار الأمان

### بعد النشر

- [ ] مراقبة السجلات
- [ ] تحديثات أمنية منتظمة
- [ ] مراجعة الصلاحيات دورياً
- [ ] اختبار النسخ الاحتياطي
- [ ] مراقبة الأداء
- [ ] فحص الثغرات

---

## الثغرات المعروفة

لا توجد ثغرات معروفة حالياً.

سيتم تحديث هذا القسم عند اكتشاف أي ثغرات.

---

## الشكر والتقدير

نشكر الأشخاص التالية أسماؤهم على الإبلاغ عن ثغرات أمنية:

- (لا يوجد حالياً)

---

## الموارد الإضافية

### أدوات الأمان

- **Bandit:** فحص الكود Python
  ```bash
  pip install bandit
  bandit -r app/
  ```

- **Safety:** فحص المكتبات
  ```bash
  pip install safety
  safety check
  ```

- **OWASP ZAP:** فحص تطبيقات الويب
  - [https://www.zaproxy.org/](https://www.zaproxy.org/)

### مراجع

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security](https://flask.palletsprojects.com/en/latest/security/)
- [Python Security](https://python.readthedocs.io/en/latest/library/security_warnings.html)

---

## الاتصال

- **البريد الإلكتروني:** security@erpsystem.com
- **PGP Key:** (سيتم إضافته قريباً)

---

**آخر تحديث:** 2026-01-10

